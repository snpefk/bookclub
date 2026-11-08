import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { source, fields, renderAnki, renderPreview } from '../study/crafting-interpreters/build-anki.mjs';

const root = new URL('../', import.meta.url);
const read = path => readFileSync(new URL(path, root), 'utf8');
const tsv = 'anki/crafting-interpreters/chapter-20-hash-tables.tsv';
const named = id => {
    const card = source.cards.find(card => card.id === id);
    assert.ok(card, id);
    return card;
};

test('hash-table cards are unique, focused, tagged, and source-linked', () => {
    assert.equal(source.cards.length, 46);
    assert.equal(source.cards.filter(c => c.kind === 'trace').length, 8);
    assert.equal(new Set(source.cards.map(c => c.id)).size, source.cards.length);
    assert.equal(new Set(source.cards.map(c => c.front)).size, source.cards.length);
    for (const card of source.cards) {
        assert.ok(card.front && card.back && card.section && card.anchor && card.topic);
        assert.ok(card.back.length < 450, card.id);
        assert.match(card.id, /^[a-z0-9-]+$/);
        assert.match(card.anchor, /^[a-z0-9-]+$/);
        assert.ok(['recall', 'trace'].includes(card.kind ?? 'recall'));
        const [front, back, tags] = fields(card);
        assert.ok(front.startsWith('CI Ch 20 — '));
        assert.ok(back.includes(`href="${source.url}#${card.anchor}"`));
        assert.ok(tags.includes(`hash_tables::${card.topic}`));
        assert.ok(tags.split(' ').includes(card.kind ?? 'recall'));
    }
});

test('published TSV round-trips all fields and exactly matches the generator', () => {
    const text = read(tsv);
    assert.equal(text, renderAnki());
    assert.ok(text.includes('#deck:Crafting Interpreters::Chapter 20 - Hash Tables\n'));
    for (const header of ['#separator:Tab', '#html:true', '#notetype:Basic', '#columns:Front\tBack\tTags', '#tags column:3']) {
        assert.ok(text.split('\n').includes(header));
    }
    const lines = text.trimEnd().split('\n').filter(l => !l.startsWith('#'));
    assert.equal(lines.length, source.cards.length);
    for (const [i, line] of lines.entries()) {
        const matches = [...line.matchAll(/"((?:[^"]|"")*)"(?:\t|$)/g)];
        assert.equal(matches.map(m => m[0]).join(''), line);
        const row = matches.map(m => m[1].replaceAll('""', '"'));
        assert.equal(row.length, 3);
        assert.deepEqual(row, fields(source.cards[i]));
    }
    assert.equal(read('study/crafting-interpreters/hash-tables-cards.md'), renderPreview());
});

// Independent tiny probe model for checking the numerical/tracing examples.
const tombstone = Symbol('deleted');
function probe(buckets, key, preferred) {
    let firstDeleted = null;
    const visited = [];
    for (let offset = 0; offset < buckets.length; offset++) {
        const i = (preferred + offset) % buckets.length;
        visited.push(i);
        if (buckets[i] === key) return { index: i, found: true, visited };
        if (buckets[i] === tombstone && firstDeleted === null) firstDeleted = i;
        if (buckets[i] === null) return { index: firstDeleted ?? i, found: false, visited };
    }
    throw new Error('No true empty bucket or matching key');
}

test('collision and tombstone trace cards agree with independent probing', () => {
    const wrapped = Array(8).fill(null);
    const locations = ['A', 'B', 'C'].map(key => {
        const result = probe(wrapped, key, 7);
        wrapped[result.index] = key;
        return result.index;
    });
    assert.deepEqual(locations, [7, 0, 1]);
    assert.ok(named('trace-wraparound').back.startsWith('A at 7, B at 0, C at 1.'));

    const deleted = [null, null, 'A', tombstone, 'C', null, null, null];
    assert.deepEqual(probe(deleted, 'C', 2), { index: 4, found: true, visited: [2, 3, 4] });
    assert.ok(named('trace-delete-chain').back.startsWith('2, 3, 4.'));

    const update = [null, null, tombstone, 'K', null, null, null, null];
    assert.deepEqual(probe(update, 'K', 2), { index: 3, found: true, visited: [2, 3] });
    assert.ok(named('trace-update-after-tombstone').back.startsWith('Bucket 3.'));

    const insert = [null, null, tombstone, 'J', null, null, null, null];
    assert.deepEqual(probe(insert, 'K', 2), { index: 2, found: false, visited: [2, 3, 4] });
    assert.ok(named('trace-reuse-after-search').back.startsWith('Insert K at 2, but only after reaching empty bucket 4'));
});

test('growth, bucket placement, and occupancy trace answers are consistent', () => {
    assert.equal(6 + 1 > 8 * 0.75, true);
    assert.match(named('trace-growth').back, /7.*exceeds.*6/);
    assert.deepEqual([13 % 8, 13 % 16], [5, 13]);
    assert.match(named('trace-bucket-change').back, /13 % 8 = 5.*13 % 16 = 13/);
    const live = 4, deleted = 2;
    assert.equal((live + 1) + (deleted - 1), live + deleted);
    assert.ok(named('trace-count').back.startsWith('5 live entries, 1 tombstone, count 6.'));
    assert.ok(named('trace-rebuild-count').back.startsWith('4.'));
    assert.match(named('count-meaning').back, /Live entries plus tombstones/);
    assert.match(named('collision-vs-equality').back, /^No\./);
});

const localHtml = new URL('books/crafting-interpreters/source-html/hash-tables.html', root);
test('card section anchors exist in the local chapter when available', { skip: !existsSync(localHtml) }, () => {
    const html = readFileSync(localHtml, 'utf8');
    for (const card of source.cards) {
        assert.ok(html.includes(`id="${card.anchor}"`), `${card.id}: missing anchor ${card.anchor}`);
    }
});

test('homepage makes the deck discoverable without registering a nonexistent quiz', () => {
    const index = read('index.html');
    assert.ok(index.includes(`href="${tsv}" download`));
    assert.ok(!index.includes('href="study/crafting-interpreters/hash-tables-anki.md"'));
    const section = index.match(/<p class="study-downloads">\s*<a href="anki\/crafting-interpreters\/chapter-20-hash-tables\.tsv"[\s\S]*?<\/p>/);
    assert.ok(section);
    assert.equal([...section[0].matchAll(/<a\b/g)].length, 1);
    assert.ok(!/\b(?:href|src)=["']books\//.test(index));
});
