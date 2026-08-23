"""Small, dependency-free helpers for efficient marketing images."""

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


COURSE_IMAGE_WIDTHS = (360, 640, 900)
COURSE_IMAGE_SIZES = (
    "(max-width: 575px) calc(100vw - 40px), "
    "(max-width: 991px) 50vw, 25vw"
)


def responsive_course_image(image_url: str) -> dict[str, str]:
    """Return a compact ``src``/``srcset`` for Unsplash course covers.

    Local uploads are left untouched here. A one-shot migration converts those
    originals to appropriately sized WebP files, while Unsplash can resize and
    negotiate WebP/AVIF at request time.
    """
    image_url = str(image_url or "")
    parsed = urlsplit(image_url)
    if parsed.hostname not in {"images.unsplash.com", "plus.unsplash.com"}:
        return {
            "image_src": image_url,
            "image_srcset": "",
            "image_sizes": "",
        }

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.pop("h", None)
    query.update({"auto": "format", "fit": "crop", "q": "72"})

    def with_width(width: int) -> str:
        sized_query = {**query, "w": str(width)}
        return urlunsplit(
            (parsed.scheme, parsed.netloc, parsed.path, urlencode(sized_query), "")
        )

    return {
        "image_src": with_width(640),
        "image_srcset": ", ".join(
            f"{with_width(width)} {width}w" for width in COURSE_IMAGE_WIDTHS
        ),
        "image_sizes": COURSE_IMAGE_SIZES,
    }
