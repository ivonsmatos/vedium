import frappe
import unicodedata

def normalize_title(title):
    if not title:
        return ""
    title = title.lower().strip()
    return ''.join(c for c in unicodedata.normalize('NFD', title) if unicodedata.category(c) != 'Mn')

def sync_chapter_ordering(doc, method):
    """
    Hooks into LMS Course on_update to ensure:
    1. The Course Chapter document's idx field is synchronized with the child table's idx.
    2. 'Avaliação Final' (or variants) is strictly enforced to be the last chapter.
    """
    final_keywords = ["avaliacao final", "prova final", "final assessment", "exame final"]
    
    chapters_refs = doc.get("chapters")
    if not chapters_refs:
        return
        
    chapters_data = []
    for ref in chapters_refs:
        if ref.chapter:
            try:
                title = frappe.db.get_value("Course Chapter", ref.chapter, "title")
                chapters_data.append({
                    "ref": ref,
                    "chapter_name": ref.chapter,
                    "title": title,
                    "ref_idx": ref.idx
                })
            except Exception:
                pass
                
    if not chapters_data:
        return
        
    # Sort initially by user's drag and drop order in child table
    chapters_data.sort(key=lambda x: x["ref_idx"])
    
    normal_chapters = []
    final_chapters = []
    
    for ch in chapters_data:
        norm_title = normalize_title(ch["title"])
        if any(kw == norm_title for kw in final_keywords):
            final_chapters.append(ch)
        else:
            normal_chapters.append(ch)
            
    # New correct order
    new_order = normal_chapters + final_chapters
    
    # Save indices efficiently
    for i, ch in enumerate(new_order):
        new_idx = i + 1
        
        # Update Course Chapter (for the frontend which sorts by Course Chapter idx)
        # Using db_set avoids triggering all hooks again recursively
        frappe.db.set_value("Course Chapter", ch["chapter_name"], "idx", new_idx, update_modified=False)
        
        # Ensure the child table reflects the enforced order too
        if ch["ref"].idx != new_idx:
            frappe.db.set_value(ch["ref"].doctype, ch["ref"].name, "idx", new_idx, update_modified=False)
