### 🔍 Evaluation Dimensions

| Dimension | `test_output_1.md` | `pandoc-test_output_1.md` |
| --- | --- | --- |
| Markdown Cleanliness | ✅ Very clean: no inline HTML, minimal escaping | ❌ Noisy: heavy HTML attributes, Pandoc-specific syntax |
| Section Structure | ✅ Headers, dividers (`---`), and metadata consistently used | ❌ Structure is diluted with mixed formatting |
| Link Handling | ✅ `[text](URL)` consistently used | ❌ Often appears as `[text](URL){...}` or inline `<a>` with attributes |
| Encoding and Escaping | ✅ UTF-8 compliant, no extraneous characters | ❌ Escaped backslashes `\\`, extra `{}` curly blocks |
| Layout for NLP | ✅ Easy to parse: each post cleanly block-delimited | ❌ Requires complex normalization (e.g. removing HTML spans, aria labels) |
| Repetition or Duplication | ✅ Duplicates only for post listings (expected) | ❌ Contains duplicated metadata and styling blocks |
| Footnote / Reference Handling | ✅ Pure Markdown | ❌ Embedded `<sup>` and annotated tags |
| Conversion Fidelity | ❌ Drops some rich formatting or annotations | ✅ Preserves visual styling closely from HTML |
| ML Readiness (0–5 scale) | **5/5** | **2/5** |