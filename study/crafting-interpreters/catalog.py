"""Generate the annotated Markdown index and exhaustive hyperlink catalog."""
from collections import defaultdict
import json
from pathlib import Path
import re
from urllib.parse import unquote, urldefrag, urlsplit, quote

from bs4 import BeautifulSoup

STUDY = Path(__file__).resolve().parent
ROOT = STUDY.parents[1] / 'books' / 'crafting-interpreters'
BASE = 'https://craftinginterpreters.com/'

# A few explicit descriptions supplement the book's own linking context.
DESCRIPTIONS = {
    'Curry–Howard_correspondence': 'The correspondence between propositions and types, and between proofs and programs; background for the relationship between type systems and formal reasoning.',
    'Compilers:_Principles,_Techniques,_and_Tools': 'The compiler textbook commonly known as the Dragon Book, covering compiler theory and implementation.',
    'sicp': 'Structure and Interpretation of Computer Programs, the classic programming textbook associated with the wizard cover.',
    'Lex_(software)': 'A lexical-analyzer generator that produces scanners from token-pattern specifications.',
    '/wiki/Yacc': 'A parser generator that produces parsing code from a grammar; its name means Yet Another Compiler-Compiler.',
    'GNU_bison': 'GNU Bison, a parser generator related to Yacc.',
    'Doubly_linked_list': 'A linked-list data structure in which each node links to both its predecessor and successor.',
    '/wiki/Lox-implementations': 'Community implementations and ports of the Lox language in other programming languages.',
    '/blob/master/LICENSE': 'The source repository’s license, including the separate licensing terms for book text and source code.',
    '/munificent/craftinginterpreters': 'Robert Nystrom’s repository for the book, its publishing tools, and the Java and C Lox implementations.',
}

DESCRIPTIONS.update({
    'gameprogrammingpatterns.com/': 'Robert Nystrom’s book about software design patterns used in game development.',
    'GNU_Compiler_Collection': 'GCC, a compiler collection supporting many source languages and target architectures through shared intermediate representations.',
    '/GIMPLE.html': 'GCC’s GIMPLE intermediate representation, used between language-specific front ends and later compilation stages.',
    '/RTL.html': 'GCC’s Register Transfer Language, a lower-level intermediate representation describing operations closer to target machine instructions.',
    '/wiki/X86': 'The x86 processor instruction-set family, used as an example of architecture-specific native-code targets.',
    'ARM_architecture': 'The ARM processor architecture family, contrasted with x86 to explain why native code is architecture-dependent.',
    '/x86/AAD.html': 'The x86 AAD instruction reference: ASCII Adjust AX Before Division, an example of a specialized legacy instruction.',
    'golang.org/': 'The Go programming language and toolchain; the book contrasts building an executable with compiling and immediately running it.',
    'Syntax-directed_translation': 'A compilation technique that associates semantic actions, such as code generation, with grammar productions.',
    'list-of-languages-that-compile-to-js': 'A community-maintained list of languages and compilers that target JavaScript.',
    'github.com/webassembly/': 'The WebAssembly project, providing a low-level compilation target that can execute in web browsers.',
    'why-was-the-c-syntax-for-arrays-pointers-and-functions': 'Discussion of C declaration syntax and the “declaration reflects use” design principle for pointers, arrays, and functions.',
    'Bacon04Unified.pdf': 'A Unified Theory of Garbage Collection, a research paper relating tracing collection and reference counting.',
    'landin-next-700.pdf': 'Peter J. Landin’s The Next 700 Programming Languages, a foundational paper discussed in connection with closures and language design.',
    'Class-based_programming': 'Object-oriented programming organized around classes that define the behavior and structure of instances.',
    'Prototype-based_programming': 'Object-oriented programming that reuses behavior through prototype objects rather than requiring class definitions.',
    'prototype.html#what-about-javascript': 'The JavaScript discussion in Game Programming Patterns’ Prototype chapter, explaining the relationship between prototypes and class-like conventions.',
    'finch.stuffwithstuff.com': 'Finch, Robert Nystrom’s experimental prototype-based language, cited as a practical exploration of prototype-oriented programming.',
    'WaterbedTheory': 'The “waterbed theory” of complexity: simplifying one part of a language or system can move unavoidable complexity elsewhere.',
    'query=sysexits': 'The sysexits.h conventions for standardizing process exit-status codes, used by the command-line interpreter.',
    'Regular_language': 'Formal languages recognizable by finite automata and describable by regular expressions; relevant to token scanning.',
    'Chomsky_hierarchy': 'The classification of formal grammars and languages by expressive power, from regular to unrestricted grammars.',
    'Finite-state_machine': 'A computational model with a finite collection of states and transitions, relevant to scanners and regular languages.',
    'dinosaur.compilertools.net/lex': 'Documentation for Lex, a tool that generates lexical analyzers from regular-expression token specifications.',
    'github.com/westes/flex': 'The Flex scanner-generator project, a modern tool for generating lexical analyzers from pattern rules.',
    'Character.html#isDigit': 'Java Character.isDigit documentation, cited because its Unicode-aware definition of a digit is broader than Lox’s ASCII number syntax.',
    'lua.org/pil/1.1.html': 'Programming in Lua’s discussion of language chunks and statements, referenced when comparing optional statement separators.',
    'golang.org/ref/spec#Semicolons': 'Go’s lexical rules for semicolons and automatic insertion at selected line endings.',
    'golang.org/cmd/gofmt': 'gofmt, Go’s canonical source formatter, mentioned alongside Go’s newline and semicolon rules.',
    'lexical_analysis.html#implicit-line-joining': 'Python’s implicit line-joining rules inside parentheses, brackets, and braces.',
    'ecma-262/5.1/#sec-7.9': 'The ECMAScript specification’s automatic semicolon insertion rules, contrasted with newline handling in other languages.',
    'Order_of_operations#Mnemonics': 'Mnemonics for arithmetic precedence, used to motivate expression trees that preserve the order of operations.',
    'Formal_grammar': 'Formal production rules for generating a language’s valid strings, the foundation of the book’s syntax notation.',
    'Unrestricted_grammar': 'Grammars whose production rules can replace sequences of symbols, more general than context-free grammars.',
    'Backus–Naur_form': 'Backus–Naur form, a standard notation for writing context-free grammar productions.',
    'Regular_expression#Standards': 'Regular-expression notation and standards, cited to explain familiar repetition and optionality symbols in grammar rules.',
    'Extended_Backus–Naur_form': 'Extended Backus–Naur form, a grammar notation with convenient constructs for repetition, alternatives, and optional syntax.',
    'Interpreter_pattern': 'The Interpreter design pattern, which represents syntax in objects that can evaluate or interpret themselves.',
    'Separation_of_concerns': 'The design principle of keeping distinct responsibilities separate, used to motivate separating syntax nodes from operations on them.',
    'Reverse_Polish_notation': 'Postfix expression notation, where operators follow their operands and expressions can be evaluated with a stack.',
    'Double-precision_floating-point_format': 'IEEE 754 binary64 floating-point representation, explaining precision limits and rounding effects in numeric evaluation.',
    'ncg_goldberg.html': 'David Goldberg’s What Every Computer Scientist Should Know About Floating-Point Arithmetic, covering representation, rounding, and numerical pitfalls.',
    '/wiki/LL_parser': 'Top-down LL parsing, which reads left to right and constructs a leftmost derivation using lookahead.',
    '/wiki/LR_parser': 'Bottom-up LR parsing, which reads left to right and reconstructs a rightmost derivation in reverse.',
    '/wiki/LALR_parser': 'Look-ahead LR parsing, a compact LR-family technique widely used by parser generators.',
    'Parser_combinator': 'A parsing approach that builds complex parsers by composing smaller parsing functions.',
    'Earley_parser': 'A general context-free parsing algorithm that handles a wide range of grammars using chart-based state tracking.',
    'Shunting-yard_algorithm': 'Dijkstra’s stack-based algorithm for handling expression precedence and associativity, often producing postfix output.',
    'Parsing_expression_grammar': 'Parsing expression grammars and packrat parsing: recognition-oriented grammar rules and memoization-based parsing techniques.',
    'Comma_operator': 'C’s comma operator, which evaluates a sequence of expressions and produces the final expression’s value.',
    '/wiki/IEEE_754': 'The floating-point arithmetic standard, including NaN behavior, infinities, rounding, and comparisons.',
    'Covariance_and_contravariance': 'Subtyping variance, specifically Java and C# array covariance and the runtime checks needed when static array typing permits unsafe writes.',
    'Value_(computer_science)#lrvalue': 'The distinction between l-values, which identify storage locations, and r-values, which provide computed values.',
    'clojure.core/binding': 'Clojure’s binding macro, which temporarily rebinds dynamic variables within a dynamic extent.',
    '/Statements/with': 'JavaScript’s with statement, which alters name lookup by introducing an object’s properties into the lookup environment.',
    'Parent_pointer_tree': 'A tree represented by links from children to parents, used to explain nested environment chains and cactus stacks.',
    'xe53dz5w': 'Visual Basic’s Option Explicit setting, controlling whether variables must be explicitly declared rather than introduced implicitly.',
    'Foundations_of_mathematics#Foundational_crisis': 'The foundational crisis in mathematics caused by paradoxes and questions about the consistency and limits of formal reasoning.',
    'Russell\'s_paradox': 'The contradiction arising from the set of all sets that do not contain themselves, motivating restrictions in formal set theory.',
    'Computable_function': 'Functions whose results can be obtained by an effective algorithm, central to defining the power and limits of computation.',
    'Church–Turing_thesis': 'The thesis relating effectively computable functions to formal models such as Turing machines and lambda calculus.',
    'Dangling_else': 'The grammar ambiguity in nested conditional statements about which unmatched if receives an else clause.',
    'gameprogrammingpatterns.com/prototype.html': 'The Prototype chapter of Game Programming Patterns, exploring object cloning and prototype-based reuse.',
    'Multiple_dispatch': 'Selecting a method using the runtime types of multiple arguments, rather than only one receiver.',
    'lua.org/pil/13.4.1.html': 'Lua’s __index metamethod and metatable-based delegation, used to implement prototype-like object behavior.',
    'magpie-lang.org': 'Magpie, Robert Nystrom’s experimental language exploring multimethods and multiple dispatch.',
    'Common_Lisp_Object_System': 'Common Lisp’s object system, including generic functions, multimethods, and multiple dispatch.',
    'opendylan.org': 'The Dylan programming language and implementation, cited as a language with generic functions and multiple dispatch.',
    'julialang.org': 'The Julia programming language, whose central programming model uses multiple dispatch.',
    'docs.raku.org/language/functions#Multi-dispatch': 'Raku’s multi-dispatch documentation, describing how argument signatures select among alternative routines.',
    'hidden-classes.html': 'An explanation of JavaScript engine hidden classes, which optimize object-property access by tracking object shapes.',
    'Placement_syntax': 'C++ placement new, which constructs an object in storage supplied by the caller rather than hiding all allocation details.',
    '/wiki/Metaclass': 'Classes whose instances are themselves classes, cited as a way to model class-level behavior in an object system.',
    'Prototype-based_programming#Delegation': 'Delegating property or method lookup from one object to another, enabling prototype-based behavior reuse.',
    'selflanguage.org': 'Self, the prototype-based language developed by David Ungar and Randall Smith, an influential experiment in simplifying object models.',
    'wren.io': 'Wren, Robert Nystrom’s small class-based scripting language, cited in discussions of object models and UTF-8 string design.',
    '/wiki/Simula': 'Simula, an early object-oriented language whose class and inheritance features grew out of simulation programming.',
    'Liskov_substitution_principle': 'The behavioral-subtyping principle that instances of a subtype should be usable where the supertype is expected.',
    'beta.cs.au.dk': 'The BETA language, cited for its superclass-first method execution model and inner calls to subclass behavior.',
    'the-impoliteness-of-overriding-methods': 'Robert Nystrom’s essay on method overriding and the alternative superclass-first extension model exemplified by BETA.',
    'gameprogrammingpatterns.com/data-locality.html': 'The Data Locality chapter of Game Programming Patterns, explaining cache behavior and the performance costs of scattered object layouts.',
    'llvm.org': 'LLVM, a compiler infrastructure that can turn a shared intermediate representation into native code for multiple processor architectures.',
    'P-code_machine': 'Virtual machines executing portable p-code, an early bytecode approach associated with Pascal implementations.',
    'Amortized_analysis': 'Analyzing the average cost per operation over a sequence, used to show why geometrically growing dynamic arrays have constant amortized append cost.',
    'jvms-4.html#jvms-4.4': 'The Java Virtual Machine class-file constant pool, which stores literal values and symbolic references used by compiled code.',
    'Run-length_encoding': 'Compressing repeated adjacent values as value-and-count runs, suggested for bytecode-to-source line information.',
    '/craftinginterpreters/tree/master/test': 'The book’s Lox test suite, offered for checking the behavior of other Lox implementations.',
    'the-first-rule-of-programming-its-always-your-fault': 'A Coding Horror essay about programmers’ usual assumption that bugs are in application code rather than in mature language tools.',
    'gameprogrammingpatterns.com/singleton.html': 'The Singleton chapter of Game Programming Patterns, including the architectural drawbacks of global state.',
    'Program_counter': 'The program counter or instruction pointer, which tracks the next machine or virtual-machine instruction to execute.',
    'Heap_(data_structure)': 'The heap data structure, often used for priority queues; explicitly distinguished from the dynamic-allocation memory heap.',
    'Memory_management#HEAP': 'The heap region used for dynamically allocated memory, not the similarly named priority-queue data structure.',
    'Just-in-time_compilation': 'Compiling code to native machine instructions during execution, often using runtime information to improve performance.',
    'Register_allocation': 'Assigning program values to a limited set of machine registers and managing transfers to memory when registers are insufficient.',
    'Register_window': 'Hardware register windows, especially the SPARC mechanism, compared with register-based bytecode organization.',
    'lua.org/doc/jucs05.pdf': 'The Implementation of Lua 5.0, a paper describing Lua’s implementation choices, including its register-based virtual machine.',
    '/wiki/Trie': 'A prefix-tree data structure that represents strings through shared character paths, used to recognize keywords.',
    'Deterministic_finite_automaton': 'A finite-state recognizer with a single determined transition for each state and input symbol, related to keyword recognition and tries.',
    'gameprogrammingpatterns.com/state.html': 'The State chapter of Game Programming Patterns, explaining finite-state machines and state-based behavior.',
    'Syntax_diagram': 'Railroad or syntax diagrams, a visual notation showing the paths allowed by a grammar.',
    '/src/parsing/scanner.cc#L1643': 'A specific version of V8’s scanner source code, cited as a production example of direct keyword recognition.',
    'String_interpolation': 'Embedding expressions inside a string literal and evaluating them to construct the resulting string.',
    'pratt-parsers-expression-parsing-made-easy': 'Robert Nystrom’s Pratt parsing tutorial, presenting expression parsing with binding power in a Java/object-oriented style.',
    'princeton.edu/~bwk/cbook.html': 'The C Programming Language by Brian Kernighan and Dennis Ritchie, recommended as an introductory C reference.',
    'Type_punning': 'Interpreting stored bits through different types, discussed when representing dynamically typed values in C.',
    'Flexible_array_member': 'A C struct’s trailing array of runtime-selected size, suggested for storing a string’s characters with its object header in one allocation.',
    '/wiki/ASCII': 'The ASCII character-encoding standard, used as historical background for string representation and character sets.',
    '/wiki/Unicode': 'The Unicode standard for representing characters from many writing systems through code points and related text-processing conventions.',
    'Birthday_problem': 'The surprisingly rapid growth in collision probability as more values are sampled, used to motivate hash-collision handling.',
    'Pigeonhole_principle': 'The counting principle that more items than containers force at least one shared container, explaining unavoidable hash collisions.',
    'isthe.com/chongo/tech/comp/fnv': 'The Fowler–Noll–Vo family of hash functions, including the FNV-1a variant selected for clox string hashing.',
    'Structured_programming': 'Programming with structured control constructs such as sequences, conditionals, and loops rather than unrestricted jumps.',
    'Structured_program_theorem': 'The Böhm–Jacopini result that structured sequencing, selection, and iteration can express computations otherwise written using arbitrary jumps.',
    '/wiki/Continuation': 'A representation of the remainder of a computation, explaining why some languages cannot implement every call using a simple conventional stack.',
    'Inverted_pyramid_(journalism)': 'A writing structure that puts the most important information first, used as an analogy for ordering stack traces.',
    'Map_(higher-order_function)': 'A higher-order operation that applies a function to every element in a collection, illustrating frequent closure calls.',
    'Filter_(higher-order_function)': 'A higher-order operation that retains elements satisfying a predicate, another common use of closures.',
    'ClosuresAndObjectsAreEquivalent': 'The well-known comparison between objects and closures, motivating an exercise that emulates object-like state with closures.',
    'gchandbook.org': 'The Garbage Collection Handbook, a comprehensive reference on automatic memory-management algorithms.',
    'Weak_reference': 'A reference that does not keep its target alive for garbage collection, used for the interned-string table.',
    'Boehm_garbage_collector': 'The Boehm–Demers–Weiser conservative garbage collector, which can discover potential pointers in native memory and stacks.',
    'Monte_Carlo_algorithm': 'Randomized algorithms that trade a bounded chance of an incorrect result for useful performance guarantees.',
    'the-language-strangeness-budget': 'Steve Klabnik’s language-design essay arguing that learners tolerate only a limited amount of unfamiliar syntax and behavior.',
    'Idiosyncrasy_credit': 'The social-psychology concept of earning tolerance for nonconforming behavior through prior conformity, used as an analogy for language novelty.',
    'MIT_License': 'The permissive MIT software license used for the book’s interpreter source code, distinct from the license on most book prose and illustrations.',
    'Context-free_grammar': 'A grammar in which each production replaces one nonterminal independently of its surrounding symbols, used for Lox syntax.',
    'Regular_grammar': 'A restricted grammar corresponding to regular languages and finite-state recognition, contrasted with recursive syntax grammars.',
})


def clean(s):
    return re.sub(r'\s+', ' ', s).strip()


def shorten(s, length=520):
    s = clean(s)
    if len(s) <= length:
        return s
    cut = s.rfind(' ', 0, length)
    return s[:cut if cut > 0 else length] + '…'


def md(s):
    return str(s).replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]').replace('*', '\\*').replace('`', '\\`').replace('<', '&lt;').replace('>', '&gt;')


def link(label, url):
    encoded = quote(url, safe=":/#?=&%+;,@!$'()*~.-_")
    return f'[{md(label)}](<{encoded}>)'


def topic_from_url(url):
    parts = urlsplit(url)
    path = unquote(parts.path)
    if '/wiki/' in path:
        return path.split('/wiki/', 1)[1].replace('_', ' ')
    return ''


def context_excerpt(occ):
    text = occ['context']
    label = occ['label']
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z“"(])', text)
    for i, sentence in enumerate(sentences):
        if label and label in sentence:
            # Include the preceding sentence when the link sentence starts vaguely.
            if i and re.match(r'^(This|That|It|These|Those|Here|See|They)\b', sentence):
                sentence = sentences[i-1] + ' ' + sentence
            return shorten(sentence)
    return shorten(text)


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    pages = manifest['pages']
    page_by_url = {p['url']: p for p in pages}
    documents = {p['url']: BeautifulSoup((ROOT/'source-html'/urlsplit(p['url']).path.rsplit('/',1)[-1]).read_text(), 'html.parser') for p in pages}
    grouped = defaultdict(list)
    for page in pages:
        for occurrence in page['links']:
            grouped[occurrence['url']].append(occurrence)

    external = []
    internal = []
    navigation = []
    for url, occurrences in grouped.items():
        host = urlsplit(url).netloc.lower()
        if host not in ('craftinginterpreters.com', 'www.craftinginterpreters.com'):
            external.append((url, occurrences))
        elif any(o['role'] in ('content', 'heading') for o in occurrences):
            internal.append((url, occurrences))
        else:
            navigation.append((url, occurrences))

    def order(item):
        # Keep the book's first-reference reading order, not a domain sort.
        return list(grouped).index(item[0])

    lines = ['# Crafting Interpreters — annotated link catalog', '',
        f'Author: Robert Nystrom. Source: {link("online table of contents", BASE+"contents.html")}.', '',
        f'Captured: {manifest["exported_at"]}.', '',
        f'**Coverage:** {len(pages)} exported book pages; {sum(len(p["links"]) for p in pages)} hyperlink occurrences; {len(grouped)} distinct absolute destinations.', '',
        '**What “all links” means:** every nonempty HTTP, HTTPS, or email hyperlink in the exported HTML pages, including prose, code links, asides, challenges, design notes, headings, menus, and footers. Repeated destinations appear once below, with their source sections listed. Section fragments are kept distinct. Script controls with no destination, CSS/font/image resource URLs that are not hyperlinks, and links on external sites are not recursively collected.', '',
        '**Descriptions:** internal links are described using their target heading and opening text. External links are described using the anchor text and the surrounding book passage; that contextual passage is included. External pages were not independently read or checked for availability, so this catalog does not claim their current contents have been verified.', '',
        '**PDF behavior:** links to other webpages remain online; same-page section links are PDF-internal destinations where Chromium supports them. This Markdown file also gives the original web URL for every section.', '',
        '## External references and email links', '',
        f'{len(external)} distinct destinations.', '']

    def sources(occurrences):
        seen = set()
        values = []
        for o in occurrences:
            section = o['role'].capitalize() if o['role'] in ('navigation','footer') else o['section']
            key = (o['source'], section)
            if key in seen:
                continue
            seen.add(key)
            title = page_by_url[o['source']]['title']
            label = title if section == title else title + ' / ' + section
            values.append(link(label, o['source']))
        return '; '.join(values)

    def primary(occurrences):
        return max(occurrences, key=lambda o: (o['role']=='content', len(o['context']) > len(o['label']), len(o['label'])))

    def internal_description(url, occurrences):
        base, fragment = urldefrag(url)
        doc = documents.get(base)
        target_page = page_by_url.get(base)
        if doc:
            target = doc.find(id=unquote(fragment)) if fragment else doc.select_one('article h1')
            if fragment == 'top':
                target = doc.select_one('article h1')
            if target:
                heading = target if target.name in ('h1','h2','h3','h4') else target.find_parent(['h1','h2','h3','h4'])
                title = clean((heading or target).get_text(' ', strip=True))
                if not title:
                    title = target_page['title']
                following = (heading or target).find_next(['p','pre','ul','ol'])
                text = clean(following.get_text(' ', strip=True)) if following else ''
                if not fragment:
                    title = target_page['title']
                intro = f'{"Section" if fragment else "Book page"}: {title}.'
                return intro + (' ' + shorten(text, 360) if text else '')
        if urlsplit(base).path in ('/', '/index.html'):
            return 'The Crafting Interpreters home page, with the book overview and reading or purchase options.'
        o = primary(occurrences)
        return f'Book-site resource referenced as “{o["label"]}” in {o["section"]}. Context: {context_excerpt(o)}'

    for i, (url, occurrences) in enumerate(sorted(external, key=order), 1):
        o = primary(occurrences)
        label = o['label']
        decoded = unquote(url)
        about = None
        # Prefer specific patterns to the generic repository entry.
        for pattern, description in sorted(DESCRIPTIONS.items(), key=lambda item: -len(item[0])):
            if pattern in decoded:
                about = description
                break
        topic = topic_from_url(url)
        if not about and topic:
            about = f'Background/reference material about {topic}, linked while discussing {o["section"]}.'
        if not about and url.startswith('mailto:'):
            about = f'Email contact: {unquote(url[7:]).split("?")[0]}. The surrounding passage indicates why it is provided.'
        if not about:
            # Do not invent a destination-page summary when only book context is known.
            about = f'Resource referenced as “{label}” while discussing {o["section"]}. The book’s description is quoted below.'
        assert not about.startswith(('Resource referenced as', 'Background/reference material')), f'Needs an authored description: {url}'
        lines += [f'### E{i:03d}. {md(label)}', '', link('Open resource', url), '',
                  f'**About:** {md(about)}', '', f'**Book context:** {md(context_excerpt(o))}', '',
                  f'**Linked from:** {sources(occurrences)}', '']

    lines += ['## Book chapters and section references', '', f'{len(internal)} distinct destinations. These include heading permalinks and cross-chapter references.', '']
    for i, (url, occurrences) in enumerate(sorted(internal, key=order), 1):
        o = primary(occurrences)
        lines += [f'### B{i:03d}. {md(o["label"])}', '', link('Open original book location', url), '',
                  f'**About:** {md(internal_description(url, occurrences))}', '',
                  f'**Linked from:** {sources(occurrences)}', '']

    lines += ['## Navigation-only and footer destinations', '',
              f'{len(navigation)} destinations not already covered above. This completes the hyperlink inventory.', '']
    for i, (url, occurrences) in enumerate(sorted(navigation, key=order), 1):
        lines += [f'### N{i:03d}. {md(primary(occurrences)["label"])}', '', link('Open destination', url), '',
                  f'**About:** {md(internal_description(url, occurrences))}', '', f'**Linked from:** {sources(occurrences)}', '']
    (STUDY / 'links.md').write_text('\n'.join(lines), encoding='utf-8')

    idx = ['# Crafting Interpreters — chapter PDFs', '', 'Robert Nystrom', '',
           'Searchable, linked PDFs exported from the online edition. Original attribution and license links remain in the pages.', '',
           link('Original table of contents', BASE+'contents.html'), '',
           '[Annotated catalog of every hyperlink](../../study/crafting-interpreters/links.md)', '',
           '## Chapters', '']
    for p in pages:
        if p['kind'] == 'chapter':
            idx.append(f'- {link(str(p["number"])+". "+p["title"], p["pdf"])} — {p["pages"]} PDF pages · {link("online original",p["url"])}')
    idx += ['', '## Appendices and supplementary pages', '']
    for p in pages:
        if p['kind'] != 'chapter':
            idx.append(f'- {link(p["title"], p["pdf"])} — {p["pages"]} PDF pages · {link("online original",p["url"])}')
    idx += ['', 'See [README](README.md) for layout, link behavior, limitations, and reproduction instructions.', '']
    (ROOT / 'index.md').write_text('\n'.join(idx), encoding='utf-8')
    stats = dict(pdfs=len(pages), pdf_pages=sum(p['pages'] for p in pages),
        hyperlink_occurrences=sum(len(p['links']) for p in pages), unique_destinations=len(grouped),
        external_destinations=len(external), book_destinations=len(internal), navigation_destinations=len(navigation))
    (STUDY / 'catalog-stats.json').write_text(json.dumps(stats, indent=2)+'\n')
    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
