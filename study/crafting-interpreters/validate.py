"""Check archived PDFs, link preservation, and catalog coverage."""
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import urldefrag, urlsplit, quote

from bs4 import BeautifulSoup
import fitz
from pypdf import PdfReader

STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parents[1] / 'books' / 'crafting-interpreters'


def norm(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKC', s).lower())


def canonical_url(url):
    # Chromium serializes an origin-only HTTP URL with a trailing slash.
    parts = urlsplit(url)
    if parts.scheme in ('http','https') and parts.netloc and not parts.path:
        return parts._replace(path='/').geturl()
    return url


def main():
    data = json.loads((ROOT/'manifest.json').read_text())
    catalog = (STUDY/'links.md').read_text()
    all_urls = set()
    missing_links = []
    missing_text = []
    headings_checked = 0
    passages_checked = 0
    annotations = 0
    assert sorted(p['number'] for p in data['pages'] if p['kind']=='chapter') == list(range(1,31))
    for p in data['pages']:
        path = ROOT/p['pdf']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == p['sha256'], path
        r = PdfReader(path)
        assert len(r.pages) == p['pages'] > 0
        # Positional reading order avoids Chromium's stacking/paint order placing
        # a title or epigraph between the two halves of a paginated code block.
        with fitz.open(path) as positional:
            raw = '\n'.join(pg.get_text(sort=True) for pg in positional)
        raw = re.sub(r'Crafting Interpreters · Robert Nystrom — \d+ / \d+', '', raw)
        # Right-floated section numbers can be extracted at the start of a page,
        # separate from the heading. Ignore those layout-only standalone labels.
        raw = re.sub(r'(?m)^\s*A?\d+(?:[\s ]*\.[\s ]*\d+)*\s*$', '', raw)
        text = norm(raw)
        for heading in p['headings']:
            headings_checked += 1
            title = re.sub(r'^(?:A?\d+\s*\.\s*)*A?\d+\s*', '', heading)
            if norm(title) not in text:
                missing_text.append((p['title'], 'heading', heading))
        doc = BeautifulSoup((ROOT/'source-html'/urlsplit(p['url']).path.rsplit('/',1)[-1]).read_text(), 'html.parser')
        # Check every prose paragraph and code block, including asides and exercises.
        # Short normalized excerpts avoid whitespace and pagination differences.
        for node in doc.select('article p, article pre'):
            if node.find_parent(class_='source-file-narrow'):
                continue
            sample = norm(node.get_text(' ',strip=True))[:72]
            if len(sample) >= 15:
                passages_checked += 1
                if sample not in text:
                    missing_text.append((p['title'], 'passage', node.get_text(' ',strip=True)[:120]))
        for link in p['links']:
            all_urls.add(link['url'])
            # Menus are intentionally removed from print; headings stay internal.
            if link['role'] not in ('content','footer'):
                continue
            if urldefrag(link['url'])[0] == p['url']:
                continue
            if canonical_url(link['url']) not in {canonical_url(u) for u in p['pdf_uri_targets']}:
                missing_links.append((p['title'], link['url'], link['label']))
        annotations += p['uri_link_annotations'] + p['internal_link_annotations']
    # Exact encoded destinations are checked independently of human-readable labels.
    for url in all_urls:
        encoded = quote(url, safe=":/#?=&%+;,@!$'()*~.-_")
        if f'(<{encoded}>)' not in catalog:
            raise AssertionError(f'URL missing from catalog: {url}')
    report = dict(pdfs=len(data['pages']), pdf_pages=sum(p['pages'] for p in data['pages']),
        unique_link_destinations=len(all_urls), pdf_link_annotations=annotations,
        headings_checked=headings_checked, prose_and_code_passages_checked=passages_checked,
        missing_print_links=sorted(set(missing_links)), missing_text=missing_text)
    (ROOT/'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if not k.startswith('missing_')}, indent=2))
    print(f'Missing print links: {len(missing_links)}; unmatched text excerpts: {len(missing_text)}')
    if missing_text:
        print(json.dumps(missing_text[:10], ensure_ascii=False, indent=2))
    assert not missing_links, 'Some visible content links are missing from PDF annotations; inspect validation.json'
    assert not missing_text, 'Some text excerpts need inspection; inspect validation.json'
    print('PASS: complete chapter set, PDF integrity, text checks, PDF link targets, and exhaustive Markdown URL coverage.')


if __name__ == '__main__':
    main()
