# Bookclub

The reading list, chapter quizzes, and Anki study cards for the Order of the Beerosaurs book club. The site is static and runs on GitHub Pages.

## Local books versus published study materials

- `books/<book-id>/`: **local-only, ignored by Git**. Add your own PDF/EPUB originals and chapter PDFs here. Create this folder after cloning (`mkdir -p books`). Do not link these files from the published site.
- `quizzes/<book-id>/`: tracked GIFT chapter tests used by the site.
- `anki/<book-id>/`: tracked Anki TSV downloads, grouped by book and chapter.
- `study/<book-id>/`: tracked authoring sources, answer keys, and book-specific generation/validation instructions. Do not put book originals here.
- `quizzes.mjs`: registry of books and chapters. A chapter can have an optional `anki` path as well as its quiz `file`.

Use the same stable book ID in each directory. For example, add your ML book files under:

```text
books/hundred-page-machine-learning/
  The Hundred-Page Machine Learning Book - Andriy Burkov.pdf
  The Hundred-Page Machine Learning Book - Andriy Burkov.epub
  chapters/
    01 - Introduction.pdf
    ...
```

Only `books/` is excluded. Keep study questions and flashcards outside it so others can use them without receiving the book files. Gitignore prevents accidental addition of untracked books; it does not remove already tracked files or keep a local HTTP server from serving them. Serve locally only on a trusted interface and do not deploy the entire working directory with ignored files included.

## Current study materials

**Crafting Interpreters — Robert Nystrom:** [46 Anki cards for Chapter 20: Hash Tables](anki/crafting-interpreters/chapter-20-hash-tables.tsv), with [study/import instructions and a preview](study/crafting-interpreters/hash-tables-anki.md). Also includes an [annotated reference catalog](study/crafting-interpreters/links.md) covering 648 link destinations, including 138 external resources. See [the reference-library guide](study/crafting-interpreters/README.md) for local PDF organization and export instructions. The 39 exported PDFs, HTML snapshots, and original ZIP are local-only under `books/crafting-interpreters/`; the site links to the original online chapters rather than publishing those files.

**The Hundred-Page Machine Learning Book — Chapters 1–4:** 84 questions with explanations and 107 Anki Basic cards. Six questions are self-assessed essays; the remaining 78 are automatically scored. See [the study guide](study/hundred-page-machine-learning/README.md) for accuracy notes and rebuilding.

Download either the [combined Anki file](anki/hundred-page-machine-learning/chapters-01-04.tsv) or the individual chapter files linked on the home page, **not both**. In Anki Desktop use File → Import and confirm the Front/Back/Tags mapping in the preview. No application integration or live Anki import is required.

## Add study materials for a book

1. Put your own reading copy in the ignored `books/<book-id>/` folder.
2. Author original, chapter-specific tests and concise recall cards, checking them against that reading copy. Include explanations, source sections, and explicit rubrics for essays.
3. Add tests under `quizzes/<book-id>/`, cards under `anki/<book-id>/`, and any authoring notes/scripts under `study/<book-id>/`.
4. Register chapter IDs, test paths, and optional Anki download paths in `quizzes.mjs`. Set the book's `data-quiz-book` on its `.book-info` in `index.html`. See [QUIZZES.md](QUIZZES.md) for syntax and static-link examples.
5. Run `node --test`, check the page in a browser, and review `git status` to ensure no original book files are staged. Do not commit or publish copyrighted reading copies.

## Preview and test

```sh
node --test
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://localhost:8000/`. Use HTTP, not a `file://` URL, so the browser can load the GIFT files. Quiz results are stored in the reader's browser; they are not shared across devices.
