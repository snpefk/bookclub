import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const index = readFileSync(new URL('index.html', root), 'utf8');

test('diplomas belong to the Rust book card, not a separate page section', () => {
    const start = index.indexOf('<li class="rust-atomics-book">');
    const end = index.indexOf('</section>', start);
    const cardEnd = index.indexOf('</li>', end);
    assert.ok(start >= 0 && end > start && cardEnd > end);
    const card = index.slice(start, cardEnd);
    assert.ok(card.includes('data-quiz-book="rust-atomics-and-locks"'));
    assert.ok(card.includes('<section class="book-diplomas"'));
    assert.ok(card.includes('id="rust-diplomas-title"'));
    assert.equal((index.match(/class="diploma-gallery"/g) || []).length, 1);
    assert.ok(!index.includes('class="diplomas"'));
    for (const person of ['snpefk', 'barsoosayque', 'alradish']) {
        assert.ok(card.includes(`src="diploma/${person}.jpg"`));
        assert.ok(card.includes(`download="${person}-diploma.jpg"`));
        assert.ok(card.includes(`aria-label="View full-size diploma for @${person}"`));
        assert.ok(existsSync(new URL(`diploma/${person}.jpg`, root)));
    }
});
