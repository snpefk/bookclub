# Chapter 20 — Hash Tables: Anki card preview

Original recall prompts based on Robert Nystrom’s chapter, not official author material.

[Read the chapter](https://craftinginterpreters.com/hash-tables.html) · [Import instructions](hash-tables-anki.md)

Spoilers: this preview shows both sides. Import the TSV to practice active recall.

## 1. What does a hash table associate, and what identifies an entry?

It associates keys with values. The key identifies an entry and is used to retrieve its value.

[Source: §20](https://craftinginterpreters.com/hash-tables.html#top) · recall · fundamentals

## 2. What happens when you insert a new value for a key already in a hash table?

The existing value is replaced; a second entry for the same key is not created.

[Source: §20](https://craftinginterpreters.com/hash-tables.html#top) · recall · fundamentals

## 3. Is hash-table lookup guaranteed O(1)?

No. With well-distributed hashes and controlled load it is expected/average O(1) in the number of entries. A long collision chain or probe sequence can make a lookup O(n). Hashing and key-comparison costs are additional.

[Source: §20 and 20.2.1](https://craftinginterpreters.com/hash-tables.html#separate-chaining) · recall · fundamentals

## 4. Why can a hash-table lookup for a fresh length-m string still require O(m) work even when bucket probing is expected O(1)?

Computing the string's hash requires reading its characters. Expected constant bucket-search cost does not make hashing a fresh arbitrary-length string free.

[Source: §20.4.1](https://craftinginterpreters.com/hash-tables.html#hashing-strings) · recall · hashing

## 5. What three qualities does the chapter seek in a non-cryptographic hash function?

Deterministic, well-distributed for typical inputs, and fast. These goals do not imply cryptographic security.

[Source: §20.3](https://craftinginterpreters.com/hash-tables.html#hash-functions) · recall · hashing

## 6. How does Chapter 20 map a hash code to a bucket index?

index = hash % capacity, with positive capacity. Reducing the hash to the bucket range can make distinct hashes land in the same bucket.

[Source: §20.4.2](https://craftinginterpreters.com/hash-tables.html#inserting-entries) · recall · hashing

## 7. Two keys have equal hash codes. Does that prove the keys are equal?

No. Different keys can have the same hash. Equality still needs a correct key comparison. Conversely, keys considered equal must have equal hashes for the table to work correctly.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · hashing

## 8. What is a hash table's ordinary live-entry load factor?

Number of live entries divided by number of buckets. In the chapter's final tombstone-based clox table, the growth counter instead counts live entries plus tombstones.

[Source: §20.1.1 and 20.4.6](https://craftinginterpreters.com/hash-tables.html#load-factor-and-wrapped-keys) · recall · fundamentals

## 9. Does keeping a hash table mostly empty eliminate the need for collision handling?

No. Distinct keys can still map to the same bucket even at low load. More buckets reduce collision likelihood, not the requirement to handle collisions correctly.

[Source: §20.2](https://craftinginterpreters.com/hash-tables.html#collision-resolution) · recall · collisions

## 10. How does separate chaining resolve a bucket collision?

The bucket holds a collection of entries, commonly a linked list. Lookup searches that collection for a matching key.

[Source: §20.2.1](https://craftinginterpreters.com/hash-tables.html#separate-chaining) · recall · collisions

## 11. Where are colliding entries stored in open addressing?

In other buckets of the same array, found by following a probe sequence. Entries do not require a separate linked list outside the array.

[Source: §20.2.2](https://craftinginterpreters.com/hash-tables.html#open-addressing) · recall · collisions

## 12. What is the next bucket in the chapter's linear probing scheme?

(index + 1) % capacity: advance one bucket and wrap to bucket zero after the last bucket. Insertion and lookup must follow the same probe sequence.

[Source: §20.2.2 and 20.4.2](https://craftinginterpreters.com/hash-tables.html#open-addressing) · recall · collisions

## 13. Why is linear probing often cache-friendly?

It examines neighboring entries in a contiguous array instead of chasing pointers to scattered nodes.

[Source: §20.2.2](https://craftinginterpreters.com/hash-tables.html#open-addressing) · recall · collisions

## 14. What performance problem can linear probing create as occupied runs grow?

Clustering: adjacent occupied buckets form long runs, so later lookups and insertions may have to inspect many buckets.

[Source: §20.2.2](https://craftinginterpreters.com/hash-tables.html#open-addressing) · recall · collisions

## 15. In the chapter's linear-probed table, what does reaching a truly empty bucket prove during lookup?

The key is absent. A valid insertion following the same probe sequence would not have skipped that truly empty bucket. A tombstone is not truly empty.

[Source: §20.4.2 and 20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · recall · tombstones

## 16. Why can't deletion simply turn a bucket into an ordinary empty bucket in this linear-probed table?

That could break a probe sequence: a later lookup would stop at the new empty bucket and miss keys displaced beyond it.

[Source: §20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · recall · tombstones

## 17. What does a tombstone mean to lookup versus insertion?

Lookup must continue past it. Insertion may reuse it, but must first establish that the key does not already occur later in the probe sequence.

[Source: §20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · recall · tombstones

## 18. How does clox distinguish an empty bucket from a tombstone?

Both have key == NULL. An empty bucket has a nil value; a tombstone has a true Boolean value. A live entry has a non-NULL key, even if its stored value is nil.

[Source: §20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · recall · implementation

## 19. Why does findEntry() remember the FIRST tombstone while continuing to probe?

If the key is found later, it must return that existing entry. If a truly empty bucket proves absence, the first tombstone is the reusable insertion slot.

[Source: §20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · recall · tombstones

## 20. After tombstone support, what does clox Table.count count?

Live entries plus tombstones, not just live key/value pairs. It measures buckets that are not truly empty for the growth policy.

[Source: §20.4.6](https://craftinginterpreters.com/hash-tables.html#counting-tombstones) · recall · tombstones

## 21. Why does deleting a live clox table entry NOT decrement Table.count?

Deletion replaces a live entry with a tombstone. The bucket still counts as occupied for the growth policy, so live-plus-tombstone count is unchanged.

[Source: §20.4.6](https://craftinginterpreters.com/hash-tables.html#counting-tombstones) · recall · tombstones

## 22. When does the final Chapter 20 tableSet() increment Table.count?

Only when a new key occupies a truly empty bucket. Reusing a tombstone or replacing an existing key's value leaves count unchanged, apart from any preceding rebuild.

[Source: §20.4.6](https://craftinginterpreters.com/hash-tables.html#counting-tombstones) · recall · implementation

## 23. Why must clox's growth policy count tombstones as occupied?

Ignoring them could allow all buckets to become live entries or tombstones, with no truly empty bucket to terminate an unsuccessful probe. Counting them preserves empty buckets through timely growth/rebuilding.

[Source: §20.4.6](https://craftinginterpreters.com/hash-tables.html#counting-tombstones) · recall · tombstones

## 24. Why can't a growing hash table simply copy entries to the same indices of a larger array?

The preferred bucket depends on hash % capacity. Changing capacity changes preferred buckets and collision/probe sequences, so live entries must be placed again using the new capacity.

[Source: §20.4.3](https://craftinginterpreters.com/hash-tables.html#allocating-and-resizing) · recall · resizing

## 25. Does resizing clox's table require hashing every string's characters again?

No. Each immutable ObjString already caches its hash code. Resizing recomputes bucket placement and probe sequences using that cached hash and the new capacity.

[Source: §20.4.1 and 20.4.3](https://craftinginterpreters.com/hash-tables.html#allocating-and-resizing) · recall · resizing

## 26. What happens to tombstones and Table.count when clox rebuilds a table?

Only live entries are reinserted; tombstones are discarded. Count is reset and recomputed, so immediately after rebuilding it equals the number of live entries.

[Source: §20.4.6](https://craftinginterpreters.com/hash-tables.html#counting-tombstones) · recall · resizing

## 27. What is Chapter 20's clox growth check before tableSet() searches for its key?

Grow if count + 1 > capacity * 0.75. The 0.75 threshold is this implementation's choice, not a universal optimum. Because the check happens first, even an overwrite can trigger growth.

[Source: §20.4.2 and 20.4.6](https://craftinginterpreters.com/hash-tables.html#inserting-entries) · recall · implementation

## 28. How can hash-table insertions be expected amortized O(1) even though a resize is expensive?

Geometric growth makes rebuilds infrequent, spreading their cost over many insertions. A single rebuilding insertion is not O(1); the claim also assumes hashing/probing behaves well.

[Source: §20.4.2–20.4.3](https://craftinginterpreters.com/hash-tables.html#allocating-and-resizing) · recall · resizing

## 29. Why can ObjString safely cache its hash code for its lifetime?

Lox strings are immutable, so their contents and content-derived hash do not change. Mutating a key without updating its placement could make it unreachable in a hash table.

[Source: §20.4.1](https://craftinginterpreters.com/hash-tables.html#hashing-strings) · recall · hashing

## 30. In the chapter's FNV-1a string hash, what two operations process each byte, and in what order?

XOR the byte into the running hash, then multiply by the FNV prime using unsigned arithmetic. Remember the mixing order, not the numeric constants.

[Source: §20.4.1](https://craftinginterpreters.com/hash-tables.html#hashing-strings) · recall · hashing

## 31. What invariant does string interning establish within clox's VM?

Each distinct character sequence has one canonical string object. Creating the same text again returns the already interned object.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 32. Why can clox compare strings with pointer equality AFTER interning all of them?

Equal text is represented by the same canonical object. Thus pointer identity matches textual equality within that intern pool. Without the invariant, equal strings can live at different addresses.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 33. Why does tableFindString() accept raw characters, length, and hash instead of using ordinary pointer-key tableGet()?

It is trying to find a canonical string before allocating its ObjString. Ordinary lookup expects an already interned object key and uses pointer equality, which cannot deduplicate raw text.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 34. Which checks establish that a candidate interned string matches raw input text?

Matching length, matching hash, and matching character bytes. Length and hash are fast rejection tests; equal hashes alone are not proof.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 35. Why do entries in clox's interned-string table use nil as their stored value?

The table is being used as a set: only the canonical string keys matter. A nil value with a non-NULL key is a live entry, not an empty bucket.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 36. If copyString() finds that its input text is already interned, what does it return?

The existing canonical ObjString, without allocating a duplicate string object or copying another character buffer for it.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 37. If takeString() finds an existing interned match, what must it do with the incoming owned character buffer?

Free that redundant buffer, then return the existing interned object. Ownership was transferred to takeString(), so simply returning without freeing it would leak memory.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 38. What performance tradeoff does string interning make in this interpreter?

Extra work to deduplicate strings at creation time buys cheap pointer-based equality later, particularly useful for repeated variable, field, and method-name lookups.

[Source: §20.5](https://craftinginterpreters.com/hash-tables.html#string-interning) · recall · interning

## 39. Trace: capacity 8, initially empty, no resizing. Distinct keys A, B, C all prefer bucket 7. Insert A, then B, then C using linear probing. Where do they land?

A at 7, B at 0, C at 1. Each collision advances one bucket, wrapping from 7 to 0.

[Source: §20.2.2](https://craftinginterpreters.com/hash-tables.html#open-addressing) · trace · collisions

## 40. Trace: A, B, C occupy buckets 2, 3, 4 and all prefer bucket 2. Delete B, leaving a tombstone at 3. Which buckets does lookup of C examine?

2, 3, 4. It skips A, continues past B's tombstone, and finds C at 4. Clearing bucket 3 to truly empty would incorrectly hide C.

[Source: §20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · trace · tombstones

## 41. Trace: a key K prefers bucket 2. Bucket 2 is a tombstone, K already occupies 3, and 4 is empty. Without resizing, tableSet(K, newValue) writes to which bucket?

Bucket 3. It must continue past the tombstone and update the existing K, not create a duplicate K at 2.

[Source: §20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · trace · tombstones

## 42. Trace: new key K prefers bucket 2. Bucket 2 is a tombstone, 3 holds another key, and 4 is truly empty. Without resizing, where is K inserted, and when is its absence established?

Insert K at 2, but only after reaching empty bucket 4 to prove K is absent. Bucket 2 is remembered as the first reusable tombstone.

[Source: §20.4.5](https://craftinginterpreters.com/hash-tables.html#deleting-entries) · trace · tombstones

## 43. Trace: clox capacity is 8, count is 6, and maximum load is 0.75. What happens BEFORE the next tableSet() searches for its key?

It grows: count + 1 is 7, which exceeds 8 * 0.75 = 6. The check runs even if the call ultimately overwrites an existing key.

[Source: §20.4.2](https://craftinginterpreters.com/hash-tables.html#inserting-entries) · trace · resizing

## 44. Trace: capacity 16, 4 live entries, 2 tombstones. Without resizing, insert a NEW key into a tombstone. What are the new live-entry, tombstone, and clox count values?

5 live entries, 1 tombstone, count 6. Reusing a tombstone changes the live/deleted split but not their sum.

[Source: §20.4.6](https://craftinginterpreters.com/hash-tables.html#counting-tombstones) · trace · tombstones

## 45. Trace: a key's cached hash is 13. What is its PREFERRED bucket at capacity 8 versus capacity 16, before considering collisions?

At capacity 8: 13 % 8 = 5. At capacity 16: 13 % 16 = 13. The hash stays the same, but its preferred bucket changes.

[Source: §20.4.3](https://craftinginterpreters.com/hash-tables.html#allocating-and-resizing) · trace · resizing

## 46. Trace: a clox table has 4 live entries and 2 tombstones (count 6). It is rebuilt into a larger array, with no new key inserted yet. What is count immediately afterward?

4. Rebuilding reinserts only the four live entries and discards both tombstones.

[Source: §20.4.6](https://craftinginterpreters.com/hash-tables.html#counting-tombstones) · trace · resizing
