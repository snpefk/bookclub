# Remembering Chapter 20 — Hash Tables

[Original chapter](https://craftinginterpreters.com/hash-tables.html) · [Card preview](hash-tables-cards.md) · [Download Anki cards](../../anki/crafting-interpreters/chapter-20-hash-tables.tsv)

This deck targets the chapter's mental model and correctness invariants, not memorization of every C function or numeric hash constant. It uses short question/answer cards plus eight small tracing exercises. It is original study material, not an official deck from Robert Nystrom.

## What to remember

- Keys, values, equality, hashing costs, and expected versus worst-case lookup.
- Separate chaining versus open addressing, linear probing, locality, and clustering.
- The distinction between live, truly empty, and tombstone buckets.
- Why deletion must preserve a probe sequence and insertion must search beyond a tombstone.
- Why capacity changes require reinsertion, but not rehashing immutable string bytes.
- clox's live-plus-tombstone growth counter and implementation-specific 0.75 threshold.
- String interning, canonical objects, content checks, pointer equality, and owned-buffer cleanup.

Generic hash-table principles are distinguished from Chapter 20's particular implementation. The deck does not claim that all languages implement maps identically or that every operation is guaranteed constant time. Later garbage-collector changes to the intern pool are outside this chapter's scope.

## Import into Anki

1. Download `anki/crafting-interpreters/chapter-20-hash-tables.tsv`.
2. In Anki Desktop, choose **File → Import**.
3. Confirm note type **Basic**, tab separator, HTML enabled, and **Front / Back / Tags** mapping.
4. Confirm the deck **Crafting Interpreters::Chapter 20 - Hash Tables**.

There is one forward card per note, with no automatic reverse cards. The headers request the settings above; inspect Anki's preview, especially if your profile uses localized or customized note types. Existing cards are not automatically modified by downloading this file. No live Anki import was performed.

Tags include `crafting_interpreters::ch20`, `hash_tables`, a topic tag, and `recall` or `trace`. Every answer has a clickable source-section link. Chapter-prefixed fronts reduce accidental collisions with existing notes; reimport/update behavior still depends on your import settings.

## How to use

Try 5–10 new cards a day. Answer aloud before revealing the back. Sketch the bucket array for tracing cards; do not just recognize the expected result. If a card is hard, revisit its linked section rather than repeatedly guessing. As a final understanding check, implement deletion and tombstone reuse in a tiny table and explain why lookup still terminates.

## Rebuild and check

From the repository root:

```sh
node study/crafting-interpreters/build-anki.mjs
node --test
```

`hash-tables-cards.json` is the authoring source; `hash-tables-cards.md` and the TSV are generated. Rebuilding does not access Anki or change the private reading copies.
