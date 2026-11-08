// Enhance the reading lists only after JavaScript loads; without it all books remain visible.
export function initBookTabs(root = document, view = window) {
    const tablist = root.querySelector('.book-tabs');
    if (!tablist) return;
    const tabs = [...tablist.querySelectorAll('[role="tab"]')];
    const panels = tabs.map(tab => root.getElementById(tab.getAttribute('aria-controls')));
    if (!tabs.length || panels.some(panel => !panel)) return;

    function select(index, { focus = false, updateHash = false } = {}) {
        tabs.forEach((tab, i) => {
            tab.setAttribute('aria-selected', String(i === index));
            tab.tabIndex = i === index ? 0 : -1;
            panels[i].hidden = i !== index;
        });
        if (focus) tabs[index].focus();
        if (updateHash) view.history.replaceState(null, '', `#${panels[index].id}`);
    }

    function fromHash() {
        const index = panels.findIndex(panel => `#${panel.id}` === view.location.hash);
        select(index >= 0 ? index : 0);
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => select(index, { updateHash: true }));
        tab.addEventListener('keydown', event => {
            let next;
            if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
            else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
            else if (event.key === 'Home') next = 0;
            else if (event.key === 'End') next = tabs.length - 1;
            else return;
            event.preventDefault();
            select(next, { focus: true, updateHash: true });
        });
    });
    panels.forEach(panel => {
        const heading = panel.querySelector('h2');
        if (heading) heading.hidden = true;
    });
    fromHash();
    tablist.hidden = false;
    view.addEventListener('hashchange', fromHash);
}
