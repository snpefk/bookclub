// The GIFT files are the source of truth; no service or build step is required.
const unescapeGift = (text) => text.replace(/\\([\\:#={}~n])/g, (_, char) => char === 'n' ? '\n' : char);

function splitOn(text, delimiter) {
    const pieces = [];
    let start = 0;
    for (let i = 0; i < text.length; i++) {
        if (text[i] === '\\') {
            i++;
        } else if (text.startsWith(delimiter, i)) {
            pieces.push(text.slice(start, i));
            i += delimiter.length - 1;
            start = i + 1;
        }
    }
    pieces.push(text.slice(start));
    return pieces;
}

function firstUnescaped(text, character) {
    for (let i = 0; i < text.length; i++) {
        if (text[i] === '\\') i++;
        else if (text[i] === character) return i;
    }
    return -1;
}

function textValue(raw) {
    // Treat formatted GIFT text as literal text. Never inject authored HTML into the page.
    return unescapeGift(raw.trim().replace(/^\[(?:plain|html|markdown|moodle)\]/i, '').trim());
}

function blocks(source) {
    const result = [];
    let lines = [];
    let depth = 0;
    let start = 1;
    const flush = () => {
        if (lines.length) result.push({ text: lines.join('\n').trim(), line: start });
        lines = [];
    };
    source.replace(/^\uFEFF/, '').replace(/\r\n?/g, '\n').split('\n').forEach((line, index) => {
        if (/^\s*\/\//.test(line)) return;
        if (!line.trim() && depth === 0) { flush(); return; }
        if (!lines.length) start = index + 1;
        lines.push(line);
        for (let i = 0; i < line.length; i++) {
            if (line[i] === '\\') i++;
            else if (line[i] === '{') depth++;
            else if (line[i] === '}') depth--;
        }
        if (depth < 0) throw new Error(`Line ${index + 1}: unexpected closing brace`);
    });
    if (depth) throw new Error(`Line ${start}: unclosed answer block`);
    flush();
    return result;
}

function choices(raw) {
    const result = [];
    let marker = null;
    let start = 0;
    for (let i = 0; i < raw.length; i++) {
        if (raw[i] === '\\') { i++; continue; }
        if (raw[i] === '=' || raw[i] === '~') {
            if (marker !== null) result.push({ marker, value: raw.slice(start, i).trim() });
            else if (raw.slice(0, i).trim()) throw new Error('Unexpected text before answer');
            marker = raw[i];
            start = i + 1;
        }
    }
    if (marker !== null) result.push({ marker, value: raw.slice(start).trim() });
    return result;
}

function weighted(raw, defaultWeight) {
    const match = raw.match(/^%(-?\d+(?:\.\d+)?)%/);
    if (raw.startsWith('%') && !match) throw new Error('Invalid answer weight');
    const weight = match ? Number(match[1]) / 100 : defaultWeight;
    if (weight < -1 || weight > 1) throw new Error('Answer weight must be between -100% and 100%');
    return { weight, value: match ? raw.slice(match[0].length).trim() : raw };
}

function answer(raw, defaultWeight) {
    const { weight, value } = weighted(raw, defaultWeight);
    const [text, ...feedback] = splitOn(value, '#');
    if (!text.trim()) throw new Error('Empty answer');
    return { text: textValue(text), feedback: textValue(feedback.join('#')), weight };
}

function parseQuestion(block, category) {
    let source = block.text;
    let title = '';
    if (source.startsWith('::')) {
        const end = source.indexOf('::', 2);
        if (end < 0) throw new Error('Unclosed question title');
        title = unescapeGift(source.slice(2, end));
        source = source.slice(end + 2).trim();
    }
    const open = firstUnescaped(source, '{');
    const close = firstUnescaped(source, '}');
    if ((open < 0) !== (close < 0) || (close >= 0 && close < open)) throw new Error('Unmatched answer braces');
    let raw = '';
    let prompt = source;
    let missingWord = false;
    if (open >= 0) {
        raw = source.slice(open + 1, close).trim();
        const before = source.slice(0, open);
        const after = source.slice(close + 1);
        if (firstUnescaped(after, '{') >= 0 || firstUnescaped(after, '}') >= 0) throw new Error('Multiple answer blocks');
        missingWord = Boolean(after.trim());
        prompt = before + (missingWord ? '_____' : '') + after;
    }
    prompt = textValue(prompt);
    if (!prompt) throw new Error('Empty question');
    const generalParts = splitOn(raw, '####');
    if (generalParts.length > 2) throw new Error('Multiple general feedback sections');
    raw = generalParts[0].trim();
    const question = { title, prompt, category, missingWord, generalFeedback: textValue(generalParts[1] || '') };
    if (open < 0) return { ...question, type: 'description' };
    if (!raw) return { ...question, type: 'essay' };

    if (raw.startsWith('#')) {
        const numeric = raw.slice(1).trim();
        const wrong = splitOn(numeric, '~');
        if (wrong.length > 2) throw new Error('Invalid numerical wrong-answer feedback');
        const entries = choices(wrong[0].startsWith('=') ? wrong[0] : '=' + wrong[0]);
        const answers = entries.map(({ marker, value }) => {
            if (marker !== '=') throw new Error('Invalid numerical answer');
            const parsed = answer(value, 1);
            const range = parsed.text.match(/^(-?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)\s*\.\.\s*(-?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)$/i);
            const exact = parsed.text.match(/^(-?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)(?::(\d*\.?\d+(?:e[+-]?\d+)?))?$/i);
            if (!range && !exact) throw new Error(`Invalid numerical answer: ${parsed.text}`);
            const min = range ? Number(range[1]) : Number(exact[1]) - Number(exact[2] || 0);
            const max = range ? Number(range[2]) : Number(exact[1]) + Number(exact[2] || 0);
            if (min > max) throw new Error('Numerical range has its bounds reversed');
            return { ...parsed, min, max };
        });
        return { ...question, type: 'numerical', answers, wrongFeedback: wrong[1] ? textValue(wrong[1].replace(/^#/, '')) : '' };
    }
    const tf = splitOn(raw, '#');
    if (/^(?:T|TRUE|F|FALSE)$/.test(tf[0].trim())) {
        if (tf.length > 3) throw new Error('Invalid true/false feedback');
        return { ...question, type: 'truefalse', correct: /^T/.test(tf[0].trim()), wrongFeedback: textValue(tf[1] || ''), rightFeedback: textValue(tf[2] || '') };
    }
    const entries = choices(raw);
    if (!entries.length) throw new Error('No answers found');
    if (entries.some(({ marker }) => marker === '~')) {
        if (entries.length < 2) throw new Error('Multiple choice needs at least two answers');
        const single = entries.some(({ marker }) => marker === '=');
        const answers = entries.map(({ marker, value }) => answer(value, marker === '=' ? 1 : 0));
        if (!answers.some(({ weight }) => weight > 0)) throw new Error('Multiple choice needs a positive answer');
        return { ...question, type: single ? 'single' : 'multiple', answers };
    }
    if (entries.some(({ value }) => splitOn(value, '->').length > 1)) {
        if (entries.length < 2) throw new Error('Matching needs at least two pairs');
        const pairs = entries.map(({ value }) => {
            const parts = splitOn(value, '->');
            if (parts.length !== 2 || !parts.every(part => part.trim())) throw new Error('Invalid matching pair');
            return { left: textValue(parts[0]), right: textValue(parts[1]) };
        });
        return { ...question, type: 'matching', pairs };
    }
    if (entries.some(({ marker }) => marker !== '=')) throw new Error('Short answers must start with =');
    return { ...question, type: 'short', answers: entries.map(({ value }) => answer(value, 1)) };
}

export function parseGift(source) {
    let category = '';
    const questions = [];
    for (const block of blocks(source)) {
        if (block.text.startsWith('$CATEGORY:')) {
            category = textValue(block.text.slice(10));
            continue;
        }
        try {
            questions.push(parseQuestion(block, category));
        } catch (error) {
            throw new Error(`Line ${block.line}: ${error.message}`);
        }
    }
    if (!questions.some(question => question.type !== 'description')) throw new Error('No gradable questions in this file');
    return questions;
}

const clamp = value => Math.max(0, Math.min(1, value));

export function grade(question, response) {
    if (question.type === 'description') return null;
    if (question.type === 'essay') return response === true ? 1 : response === false ? 0 : null;
    if (question.type === 'truefalse') return response === question.correct ? 1 : 0;
    if (question.type === 'single') return clamp(question.answers[response]?.weight ?? 0);
    if (question.type === 'multiple') return clamp([...response].reduce((total, index) => total + (question.answers[index]?.weight ?? 0), 0));
    if (question.type === 'matching') return question.pairs.reduce((sum, pair, index) => sum + (response[index] === pair.right ? 1 : 0), 0) / question.pairs.length;
    if (question.type === 'short') {
        const input = String(response).trim();
        return clamp(Math.max(0, ...question.answers.filter(item => {
            const pattern = item.text.split('*').map(part => part.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('.*');
            return new RegExp(`^${pattern}$`, 'i').test(input);
        }).map(item => item.weight)));
    }
    if (question.type === 'numerical') {
        const input = String(response).trim();
        if (!input || !Number.isFinite(Number(input))) return 0;
        return clamp(Math.max(0, ...question.answers.filter(item => Number(input) >= item.min && Number(input) <= item.max).map(item => item.weight)));
    }
    throw new Error(`Unknown question type: ${question.type}`);
}
