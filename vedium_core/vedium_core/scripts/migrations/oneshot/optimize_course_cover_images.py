"""Convert oversized public LMS course covers to compact WebP files.

Run with:
    bench --site app.vediums.com execute \
      vedium_core.scripts.migrations.oneshot.optimize_course_cover_images.execute
"""

from io import BytesIO
from pathlib import Path

import frappe
from PIL import Image, ImageOps
from frappe.utils.file_manager import save_file


MAX_WIDTH = 720
WEBP_QUALITY = 72


def execute():
    converted = []
    courses = frappe.get_all(
        "LMS Course",
        filters={"published": 1},
        fields=["name", "image"],
        limit_page_length=0,
    )

    for course in courses:
        image_url = str(course.image or "")
        if not image_url.startswith("/files/") or image_url.lower().endswith(".webp"):
            continue

        source_path = Path(frappe.get_site_path("public", image_url.lstrip("/")))
        if not source_path.is_file():
            frappe.log_error(
                f"Course cover not found: {source_path}",
                "Vedium course image optimization",
            )
            continue

        with Image.open(source_path) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            if image.width > MAX_WIDTH:
                target_height = round(image.height * MAX_WIDTH / image.width)
                image = image.resize((MAX_WIDTH, target_height), Image.Resampling.LANCZOS)

            output = BytesIO()
            image.save(
                output,
                format="WEBP",
                quality=WEBP_QUALITY,
                method=6,
                optimize=True,
            )

        optimized_name = f"{source_path.stem}-optimized.webp"
        file_doc = save_file(
            optimized_name,
            output.getvalue(),
            "LMS Course",
            course.name,
            is_private=0,
        )
        frappe.db.set_value("LMS Course", course.name, "image", file_doc.file_url)
        converted.append(
            {
                "course": course.name,
                "before": source_path.stat().st_size,
                "after": len(output.getvalue()),
                "file_url": file_doc.file_url,
            }
        )

    frappe.db.commit()
    print({"converted": len(converted), "files": converted})
    return converted
