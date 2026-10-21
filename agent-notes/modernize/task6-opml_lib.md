# opml_lib Python 3.7 compatibility

## Goal

Restore the already-declared Python >=3.7 reader import contract without raising support targets or changing reader/writer APIs. Worker `/root/modernize_qfeed`; host thread ID not supplied.

## State

- Existing draft PR #1: https://github.com/accessibleapps/opml_lib/pull/1, originally published at 13392c5c8ccdedb4fadfe970667f733b447a848d. Fresh default remains 437f01b7e0e32cc533dbff03d4fb83b51fd23fa3. Actions enabled=true verified read-only; no settings changed.
- CI amendment is isolated in worktrees/opml-lib-ci, branch repair/task6-opml-lib-ci. Original feature/local tips remain separately archived as archive/task6-opml-ci-local and archive/task6-opml-ci-published. Original feature checkout and dirty canonical files/research data remain untouched.
- Smallest CI slice: one Linux workflow for the existing full pytest suite, configured Ruff/Pyright and Hatchling build on Python 3.7 and 3.13, six-line monthly Actions pin maintenance and this existing-note refresh. Original source/tests/manifest/lock remain unchanged; lock SHA256 942F321A354B1E605B7E90E3C73B7F0EB5B5F1013FAC0027B1512D9DDDC6F9D4.
- Python 3.7 exercises this PR's actual TypedDict/backport and fixture cleanup regressions; 3.13 checks the stdlib branch. Official setup-python provides 3.7.17 on Ubuntu 22.04; uv 0.8.8 has no managed 3.7 record. Locked sync retains existing public html_stripper Git revision cc3842c092e5f539f1bebee0da2971718155ad0d and all package records.
- Existing reader/writer/property tests use committed OPML fixtures and temporary local files. URLs are XML data, not network calls. No live service, credential-bearing collection, model call, dependency refresh or local full CI run.
- Authored YAML passed actionlint v1.7.12 and offline zizmor v1.31.1 with no findings; diff whitespace check and original source/test/manifest/lock comparison pass. Hosted final-head checks remain pending publication; historical local test results below are not new CI runs.

### Historical initial feature state

- Exact public `accessibleapps/opml_lib`, origin `git@github.com:accessibleapps/opml_lib.git`; fresh master/base `437f01b7e0e32cc533dbff03d4fb83b51fd23fa3`, archived=false, fork=false, paginated open PRs empty.
- Canonical tracked state clean; preserve unrelated `.coverage`, `html_stripper_bugs.md`, research project and existing hypothesis-bughunt branch. New `modernize/task6-opml_lib` worktree created directly inside writable task root at verified base after absent-path check.
- Read global instructions, repository inventory, pyproject/uv.lock, README API examples, reader/writer and all three test suites/real fixtures. No AGENTS/CLAUDE/task notes or hosted workflow tracked/found.
- Existing canonical topology does not include this library. Coordinator explicitly settled standalone exact-remote/module ownership for this named repository, without topology expansion, other-owner edits or consumer pin changes.
- No previous tracked full-test command/CI exists. Coordinator authorized existing full `uv run --locked --python <3.7path> python -m pytest -q tests` once, plus configured Ruff/Pyright using a supported tool runtime and focused reader checks on 3.7 and newer. No new workflow.

## Initial decisions and why (historical)

- `pyproject.toml` declares Python >=3.7; `opml_lib/reader.py:3` imports typing.TypedDict, introduced in Python 3.8. Actual installed CPython 3.7.9 x86 reproduces ImportError before existing reader contracts collect.
- Smallest fix: conditional stdlib/backport TypedDict import (~6 lines), declare typing-extensions runtime dependency only for Python<3.8 (one manifest line), let uv update only own dependency metadata/marker while retaining resolved versions. typing-extensions 4.7.1 already occurs transitively in locked 3.7 development graph. No major upgrade or dependency-source move.
- Existing `tests/test_reader.py` is the real regression; do not add duplicate assertions merely to create churn. Real fixtures/README reader API and QCast OPML caller establish producer/consumer.

## Historical initial regression evidence

- Interpreter: `C:/Users/Q/scoop/apps/python37/current/python.exe`, CPython 3.7.9 x86.
- Initial uv pytest console launcher failed SyntaxError Non-UTF-8 `\\xc0` before collection. This is launcher failure, not product evidence; coordinator approved equivalent `python -m pytest` invocation with same interpreter/environment.
- Actual red: `uv run --locked --python <exact interpreter above> python -m pytest -q tests/test_reader.py`; **1 collection error in 0.23s**, `ImportError: cannot import name TypedDict from typing` at reader.py:3. Production/manifest/lock unchanged at proof.

## Historical implementation and check history

Implemented conditional import and Python<3.8 backport declaration. uv lock delta exactly two own dependency/metadata lines; no versions or other packages changed. Focused reader on Python 3.7: **9 passed in 0.21s**.

First authorized full Python 3.7 run: **8 failed, 17 passed in 10.96s**. All failures are pre-existing property-test cleanup `Path.unlink(missing_ok=True)`, unavailable before Python 3.8. Coordinator settled this directly related supported-minimum fixture correction: remove only that keyword at eight sites, each after a guaranteed NamedTemporaryFile(delete=False) creation. No helper/catch or suppressed failures. Rerun changed property file then full minimum suite once after meaningful correction.

After cleanup: Python 3.7 property file **8 passed in 40.05s**; full supported-minimum suite **25 passed in 41.09s**. Python 3.10.11 focused reader **9 passed in 1.89s**. Ruff then reported only UP036 on new conditional because its configured target py38 contradicted declared >=3.7; align only Ruff target-version to py37, preserving minimum and avoiding suppressions. Pyright remains unrun until Ruff passes.

Reader source has committed CRLF, other touched files LF; preserve both. Default git diff --check treats new CRLF lines as trailing whitespace, so use cr-at-eol whitespace interpretation per command, without changing repository/global configuration or line endings.

Configured Ruff **passes** after minimum target correction. First Pyright/lock/whitespace result retrieval failed with exec-server transport error `process event reorder buffer exceeds 256 entries`. Approved read-only process inspection established no active task check, then coordinator authorized exactly one missing-result recovery with output captured in memory; no test rerun, process kill, restart or security change.

Recovered results: `uv lock --check` **exit 0**, 47 packages; command-local CRLF-aware whitespace check **exit 0**. Configured `uv run --locked --python cpython-3.10-windows-x86_64 python -m pyright` **exit 1**, 84,371 errors / 3,250 warnings, 105,918 output lines. Explicit Pyright excludes omit `.venv`; checker scans installed environment. Observed tail contains installed typing_extensions/activate_this.py errors and the reader's existing protected `_tree` warning. No green type-check claim, no automatic exclusion/suppression or third rerun. Report failed authority privately to coordinator for settlement; do not expand the slice silently.

Proposed PR title: Restore reader imports on supported Python 3.7.

Proposed body: Use the TypedDict backport only on Python 3.7 while retaining the standard-library type on newer interpreters. Declare the conditional runtime dependency, align Ruff's target with the supported minimum, and keep existing temporary-file cleanup compatible with Python 3.7. Exclude the local virtual environment from project type checking while retaining strict project diagnostics. Validation: all 25 tests pass on Python 3.7, all nine reader tests pass on Python 3.10, and Ruff, Pyright and lock validation pass.

Initial local implementation commit `f7345c7dfe22ab63de9d096edbc095dbb9cb8f16` kept this exact supported-minimum slice with failed Pyright authority recorded. Before publication, coordinator independently verified the existing exclude-list cause and authorized adding only `.venv` to it, retaining strict project diagnostics. Run only Pyright once after actual exclusion change; do not repeat successful tests or chase unrelated project diagnostics.

After only `.venv` exclusion: configured Pyright **exit 0**, **0 errors / 1 warning / 0 informations**. Remaining warning is existing reader `_tree` protected attribute access, unchanged by this patch. No successful tests repeated for this exclusion-only correction. `.venv` is the only new excluded path; strict project diagnostics remain enabled. Final locked run succeeds and graph diff remains two own conditional metadata lines.

Next: amend this worker's unpublished local implementation commit with final check-scope correction/note, return exact concrete patch for coordinator review before publication. Preserve canonical files and all support targets; no consumer pin updates.

## Next step

Return the feature-derived CI/config/note amendment and exact local head for coordinator review before publication. Final published head needs actual Claude review and green hosted checks before merge. Existing original evidence above is historical; the CI amendment does not change source/tests, support, lock or strict diagnostics. No local full CI, model call, merge, settings/description edit or release here; preserve original branches/worktrees/archive refs.
