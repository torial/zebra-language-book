// Zebra syntax highlighting for mdBook.
//
// mdBook bundles highlight.js (10.x) with a fixed set of languages, so
// ```zebra fences would otherwise render as plain text. This file registers a
// small "zebra" grammar and then re-highlights the zebra blocks, because
// book.js has already run hljs over the page by the time additional-js loads.
//
// Loaded via `additional-js` in book.toml.
(function () {
    if (typeof hljs === "undefined" || !hljs.registerLanguage) { return; }

    function zebra(hljs) {
        var KEYWORDS = {
            keyword:
                "def cue class interface struct union mixin adds implements extend " +
                "var const let static private pub sig lambda " +
                "if elif else while for in branch on match is as pass " +
                "return break continue yield " +
                "try catch raise defer spawn " +
                "require ensure invariant assert test " +
                "use import from namespace module extern out " +
                "and or not new",
            literal: "true false nil this self",
            built_in:
                "int float bool str char void List HashMap Set Result " +
                "print println File Console Math"
        };
        var STRING = {
            className: "string",
            variants: [
                { begin: '"""', end: '"""' },
                { begin: '"', end: '"', illegal: "\\n", contains: [hljs.BACKSLASH_ESCAPE, { className: "subst", begin: "\\$\\{", end: "\\}" }] },
                { begin: "'", end: "'", illegal: "\\n", contains: [hljs.BACKSLASH_ESCAPE] }
            ]
        };
        var NUMBER = { className: "number", variants: [{ begin: "\\b0[xX][0-9a-fA-F_]+" }, { begin: "\\b\\d[\\d_]*(\\.\\d[\\d_]*)?([eE][+-]?\\d+)?" }] };
        var ATTRIBUTE = { className: "meta", begin: "@[A-Za-z_][A-Za-z0-9_]*" };
        var TYPE = { className: "type", begin: "\\b[A-Z][A-Za-z0-9_]*\\b", relevance: 0 };
        var FUNCTION = {
            className: "function",
            beginKeywords: "def cue", end: /\(|$/, excludeEnd: true,
            contains: [hljs.inherit(hljs.TITLE_MODE, { begin: "[A-Za-z_][A-Za-z0-9_]*" })]
        };
        var CLASS = {
            className: "class",
            beginKeywords: "class interface struct union mixin namespace", end: /$/,
            keywords: "class interface struct union mixin namespace implements adds",
            contains: [hljs.inherit(hljs.TITLE_MODE, { begin: "[A-Za-z_][A-Za-z0-9_]*" })]
        };
        return {
            name: "Zebra",
            aliases: ["zbr"],
            keywords: KEYWORDS,
            contains: [hljs.HASH_COMMENT_MODE, STRING, NUMBER, ATTRIBUTE, FUNCTION, CLASS, TYPE]
        };
    }

    hljs.registerLanguage("zebra", zebra);

    var blocks = document.querySelectorAll("code.language-zebra, code.language-zbr");
    Array.prototype.forEach.call(blocks, function (block) {
        // Reset anything the first pass left behind, then highlight for real.
        block.classList.remove("hljs");
        if (block.dataset) { delete block.dataset.highlighted; }
        hljs.highlightBlock(block);
        block.classList.add("hljs");
    });
})();
