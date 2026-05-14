from __future__ import annotations

from typing import Any

import jinja2

opml_template = """<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
  <head>
    <title>{{ title|e }}</title>
  </head>
  <body>
    {% for podcast in podcasts %}
    <outline
        text="{{ podcast.title|e }}"
        title="{{ podcast.title|e }}"
        type="rss"
        xmlUrl="{{ podcast.url|e }}"
        {% if podcast.get("link") is not none %}
        htmlUrl="{{ podcast.link|e }}"
        {% endif %}
      />
    {% endfor %}
  </body>
</opml>
"""


def write_opml(podcasts: list[dict[str, Any]], filename: str, title: str = "OPML output") -> None:
    template = jinja2.Template(opml_template)
    opml_title = title
    contents: str = template.render(podcasts=podcasts, title=opml_title)
    with open(filename, mode="w", encoding="utf8") as output_file:
        output_file.write(contents)
