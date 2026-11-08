# Machine learning — Chapters 1–4 study pack

Original English-language study material based on **The Hundred-Page Machine Learning Book**, Andriy Burkov (2019), Chapters 1–4. The full source PDFs remain unchanged. This is a study aid, not official material from the author.

## Contents

- **84 test questions:** Chapter 1: 18; Chapter 2: 24; Chapter 3: 24; Chapter 4: 18.
- **107 Anki Basic notes/cards:** Chapter 1: 20; Chapter 2: 31; Chapter 3: 34; Chapter 4: 22.
- Tests mix single-choice, multiple-answer, matching, numerical calculations, and essays. Every question has an explanation and source section.
- Six essays use explicit self-assessment rubrics. The other 78 questions are automatically scored; matching and multiple-answer questions can receive partial credit under Bookclub's rules.
- `answer-key.md` contains spoilers, worked calculations, and essay rubrics.
- `source.json` is a readable structured export; `build.py` contains the authored source and regenerates the deliverables.

## Use with Bookclub

The material is integrated into this repository. Tests live in `quizzes/hundred-page-machine-learning/`, Anki files in `anki/hundred-page-machine-learning/`, and authoring sources here under `study/hundred-page-machine-learning/`. All paths in this guide are relative to the repository root.

Chapters 1–4 are registered in `quizzes.mjs` and linked, with Anki downloads, from the ML book's existing home-page entry. Add your own original PDF/EPUB and chapter PDFs to the ignored `books/hundred-page-machine-learning/` directory; no reading copies are published. See [the repository guide](../../README.md) and [QUIZZES.md](../../QUIZZES.md) for adding more books or chapters.

The files use the GIFT types actually supported by your parser, with escaped control characters and plain-text formulas. Bookclub's existing 80% pass threshold is unchanged. Multiple-answer questions explicitly request two choices; selecting every choice scores zero. Essays are manually self-assessed and are not automatically evaluated free-text answers.

## Import into Anki

Nothing has been imported into your live Anki collection.

**Choose one import route, not both:**

- Import `anki/hundred-page-machine-learning/chapter-01.tsv` through `chapter-04.tsv` for four chapter subdecks.
- Or import `anki/hundred-page-machine-learning/chapters-01-04.tsv` for one combined subdeck. This contains the same cards, not extra cards.

In Anki Desktop, choose **File → Import** and select the TSV. The headers request the Basic note type, tab separator, HTML, deck name, and mapping `Front / Back / Tags`. Confirm these in the preview before importing. If your profile lacks a note type named `Basic`, choose a compatible front/back note type. Modern Anki versions read these headers; older versions may need manual mapping and enabling HTML.

Tags are `hpml` and `hpml::ch01` through `hpml::ch04`. Fronts include a chapter prefix to reduce accidental first-field collisions. Backs include source-section references. The cards are concise recall prompts rather than verbatim copies of quiz multiple-choice questions; there are no automatically reversed cards. Reimport handling depends on your duplicate/update settings, so inspect the import preview and do not import both routes.

Suggested use: read a chapter, attempt its quiz closed-book, inspect explanations after each answer, then import/review that chapter's cards. Use the application and essay questions to check understanding beyond memorization.

## Accuracy notes

The pack follows the chapter topics but does not reproduce several misleading mathematical shortcuts in the text:

- **SVM C:** questions explicitly use the book's objective `C*||w||² + mean hinge loss`. In common library formulations, C multiplies the loss instead; its direction of effect is reversed.
- **Hinge loss:** even a correctly classified point has positive loss when its signed score lies strictly between zero and one.
- **Entropy units:** maximum binary entropy is `ln(2)` with natural logs and `1` with base-2 logs.
- **Convexity:** local minima of convex functions are global, but convexity alone does not imply a unique minimizer or existence of a finite minimizer.
- **Bayesian updating:** use the posterior as the next prior; do not multiply independent single-observation posteriors and accidentally count the prior repeatedly. MAP maximizes the posterior conditioned on the full dataset.
- **Generalization:** linear models can overfit; independently sampled representative data supports generalization but does not guarantee perfect future predictions.
- **Library capabilities:** categorical inputs, probability output, and incremental fitting are implementation-dependent. The book's illustrative API snippets are not treated as universally valid current library calls.

## Rebuild and validate

From the repository root, regenerate the ML GIFT tests, Anki TSVs, and this directory's answer key and structured export. The shared registry and home page are not overwritten; register any new chapters explicitly and bump revisions when existing questions change.

```sh
python3 -B study/hundred-page-machine-learning/build.py
node --test
node study/hundred-page-machine-learning/validate.mjs
```

Validation uses Bookclub's actual parser and grading function. It checks all question types, exact prompt and feedback round-trips, correct and incorrect grading, multiple-answer anti-select-all scoring, and manifest ID uniqueness. The repository tests also check Anki field mappings, source content, tags, unique fronts, the combined file, and home-page links. Structural validation does not replace human review of question wording and subject-matter accuracy.
