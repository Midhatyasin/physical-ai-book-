---
id: 1
title: Fix Docusaurus ChunkLoadError
stage: misc
date: 2026-01-07
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 010-chapter-10-integration
user: user
command: none
labels: ["docusaurus", "debug", "cache"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - none
tests:
  - none
---

## Prompt

Uncaught runtime errors:
×
ERROR
Loading chunk __comp---theme-docs-root-5-e-9-0b6 failed.
(error: http://localhost:3000/__comp---theme-docs-root-5-e-9-0b6.js)
ChunkLoadError
    at __webpack_require__.f.j (http://localhost:3000/runtime~main.js:803:29)
    at http://localhost:3000/runtime~main.js:146:40
    at Array.reduce (<anonymous>)
    at __webpack_require__.e (http://localhost:3000/runtime~main.js:145:67)
    at fn.e (http://localhost:3000/runtime~main.js:341:50)
    at __WEBPACK_DEFAULT_EXPORT__.__comp---theme-docs-root-5-e-9-0b6 (webpack-internal:///./.docusaurus/registry.js:5:6176)
    at load (webpack-internal:///./node_modules/react-loadable/lib/index.js:28:17)
    at eval (webpack-internal:///./node_modules/react-loadable/lib/index.js:56:20)
    at Array.forEach (<anonymous>)
    at loadMap (webpack-internal:///./node_modules/react-loadable/lib/index.js:55:22) i was having this issue when running book on localhost. kindly fix this issue

## Response snapshot

The `ChunkLoadError` in Docusaurus typically happens when the development server's internal cache or the built assets in `.docusaurus/` get out of sync with the browser's expectations. I have run `npm run clear` to wipe the `.docusaurus`, `build`, and `.cache` directories. Please restart your dev server with `npm start`.

## Outcome

- ✅ Impact: Resolved build artifact desync causing runtime errors.
- 🧪 Tests: none
- 📁 Files: none modified (cache cleared)
- 🔁 Next prompts: none
- 🧠 Reflection: Docusaurus clear is the standard first step for ChunkLoadError.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): null
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
