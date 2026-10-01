import { parseGift, grade } from './gift.mjs';
// The chapter list changes more often than the quiz UI. Fetch a fresh module so a
// previously cached list cannot reject a link added by a newer index.html.
const { books, scoreKey } = await import(`./quizzes.mjs?updated=${Date.now()}`);

const title = document.querySelector('#quiz-title');
const status = document.querySelector('#quiz-status');
const form = document.querySelector('#quiz-form');
const result = document.querySelector('#quiz-result');
const id = new URLSearchParams(location.search).get('chapter');
const chapter = books.flatMap(book => book.chapters).find(item => item.id === id);

function el(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
}

function renderInput(question, index, container) {
    const name = `q${index}`;
    if (question.type === 'description') return;
    if (question.type === 'single' || question.type === 'multiple' || question.type === 'truefalse') {
        const options = question.type === 'truefalse' ? ['True', 'False'] : question.answers.map(item => item.text);
        options.forEach((text, option) => {
            const label = el('label', undefined, 'quiz-option');
            const input = document.createElement('input');
            input.type = question.type === 'multiple' ? 'checkbox' : 'radio';
            input.name = name;
            input.value = String(option);
            label.append(input, document.createTextNode(' ' + text));
            container.append(label);
        });
    } else if (question.type === 'matching') {
        const options = [...new Set(question.pairs.map(pair => pair.right))].sort();
        question.pairs.forEach((pair, row) => {
            const label = el('label', pair.left + ' → ', 'quiz-match');
            const select = document.createElement('select');
            select.name = `${name}-${row}`;
            select.append(new Option('Choose an answer', ''));
            options.forEach(option => select.append(new Option(option, option)));
            label.append(select);
            container.append(label);
        });
    } else {
        const label = el('label', 'Your answer', 'quiz-input');
        const input = document.createElement(question.type === 'essay' ? 'textarea' : 'input');
        if (input.tagName === 'INPUT') input.type = question.type === 'numerical' ? 'number' : 'text';
        if (input.tagName === 'INPUT' && question.type === 'numerical') input.step = 'any';
        input.name = name;
        label.append(input);
        container.append(label);
    }
}

function responseFor(question, index) {
    const name = `q${index}`;
    if (question.type === 'description') return undefined;
    if (question.type === 'multiple') {
        return [...form.querySelectorAll(`[name="${name}"]:checked`)].map(input => Number(input.value));
    }
    if (question.type === 'matching') {
        return question.pairs.map((_, row) => form.elements.namedItem(`${name}-${row}`).value);
    }
    if (question.type === 'single' || question.type === 'truefalse') {
        const checked = form.querySelector(`[name="${name}"]:checked`);
        if (!checked) return undefined;
        return question.type === 'truefalse' ? checked.value === '0' : Number(checked.value);
    }
    return form.elements.namedItem(name).value.trim();
}

function feedbackFor(question, response) {
    if (question.type === 'truefalse') return response === question.correct ? question.rightFeedback : question.wrongFeedback;
    if (question.type === 'single') return question.answers[response]?.feedback;
    if (question.type === 'multiple') return response.map(index => question.answers[index].feedback).filter(Boolean).join(' · ');
    if (question.type === 'short') return question.answers.find(item => grade({ ...question, answers: [item] }, response) > 0)?.feedback;
    if (question.type === 'numerical') return question.answers.find(item => Number(response) >= item.min && Number(response) <= item.max)?.feedback || question.wrongFeedback;
    return '';
}

function finish(scores) {
    const score = 100 * scores.reduce((sum, value) => sum + value, 0) / scores.length;
    result.replaceChildren(el('h2', `${score.toFixed(2)}% — ${score >= 80 ? 'Passed!' : 'Try again'}`));
    result.append(el('p', `You earned ${scores.reduce((sum, value) => sum + value, 0).toFixed(2)} of ${scores.length} points.`));
    const retry = el('button', 'Try again');
    retry.type = 'button';
    retry.addEventListener('click', () => location.reload());
    result.append(retry);
    try {
        localStorage.setItem(scoreKey(chapter), JSON.stringify({ score, at: Date.now() }));
        result.append(el('p', 'Result saved on this device.'));
    }
    catch { result.append(el('p', 'This browser could not save the result locally.')); }
    result.scrollIntoView({ behavior: 'smooth' });
}

function setupChecking(questions) {
    const scores = [];
    const total = questions.filter(question => question.type !== 'description').length;
    const updateProgress = () => {
        const checked = scores.filter(value => value !== undefined).length;
        if (checked === total) finish(scores.filter(value => value !== undefined));
        else result.replaceChildren(el('p', `${checked} of ${total} questions checked. Check each answer to finish the test.`));
    };
    updateProgress();
    questions.forEach((question, index) => {
        if (question.type === 'description') return;
        const card = document.getElementById(`question-${index}`);
        const check = el('button', 'Check answer');
        check.type = 'button';
        const message = el('p');
        message.setAttribute('role', 'status');
        card.append(check, message);
        check.addEventListener('click', () => {
            const response = responseFor(question, index);
            if (response === undefined || response === '' ||
                (Array.isArray(response) && (!response.length || response.some(value => value === '')))) {
                message.textContent = 'Choose or enter an answer first.';
                return;
            }
            message.textContent = '';
            check.remove();
            card.querySelectorAll('input, select, textarea').forEach(input => input.disabled = true);
            if (question.type === 'essay') {
                if (question.generalFeedback) card.append(el('p', question.generalFeedback, 'quiz-feedback'));
                const assessment = el('div', undefined, 'quiz-assessment');
                assessment.append(el('p', 'Compare your answer with the feedback, then assess yourself:'));
                for (const [label, value] of [['Correct', 1], ['Incorrect', 0]]) {
                    const button = el('button', label);
                    button.type = 'button';
                    button.addEventListener('click', () => {
                        scores[index] = value;
                        assessment.replaceChildren(el('p', `Self-assessed: ${label.toLowerCase()}.`));
                        updateProgress();
                    });
                    assessment.append(button);
                }
                card.append(assessment);
                return;
            }
            scores[index] = grade(question, response);
            card.append(el('p', `Score: ${Math.round(scores[index] * 100)}% of 1 point`, 'quiz-feedback'));
            const feedback = feedbackFor(question, response);
            if (feedback) card.append(el('p', feedback, 'quiz-feedback'));
            if (question.generalFeedback) card.append(el('p', question.generalFeedback, 'quiz-feedback'));
            if (scores[index] !== 1) {
                const solution = question.type === 'truefalse' ? String(question.correct) :
                    question.type === 'matching' ? question.pairs.map(pair => `${pair.left} → ${pair.right}`).join('; ') :
                    question.type === 'numerical' ? question.answers.map(item => item.text).join(' / ') :
                    question.answers.filter(item => item.weight > 0).map(item => item.text).join(' / ');
                card.append(el('p', `Answer: ${solution}`, 'quiz-feedback'));
            }
            updateProgress();
        });
    });
}

async function load() {
    if (!chapter) throw new Error('Unknown chapter test. Use a link from the book list.');
    title.textContent = chapter.title;
    const response = await fetch(chapter.file);
    if (!response.ok) throw new Error(`Could not load questions (${response.status}).`);
    const questions = parseGift(await response.text());
    status.textContent = `${questions.filter(item => item.type !== 'description').length} questions · Check each answer as you go · Pass at 80% · Results stay on this device`;
    questions.forEach((question, index) => {
        const card = el('section', undefined, 'quiz-card');
        card.id = `question-${index}`;
        if (question.category) card.append(el('p', question.category, 'quiz-category'));
        card.append(el('h3', `${index + 1}. ${question.title || question.prompt}`));
        if (question.title) card.append(el('p', question.prompt));
        renderInput(question, index, card);
        form.append(card);
    });
    form.hidden = false;
    form.addEventListener('submit', event => event.preventDefault());
    setupChecking(questions);
}

load().catch(error => { status.textContent = error.message; });
