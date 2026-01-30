import frappe

def get_context(context):
    # Fetch Featured or All Published Courses
    context.courses = get_courses()
    context.featured_courses = context.courses[:3] if context.courses else []
    
    # Shopping Cart Count
    context.cart_count = get_cart_count()

def get_cart_count():
    if frappe.db.exists("DocType", "Quotation"):
        quotation = frappe.get_all("Quotation", 
            filters={"party_name": frappe.session.user, "docstatus": 0}, 
            fields=["name"])
        if quotation:
            return frappe.db.count("Quotation Item", {"parent": quotation[0].name})
    return 0

def get_courses():
    try:
        courses = frappe.get_all("LMS Course",
            fields=["name", "title", "short_description", "image", "instructor", "status"],
            filters={"status": "Approved", "published": 1},
            limit=8
        )
        
        # Enrich course data if needed (e.g. formatting price if available)
        for course in courses:
            # Fallback image if none
            if not course.image:
                course.image = "/assets/vedium_core/vedium_assets/images/resources/courses-v1-img1.jpg"
                
            # Fetch Instructor Name if 'instructor' is a link field to User or Member
            if course.instructor:
                course.instructor_name = frappe.db.get_value("User", course.instructor, "full_name") or course.instructor
            else:
                course.instructor_name = "Vedium Instructor"
                
        return courses
    except Exception as e:
        frappe.log_error(f"Error fetching courses: {str(e)}", "Vedium LMS")
        return []
