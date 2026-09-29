import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { parseGift, grade } from '../gift.mjs';
import { books } from '../quizzes.mjs';

test('the published demo loads as a real quiz with every supported question type', () => {
    const source = readFileSync(new URL('../quizzes/rust-atomics-and-locks/sample.gift', import.meta.url), 'utf8');
    const questions = parseGift(source);
    assert.deepEqual(questions.map(q => q.type), ['single', 'multiple', 'truefalse', 'short', 'matching', 'numerical', 'single', 'essay', 'description']);
    assert.equal(questions[0].category, 'Sample chapter');
    assert.equal(questions[0].generalFeedback, 'This is a demonstration question, not a test of the book.');
    assert.deepEqual(questions[4].pairs, [{ left: '=', right: 'equals' }, { left: '~', right: 'tilde' }]);
    assert.equal(grade(questions[0], 1), 1);
    assert.equal(grade(questions[1], [1, 2]), 1);
    assert.equal(grade(questions[1], [0, 1, 2]), 0.5);
    assert.equal(grade(questions[2], true), 1);
    assert.equal(grade(questions[3], ' TWO '), 1);
    assert.equal(grade(questions[3], '2'), 0.5);
    assert.equal(grade(questions[4], ['equals', 'wrong']), 0.5);
    assert.equal(grade(questions[5], '5.09'), 1);
    assert.equal(grade(questions[5], '5.11'), 0);
    assert.equal(grade(questions[7], true), 1);
    assert.equal(grade(questions[7], false), 0);
    assert.equal(grade(questions[8]), null);
});

test('escaped delimiters, weighted alternatives, numerical ranges and wildcards', () => {
    const questions = parseGift(String.raw`// Comment
::Punctuation::[html]What is \{2 + 2\}?{~wrong\=answer#bad\#guess =%75%4#nearly ####General \~ feedback}

Number in range? {#=1..3#yes =%50%4:1#near ~#no}

Complete the name: {=New * City =%50%NYC}

Multiline essay {####Assess your own response.}
`);
    assert.equal(questions[0].prompt, 'What is {2 + 2}?');
    assert.equal(questions[0].answers[0].text, 'wrong=answer');
    assert.equal(questions[0].answers[0].feedback, 'bad#guess');
    assert.equal(questions[0].generalFeedback, 'General ~ feedback');
    assert.equal(grade(questions[0], 1), 0.75);
    assert.equal(grade(questions[1], '2'), 1);
    assert.equal(grade(questions[1], '4.5'), 0.5);
    assert.equal(questions[1].wrongFeedback, 'no');
    assert.equal(grade(questions[2], 'new york city'), 1);
    assert.equal(grade(questions[3], null), null);
});

test('invalid syntax is rejected with a useful line number', () => {
    assert.throws(() => parseGift('Valid? {T}\n\nBad? {#not-a-number}'), /Line 3: Invalid numerical answer/);
    assert.throws(() => parseGift('What? {=yes'), /Line 1: unclosed answer block/);
    assert.throws(() => parseGift('Choices? {~%oops%no =yes}'), /Line 1: Invalid answer weight/);
    assert.throws(() => parseGift('Only a description'), /No gradable questions/);
});

test('the hardware chapter test is registered and grades representative answers', () => {
    const chapter = books[0].chapters.find(item => item.id === 'hardware');
    assert.ok(chapter);
    const source = readFileSync(new URL('../' + chapter.file, import.meta.url), 'utf8');
    const questions = parseGift(source);
    assert.equal(questions.length, 28);
    assert.ok(questions.every(question => question.category.includes('Chapter 7')));
    const named = title => questions.find(question => question.title === title);
    assert.equal(grade(named('Compiler versus processor'), 1), 1);
    assert.equal(grade(named('Inspecting optimized assembly'), [0, 1]), 1);
    assert.equal(grade(named('Inspecting optimized assembly'), [0, 1, 2]), 0.5);
    assert.equal(grade(named('ARM64 exclusive instructions'), ['load an exclusive value', 'try a conditional store and report success or failure', 'abandon exclusive tracking without storing']), 1);
    assert.equal(grade(named('Cache lines'), 64), 1);
    assert.equal(grade(named('Alignment and padding'), 8), 0);
    assert.equal(grade(named('x86-64 ordering'), 1), 1);
    assert.equal(grade(named('Putting it together'), true), 1);
});
