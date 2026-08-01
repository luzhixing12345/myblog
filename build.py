from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import socket
import threading
import time
import types
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote

import MarkdownParser
import syntaxlight


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "md-docs"
OUTPUT_DIR = ROOT / "docs"
TEMPLATE_PATH = ROOT / "base.html"
STYLESHEET_PATH = ROOT / "blog.css"
FAVICON_PATH = ROOT / "favicon.svg"

SITE_TITLE = "Kamilu's Blog"
SITE_DESCRIPTION = "关于编程、系统与实践的个人记录"
GITHUB_URL = "https://github.com/luzhixing12345"
DEFAULT_PORT = 9381
PAGE_SIZE = 10

EXCLUDED_POSTS = {"README.md", "about.md"}
MARKDOWN_LINK = re.compile(r'href="([^"]+?\.md)(#[^"]*)?"')
MARKDOWN_MARKS = re.compile(r"[#>*_`~\[\]()]")
FIRST_H1 = re.compile(r"<h1([^>]*)>.*?</h1>", re.DOTALL)

BUILD_LOCK = threading.Lock()


@dataclass
class Post:
    source: Path
    title: str
    category: str
    summary: str
    modified: datetime
    content: str = ""
    page_number: int = 1

    @property
    def slug(self) -> str:
        return self.source.stem

    @property
    def output_path(self) -> Path:
        return OUTPUT_DIR / "blog" / self.slug / "index.html"

    @property
    def home_path(self) -> Path:
        if self.page_number == 1:
            return OUTPUT_DIR / "index.html"
        return OUTPUT_DIR / "page" / str(self.page_number) / "index.html"

    @property
    def category_path(self) -> Path:
        return OUTPUT_DIR / "category" / self.category / "index.html"

    @property
    def anchor(self) -> str:
        return f"post-{self.slug}"


def extract_summary(markdown: str) -> str:
    in_code = False
    paragraph: list[str] = []
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line or line.startswith(("#", "!", "|", "---")):
            if paragraph:
                break
            continue
        paragraph.append(line)
        if len(" ".join(paragraph)) >= 120:
            break

    summary = " ".join(paragraph)
    summary = re.sub(r"!\[[^\]]*]\([^)]*\)", "", summary)
    summary = re.sub(r"\[([^\]]+)]\([^)]*\)", r"\1", summary)
    summary = MARKDOWN_MARKS.sub("", summary)
    summary = re.sub(r"\s+", " ", summary).strip()
    if not summary:
        return "暂无摘要"
    return summary[:140].rstrip() + ("…" if len(summary) > 140 else "")


def highlight_code(tree, languages: set[str]) -> None:
    def code_to_html(self) -> str:
        language = html.escape(self.input["language"], quote=True)
        return f'<pre class="language-{language}"><code>{self.input["code"]}</code></pre>'

    for block in tree.sub_blocks:
        if block.block_name == "CodeBlock":
            language = block.input.get("language") or "txt"
            try:
                language = syntaxlight.clean_language(language)
                if not syntaxlight.is_language_support(language):
                    language = "txt"
                result = syntaxlight.parse(block.input["code"], language)
                block.input["code"] = result.parser.to_html()
            except Exception:
                language = "txt"
                block.input["code"] = html.escape(block.input["code"])
            block.input["language"] = language
            block.to_html = types.MethodType(code_to_html, block)
            languages.add(language)
        highlight_code(block, languages)


def render_markdown(markdown: str, languages: set[str]) -> str:
    parser = MarkdownParser.Markdown()
    lines = parser.preprocess_parser(markdown)
    root = parser.block_parser(lines)
    tree = parser.tree_parser(root)
    highlight_code(tree, languages)
    return tree.to_html(parser.get_toc(tree))


def use_filename_as_title(content: str, title: str) -> str:
    heading = html.escape(title)
    if FIRST_H1.search(content):
        return FIRST_H1.sub(rf"<h1\1>{heading}</h1>", content, count=1)
    return content.replace("<div class='markdown-body'>", f"<div class='markdown-body'><h1>{heading}</h1>", 1)


def rewrite_markdown_links(content: str, post: Post) -> str:
    def replace(match: re.Match[str]) -> str:
        target_text = unquote(html.unescape(match.group(1)))
        if target_text.startswith(("http://", "https://")):
            return match.group(0)
        target = (post.source.parent / target_text).resolve()
        try:
            target.relative_to(SOURCE_DIR.resolve())
        except ValueError:
            return match.group(0)

        target_output = OUTPUT_DIR / "blog" / target.stem / "index.html"
        href = os.path.relpath(target_output, post.output_path.parent).replace(os.sep, "/")
        return f'href="{href}{match.group(2) or ""}"'

    return MARKDOWN_LINK.sub(replace, content)


def page_url(from_path: Path, target_path: Path) -> str:
    return os.path.relpath(target_path, from_path.parent).replace(os.sep, "/")


def render_page(
    *,
    output_path: Path,
    title: str,
    content: str,
    description: str = SITE_DESCRIPTION,
    active_nav: str = "",
) -> None:
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    replacements = {
        "{{PAGE_TITLE}}": html.escape(f"{title} · {SITE_TITLE}" if title != SITE_TITLE else title),
        "{{DESCRIPTION}}": html.escape(description, quote=True),
        "{{SITE_TITLE}}": html.escape(SITE_TITLE),
        "{{HOME_URL}}": page_url(output_path, OUTPUT_DIR / "index.html"),
        "{{CATEGORY_URL}}": page_url(output_path, OUTPUT_DIR / "category" / "index.html"),
        "{{ABOUT_URL}}": page_url(output_path, OUTPUT_DIR / "about" / "index.html"),
        "{{GITHUB_URL}}": GITHUB_URL,
        "{{CSS_URL}}": page_url(output_path, OUTPUT_DIR / "assets" / "blog.css"),
        "{{SYNTAX_CSS_URL}}": page_url(output_path, OUTPUT_DIR / "assets" / "syntax.css"),
        "{{ICON_URL}}": page_url(output_path, OUTPUT_DIR / "assets" / "favicon.svg"),
        "{{HOME_ACTIVE}}": ' aria-current="page"' if active_nav == "blog" else "",
        "{{CATEGORY_ACTIVE}}": ' aria-current="page"' if active_nav == "category" else "",
        "{{ABOUT_ACTIVE}}": ' aria-current="page"' if active_nav == "about" else "",
        "{{CONTENT}}": content,
        "{{YEAR}}": str(datetime.now().year),
    }
    for marker, value in replacements.items():
        template = template.replace(marker, value)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template, encoding="utf-8")


def discover_posts() -> list[Post]:
    posts: list[Post] = []
    slugs: dict[str, Path] = {}
    for source in SOURCE_DIR.rglob("*.md"):
        relative_path = source.relative_to(SOURCE_DIR)
        if relative_path.as_posix() in EXCLUDED_POSTS:
            continue
        if source.stem in slugs:
            raise RuntimeError(f"文章文件名重复：{slugs[source.stem]} 和 {source}")
        slugs[source.stem] = source

        markdown = source.read_text(encoding="utf-8")
        category_path = source.parent.relative_to(SOURCE_DIR).as_posix()
        posts.append(
            Post(
                source=source,
                title=source.stem,
                category="随笔" if category_path == "." else category_path,
                summary=extract_summary(markdown),
                modified=datetime.fromtimestamp(source.stat().st_mtime),
            )
        )
    posts.sort(key=lambda post: post.modified, reverse=True)
    for index, post in enumerate(posts):
        post.page_number = index // PAGE_SIZE + 1
    return posts


def render_post_cards(posts: list[Post], output_path: Path, with_anchors: bool = False) -> str:
    cards = []
    for post in posts:
        href = page_url(output_path, post.output_path)
        anchor = f' id="{html.escape(post.anchor, quote=True)}"' if with_anchors else ""
        cards.append(
            f"""
            <article class="post-card"{anchor}>
                <time datetime="{post.modified:%Y-%m-%d}">{post.modified:%Y.%m.%d}</time>
                <h2><a href="{href}">{html.escape(post.title)}</a></h2>
                <p>{html.escape(post.summary)}</p>
            </article>"""
        )
    return "".join(cards)


def pagination_html(current_page: int, total_pages: int, output_path: Path) -> str:
    links = []
    for page_number in range(1, total_pages + 1):
        target = OUTPUT_DIR / "index.html" if page_number == 1 else OUTPUT_DIR / "page" / str(page_number) / "index.html"
        current = ' aria-current="page"' if page_number == current_page else ""
        links.append(f'<a href="{page_url(output_path, target)}"{current}>{page_number}</a>')
    return f'<nav class="pagination" aria-label="文章分页">{"".join(links)}</nav>'


def render_home(posts: list[Post]) -> None:
    total_pages = max(1, (len(posts) + PAGE_SIZE - 1) // PAGE_SIZE)
    for page_number in range(1, total_pages + 1):
        output_path = (
            OUTPUT_DIR / "index.html"
            if page_number == 1
            else OUTPUT_DIR / "page" / str(page_number) / "index.html"
        )
        page_posts = posts[(page_number - 1) * PAGE_SIZE : page_number * PAGE_SIZE]
        if page_number == 1:
            heading = f"""
            <section class="hero">
                <p class="eyebrow">WRITING &amp; NOTES</p>
                <h1>个人博客</h1>
                <p>{html.escape(SITE_DESCRIPTION)}。目前共收录 {len(posts)} 篇文章。</p>
            </section>"""
        else:
            heading = f"""
            <section class="archive-heading">
                <p class="eyebrow">ALL POSTS</p>
                <h1>全部文章</h1>
                <p>第 {page_number} / {total_pages} 页</p>
            </section>"""

        content = f"""
        {heading}
        <section class="post-list" aria-label="文章列表">
            {render_post_cards(page_posts, output_path, with_anchors=True)}
        </section>
        {pagination_html(page_number, total_pages, output_path)}
        """
        render_page(
            output_path=output_path,
            title=SITE_TITLE if page_number == 1 else f"Blog · 第 {page_number} 页",
            content=content,
            active_nav="blog",
        )


def render_categories(posts: list[Post]) -> None:
    categories: dict[str, list[Post]] = {}
    for post in posts:
        categories.setdefault(post.category, []).append(post)

    index_path = OUTPUT_DIR / "category" / "index.html"
    category_cards = []
    for category, category_posts in categories.items():
        href = page_url(index_path, category_posts[0].category_path)
        category_cards.append(
            f"""
            <a class="category-card" href="{href}">
                <h2>{html.escape(category)}</h2>
                <p>{len(category_posts)} 篇文章</p>
                <time>最近更新 {category_posts[0].modified:%Y.%m.%d}</time>
            </a>"""
        )

    render_page(
        output_path=index_path,
        title="Category",
        content=f"""
        <section class="archive-heading">
            <p class="eyebrow">CATEGORIES</p>
            <h1>文章分类</h1>
            <p>按主题浏览全部文章。</p>
        </section>
        <section class="category-grid">{"".join(category_cards)}</section>
        """,
        active_nav="category",
    )

    for category, category_posts in categories.items():
        output_path = category_posts[0].category_path
        render_page(
            output_path=output_path,
            title=category,
            content=f"""
            <section class="archive-heading">
                <p class="eyebrow">CATEGORY</p>
                <h1>{html.escape(category)}</h1>
            </section>
            <section class="post-list" aria-label="{html.escape(category, quote=True)}分类文章">
                {render_post_cards(category_posts, output_path)}
            </section>
            """,
            active_nav="category",
        )


def render_about(languages: set[str]) -> None:
    source = SOURCE_DIR / "about.md"
    markdown = source.read_text(encoding="utf-8") if source.exists() else ""
    if markdown.strip():
        content = render_markdown(markdown, languages)
    else:
        content = "<div class='markdown-body'><h1>About</h1><p>关于页面尚未填写。</p></div>"
    render_page(
        output_path=OUTPUT_DIR / "about" / "index.html",
        title="About",
        content=f'<article class="article-shell">{content}</article>',
        active_nav="about",
    )


def render_posts(posts: list[Post], languages: set[str]) -> None:
    for post in posts:
        markdown = post.source.read_text(encoding="utf-8")
        post.content = use_filename_as_title(
            rewrite_markdown_links(render_markdown(markdown, languages), post),
            post.title,
        )
        category_url = page_url(post.output_path, post.category_path)
        article = f"""
        <article class="article-shell">
            <div class="article-meta">
                <a href="{category_url}">{html.escape(post.category)}</a>
                <time datetime="{post.modified:%Y-%m-%d}">更新于 {post.modified:%Y 年 %m 月 %d 日}</time>
            </div>
            {post.content}
        </article>
        """
        render_page(
            output_path=post.output_path,
            title=post.title,
            content=article,
            description=post.summary,
            active_nav="blog",
        )


def build() -> None:
    with BUILD_LOCK:
        if not SOURCE_DIR.exists():
            raise RuntimeError(f"Markdown 目录不存在：{SOURCE_DIR}")
        if not TEMPLATE_PATH.exists() or not STYLESHEET_PATH.exists() or not FAVICON_PATH.exists():
            raise RuntimeError("缺少 base.html、blog.css 或 favicon.svg")

        shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
        (OUTPUT_DIR / "assets").mkdir(parents=True)
        shutil.copy2(STYLESHEET_PATH, OUTPUT_DIR / "assets" / "blog.css")
        shutil.copy2(FAVICON_PATH, OUTPUT_DIR / "assets" / "favicon.svg")

        languages: set[str] = set()
        posts = discover_posts()
        render_home(posts)
        render_categories(posts)
        render_posts(posts, languages)
        render_about(languages)
        syntaxlight.export_css(sorted(languages), str(OUTPUT_DIR / "assets"))

        syntax_css = []
        for language in sorted(languages):
            language_css = OUTPUT_DIR / "assets" / f"{language}.css"
            if language_css.exists():
                syntax_css.append(language_css.read_text(encoding="utf-8"))
        (OUTPUT_DIR / "assets" / "syntax.css").write_text("\n".join(syntax_css), encoding="utf-8")
        print(f"\033[36m>\033[0m 已生成 {len(posts)} 篇文章")


class BlogRequestHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def do_GET(self) -> None:
        try:
            super().do_GET()
        except (BrokenPipeError, ConnectionResetError):
            pass


def get_ip_address() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("10.255.255.255", 1))
        return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        sock.close()


def find_available_port(start: int) -> int:
    for port in range(start, min(start + 100, 65536)):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("", port))
                return port
            except OSError:
                continue
    raise RuntimeError("没有可用的 HTTP 端口")


def show_server_info(port: int, elapsed: float) -> None:
    print(
        f"""
    \033[1mZOOD BLOG\033[0m  ready in {elapsed:.2f} s

    \033[36m>\033[0m  \033[1mLocal:\033[0m   http://127.0.0.1:{port}/
    \033[36m>\033[0m  \033[1mRemote:\033[0m  http://{get_ip_address()}:{port}/
    \033[36m>\033[0m  输入 \033[1mq\033[0m 退出
"""
    )


def serve(port: int) -> None:
    started_at = time.perf_counter()
    build()
    actual_port = find_available_port(port)
    handler = partial(BlogRequestHandler, directory=str(OUTPUT_DIR))
    server = ThreadingHTTPServer(("", actual_port), handler)

    local_url = f"http://127.0.0.1:{actual_port}/"
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    show_server_info(actual_port, time.perf_counter() - started_at)
    webbrowser.open(local_url)

    try:
        while True:
            command = input().strip().lower()
            if command == "q":
                break
    except (KeyboardInterrupt, EOFError):
        print("\n正在关闭服务器...")
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=1)


def main() -> None:
    parser = argparse.ArgumentParser(description="构建并预览个人静态博客")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="开发服务器端口")
    parser.add_argument("--build-only", action="store_true", help="只构建，不启动服务器")
    args = parser.parse_args()
    if args.build_only:
        build()
    else:
        serve(args.port)


if __name__ == "__main__":
    main()
