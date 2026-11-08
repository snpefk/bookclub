import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const root = new URL('../', import.meta.url);
const read = path => readFileSync(new URL(path, root), 'utf8');
const study = 'study/crafting-interpreters/';

test('Crafting Interpreters catalog includes every counted destination and an external description', () => {
    const stats = JSON.parse(read(study + 'catalog-stats.json'));
    const catalog = read(study + 'links.md');
    const external = [...catalog.matchAll(/^### E\d+\./gm)];
    const book = [...catalog.matchAll(/^### B\d+\./gm)];
    const navigation = [...catalog.matchAll(/^### N\d+\./gm)];
    assert.equal(external.length, stats.external_destinations);
    assert.equal(book.length, stats.book_destinations);
    assert.equal(navigation.length, stats.navigation_destinations);
    assert.equal(external.length + book.length + navigation.length, stats.unique_destinations);
    assert.equal([...catalog.matchAll(/^\*\*About:\*\*/gm)].length, stats.unique_destinations);
    assert.equal([...catalog.matchAll(/^\*\*Book context:\*\*/gm)].length, stats.external_destinations);
    const destinations = [...catalog.matchAll(/\[(?:Open resource|Open original book location|Open destination)\]\(<([^>]+)>\)/g)].map(m => m[1]);
    assert.equal(destinations.length, stats.unique_destinations);
    assert.equal(new Set(destinations).size, destinations.length);
    assert.ok(destinations.every(url => /^(https?:|mailto:)/.test(url)));
    assert.ok(!catalog.includes('/Users/'));
});

test('homepage exposes public references, never private reading copies', () => {
    const index = read('index.html');
    assert.ok(index.includes('href="https://craftinginterpreters.com/contents.html"'));
    assert.ok(index.includes(`href="${study}links.md" download`));
    assert.ok(index.includes(`href="${study}README.md"`));
    assert.ok(!/\b(?:href|src)=["'](?:\.\/)?books\//.test(index));
    for (const name of ['links.md', 'README.md', 'LICENSE-NOTICE.md', 'export.py', 'catalog.py', 'validate.py']) {
        assert.ok(read(study + name).length > 0);
    }
    assert.ok(read('.gitignore').split(/\r?\n/).includes('/books/'));
});

test('export utilities keep reading copies and shareable reference materials separate', () => {
    for (const name of ['export.py', 'catalog.py', 'validate.py']) {
        const script = read(study + name);
        assert.ok(script.includes("STUDY.parents[1] / 'books' / 'crafting-interpreters'"));
        assert.ok(!script.includes('/Users/'));
    }
    assert.ok(read(study + 'export.py').includes("ROOT / 'chapters'"));
    assert.ok(read(study + 'catalog.py').includes("STUDY / 'links.md'"));
    assert.ok(read(study + 'validate.py').includes("STUDY/'links.md'"));
});
