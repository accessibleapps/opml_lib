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
    parsed = [opml.OutlineElement(i) for i in opml.parse(filename)._tree.xpath(".//outline[@xmlUrl or @url]")]
    parsed = sorted(parsed, key=lambda item: getattr(item, "title", getattr(item, "text", "")))  # pyright: ignore[reportUnknownLambdaType]
    for outline in parsed:
        raw_title = getattr(outline, "title", None) or getattr(outline, "text", None) or "Untitled"
        # Only strip HTML if there's something that looks like a tag (has alpha char after <)
        if (
            "<" in raw_title
            and ">" in raw_title
            and any(c.isalpha() for c in raw_title[raw_title.index("<") + 1 : raw_title.index(">")])
        ):
            try:
                title: str = html_stripper.strip_tags(raw_title)  # pyright: ignore[reportAttributeAccessIssue]
            except (AttributeError, ValueError):  # html_stripper can fail on malformed input
                title = raw_title
        else:
            title = raw_title
        url: str | None = getattr(outline, "xmlUrl", getattr(outline, "url", None))
        if url is None:  # pragma: no cover - xpath already filters for xmlUrl or url
            continue
        link: str | None = getattr(outline, "htmlUrl", None)
        new: OPMLEntry = {
            "title": title,
            "url": url,
            "link": link,
        }
        lst.append(new)
    return lst
