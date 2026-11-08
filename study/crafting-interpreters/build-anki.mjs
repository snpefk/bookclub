// Rebuild Chapter 20 cards without Anki, browser access, or third-party packages.
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const study = new URL('./', import.meta.url);
export const source = JSON.parse(readFileSync(new URL('hash-tables-cards.json', study), 'utf8'));

export const escapeHtml = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#x27;');

export function fields(card) {
    const kind = card.kind ?? 'recall';
    return [
        escapeHtml(`CI Ch 20 — ${card.front}`),
        escapeHtml(card.back) + '<br><br><small>' +
            `<a href="${source.url}#${card.anchor}">` +
            escapeHtml(`${source.book}, ${source.author}, §${card.section}`) + '</a></small>',
        `crafting_interpreters crafting_interpreters::ch20 hash_tables hash_tables::${card.topic} ${kind}`
    ];
}

export function renderAnki() {
    const quote = s => '"' + s.replaceAll('"', '""') + '"';
    const rows = source.cards.map(card => fields(card).map(quote).join('\t'));
    return ['#separator:Tab', '#html:true', '#notetype:Basic', '#columns:Front\tBack\tTags',
        '#tags column:3', `#deck:${source.deck}`, ...rows, ''].join('\n');
}

export function renderPreview() {
    const lines = ['# Chapter 20 — Hash Tables: Anki card preview', '',
        'Original recall prompts based on Robert Nystrom’s chapter, not official author material.', '',
        `[Read the chapter](${source.url}) · [Import instructions](hash-tables-anki.md)`, '',
        'Spoilers: this preview shows both sides. Import the TSV to practice active recall.', ''];
    for (const [i, card] of source.cards.entries()) {
        lines.push(`## ${i + 1}. ${card.front}`, '', card.back, '',
            `[Source: §${card.section}](${source.url}#${card.anchor}) · ${card.kind ?? 'recall'} · ${card.topic}`, '');
    }
    return lines.join('\n');
}

if (process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url) {
    const output = new URL('../../anki/crafting-interpreters/', study);
    mkdirSync(output, { recursive: true });
    writeFileSync(new URL('chapter-20-hash-tables.tsv', output), renderAnki());
    writeFileSync(new URL('hash-tables-cards.md', study), renderPreview());
    console.log(`Built ${source.cards.length} Basic notes/cards: ${fileURLToPath(output)}chapter-20-hash-tables.tsv`);
}
