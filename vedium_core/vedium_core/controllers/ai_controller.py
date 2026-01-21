
import frappe
from frappe import _
from groq import Groq
import time

RATE_LIMIT_QUOTA = 50
RATE_LIMIT_WINDOW = 3600

def get_groq_client():
    """
    Retrieve Groq client with API Key from site config or settings.
    """
    api_key = frappe.conf.get("groq_api_key")
    
    if not api_key:
        # Fallback to Vedium Settings if not in site config
        # Assuming single DocType 'Vedium Settings' exists or will exist
        try:
            api_key = frappe.db.get_single_value("Vedium Settings", "groq_api_key")
        except Exception:
            pass
            
    if not api_key:
        frappe.throw(_("Groq API Key not configured. Please check site config or Vedium Settings."))
        
    return Groq(api_key=api_key)

def check_rate_limit(user):
    """
    Check if user has exceeded the rate limit of 50 messages per hour.
    """
    if user == "Administrator":
        return

    cache_key = f"ai_rate_limit:{user}"
    # get_value returns None if not found, or the integer value
    current_count = frappe.cache().get_value(cache_key) or 0
    
    if int(current_count) >= RATE_LIMIT_QUOTA:
        frappe.throw(_("Rate limit exceeded. You can only send 50 messages per hour."), frappe.PermissionError)
        
    # Increment counter
    # If key doesn't exist, set to 1 with expiry. If exists, incr.
    # Frappe cache doesn't have atomic incr with expire easily exposed, 
    # so we use set_value if new, or incr if existing (but incr in redis-py/frappe-wrapper might not reset expire).
    # Simplified approach:
    
    new_count = int(current_count) + 1
    if new_count == 1:
        frappe.cache().set_value(cache_key, new_count, expires_in_sec=RATE_LIMIT_WINDOW)
    else:
        # Update without resetting ttl? Frappe set_value usually resets TTL. 
        # Ideally we want strictly window based.
        # Just set it again with remaining time or fixed window? 
        # Using simple fixed window reset for now as per requirement simplicity.
        # Or better: use user_specific TTL if precise. 
        # For MVP: just increment.
        try:
            frappe.cache().incr(cache_key)
        except Exception:
             frappe.cache().set_value(cache_key, new_count, expires_in_sec=RATE_LIMIT_WINDOW)

@frappe.whitelist()
def chat_with_tutor(message, persona_id, context=None):
    """
    Chat with AI Tutor using Groq Llama 3.
    """
    user = frappe.session.user
    
    if user == "Guest":
        frappe.throw(_("You must be logged in to use the AI Tutor."), frappe.PermissionError)
        
    # Rate Limiting
    check_rate_limit(user)
    
    # Fetch Persona
    if not persona_id:
        frappe.throw(_("Persona ID is required."))
        
    try:
        persona = frappe.get_doc("AI Persona", persona_id)
    except frappe.DoesNotExistError:
        frappe.throw(_("AI Persona not found."))
        
    # Guardrails
    guardrails = """
    CRITICAL INSTRUCTIONS:
    - You are a helpful AI Tutor for the Vedium platform.
    - Do NOT discuss politics, religion, or controversial topics.
    - Do NOT generate violent, hateful, or explicit content.
    - If asked about these topics, politely decline and steer back to the subject.
    - Be concise and educational.
    """
    
    system_prompt = f"{guardrails}\n\n{persona.system_prompt}"
    
    # Build Messages
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    user_content = message
    if context:
        user_content = f"Context:\n{context}\n\nUser Question:\n{message}"
        
    messages.append({"role": "user", "content": user_content})
    
    # Client
    client = get_groq_client()
    
    try:
        start_time = time.time()
        
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama3-70b-8192",
            temperature=0.7,
            max_tokens=400,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        # Logging
        # Assuming 'AI Interaction Log' exists
        try:
            log = frappe.get_doc({
                "doctype": "AI Interaction Log",
                "user": user,
                "persona": persona_id,
                "input_tokens": chat_completion.usage.prompt_tokens if hasattr(chat_completion, 'usage') else 0,
                "output_tokens": chat_completion.usage.completion_tokens if hasattr(chat_completion, 'usage') else 0,
                "timestamp": frappe.utils.now(),
                "duration": time.time() - start_time
            })
            log.insert(ignore_permissions=True)
        except Exception as e:
            # Don't fail the chat if logging fails, but log error to system
            frappe.log_error(f"Failed to log AI interaction: {str(e)}", "AI Tutor Log Error")
            
        return response_text

    except Exception as e:
        frappe.log_error(f"Groq API Error: {str(e)}", "AI Tutor Error")
        frappe.throw(_("An error occurred while communicating with the AI Tutor. Please try again later."))
