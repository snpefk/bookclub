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
            }
        ]
    }
];

export const scoreKey = chapter => `bookclub:quiz:${chapter.id}:${chapter.revision}`;
