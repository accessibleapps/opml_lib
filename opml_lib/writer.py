import jinja2

opml_template = u"""<?xml version="1.0" encoding="UTF-8"?>
<opml version="1.0">
  <head>
    <title>{{ title }}</title>
  </head>
  <body>
    {% for podcast in podcasts %}    
    <outline
        text="{{ podcast.title|e }}"
        title="{{ podcast.title|e }}"
        type="rss"
        xmlUrl="{{ podcast.url|e }}"
        htmlUrl="{{ podcast.link|e }}"
      />
    {% endfor %}
  </body>
</opml>
"""

def write_opml(podcasts, filename, title="OPML output"):
 template = jinja2.Template(opml_template)
 opml_title = title
 contents = template.render(podcasts=podcasts, title=opml_title)
 with open(filename, mode='wt', encoding='utf8') as output_file:
  output_file.write(contents)

