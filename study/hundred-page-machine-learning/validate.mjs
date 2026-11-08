// node study/hundred-page-machine-learning/validate.mjs
// Uses the real consumer parser; no copy or modification of Bookclub is needed.
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = fileURLToPath(new URL('.', import.meta.url));
const repo = resolve(root, '../..');
const parserPath = process.argv[2] || resolve(repo, 'gift.mjs');
const { parseGift, grade } = await import(pathToFileURL(resolve(parserPath)).href);
const read = path => readFileSync(resolve(root, path), 'utf8');
const source = JSON.parse(read('source.json'));
const { books } = await import(pathToFileURL(resolve(repo, 'quizzes.mjs')).href);
const manifest = books.find(book => book.id === 'hundred-page-machine-learning');
assert.ok(manifest, 'The ML book must be registered in quizzes.mjs');
const titles = new Set();
let count = 0;
for (const [ci, ch] of source.entries()) {
    const entry = manifest.chapters[ci];
    const parsed = parseGift(readFileSync(resolve(repo, entry.file), 'utf8'));
    assert.equal(parsed.length, ch.questions.length);
    assert.ok(Number.isInteger(entry.revision) && entry.revision >= 1);
    let essays = 0;
    for (const [i, q] of parsed.entries()) {
        const original = ch.questions[i];
        assert.equal(q.type, original.type, original.title);
        assert.equal(q.title, original.title);
        assert.equal(q.prompt, original.prompt);
        assert.equal(q.generalFeedback, `${original.explanation} Source: section ${original.section}.`);
        assert.ok(q.category.startsWith(`Chapter ${ch.number} — `));
        const id = `${entry.id}:${q.title}`;
        assert.ok(!titles.has(id), id);
        titles.add(id);
        if (q.type === 'single') {
            assert.equal(q.answers.length, 4);
            assert.equal(q.answers.filter(a => a.weight === 1).length, 1);
            assert.deepEqual(q.answers.map(a => a.text), original.options);
            for (const [j] of q.answers.entries()) {
                assert.equal(grade(q, j), j === original.correct ? 1 : 0, q.title);
            }
        } else if (q.type === 'multiple') {
            assert.deepEqual(q.answers.map(a => a.text), original.options);
            assert.equal(grade(q, original.correct), 1);
            assert.equal(grade(q, []), 0);
            assert.equal(grade(q, [0, 1, 2, 3]), 0);
            assert.equal(grade(q, [original.correct[0]]), 0.5);
        } else if (q.type === 'numerical') {
            assert.equal(grade(q, original.value), 1);
            assert.equal(grade(q, original.value + 100), 0);
            assert.equal(grade(q, ''), 0);
            assert.equal(grade(q, 'not a number'), 0);
        } else if (q.type === 'matching') {
            assert.deepEqual(q.pairs.map(p => [p.left, p.right]), original.pairs);
            assert.equal(grade(q, original.pairs.map(p => p[1])), 1);
            assert.equal(grade(q, original.pairs.map(() => 'not a match')), 0);
        } else if (q.type === 'essay') {
            assert.ok(q.generalFeedback.includes('ALL'));
            assert.equal(grade(q, null), null);
            assert.equal(grade(q, true), 1);
            assert.equal(grade(q, false), 0);
            essays++;
        }
        count++;
    }
    console.log(`Chapter ${ch.number}: ${parsed.length} questions validated (${essays} self-assessed)`);
}
assert.equal(new Set(manifest.chapters.map(c => c.id)).size, 4);
assert.equal(new Set(source.flatMap(ch => ch.cards.map(c => `ch${ch.number}:${c.front}`))).size,
    source.reduce((n, ch) => n + ch.cards.length, 0));
console.log(`PASS: ${count} questions parsed and scored using ${parserPath}`);
