# Crafting Interpreters — reference library

**Robert Nystrom** · [Read the original book online](https://craftinginterpreters.com/contents.html)

## Reference materials

- [Annotated link catalog](links.md): **648 distinct destinations**, including **138 external resources**, with topic descriptions, book context, and the chapters/sections that link to them.
- `catalog-stats.json`: counts from the captured online edition.
- [Attribution and licensing](LICENSE-NOTICE.md): the book and interpreter code have different licensing terms.

The catalog includes prose links, asides, exercises, design notes, section permalinks, navigation, and footer links. Repeated URLs are merged, while distinct fragments remain separate. Descriptions of external resources are grounded in the book's linking context and the referenced topic; the external sites were not independently reviewed or checked for availability. Unlinked asset URLs and links on external sites are not recursively collected.

## Chapter 20 — Hash Tables: Anki cards

[Download 46 Anki cards](../../anki/crafting-interpreters/chapter-20-hash-tables.tsv) · [Import and study guide](hash-tables-anki.md) · [Preview both sides](hash-tables-cards.md)

The deck has 38 recall prompts and eight tracing exercises covering hashing, collisions, linear probing, tombstones, resizing, and string interning. Every answer links to its source section. It is an importable Basic-note TSV; no cards have been added to your live Anki collection, and no chapter quiz is registered for this book.

Edit `hash-tables-cards.json` and run `node study/crafting-interpreters/build-anki.mjs` from the repository root to rebuild the TSV and preview. This generator has no external dependencies and does not use the local PDFs.

## Local reading copies

The exported PDFs are kept in the Git-ignored `books/crafting-interpreters/` directory, not published by the site:

```text
books/crafting-interpreters/
  chapters/                   # 30 numbered chapters + 9 supplementary PDFs
  source-html/                # Captured HTML, not a fully offline website
  validation-previews/        # Sample PDF page renderings used to inspect layout
  archive/original-export.zip # Unchanged original Downloads package
  index.md                    # Local chapter links and online originals
  manifest.json               # Source URLs, PDF hashes, and hyperlink occurrences
  validation.json             # PDF/link/text validation results
  README.md                   # Local reading and export details
```

The export contains **39 PDFs / 659 pages**. PDFs have selectable text, illustrations, code snippets, challenges, design notes, and inline side notes. Cross-chapter links open the original online book; same-page links use PDF destinations where Chromium supports them. Local reading copies will not exist in a fresh clone until you export them or provide your own.

Do not add links to `books/` in the public site. Gitignore prevents accidental Git additions; it does not stop a local HTTP server or a deployment command that copies ignored files from exposing them.

## Regenerate and validate

From the repository root, with `uv` and Google Chrome installed:

```sh
# Download the online book and regenerate local PDFs/HTML/manifest.
uv run --no-project --python /usr/bin/python3 --with playwright --with beautifulsoup4 --with pypdf --with pymupdf python -B study/crafting-interpreters/export.py

# Rebuild the public Markdown catalog and private chapter index from local HTML.
uv run --no-project --python /usr/bin/python3 --with beautifulsoup4 python -B study/crafting-interpreters/catalog.py

# Check all PDFs, link preservation, text samples, and catalog coverage.
uv run --no-project --python /usr/bin/python3 --with beautifulsoup4 --with pypdf --with pymupdf python -B study/crafting-interpreters/validate.py

# Run repository tests, including checks that public links avoid local books.
node --test
```

Scripts locate the repository relative to themselves, so their outputs do not depend on the shell's current working directory. Exporting again may reflect changes to the website, so review generated catalog changes and update the documented counts when necessary. The original ZIP is a historical snapshot and is not regenerated.
