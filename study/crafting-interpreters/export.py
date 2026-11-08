"""Archive the book's TOC-linked pages as linked PDFs plus a link inventory.

Run through uv with playwright, beautifulsoup4, pypdf, and pymupdf.
Uses an isolated headless Chrome session, not the user's browser profile.
"""
import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit, urldefrag

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from pypdf import PdfReader

STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parents[1] / 'books' / 'crafting-interpreters'
BASE = 'https://craftinginterpreters.com/'
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

PRINT_CSS = r'''
@page { size: A4; }
html, body { margin: 0 !important; padding: 0 !important; background: white !important; }
body { font-size: 11pt !important; line-height: 1.42 !important; }
nav, .nav-wrapper, .sign-up, .scrim { display: none !important; }
.page, article, article.contents, article.contents .chapters, article.contents .row,
article.contents .first, article.contents .second {
  display: block !important; width: auto !important; max-width: none !important;
  margin: 0 !important; padding: 0 !important;
}
article h1, article h1.part { padding: 10pt 0 12pt !important; font-size: 28pt !important; line-height: 1.15 !important; }
article .number { position: static !important; font-size: 13pt !important; color: #555 !important; }
article h2 { font-size: 18pt !important; line-height: 1.2 !important; margin-top: 24pt !important; }
article h3 { font-size: 14pt !important; line-height: 1.2 !important; margin-top: 18pt !important; }
h1, h2, h3, h4 { break-after: avoid; }
article h2 a::before, article h3 a::before { content: none !important; }
article p, article ul, article ol { margin-top: 10pt; margin-bottom: 10pt; }
aside, aside.bottom {
  display: block !important; position: static !important; float: none !important;
  top: auto !important; left: auto !important; right: auto !important; bottom: auto !important;
  width: auto !important; height: auto !important; margin: 10pt 0 !important;
  padding: 5pt 9pt !important; border-left: 2pt solid #a6b6c0 !important;
  border-top: 0 !important; border-bottom: 0 !important; font-size: 9.5pt !important;
  line-height: 1.35 !important; background: #f5f7f8 !important;
}
aside img.above { position: static !important; margin: 5pt auto !important; }
.source-file {
  display: block !important; position: static !important; width: auto !important;
  padding: 4pt 0 !important; color: #444 !important; font-size: 8pt !important;
}
.source-file::before { content: none !important; }
.source-file em { color: #444 !important; }
.source-file-narrow { display: none !important; }
.codehilite, article .challenges .codehilite, article .design-note .codehilite {
  margin: 7pt 0 !important; padding: 5pt !important; max-width: 100% !important;
}
pre, .codehilite pre { font-size: 8pt !important; line-height: 1.3 !important; white-space: pre-wrap !important; overflow-wrap: anywhere !important; }
code { font-size: 9pt !important; white-space: normal !important; overflow-wrap: anywhere !important; }
pre code { font-size: inherit !important; }
article img, article img.wide, aside img { max-width: 100% !important; width: auto !important; max-height: 235mm !important; object-fit: contain; break-inside: avoid; }
blockquote { margin: 14pt 0 !important; }
blockquote p { font-size: 14pt !important; line-height: 1.4 !important; margin: 0 18pt !important; }
blockquote cite { font-size: 10pt !important; }
.challenges, .design-note { margin: 16pt 0 !important; padding: 9pt !important; font-size: 10pt !important; }
.challenges h2, .design-note h2 { font-size: 12pt !important; margin: 0 !important; }
footer, article.contents footer { width: auto !important; margin: 18pt 0 0 !important; padding: 8pt 0 !important; font-size: 9pt !important; }
footer .next { position: static !important; display: block !important; font-size: 10pt !important; margin-bottom: 8pt; }
p, li { orphans: 2; widows: 2; }
a[href] { color: #164f73 !important; text-decoration: underline !important; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
'''


def clean(text):
    return re.sub(r'\s+', ' ', text).strip()


def filename(title):
    return re.sub(r'[/:*?"<>|]', '-', title).strip(' .')


def inventory(html, url, title):
    soup = BeautifulSoup(html, 'html.parser')
    result = []
    for a in soup.select('a[href]'):
        href = a['href'].strip()
        if not href:
            continue
        target = urljoin(url, href)
        scheme = urlsplit(target).scheme
        if scheme not in ('http', 'https', 'mailto'):
            continue
        label = clean(a.get_text(' ', strip=True)) or a.get('title', '')
        if not label:
            label = clean(' '.join(i.get('alt', '') or i.get('title', '') for i in a.select('img')))
        label = label or target
        parent = a.find_parent(['p', 'li', 'blockquote', 'aside', 'h1', 'h2', 'h3', 'h4'])
        context = clean(parent.get_text(' ', strip=True)) if parent else label
        heading = a.find_previous(['h1', 'h2', 'h3'])
        section = clean(heading.get_text(' ', strip=True)) if heading else title
        if a.find_parent('nav'):
            role = 'navigation'
        elif a.find_parent('footer'):
            role = 'footer'
        elif a.find_parent(['h1', 'h2', 'h3', 'h4']):
            role = 'heading'
        else:
            role = 'content'
        result.append(dict(url=target, label=label, context=context, section=section,
                           role=role, source=url, source_title=title))
    return result


async def run(pilot):
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'chapters').mkdir(exist_ok=True)
    (ROOT / 'source-html').mkdir(exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=CHROME, headless=True)
        context = await browser.new_context(viewport={'width': 900, 'height': 1000})
        # Tracking is unnecessary; book assets and fonts remain available.
        await context.route(re.compile(r'https?://(?:www\.)?google-analytics\.com/'), lambda route: route.abort())
        response = await context.request.get(BASE + 'contents.html')
        assert response.ok, response.status
        toc_html = await response.text()
        soup = BeautifulSoup(toc_html, 'html.parser')
        article = soup.select_one('article')
        assert article
        urls = [BASE + 'contents.html']
        for a in article.select('a[href]'):
            url = urldefrag(urljoin(BASE + 'contents.html', a['href']))[0]
            if urlsplit(url).netloc == 'craftinginterpreters.com' and urlsplit(url).path.endswith('.html') and url not in urls:
                urls.append(url)
        assert len(urls) >= 38, len(urls)
        if pilot:
            urls = [BASE + 'introduction.html']
        records = []
        chapter_num = 0
        for url in urls:
            page = await context.new_page()
            try:
                response = await page.goto(url, wait_until='load', timeout=90000)
                assert response and response.ok, (url, response.status if response else None)
                await page.locator('article h1').wait_for()
                await page.evaluate('document.fonts.ready')
                await page.evaluate('''async () => {
                  await Promise.all(Array.from(document.images).map(img => {
                    if (img.complete) return Promise.resolve();
                    return new Promise(resolve => { img.onload = resolve; img.onerror = resolve; });
                  }));
                }''')
                broken = await page.locator('article img').evaluate_all('(imgs) => imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)')
                assert not broken, (url, broken)
                raw_html = await page.content()
                doc = BeautifulSoup(raw_html, 'html.parser')
                title = clean(doc.select_one('article h1').get_text(' ', strip=True))
                num = doc.select_one('article .number')
                numtext = clean(num.get_text()) if num else ''
                if numtext.isdigit():
                    chapter_num += 1
                    prefix = f'{int(numtext):02d}'
                    kind = 'chapter'
                else:
                    stem = urlsplit(url).path.rsplit('/', 1)[-1]
                    extras = {
                        'contents.html': '00', 'dedication.html': 'F01', 'acknowledgements.html': 'F02',
                        'welcome.html': 'P01', 'a-tree-walk-interpreter.html': 'P02',
                        'a-bytecode-virtual-machine.html': 'P03', 'backmatter.html': 'B01',
                        'appendix-i.html': 'A01', 'appendix-ii.html': 'A02',
                    }
                    prefix = extras[stem]
                    kind = 'appendix' if prefix.startswith('A') else 'supplement'
                path = ROOT / 'chapters' / f'{prefix} - {filename(title)}.pdf'
                links = inventory(raw_html, url, title)
                (ROOT / 'source-html' / urlsplit(url).path.rsplit('/', 1)[-1]).write_text(raw_html, encoding='utf-8')
                # Cross-page links are absolute online URLs; same-page anchors stay internal.
                await page.locator('a[href]').evaluate_all('''anchors => {
                  for (const a of anchors) {
                    const href = a.getAttribute('href');
                    if (href && !href.startsWith('#')) a.setAttribute('href', a.href);
                  }
                }''')
                await page.emulate_media(media='print')
                await page.add_style_tag(content=PRINT_CSS)
                await page.pdf(path=str(path), format='A4', print_background=True,
                    margin={'top': '15mm', 'right': '16mm', 'bottom': '18mm', 'left': '16mm'},
                    display_header_footer=True, header_template='<span></span>',
                    footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#666">Crafting Interpreters · Robert Nystrom — <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
                    tagged=True, outline=True)
                reader = PdfReader(path)
                pdf_text = '\n'.join(pg.extract_text() for pg in reader.pages)
                assert len(pdf_text.strip()) > 20, (url, 'No selectable text')
                annotations = [a.get_object() for pg in reader.pages for a in pg.get('/Annots', [])]
                uri_links = [str(a['/A']['/URI']) for a in annotations if a.get('/A', {}).get('/S') == '/URI']
                internal_links = [a for a in annotations if '/Dest' in a or a.get('/A', {}).get('/S') == '/GoTo']
                content = doc.select_one('article')
                record = dict(title=title, url=url, kind=kind, number=int(numtext) if numtext.isdigit() else None,
                    pdf=str(path.relative_to(ROOT)), pages=len(reader.pages), text_characters=len(pdf_text),
                    sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                    uri_link_annotations=len(uri_links), internal_link_annotations=len(internal_links),
                    pdf_uri_targets=sorted(set(uri_links)), links=links,
                    headings=[clean(h.get_text(' ', strip=True)) for h in content.select('h2,h3')],
                    images=len(content.select('img')))
                records.append(record)
                if pilot:
                    await page.screenshot(path=str(ROOT / 'pilot-layout.png'), full_page=False)
                print(f'{path.name}: {record["pages"]} pages; {len(uri_links)} web/email link annotations, {len(internal_links)} internal link annotations', flush=True)
            finally:
                await page.close()
        await browser.close()
    if not pilot:
        assert sorted(r['number'] for r in records if r['kind'] == 'chapter') == list(range(1, 31))
        payload = dict(exported_at=datetime.now(timezone.utc).isoformat(), base_url=BASE, pages=records)
        (ROOT / 'manifest.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'COMPLETE: {len(records)} PDFs, {sum(r["pages"] for r in records)} pages.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pilot', action='store_true')
    asyncio.run(run(parser.parse_args().pilot))
