import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

test('the shared background is fixed to the viewport instead of the reading-list height', () => {
    const css = readFileSync(new URL('../style.css', import.meta.url), 'utf8');
    const layer = css.match(/body::before\s*\{([^}]+)\}/)?.[1];
    assert.ok(layer);
    for (const rule of ['position: fixed', 'inset: 0', 'z-index: -1', 'pointer-events: none', 'background-size: cover']) {
        assert.ok(layer.includes(rule), rule);
    }
    assert.ok(layer.includes("url('img/bckg.jpg')"));
    assert.match(css, /body\s*\{[^}]*isolation:\s*isolate/);
    for (const file of ['index.html', 'quiz.html']) {
        assert.ok(readFileSync(new URL(`../${file}`, import.meta.url), 'utf8').includes('style.css?v=5'));
    }
});

test('short tabs still fill the viewport and scrollbar changes do not reframe the background', () => {
    const css = readFileSync(new URL('../style.css', import.meta.url), 'utf8');
    const body = css.match(/(?:^|\n)body\s*\{([^}]+)\}/)?.[1];
    assert.ok(body);
    for (const rule of ['min-height: 100vh', 'min-height: 100svh', 'box-sizing: border-box', 'margin: 0', 'padding: 2rem']) {
        assert.ok(body.includes(rule), rule);
    }
    assert.match(css, /html\s*\{[^}]*scrollbar-gutter:\s*stable/);
    assert.match(css, /@media[^}]+body\s*\{\s*padding:\s*1rem;/);
});
