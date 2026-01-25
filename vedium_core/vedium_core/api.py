# -*- coding: utf-8 -*-
# Vedium Core - Courses API
# API endpoints for the public website

import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_published_courses(category=None, limit=10):
    """
    Get published courses for the public website
    Returns courses from LMS with basic info for display
    """
    filters = {"published": 1}
    if category:
        filters["category"] = category
    
    courses = frappe.get_all(
        "LMS Course",
        filters=filters,
        fields=[
            "name",
            "title", 
            "short_introduction",
            "image",
            "paid_course",
            "course_price",
            "currency",
            "category",
            "status"
        ],
        order_by="creation desc",
        limit_page_length=limit
    )
    
    # Enrich with additional data
    for course in courses:
        # Get instructor info
        instructors = frappe.get_all(
            "Course Instructor",
            filters={"parent": course.name},
            fields=["instructor"],
            limit=1
        )
        if instructors:
            instructor_user = frappe.get_value("User", instructors[0].instructor, ["full_name", "user_image"])
            course["instructor_name"] = instructor_user[0] if instructor_user else None
            course["instructor_image"] = instructor_user[1] if instructor_user else None
        
        # Get lesson count
        course["lesson_count"] = frappe.db.count("Course Lesson", {"course": course.name})
        
        # Get enrollment count
        course["enrollment_count"] = frappe.db.count("LMS Enrollment", {"course": course.name})
        
        # Course URL
        course["url"] = f"/lms/courses/{course.name}"
    
    return courses


@frappe.whitelist(allow_guest=True)
def get_course_categories():
    """
    Get all course categories
    """
    categories = frappe.get_all(
        "LMS Category",
        filters={},
        fields=["name", "category"],
        order_by="category"
    )
    return categories


@frappe.whitelist(allow_guest=True)
def get_featured_courses(limit=6):
    """
    Get featured/popular courses for homepage
    """
    # Get courses with most enrollments
    courses = frappe.db.sql("""
        SELECT 
            c.name,
            c.title,
            c.short_introduction,
            c.image,
            c.paid_course,
            c.course_price,
            c.currency,
            c.category,
            COUNT(e.name) as enrollment_count
        FROM `tabLMS Course` c
        LEFT JOIN `tabLMS Enrollment` e ON c.name = e.course
        WHERE c.published = 1
        GROUP BY c.name
        ORDER BY enrollment_count DESC
        LIMIT %s
    """, (limit,), as_dict=True)
    
    for course in courses:
        course["url"] = f"/lms/courses/{course.name}"
        course["lesson_count"] = frappe.db.count("Course Lesson", {"course": course.name})
    
    return courses


@frappe.whitelist()
def create_checkout_session(course_name):
    """
    Create a Stripe checkout session for course purchase
    Requires logged-in user
    """
    if frappe.session.user == "Guest":
        frappe.throw(_("Please login to purchase this course"))
    
    course = frappe.get_doc("LMS Course", course_name)
    
    if not course.paid_course:
        frappe.throw(_("This is a free course"))
    
    # Check if already enrolled
    existing = frappe.db.exists("LMS Enrollment", {
        "course": course_name,
        "member": frappe.session.user
    })
    if existing:
        frappe.throw(_("You are already enrolled in this course"))
    
    # Create Stripe checkout (placeholder - needs Stripe config)
    checkout_url = create_stripe_checkout(course)
    
    return {"checkout_url": checkout_url}


def create_stripe_checkout(course):
    """
    Create Stripe checkout session
    """
    # This will be configured when Stripe keys are added
    # For now, return a placeholder
    return f"/lms/courses/{course.name}/enroll"


@frappe.whitelist(allow_guest=True)
def handle_payment_webhook():
    """
    Handle Stripe payment webhook
    Creates enrollment on successful payment
    """
    # Webhook handling logic
    # 1. Verify webhook signature
    # 2. Extract payment data
    # 3. Create LMS Enrollment
    # 4. Create Customer in ERPNext
    # 5. Send confirmation email
    pass
