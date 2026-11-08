# Chapter tests

The site runs entirely on GitHub Pages. Its GIFT files, parser, and quiz UI are committed to this repository. Readers check each question individually and see feedback immediately; after all questions are checked, a score of 80% or more passes. Each scored question is worth one point. Essays are self-assessed after revealing their feedback. Results are saved in each reader's browser, not shared between devices or readers. The included `sample.gift` is an authoring template, not a book chapter test.

## Add a chapter

1. Write a UTF-8 `.gift` file in `quizzes/<book-id>/`. Start with [the sample](quizzes/rust-atomics-and-locks/sample.gift), or use [Moodle's GIFT reference](https://docs.moodle.org/403/en/GIFT_format). Separate questions with a blank line. Escape literal GIFT control characters with a backslash (for example `\=`, `\#`, `\{`).
2. Add a unique chapter `id`, visible `title`, and relative `file` path to the corresponding book in [quizzes.mjs](quizzes.mjs). Start `revision` at 1 and increase it whenever you edit the questions so an old result does not appear to describe a new test.
3. On the book's `.book-info` element in [index.html](index.html), set `data-quiz-book` to the book's `id` in `quizzes.mjs`. For a link visible immediately, add a chapter link to its `.chapter-list` with `<li data-quiz-chapter="your-chapter-id"><a href="quiz.html?chapter=your-chapter-id">Chapter title test</a></li>`. Its `data-quiz-chapter` must match the manifest `id`; JavaScript adds local scores beside it and generates links for any chapters without a static link.

## Add Anki cards and local reading copies

Store book PDFs/EPUBs and split chapters under `books/<book-id>/`. This entire folder is ignored by Git; readers add their own copies. Never place book originals in the published quiz or Anki directories. See [README.md](README.md) for the full layout.

Put Anki TSVs in `anki/<book-id>/` and add an optional `anki: 'anki/<book-id>/chapter-01.tsv'` path to the chapter entry in `quizzes.mjs`. The home-page script adds a download link alongside the test. For a static link, add `<a class="anki-download" href="anki/<book-id>/chapter-01.tsv" download>Anki cards</a>` to the same chapter list item. Include source sections in card backs and chapter tags. Use tab-separated Front / Back / Tags fields and Anki import headers; the ML book's files provide an example.

Keep authoring scripts, answer keys, and validation notes in `study/<book-id>/`. For the ML book, run `python3 -B study/hundred-page-machine-learning/build.py` to regenerate the four chapter tests and Anki files, then `node --test`. The generator does not modify the shared manifest or page, so add new chapter registrations and links explicitly and bump revisions when existing quiz questions change.

Supported GIFT question types: single-choice, weighted multiple-answer, true/false, short answer (including `*` wildcards), matching, numerical (exact value, `:tolerance`, `min..max`, weighted alternatives), missing-word variants, essay (`{}`), and descriptions (no answer block). Question names, categories, comments, per-answer feedback, general feedback (`####`), and escaped control characters are accepted. `[plain]`, `[html]`, `[markdown]`, and `[moodle]` format labels are accepted, but authored content is displayed as plain text for safe rendering. Moodle-specific media, embedded HTML formatting, plugin question types, and question-bank metadata are not rendered as rich content. Malformed question syntax stops the test with a line-numbered error rather than awarding an incorrect score.

For local preview, serve the repository directory with `python3 -m http.server 8000` and visit `http://localhost:8000/`. Opening `index.html` directly as a `file://` URL may block the browser from fetching GIFT files. Run parser and scoring checks with `node --test`.
