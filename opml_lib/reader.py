import opml
import html_stripper

def read_opml(filename):
 lst = []
 parsed = [opml.OutlineElement(i) for i in opml.parse(filename)._tree.xpath('.//outline[@xmlUrl or @url]')]
 parsed = sorted(parsed, key=lambda item: getattr(item, 'title', getattr(item, 'text', '')))
 last = None
 for outline in parsed:
  title = html_stripper.strip_html_entities(getattr(outline, 'title', getattr(outline, 'text', 'Untitled')))
  url = getattr(outline, 'xmlUrl', getattr(outline, 'url', None))
  if url is None:
   continue
  link = getattr(outline, 'htmlUrl', None)
  new = {
   "title": title,
   "url": url,
   "link": link,
  }
  lst.append(new)
 return lst
