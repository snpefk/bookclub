const { books, scoreKey } = await import(`./quizzes.mjs?updated=${Date.now()}`);

for (const book of books) {
    const target = document.querySelector(`[data-quiz-book="${book.id}"]`);
    if (!target || !book.chapters.length) continue;
    let list = target.querySelector('.chapter-list');
    if (!list) {
        const heading = document.createElement('h4');
        heading.textContent = 'Chapter tests';
        target.append(heading);
        list = document.createElement('ul');
        list.className = 'chapter-list';
        target.append(list);
    }
    for (const chapter of book.chapters) {
        let item = [...list.children].find(child => child.dataset.quizChapter === chapter.id);
        if (!item) {
            item = document.createElement('li');
            item.dataset.quizChapter = chapter.id;
            const link = document.createElement('a');
            link.href = `quiz.html?chapter=${encodeURIComponent(chapter.id)}&v=3`;
            link.textContent = chapter.title;
            item.append(link);
            list.append(item);
        }
        try {
            const result = JSON.parse(localStorage.getItem(scoreKey(chapter)));
            if (result && Number.isFinite(result.score)) {
                const status = document.createElement('span');
                status.textContent = ` · ${result.score.toFixed(2)}% · ${result.score >= 80 ? 'Passed' : 'Try again'}`;
                item.append(status);
            }
        } catch { /* Private browsing may disable local storage. */ }
    }
}
