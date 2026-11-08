import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { initBookTabs } from '../tabs.mjs';

function fixture(hash = '') {
    const ids = ['finished', 'backlog'];
    let focused;
    const panels = ids.map(id => ({ id, hidden: false, heading: { hidden: false }, querySelector() { return this.heading; } }));
    const tabs = ids.map((id, index) => ({
        attrs: { 'aria-controls': id }, handlers: {}, tabIndex: -1,
        getAttribute(name) { return this.attrs[name]; },
        setAttribute(name, value) { this.attrs[name] = value; },
        addEventListener(name, handler) { this.handlers[name] = handler; },
        focus() { focused = index; }
    }));
    const bar = { hidden: true, querySelectorAll: () => tabs };
    const inProgress = { id: 'in-progress', hidden: false, heading: { hidden: false } };
    const root = { querySelector: () => bar, getElementById: id => id === 'in-progress' ? inProgress : panels.find(panel => panel.id === id) };
    const view = { location: { hash }, handlers: {},
        history: { replaceState(_state, _unused, value) { view.location.hash = value; } },
        addEventListener(name, handler) { this.handlers[name] = handler; }
    };
    initBookTabs(root, view);
    return { tabs, panels, bar, view, inProgress, focus: () => focused };
}

function assertSelected(f, index) {
    assert.deepEqual(f.panels.map(panel => panel.hidden), [0, 1].map(i => i !== index));
    assert.deepEqual(f.tabs.map(tab => tab.attrs['aria-selected']), [0, 1].map(i => String(i === index)));
    assert.deepEqual(f.tabs.map(tab => tab.tabIndex), [0, 1].map(i => i === index ? 0 : -1));
    assert.equal(f.inProgress.hidden, false);
    assert.equal(f.inProgress.heading.hidden, false);
}

test('Finished is the default tab while In Progress remains permanently visible', () => {
    const f = fixture();
    assertSelected(f, 0);
    assert.equal(f.bar.hidden, false);
    assert.ok(f.panels.every(panel => panel.heading.hidden));
    assert.equal(f.focus(), undefined, 'Initial load must not steal focus');
});

test('clicking a tab switches shelves and creates a shareable hash', () => {
    const f = fixture();
    for (const i of [1, 0, 1]) {
        f.tabs[i].handlers.click();
        assertSelected(f, i);
        assert.equal(f.view.location.hash, `#${f.panels[i].id}`);
    }
});

test('arrow keys wrap, Home/End work, and unrelated keys are not intercepted', () => {
    const f = fixture();
    for (const [start, key, expected] of [[0, 'ArrowRight', 1], [1, 'ArrowRight', 0], [0, 'ArrowLeft', 1], [1, 'Home', 0], [0, 'End', 1]]) {
        let prevented = false;
        f.tabs[start].handlers.keydown({ key, preventDefault() { prevented = true; } });
        assertSelected(f, expected);
        assert.equal(f.focus(), expected);
        assert.equal(prevented, true);
    }
    f.tabs[1].handlers.keydown({ key: 'Tab', preventDefault() { assert.fail('Native Tab must not be intercepted'); } });
    assertSelected(f, 1);
});

test('hash navigation selects Finished or Backlog without hiding In Progress', () => {
    for (const [hash, expected] of [['#finished', 0], ['#backlog', 1], ['#in-progress', 0], ['#unknown', 0]]) assertSelected(fixture(hash), expected);
    const f = fixture();
    f.view.location.hash = '#finished';
    f.view.handlers.hashchange();
    assertSelected(f, 0);
});

test('markup preserves all reading lists without JavaScript and orders the tab controls', () => {
    const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
    const buttons = [...html.matchAll(/<button id="tab-([^"]+)"[^>]*>/g)].map(match => match[1]);
    assert.deepEqual(buttons, ['finished', 'backlog']);
    assert.ok(html.indexOf('id="in-progress"') < html.indexOf('class="book-tabs"'));
    const progress = html.match(/<section id="in-progress"[^>]*>/)?.[0];
    assert.ok(progress && !progress.includes('tabpanel') && !progress.includes('hidden'));
    assert.equal((html.match(/id="in-progress"/g) || []).length, 1);
    for (const id of buttons) {
        assert.ok(html.includes(`aria-controls="${id}"`));
        const panel = html.match(new RegExp(`<section id="${id}"[^>]*>`));
        assert.ok(panel);
        assert.ok(!panel[0].includes('hidden'), 'Fallback reading lists must be visible without JavaScript');
    }
    assert.match(html, /class="book-tabs"[^>]*hidden/);
});
