# opml_lib

opml_lib is a Python package that enables users to work with OPML (Outline Processor Markup Language) files. This package allows reading and writing to OPML files in an efficient manner. The primary use case of this package is for parsing and generating OPML files, which are commonly used for exchanging lists of web feeds between web feed aggregators.

## Modules

### opml_lib.reader

The reader module houses the `read_opml` function, which reads an OPML file and returns a list of dictionaries. Each dictionary in the list represents an outline node from the OPML file, containing "title", "url" and "link" keys.

Example usage:

```python
from opml_lib.reader import read_opml

data = read_opml('example.opml')
print(data)
```

### opml_lib.writer

The writer module contains the `write_opml` function, which takes a list of dictionaries (like the ones produced by read_opml), an output filename, and an optional title for the OPML file. It generates an OPML file from the provided data.

Example usage:

```python
from opml_lib.writer import write_opml

data = [{'title': 'Python Podcast', 'url': 'https://pythonpodcast.com/rss.xml', 'link': 'https://pythonpodcast.com'}]
write_opml(data, 'output.opml', 'Python Podcasts')
```
