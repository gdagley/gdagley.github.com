#!/usr/bin/env python3
"""Convert the resume .md file to a styled .html file.

Usage: python3 md_to_html.py <input.md> <output.html>

The markdown is exported from Google Docs, so it has some quirks this script
handles: backslash-escaped punctuation (\\-, \\#, \\&, \\)), bullets that are
themselves H3 headings (`* ### **Label:** value`), and the first job's role
title rendered as plain bold-italic instead of a `####` heading.
"""

import html
import re
import sys
from pathlib import Path

CSS = """\
        body {
            font-family: 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 0;
        }
        .subtitle {
            font-size: 1.2em;
            font-style: italic;
            color: #555;
            margin-bottom: 0;
        }
        .contact-info {
            margin-bottom: 30px;
        }
        .contact-info a {
            color: #2c3e50;
        }
        h2 {
            color: #2c3e50;
            border-bottom: 2px solid #2c3e50;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        h3 {
            color: #2c3e50;
            margin-top: 25px;
            margin-bottom: 5px;
        }
        h4 {
            font-style: italic;
            margin-top: 5px;
            margin-bottom: 10px;
            color: #555;
        }
        h5 {
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 10px;
        }
        ul {
            padding-left: 25px;
        }
        li {
            margin-bottom: 8px;
        }
        strong {
            font-weight: bold;
        }
        .section {
            margin-bottom: 30px;
        }
        .location {
            font-size: 0.95em;
            color: #888;
            margin-bottom: 5px;
        }
        .role-dates {
            font-size: 0.95em;
            color: #888;
            margin-bottom: 10px;
        }
"""

BULLET_RE = re.compile(r'^\s*\*\s+(.*)$')
DATE_LINE_RE = re.compile(r'^\*([^*].*?)\*$')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$')


def unescape(s: str) -> str:
    """Undo backslash escapes Google Docs adds when exporting to Markdown."""
    return re.sub(r'\\([\\\-#&)(*\[\]+.!_])', r'\1', s)


def en_dash_dates(s: str) -> str:
    """Normalize date-range separators to en-dash to match the rest of the page."""
    s = re.sub(r' - ', ' – ', s)
    s = re.sub(r'(\d{4})-(\d{4})', r'\1 – \2', s)
    return s


def escape_amp(s: str) -> str:
    """Escape stray ampersands without double-escaping existing entities."""
    return re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', s)


def render_link(match: re.Match) -> str:
    text, url = match.group(1), match.group(2)
    if url.startswith(('http://', 'https://')):
        return f'<a href="{url}" target="_blank">{text}</a>'
    return f'<a href="{url}">{text}</a>'


def inline(s: str) -> str:
    """Render inline markdown (links, bold, italic) as HTML."""
    s = unescape(s)
    s = re.sub(r'\b([\w.+-]+@[\w-]+\.[\w.-]+)\b',
               r'<a href="mailto:\1">\1</a>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', render_link, s)
    s = re.sub(r'\*\*\*([^*]+?)\*\*\*', r'<strong><em>\1</em></strong>', s)
    s = re.sub(r'\*\*([^*]+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![*])\*([^*]+?)\*(?![*])', r'<em>\1</em>', s)
    return escape_amp(s)


def plain(s: str) -> str:
    """Strip markdown emphasis markers and return HTML-escaped plain text."""
    s = re.sub(r'\*+', '', unescape(s)).strip()
    return html.escape(s, quote=False)


def parse(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            out.append('    </ul>')
            in_list = False

    # Preamble: first `#` is name, second `#` is subtitle, next non-blank is contacts.
    name = subtitle = contact = None
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue
        m = HEADING_RE.match(line)
        if m and m.group(1) == '#':
            if name is None:
                name = plain(m.group(2))
            elif subtitle is None:
                subtitle = plain(m.group(2))
            i += 1
            continue
        if name and subtitle and contact is None:
            contact = inline(line)
            i += 1
            break
        i += 1

    out.append(f'    <h1>{name}</h1>')
    out.append(f'    <div class="subtitle">{subtitle}</div>')
    out.append(f'    <div class="contact-info">{contact}</div>')

    # Body
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue

        m = HEADING_RE.match(line)
        if m:
            level, text = len(m.group(1)), m.group(2)
            if level == 2:
                close_list()
                out.append('')
                out.append(f'    <h2>{plain(text)}</h2>')
                i += 1
                # Wrap an immediate plain-text paragraph in <div class="section">.
                j = i
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    nxt = lines[j].rstrip()
                    if (not nxt.startswith('#')
                            and not BULLET_RE.match(nxt)
                            and not nxt.startswith('*')):
                        out.append('    <div class="section">')
                        out.append(f'        <p>{inline(nxt)}</p>')
                        out.append('    </div>')
                        i = j + 1
                continue
            if level == 3:
                close_list()
                out.append('')
                out.append(f'    <h3>{plain(text)}</h3>')
                i += 1
                # An immediate plain-text line is either a location or a date range.
                j = i
                while j < len(lines) and not lines[j].strip():
                    j += 1
                if j < len(lines):
                    nxt = lines[j].rstrip()
                    if (not nxt.startswith('#')
                            and not BULLET_RE.match(nxt)
                            and not nxt.startswith('*')):
                        is_date = bool(re.search(r'\b(19|20)\d{2}\b', nxt))
                        cls = 'role-dates' if is_date else 'location'
                        rendered = en_dash_dates(inline(nxt)) if is_date else inline(nxt)
                        out.append(f'    <div class="{cls}">{rendered}</div>')
                        i = j + 1
                continue
            if level == 4:
                close_list()
                out.append(f'    <h4>{plain(text)}</h4>')
                i += 1
                continue

        # Bold-italic role title without a `####` prefix (Codenta in the source).
        if line.startswith('***'):
            close_list()
            out.append(f'    <h4>{plain(line)}</h4>')
            i += 1
            continue

        # *Mar 2023 - Feb 2024* style date line.
        dm = DATE_LINE_RE.match(line)
        if dm:
            text = en_dash_dates(html.escape(unescape(dm.group(1)), quote=False))
            out.append(f'    <div class="role-dates">{text}</div>')
            i += 1
            continue

        bm = BULLET_RE.match(line)
        if bm:
            content = re.sub(r'^###\s+', '', bm.group(1))
            if not in_list:
                out.append('    <ul>')
                in_list = True
            out.append(f'        <li>{inline(content)}</li>')
            i += 1
            continue

        # Fallback: plain paragraph (used for the Codenta job's intro paragraph).
        close_list()
        out.append(f'    <p>{inline(line)}</p>')
        i += 1

    close_list()
    return '\n'.join(out)


def render(md: str, title: str = "Geoffrey Dagley - Resume") -> str:
    body = parse(md)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
{CSS}    </style>
</head>
<body>
{body}
</body>
</html>
"""


def main():
    if len(sys.argv) != 3:
        print("Usage: md_to_html.py <input.md> <output.html>", file=sys.stderr)
        sys.exit(1)
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.write_text(render(src.read_text()))
    print(f"Wrote {dst}")


if __name__ == '__main__':
    main()
