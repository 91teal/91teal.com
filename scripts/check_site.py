#!/usr/bin/env python3
"""Dependency-free checks for the static 91teal.com site."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
HTML_FILES = (ROOT / "index.html", ROOT / "photo-organizer.html")
SKIPPED_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:")


class SiteHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        for attribute in ("href", "src", "poster"):
            if values.get(attribute):
                self.references.append((attribute, values[attribute] or ""))


def exact_case_path_exists(path: Path) -> bool:
    """Return True only if every path component matches filesystem case."""
    try:
        relative = path.resolve().relative_to(ROOT.resolve())
    except (OSError, ValueError):
        return False

    current = ROOT.resolve()
    for part in relative.parts:
        try:
            names = {child.name for child in current.iterdir()}
        except OSError:
            return False
        if part not in names:
            return False
        current = current / part
    return current.is_file()


def local_path(raw_reference: str, source: Path) -> Path | None:
    reference = raw_reference.strip()
    if not reference or reference.startswith("#") or reference.lower().startswith(SKIPPED_SCHEMES):
        return None
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    if path_text.startswith("/"):
        return ROOT / path_text.lstrip("/")
    return source.parent / path_text


def check_html(path: Path, errors: list[str]) -> SiteHTMLParser:
    parser = SiteHTMLParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path.name}: cannot be read as UTF-8 ({exc})")
        return parser
    except Exception as exc:  # HTMLParser reports malformed constructs here.
        errors.append(f"{path.name}: HTML parsing failed ({exc})")
        return parser

    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    for item in duplicates:
        errors.append(f"{path.name}: duplicate id #{item}")

    id_set = set(parser.ids)
    for attribute, reference in parser.references:
        if reference.startswith("#") and reference[1:] not in id_set:
            errors.append(f"{path.name}: {attribute}=\"{reference}\" has no matching id")
        referenced_path = local_path(reference, path)
        if referenced_path is not None and not exact_case_path_exists(referenced_path):
            errors.append(f"{path.name}: missing or case-mismatched local file {reference}")
    return parser


def check_css(errors: list[str]) -> None:
    css_path = ROOT / "styles.css"
    try:
        css = css_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"styles.css: cannot be read as UTF-8 ({exc})")
        return

    for raw_reference in re.findall(r"url\(\s*['\"]?([^)'\"]+)", css):
        referenced_path = local_path(raw_reference, css_path)
        if referenced_path is not None and not exact_case_path_exists(referenced_path):
            errors.append(f"styles.css: missing or case-mismatched local file {raw_reference}")


def check_gallery(errors: list[str]) -> None:
    try:
        html = (ROOT / "index.html").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return

    filenames = re.findall(r"\{\s*file:\s*['\"]([^'\"]+)['\"]", html)
    if not filenames:
        errors.append("index.html: galleryData contains no photos")
        return

    if len(filenames) != len(set(filenames)):
        errors.append("index.html: galleryData contains duplicate filenames")

    for filename in filenames:
        image_path = ROOT / "Images" / filename
        if not exact_case_path_exists(image_path):
            errors.append(f"index.html: gallery image is missing or case-mismatched: Images/{filename}")


def main() -> int:
    errors: list[str] = []

    cname_path = ROOT / "CNAME"
    try:
        cname = cname_path.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeError) as exc:
        errors.append(f"CNAME: cannot be read ({exc})")
    else:
        if cname != "www.91teal.com":
            errors.append(f"CNAME: expected www.91teal.com, found {cname!r}")

    for html_file in HTML_FILES:
        if not exact_case_path_exists(html_file):
            errors.append(f"Missing required file: {html_file.name}")
            continue
        check_html(html_file, errors)

    check_css(errors)
    check_gallery(errors)

    if errors:
        print("Site checks failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Site checks passed: HTML anchors, local files, gallery images, CSS URLs, and CNAME.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
