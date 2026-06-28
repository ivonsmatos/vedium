
from vedium_core.marketing_landing_content import get_marketing_landing


def jinja_methods(site_name):
    """
    Add custom Jinja methods
    """
    return {"get_marketing_landing": get_marketing_landing}
