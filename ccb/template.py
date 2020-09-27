from typing import Optional

import jinja2

DEFAULT = """Here are the coffee matches!

{{ groups_string }}

Seed: {{ seed }}
"""


def is_template_valid(template: str) -> bool:
    # TODO: Validate
    return True


def build_message(groups_string: str, seed, template: Optional[str] = None) -> str:
    template = template or DEFAULT

    tpl = jinja2.Template(template)
    return tpl.render(groups_string=groups_string, seed=seed)
