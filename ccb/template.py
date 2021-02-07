from typing import Optional

import jinja2

DEFAULT = """Here are the coffee matches!

{{ groups_string }}
"""


def build_matches_message(groups_string: str, template: Optional[str] = None) -> str:
    """
    Build messages for coffee matches. Use a default template, if not provided.
    """

    template = template or DEFAULT

    tpl = jinja2.Template(template)
    return tpl.render(groups_string=groups_string)
