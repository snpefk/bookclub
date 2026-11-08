import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { books } from '../quizzes.mjs';

const root = new URL('../', import.meta.url);
const read = path => readFileSync(new URL(path, root), 'utf8');
const bookId = 'hundred-page-machine-learning';
const book = books.find(book => book.id === bookId);
const source = JSON.parse(read(`study/${bookId}/source.json`));

function parseAnki(path) {
    const lines = read(path).trimEnd().split('\n');
    const headers = lines.filter(line => line.startsWith('#'));
    const rows = lines.filter(line => !line.startsWith('#')).map(line => {
        // Each generated field is quoted; doubled quotes are literal quote characters.
        const matches = [...line.matchAll(/"((?:[^"]|"")*)"(?:\t|$)/g)];
        assert.equal(matches.map(match => match[0]).join(''), line, `Invalid TSV row in ${path}`);
        return matches.map(match => match[1].replaceAll('""', '"'));
    });
    for (const header of ['#separator:Tab', '#html:true', '#notetype:Basic', '#columns:Front\tBack\tTags', '#tags column:3']) {
        assert.ok(headers.includes(header), `${path}: missing ${header}`);
    }
    return { headers, rows };
}

const escapeHtml = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#x27;');

test('all ML chapter questions round-trip and grade with the production parser', () => {
    const output = execFileSync(process.execPath, [fileURLToPath(new URL(`study/${bookId}/validate.mjs`, root))], { encoding: 'utf8' });
    assert.match(output, /PASS: 84 questions parsed and scored/);
});

test('registered study chapters and homepage links point to real public assets', () => {
    assert.ok(book);
    assert.equal(book.chapters.length, 4);
    const allIds = books.flatMap(b => b.chapters.map(ch => ch.id));
    assert.equal(new Set(allIds).size, allIds.length);
    const index = read('index.html');
    assert.ok(index.includes(`data-quiz-book="${bookId}"`));
    for (const ch of book.chapters) {
        assert.ok(read(ch.file).includes('$CATEGORY: Chapter'));
        assert.ok(ch.anki.startsWith(`anki/${bookId}/`));
        assert.ok(index.includes(`data-quiz-chapter="${ch.id}"`));
        assert.ok(index.includes(`quiz.html?chapter=${ch.id}&amp;v=3`));
        assert.ok(index.includes(`href="${ch.anki}" download`));
        assert.ok(!ch.file.startsWith('books/') && !ch.anki.startsWith('books/'));
    }
    assert.ok(index.includes(`href="anki/${bookId}/chapters-01-04.tsv" download`));
    assert.ok(!/\b(?:href|src)=["']books\//.test(index));
});

test('Anki chapter files contain exact source cards, source references and chapter tags', () => {
    const all = [];
    const expectedCounts = [20, 31, 34, 22];
    for (const [i, ch] of source.entries()) {
        const { headers, rows } = parseAnki(book.chapters[i].anki);
        assert.equal(rows.length, expectedCounts[i]);
        assert.equal(rows.length, ch.cards.length);
        assert.ok(headers.includes(`#deck:The Hundred-Page Machine Learning Book::Chapter ${String(ch.number).padStart(2, '0')} - ${ch.title}`));
        for (const [j, row] of rows.entries()) {
            const card = ch.cards[j];
            assert.equal(row.length, 3);
            assert.equal(row[0], escapeHtml(`HPML Ch ${ch.number} — ${card.front}`));
            assert.equal(row[1], escapeHtml(card.back) + '<br><br><small>' +
                escapeHtml(`The Hundred-Page Machine Learning Book, Andriy Burkov (2019), §${card.section}.`) + '</small>');
            assert.equal(row[2], `hpml hpml::ch${String(ch.number).padStart(2, '0')}`);
        }
        all.push(...rows);
    }
    assert.equal(all.length, 107);
    assert.equal(new Set(all.map(row => row[0])).size, all.length);
    const combined = parseAnki(`anki/${bookId}/chapters-01-04.tsv`);
    assert.deepEqual(combined.rows, all);
    assert.ok(combined.headers.includes('#deck:The Hundred-Page Machine Learning Book::Chapters 01-04'));
});

test('six ML essays have explicit rubrics and every question has a source section', () => {
    const questions = source.flatMap(ch => ch.questions);
    assert.equal(questions.length, 84);
    const essays = questions.filter(q => q.type === 'essay');
    assert.equal(essays.length, 6);
    assert.ok(essays.every(q => q.explanation.includes('ALL')));
    assert.ok(questions.every(q => q.section && q.explanation));
});
