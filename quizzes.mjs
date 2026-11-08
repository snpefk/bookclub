// Add one entry per chapter. Bump revision when its GIFT questions change.
export const books = [
    {
        id: 'rust-atomics-and-locks',
        chapters: [
            {
                id: 'hardware',
                title: 'Chapter 7 — Understanding the Processor',
                file: 'quizzes/rust-atomics-and-locks/hardware.gift',
                revision: 1
            },
            {
                id: 'building-locks',
                title: 'Chapter 9 — Building Our Own Locks',
                file: 'quizzes/rust-atomics-and-locks/building-locks.gift',
                revision: 1
            }
        ]
    },
    {
        id: 'hundred-page-machine-learning',
        chapters: [
            {
                id: 'hundred-page-machine-learning-chapter-01',
                title: 'Chapter 1 — Introduction',
                file: 'quizzes/hundred-page-machine-learning/chapter-01.gift',
                anki: 'anki/hundred-page-machine-learning/chapter-01.tsv',
                revision: 1
            },
            {
                id: 'hundred-page-machine-learning-chapter-02',
                title: 'Chapter 2 — Notation and Definitions',
                file: 'quizzes/hundred-page-machine-learning/chapter-02.gift',
                anki: 'anki/hundred-page-machine-learning/chapter-02.tsv',
                revision: 1
            },
            {
                id: 'hundred-page-machine-learning-chapter-03',
                title: 'Chapter 3 — Fundamental Algorithms',
                file: 'quizzes/hundred-page-machine-learning/chapter-03.gift',
                anki: 'anki/hundred-page-machine-learning/chapter-03.tsv',
                revision: 1
            },
            {
                id: 'hundred-page-machine-learning-chapter-04',
                title: 'Chapter 4 — Anatomy of a Learning Algorithm',
                file: 'quizzes/hundred-page-machine-learning/chapter-04.gift',
                anki: 'anki/hundred-page-machine-learning/chapter-04.tsv',
                revision: 1
            }
        ]
    }
];

export const scoreKey = chapter => `bookclub:quiz:${chapter.id}:${chapter.revision}`;
