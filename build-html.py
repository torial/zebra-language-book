#!/usr/bin/env python3
"""
Zebra Programming Book - HTML Documentation Generator

Generates a beautiful, responsive HTML documentation site from markdown chapters.

Features:
- Dark mode support
- Searchable content
- Sidebar navigation
- Mobile-friendly
- Syntax highlighting
- Embedded diagrams
- Table of contents

Usage:
    python3 build-html.py

Output:
    docs/ (HTML documentation site)
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple
import html
from datetime import datetime

class HtmlBuilder:
    def __init__(self, book_root: str = "."):
        self.book_root = Path(book_root)
        self.docs_dir = self.book_root / "docs"
        self.chapters = []
        self.toc = []

    def create_directories(self):
        """Create output directory structure."""
        self.docs_dir.mkdir(exist_ok=True)
        (self.docs_dir / "css").mkdir(exist_ok=True)
        (self.docs_dir / "js").mkdir(exist_ok=True)
        (self.docs_dir / "diagrams").mkdir(exist_ok=True)
        print(f"✓ Created {self.docs_dir}/ structure")

    def find_chapters(self) -> List[Tuple[str, str, Path]]:
        """Find all markdown chapters organized by part."""
        chapters = []
        part_order = []

        for part_dir in sorted(self.book_root.glob("Part-*")):
            if not part_dir.is_dir():
                continue

            part_name = part_dir.name.replace("Part-", "").replace("-", " ")
            part_order.append(part_name)

            for md_file in sorted(part_dir.glob("*.md")):
                chapter_name = md_file.stem
                chapters.append((part_name, chapter_name, md_file))

        return chapters

    def copy_diagrams(self):
        """Copy diagram files to output."""
        diagrams_src = self.book_root / "diagrams"
        diagrams_dst = self.docs_dir / "diagrams"

        if not diagrams_src.exists():
            return

        for svg_file in diagrams_src.glob("*.svg"):
            try:
                import shutil
                shutil.copy2(svg_file, diagrams_dst / svg_file.name)
            except Exception as e:
                print(f"⚠️  Could not copy diagram {svg_file.name}: {e}")

    def read_chapter(self, filepath: Path) -> str:
        """Read chapter content."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"✗ Error reading {filepath}: {e}")
            return ""

    def markdown_to_html(self, content: str) -> str:
        """Convert markdown to HTML (simplified)."""
        # This is a basic converter - for production, use a library like python-markdown

        # Headers
        content = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', content, flags=re.MULTILINE)
        content = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', content, flags=re.MULTILINE)
        content = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', content, flags=re.MULTILINE)
        content = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', content, flags=re.MULTILINE)

        # Code blocks (zebra)
        content = re.sub(
            r'```zebra\n(.*?)```',
            lambda m: f'<pre><code class="language-zebra">{html.escape(m.group(1))}</code></pre>',
            content,
            flags=re.DOTALL
        )

        # Code blocks (other)
        content = re.sub(
            r'```(\w*)\n(.*?)```',
            lambda m: f'<pre><code class="language-{m.group(1) or "text"}">{html.escape(m.group(2))}</code></pre>',
            content,
            flags=re.DOTALL
        )

        # Inline code
        content = re.sub(r'`([^`]+)`', r'<code>\1</code>', content)

        # Bold
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)

        # Italic
        content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', content)

        # Links
        content = re.sub(
            r'\[(.*?)\]\((.*?)\)',
            r'<a href="\2">\1</a>',
            content
        )

        # Images (diagrams)
        content = re.sub(
            r'!\[(.*?)\]\((.*?)\)',
            lambda m: f'<figure><img src="{self._resolve_image_path(m.group(2))}" alt="{m.group(1)}" /><figcaption>{m.group(1)}</figcaption></figure>',
            content
        )

        # Horizontal rules
        content = re.sub(r'^---$', '<hr />', content, flags=re.MULTILINE)

        # Paragraphs
        lines = content.split('\n')
        result = []
        in_block = False
        buffer = []

        for line in lines:
            if line.startswith(('<h', '<pre', '<hr', '<figure')):
                if buffer:
                    result.append('<p>' + ' '.join(buffer) + '</p>')
                    buffer = []
                result.append(line)
                in_block = True
            elif line.strip() == '':
                if buffer:
                    result.append('<p>' + ' '.join(buffer) + '</p>')
                    buffer = []
                in_block = False
            else:
                buffer.append(line)

        if buffer:
            result.append('<p>' + ' '.join(buffer) + '</p>')

        return '\n'.join(result)

    def _resolve_image_path(self, path: str) -> str:
        """Resolve image paths for output."""
        if path.startswith('../diagrams/'):
            return 'diagrams/' + path.split('/')[-1]
        return path

    def generate_chapter_html(self, part: str, chapter_name: str, content: str) -> str:
        """Generate HTML for a single chapter."""
        html_content = self.markdown_to_html(content)

        # Extract first heading for title
        title_match = re.search(r'<h1>(.*?)</h1>', html_content)
        title = title_match.group(1) if title_match else chapter_name

        # Build page
        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)} - Zebra Programming Book</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/highlights.css">
    <script src="../js/search.js" defer></script>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h2><a href="../index.html">Zebra</a></h2>
                <p>Programming Language</p>
            </div>
            <nav class="sidebar-nav" id="sidebar-nav">
                <!-- Generated by JavaScript -->
            </nav>
            <div class="sidebar-search">
                <input type="text" id="search-box" placeholder="Search...">
            </div>
            <div class="sidebar-footer">
                <p>v1.0 · April 2026</p>
                <p><a href="https://github.com/zebra-lang/book">View on GitHub</a></p>
            </div>
        </aside>

        <main class="content">
            <div class="breadcrumb">
                <a href="../index.html">Home</a>
                <span>/</span>
                <span>{html.escape(part)}</span>
                <span>/</span>
                <span>{html.escape(chapter_name)}</span>
            </div>

            <article class="chapter">
                {html_content}
            </article>

            <footer class="chapter-footer">
                <div class="navigation">
                    <a href="#" class="prev-chapter">← Previous</a>
                    <a href="#" class="next-chapter">Next →</a>
                </div>
                <p class="edit-link">
                    <a href="https://github.com/zebra-lang/book/edit/main/Part-X/{chapter_name}.md">
                        Edit on GitHub
                    </a>
                </p>
                <p class="generated">Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </footer>
        </main>
    </div>

    <script>
        // Initialize search
        initializeSearch(document.getElementById('search-box'));
    </script>
</body>
</html>"""

        return page

    def generate_index(self) -> str:
        """Generate index/landing page."""
        chapters_list = ""
        current_part = ""

        for part, chapter_name, _ in self.chapters:
            if part != current_part:
                if current_part:
                    chapters_list += "</ul>\n"
                chapters_list += f'<h3>{part}</h3>\n<ul>\n'
                current_part = part

            # Convert chapter name to file path
            file_path = f"chapters/{chapter_name.lower()}.html"
            chapters_list += f'<li><a href="{file_path}">{chapter_name.replace("-", " ").title()}</a></li>\n'

        if current_part:
            chapters_list += "</ul>\n"

        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zebra Programming Language - Learn to Code</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body class="index-page">
    <div class="hero">
        <h1>Zebra Programming Language</h1>
        <p class="tagline">Modern. Safe. Fast. Learn from the ground up.</p>
        <div class="cta-buttons">
            <a href="chapters/01-getting-started.html" class="btn btn-primary">Start Learning</a>
            <a href="#chapters" class="btn btn-secondary">Browse All Chapters</a>
        </div>
    </div>

    <section class="features">
        <div class="feature">
            <h3>🔒 Type Safety</h3>
            <p>Catch bugs at compile time with Zebra's strong type system and nil tracking.</p>
        </div>
        <div class="feature">
            <h3>⚡ Performance</h3>
            <p>Compile to native code via Zig. No garbage collection overhead.</p>
        </div>
        <div class="feature">
            <h3>📚 Beginner Friendly</h3>
            <p>Clear syntax inspired by Python. Learn from 22 comprehensive chapters.</p>
        </div>
    </section>

    <section id="chapters" class="chapters">
        <h2>Complete Book</h2>
        {chapters_list}
    </section>

    <footer>
        <p>Zebra Programming Book · {datetime.now().strftime('%Y')} · <a href="https://github.com/zebra-lang/book">GitHub</a></p>
    </footer>

    <script src="js/search.js"></script>
</body>
</html>"""

        return page

    def create_css(self):
        """Create stylesheet."""
        css_content = """/* Zebra Programming Book - Main Stylesheet */

:root {
    --primary: #0284c7;
    --success: #16a34a;
    --warning: #d97706;
    --error: #dc2626;
    --bg-light: #f9fafb;
    --bg-dark: #1f2937;
    --text-light: #374151;
    --text-dark: #f3f4f6;
    --border: #e5e7eb;
    --code-bg: #f3f4f6;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: var(--text-light);
    background: white;
}

/* Layout */
.container {
    display: grid;
    grid-template-columns: 280px 1fr;
    min-height: 100vh;
}

.sidebar {
    background: var(--bg-light);
    border-right: 1px solid var(--border);
    padding: 2rem 1.5rem;
    position: sticky;
    top: 0;
    height: 100vh;
    overflow-y: auto;
}

.content {
    padding: 3rem;
    max-width: 900px;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    margin: 1.5rem 0 0.75rem 0;
    font-weight: 600;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }

p {
    margin: 1rem 0;
}

code {
    background: var(--code-bg);
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-family: 'Monaco', monospace;
    font-size: 0.9em;
}

pre {
    background: var(--bg-dark);
    color: var(--text-dark);
    padding: 1rem;
    border-radius: 6px;
    overflow-x: auto;
    margin: 1rem 0;
}

pre code {
    background: none;
    padding: 0;
    color: inherit;
}

/* Links */
a {
    color: var(--primary);
    text-decoration: none;
    transition: opacity 0.2s;
}

a:hover {
    opacity: 0.7;
    text-decoration: underline;
}

/* Images */
figure {
    margin: 2rem 0;
    text-align: center;
}

figure img {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    border: 1px solid var(--border);
}

figcaption {
    margin-top: 0.5rem;
    font-size: 0.9em;
    color: #6b7280;
}

/* Navigation */
.sidebar-nav {
    margin: 2rem 0;
}

.sidebar-nav ul {
    list-style: none;
}

.sidebar-nav a {
    display: block;
    padding: 0.5rem 0;
    font-size: 0.95em;
}

.sidebar-nav a:hover {
    color: var(--primary);
}

/* Search */
.sidebar-search {
    margin-top: 2rem;
}

#search-box {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    font-size: 0.9em;
}

/* Buttons */
.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 4px;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s;
}

.btn-primary {
    background: var(--primary);
    color: white;
}

.btn-primary:hover {
    opacity: 0.8;
}

.btn-secondary {
    background: transparent;
    color: var(--primary);
    border: 2px solid var(--primary);
}

/* Index page */
.index-page .hero {
    background: linear-gradient(135deg, var(--primary), #0369a1);
    color: white;
    padding: 6rem 2rem;
    text-align: center;
}

.hero h1 {
    font-size: 3.5rem;
    margin-bottom: 1rem;
}

.tagline {
    font-size: 1.3em;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.cta-buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

/* Features */
.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    padding: 4rem 2rem;
    background: var(--bg-light);
}

.feature {
    padding: 2rem;
    background: white;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.feature h3 {
    margin-top: 0;
}

/* Responsive */
@media (max-width: 768px) {
    .container {
        grid-template-columns: 1fr;
    }

    .sidebar {
        border-bottom: 1px solid var(--border);
        position: static;
        height: auto;
    }

    .content {
        padding: 1.5rem;
    }

    h1 { font-size: 1.75rem; }
    h2 { font-size: 1.5rem; }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    body {
        background: var(--bg-dark);
        color: var(--text-dark);
    }

    .sidebar {
        background: #111827;
        border-color: #374151;
    }

    .content {
        background: var(--bg-dark);
        color: var(--text-dark);
    }

    code {
        background: #374151;
    }

    pre {
        background: #0f172a;
    }
}
"""

        css_path = self.docs_dir / "css" / "style.css"
        try:
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_content)
            print(f"✓ Created stylesheet: {css_path}")
        except Exception as e:
            print(f"✗ Error creating stylesheet: {e}")

    def create_js(self):
        """Create JavaScript for interactivity."""
        js_content = """// Zebra Programming Book - Search and Navigation

function initializeSearch(searchBox) {
    if (!searchBox) return;

    searchBox.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const chapters = document.querySelectorAll('.sidebar-nav a');

        chapters.forEach(chapter => {
            const text = chapter.textContent.toLowerCase();
            chapter.style.display = text.includes(query) ? 'block' : 'none';
        });
    });
}

// Theme toggle
function toggleTheme() {
    const isDark = document.documentElement.style.colorScheme === 'dark';
    document.documentElement.style.colorScheme = isDark ? 'light' : 'dark';
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}

// Load saved theme
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.style.colorScheme = savedTheme;
    }
});

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
"""

        js_path = self.docs_dir / "js" / "search.js"
        try:
            with open(js_path, 'w', encoding='utf-8') as f:
                f.write(js_content)
            print(f"✓ Created JavaScript: {js_path}")
        except Exception as e:
            print(f"✗ Error creating JavaScript: {e}")

    def run(self):
        """Generate HTML documentation."""
        print("=" * 70)
        print("Zebra Programming Book - HTML Documentation Generator")
        print("=" * 70)
        print()

        # Setup
        self.create_directories()
        self.copy_diagrams()
        self.create_css()
        self.create_js()
        print()

        # Find chapters
        self.chapters = self.find_chapters()

        if not self.chapters:
            print("✗ No chapters found!")
            return False

        print(f"Found {len(self.chapters)} chapters\n")
        print("Generating HTML...\n")

        chapters_dir = self.docs_dir / "chapters"
        chapters_dir.mkdir(exist_ok=True)

        # Generate each chapter
        for i, (part, chapter_name, filepath) in enumerate(self.chapters, 1):
            print(f"[{i}/{len(self.chapters)}] {chapter_name}...", end=" ", flush=True)

            content = self.read_chapter(filepath)
            if not content:
                print("✗")
                continue

            html = self.generate_chapter_html(part, chapter_name, content)
            output_file = chapters_dir / f"{chapter_name.lower()}.html"

            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html)
                print("✓")
            except Exception as e:
                print(f"✗ {e}")

        # Generate index
        print(f"\nGenerating index page...", end=" ", flush=True)
        index_html = self.generate_index()
        index_file = self.docs_dir / "index.html"

        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                f.write(index_html)
            print("✓")
        except Exception as e:
            print(f"✗ {e}")
            return False

        print()
        print("=" * 70)
        print(f"✓ HTML documentation generated successfully!")
        print("=" * 70)
        print()
        print(f"Output: {self.docs_dir}/")
        print(f"Open in browser: {(self.docs_dir / 'index.html').as_uri()}")
        print()
        print("Next: Deploy to GitHub Pages or web server")

        return True

def main():
    try:
        builder = HtmlBuilder(".")
        success = builder.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Build cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
