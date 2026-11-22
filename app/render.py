"""Tiny, safe Markdown subset for question text: ```fenced code```, `inline code`, **bold**, *italic*,
and "- " bullet lists."""
import re

from markupsafe import Markup, escape

FENCE_RE = re.compile(r"```[\w+-]*\n(.*?)```", re.S)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
ITALIC_RE = re.compile(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])")


def md(text):
    if not text:
        return Markup("")
    parts, last = [], 0
    for m in FENCE_RE.finditer(text):
        parts.append(_inline(text[last:m.start()]))
        parts.append(f'<pre class="code"><code>{escape(m.group(1).rstrip())}</code></pre>')
        last = m.end()
    parts.append(_inline(text[last:]))
    return Markup("".join(parts))


def _inline(text):
    text = text.strip("\n")
    if not text:
        return ""
    codes = []

    def stash(m):
        codes.append(f"<code>{escape(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    out = INLINE_CODE_RE.sub(stash, text)
    out = str(escape(out))
    out = BOLD_RE.sub(r"<strong>\1</strong>", out)
    out = ITALIC_RE.sub(r"<em>\1</em>", out)
    out = re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], out)
    return "".join(_block(p) for p in re.split(r"\n\s*\n", out))


def _block(par):
    lines = par.split("\n")
    if all(re.match(r"\s*[-*] ", ln) or (i and ln.startswith("  ")) for i, ln in enumerate(lines)):
        items = []
        for ln in lines:
            if re.match(r"\s*[-*] ", ln):
                items.append(re.sub(r"^\s*[-*] ", "", ln))
            else:
                items[-1] += " " + ln.strip()
        return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
    return f"<p>{'<br>'.join(lines)}</p>"


def md_inline(text):
    """Same as md() but without the wrapping <p>, for option labels."""
    html = str(md(text))
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]
    return Markup(html)


def init_app(app):
    app.jinja_env.filters["md"] = md
    app.jinja_env.filters["md_inline"] = md_inline
