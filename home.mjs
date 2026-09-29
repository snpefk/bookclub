import { books, scoreKey } from './quizzes.mjs';

for (const book of books) {
    const target = document.querySelector(`[data-quiz-book="${book.id}"]`);
    if (!target || !book.chapters.length) continue;
    const heading = document.createElement('h4');
    heading.textContent = 'Chapter tests';
    target.append(heading);
    const list = document.createElement('ul');
    list.className = 'chapter-list';
    for (const chapter of book.chapters) {
        const item = document.createElement('li');
        const link = document.createElement('a');
        link.href = `quiz.html?chapter=${encodeURIComponent(chapter.id)}`;
        link.textContent = chapter.title;
        item.append(link);
        try {
            const result = JSON.parse(localStorage.getItem(scoreKey(chapter)));
            if (result && Number.isFinite(result.score)) {
                const status = document.createElement('span');
                status.textContent = ` · ${result.score.toFixed(2)}% · ${result.score >= 80 ? 'Passed' : 'Try again'}`;
                item.append(status);
            }
        } catch { /* Private browsing may disable local storage. */ }
        list.append(item);
    }
    target.append(list);
}
