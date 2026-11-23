"""A topic's lesson is one Markdown file (lesson.md), split into sections at each `## ` heading.

- The `# ` title and anything before the first `## ` heading are the lesson's introduction.
- Every `## ` heading starts a section, which gets its own page. A heading that starts with a
  number ("## 7. Lists") gives the section that number, so practice exercises can point at it
  with `lesson: 7` in their front matter.
- A "## Table of Contents" section is dropped, since the app builds its own.
- Links to headings in the same file (`[section 17](#17-comprehensions-...)`) are turned into
  links to the right section page. Links to other local .md files that the app can't serve are
  shown as plain text.

The Markdown is rendered once, at startup, with markdown-it (CommonMark plus tables) and
Pygments for code. Raw HTML in the file is not rendered.
"""
import re

from markdown_it import MarkdownIt
from markupsafe import Markup, escape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

FENCE_RE = re.compile(r"^\s{0,3}(```|~~~)")
NUMBER_RE = re.compile(r"^(\d+)[.)]\s+")
SKIP_SECTIONS = {"table of contents", "contents"}
_FORMATTER = HtmlFormatter(nowrap=True)


def slugify(heading):
    """GitHub-style anchor: lowercase, drop punctuation, spaces become dashes."""
    text = re.sub(r"[`*_~]|\[|\]\([^)]*\)", "", heading).strip().lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def plain(heading):
    """Heading text without Markdown markup, for titles and the table of contents."""
    return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", heading)).strip()


def _split(text):
    """Return (title, intro_lines, [(heading, body_lines)]) splitting at ## outside code fences."""
    title, intro, sections = "", [], []
    in_fence = False
    current = intro
    for line in text.replace("\r\n", "\n").split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            if line.startswith("## "):
                current = []
                sections.append((line[3:].strip(), current))
                continue
            if line.startswith("# ") and not title and not sections:
                title = line[2:].strip()
                continue
        current.append(line)
    return title, intro, sections


def _anchors(body_lines):
    """Slugs of ### and deeper headings inside a section."""
    out, in_fence = [], False
    for line in body_lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            m = re.match(r"^#{3,6}\s+(.+?)\s*#*\s*$", line)
            if m:
                out.append(slugify(m.group(1)))
    return out


def _strip_rule(lines):
    """Drop the trailing --- separators the source file puts between sections."""
    while lines and lines[-1].strip() in ("", "---", "***"):
        lines.pop()
    while lines and lines[0].strip() in ("", "---", "***"):
        lines.pop(0)
    return "\n".join(lines)


def _highlight(code, lang, _attrs):
    try:
        lexer = get_lexer_by_name(lang or "text")
    except ClassNotFound:
        return ""  # markdown-it escapes it itself
    return highlight(code, lexer, _FORMATTER)


def _renderer(link_for):
    md = MarkdownIt("commonmark", {"html": False, "highlight": _highlight, "typographer": False}).enable("table").enable("strikethrough")

    def heading_open(_self, tokens, idx, options, env):
        tok = tokens[idx]
        inline = tokens[idx + 1]
        tok.attrSet("id", slugify(inline.content))
        return _self.renderToken(tokens, idx, options, env)

    def fence(_self, tokens, idx, options, env):
        tok = tokens[idx]
        lang = tok.info.strip().split(" ")[0] if tok.info else ""
        body = _highlight(tok.content, lang, None) or str(escape(tok.content))
        if lang not in ("python", "py", "python3"):
            return f'<div class="lesson-code"><pre class="code hl"><code>{body.rstrip()}</code></pre></div>\n'
        head = ('<div class="code-head"><span>Python</span><button type="button" class="linkish try-code" '
                'title="Open this code in a new scratchpad notebook and run it">Try it in the scratchpad ▸</button></div>')
        return f'<div class="lesson-code has-head">{head}<pre class="code hl"><code>{body.rstrip()}</code></pre></div>\n'

    def table_open(_self, tokens, idx, options, env):
        return '<div class="table-wrap"><table class="lesson-table">\n'

    def table_close(_self, tokens, idx, options, env):
        return "</table></div>\n"

    for level in ("heading_open",):
        md.add_render_rule(level, heading_open)
    md.add_render_rule("fence", fence)
    md.add_render_rule("table_open", table_open)
    md.add_render_rule("table_close", table_close)

    def rewrite_links(state):
        for block in state.tokens:
            if block.type != "inline" or not block.children:
                continue
            kept, drop_close = [], 0
            for tok in block.children:
                if tok.type == "link_open":
                    href = tok.attrGet("href") or ""
                    new = link_for(href)
                    if new is None:
                        drop_close += 1
                        tok.meta["dropped"] = True
                        continue
                    tok.attrSet("href", new)
                    if new.startswith(("http://", "https://")):
                        tok.attrSet("target", "_blank")
                        tok.attrSet("rel", "noopener")
                elif tok.type == "link_close" and drop_close:
                    # links don't nest in CommonMark, so the next close belongs to the dropped open
                    drop_close -= 1
                    continue
                kept.append(tok)
            block.children = kept

    md.core.ruler.push("grind_links", rewrite_links)
    return md


def parse_lesson(text, topic_id, name="lesson.md"):
    title, intro_lines, raw_sections = _split(text)
    sections = []
    for heading, body in raw_sections:
        if plain(heading).lower() in SKIP_SECTIONS:
            continue
        slug = slugify(heading)
        m = NUMBER_RE.match(plain(heading))
        sections.append({
            "id": slug,
            "heading": heading,
            "title": plain(NUMBER_RE.sub("", plain(heading))),
            "number": int(m.group(1)) if m else None,
            "body": _strip_rule(body),
            "anchors": _anchors(body),
            "exercises": [],
        })
    if not sections:
        raise ValueError(f"{topic_id}/{name}: no '## ' sections found")
    ids = [s["id"] for s in sections]
    if len(set(ids)) != len(ids):
        raise ValueError(f"{topic_id}/{name}: two sections have the same heading")

    base = f"/topics/{topic_id}/lesson"
    where = {}
    for s in sections:
        where[s["id"]] = f"{base}/{s['id']}"
        for a in s["anchors"]:
            where.setdefault(a, f"{base}/{s['id']}#{a}")

    def link_for(href):
        if href.startswith("#"):
            return where.get(href[1:], href)
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I):
            return href  # http(s), mailto, ...
        if href.split("#")[0].lower().endswith(".md"):
            return None  # another local file we can't serve: keep the text, drop the link
        return href

    md = _renderer(link_for)
    for i, s in enumerate(sections):
        s["index"] = i
        s["html"] = Markup(md.render(s.pop("body")))
    intro = _strip_rule(intro_lines)
    return {
        "title": plain(title) or "Lesson",
        "intro_html": Markup(md.render(intro)) if intro.strip() else Markup(""),
        "sections": sections,
        "by_id": {s["id"]: s for s in sections},
        "by_number": {s["number"]: s for s in sections if s["number"] is not None},
    }
