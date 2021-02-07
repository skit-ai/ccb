TPL_MATCHES = """Here are the coffee matches!

{{ groups_string }}
"""

TPL_DM = """Hi, feel free to use this group for scheduling your coffee catchup.

{% if topics %}
Here are few conversation starters for you:
{% for topic in topics %}
+ {{ topic }}
{% endfor %}
{% endif %}
"""
