// Add one entry per chapter. Bump revision when its GIFT questions change.
export const books = [
    {
        id: 'rust-atomics-and-locks',
        chapters: [
            {
                id: 'sample',
                title: 'Sample chapter (demo)',
                file: 'quizzes/rust-atomics-and-locks/sample.gift',
                revision: 1
            }
        ]
    }
];

export const scoreKey = chapter => `bookclub:quiz:${chapter.id}:${chapter.revision}`;
