TPL_MATCHES = """Here are the coffee matches!

{% for group in groups %}
Group {{ loop.index }}: {% for user in group %} <@{{ user.id }}> {% endfor %}
{% endfor %}
"""

TPL_DM = """Hi, feel free to use this group for scheduling your coffee catchup.

{% if topics %}
Here are few conversation starters for you:
{% for topic in topics %}
+ {{ topic }}
{% endfor %}
{% endif %}
"""
