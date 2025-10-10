from __future__ import annotations

from typing import TypedDict

import html_stripper  # type: ignore[import-untyped]
import opml  # type: ignore[import-untyped]


class OPMLEntry(TypedDict):
    title: str
    url: str
    link: str | None


def read_opml(filename: str) -> list[OPMLEntry]:
 lst: list[OPMLEntry] = []
 parsed = [opml.OutlineElement(i) for i in opml.parse(filename)._tree.xpath('.//outline[@xmlUrl or @url]')]
 parsed = sorted(parsed, key=lambda item: getattr(item, 'title', getattr(item, 'text', '')))  # type: ignore[no-any-return]
 for outline in parsed:
  title: str = html_stripper.strip_html_entities(getattr(outline, 'title', getattr(outline, 'text', 'Untitled')))
  url: str | None = getattr(outline, 'xmlUrl', getattr(outline, 'url', None))
  if url is None:
   continue
  link: str | None = getattr(outline, 'htmlUrl', None)
  new: OPMLEntry = {
   "title": title,
   "url": url,
   "link": link,
  }
  lst.append(new)
 return lst
