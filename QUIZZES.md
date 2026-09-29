# Chapter tests

The site runs entirely on GitHub Pages. Its GIFT files, parser, and quiz UI are committed to this repository. Test results are saved in each reader's browser, not shared between devices or readers. A score of 80% or more passes; each scored question is worth one point. Essays are self-assessed after submitting. The included `sample.gift` is an authoring template, not a book chapter test.

## Add a chapter

1. Write a UTF-8 `.gift` file in `quizzes/<book-id>/`. Start with [the sample](quizzes/rust-atomics-and-locks/sample.gift), or use [Moodle's GIFT reference](https://docs.moodle.org/403/en/GIFT_format). Separate questions with a blank line. Escape literal GIFT control characters with a backslash (for example `\=`, `\#`, `\{`).
2. Add a unique chapter `id`, visible `title`, and relative `file` path to the corresponding book in [quizzes.mjs](quizzes.mjs). Start `revision` at 1 and increase it whenever you edit the questions so an old result does not appear to describe a new test.
3. On the book's `.book-info` element in [index.html](index.html), set `data-quiz-book` to the book's `id` in `quizzes.mjs`. For a link visible immediately, add a chapter link to its `.chapter-list` with `<li data-quiz-chapter="your-chapter-id"><a href="quiz.html?chapter=your-chapter-id">Chapter title test</a></li>`. Its `data-quiz-chapter` must match the manifest `id`; JavaScript adds local scores beside it and generates links for any chapters without a static link.

Supported GIFT question types: single-choice, weighted multiple-answer, true/false, short answer (including `*` wildcards), matching, numerical (exact value, `:tolerance`, `min..max`, weighted alternatives), missing-word variants, essay (`{}`), and descriptions (no answer block). Question names, categories, comments, per-answer feedback, general feedback (`####`), and escaped control characters are accepted. `[plain]`, `[html]`, `[markdown]`, and `[moodle]` format labels are accepted, but authored content is displayed as plain text for safe rendering. Moodle-specific media, embedded HTML formatting, plugin question types, and question-bank metadata are not rendered as rich content. Malformed question syntax stops the test with a line-numbered error rather than awarding an incorrect score.

For local preview, serve the repository directory with `python3 -m http.server 8000` and visit `http://localhost:8000/`. Opening `index.html` directly as a `file://` URL may block the browser from fetching GIFT files. Run parser and scoring checks with `node --test`.
