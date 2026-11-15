# Tests as Guardrails

A pytest learning project built around real data-processing functions from
[Problem-Solving Lab](https://github.com/1h-barryy/2026-10-26_problem-solving-lab).
The focus is counting accuracy, scoring and ranking, filtering, and classification
boundaries: practices relevant to Data Analysis and Quantitative Analysis.

## Current status and HW9

The source module and pytest setup are ready. **No tests have been implemented.**
HW9 requires me to write the first test myself before Codex implements the rest.
`tests/test_concepts.py` contains only imports and guidance for that first test.

## Repository layout

```text
concepts.py              Unchanged snapshot of the original logic
UPSTREAM.txt             Source repository, commit, and file hash
tests/
    README.md            Setup, test plan, and transfer instructions
    pytest.ini           Collect this folder; import concepts.py from its parent
    requirements-dev.txt Pytest dependency
    test_concepts.py      Portable test file; first test still to be written
.gitignore               Excludes virtual environments and Python/pytest caches
```

`concepts.py` uses only Python's standard library. These unit tests need no
Streamlit, ChromaDB, API keys, network access, or application startup. Installing
pytest initially requires access to a package index unless it is already cached.
Do not install the original app's full requirements just to run this suite.

The local source is a snapshot, not a live connection to the original project.
Tests here check that snapshot; tests copied into the original repo check its
current `concepts.py`.

## Setup and run (PowerShell)

Run commands from this repository's root. This workspace already has a `.venv`
with pytest installed, so you can skip setup and run the collection command.
For a fresh checkout, use Python 3.10 or newer:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r tests/requirements-dev.txt
```

If your Python command is `python` instead of `py`, use `python -m venv .venv`.
If neither is on PATH but you use uv, create the environment with `uv venv --seed .venv`.
Environment activation is optional because the commands use its interpreter directly.

Check discovery without running tests:

```powershell
.\.venv\Scripts\python.exe -m pytest -c tests/pytest.ini --collect-only -q
```

Run the suite after writing your first test:

```powershell
.\.venv\Scripts\python.exe -m pytest -c tests/pytest.ini -q
```

Run just this file, or select tests by a word in their names:

```powershell
.\.venv\Scripts\python.exe -m pytest -c tests/pytest.ini tests/test_concepts.py -v
.\.venv\Scripts\python.exe -m pytest -c tests/pytest.ini -k document_frequencies -v
```

Until the first test is written, `no tests collected` and pytest exit code 5 are
expected. This is not a passing suite. Once tests exist, exit code 0 means they
passed; exit code 1 means at least one failed.

## Writing my first test

Open `tests/test_concepts.py`. Pytest discovers functions whose names begin with
`test_` in files named `test_*.py`. Use this sequence:

1. Arrange a small input with an expected result you can calculate by hand.
2. Act by calling the function directly.
3. Assert that the actual result equals the expected result.

Suggested first case: pass `["signal and signal", "signal"]` to
`document_frequencies()`. The expected dictionary is `{"signal": 2}`. Repeating
a term within one document must not inflate its document frequency. The stopword
`and` prevents additional phrases in this example.

Use ordinary `assert` statements for dictionaries, labels, order, and IDs. Use
`pytest.approx` for floating-point scores. Keep inputs small and fixed; avoid
random data, live documents, database fixtures, and external calls. Expected
values should be independently calculated rather than produced by the same
function being tested.

## Function behavior and proposed cases

`document_frequencies(documents)` counts distinct eligible one-, two-, and
three-word n-grams per document. It lowercases text and excludes stopwords,
pure-number tokens, and tokens of length two or less. It does not stem terms.
Check dictionary contents without relying on insertion order, since n-grams
are generated as sets.

`candidate_terms(query, hits, df, corpus_size, top=6, min_docs=2)` accepts hit
dictionaries with `id` and `document` fields. Each result has `term`, `score`, and
`paper_ids`. Its score is:

```text
number of matching hits × natural_log(corpus_size / max(document_frequency, 1))
```

A missing document frequency defaults to 1. Candidates are sorted by descending
score, then alphabetically by term. Query-word matches use crude plural folding.
A candidate contained on word boundaries in an already-selected term is skipped.
This means phrase suppression depends on selection order; it does not always
prefer longer phrases. Paper IDs follow input hit order.

`match_label(distance)` classifies lower distances as stronger matches:

| Distance | Label |
|---|---|
| Below 0.60 | `strong` |
| 0.60 through 0.70, inclusive | `moderate` |
| Above 0.70 | `weak` |

Planned coverage (not yet implemented):

| Function | Case | Expected behavior |
|---|---|---|
| `document_frequencies` | Empty document list | Empty dictionary |
| `document_frequencies` | Repeated term in one document and another document | Count each document once |
| `document_frequencies` | `collective motion`, `motion`, and an empty document | `collective`: 1, `collective motion`: 1, `motion`: 2 |
| `document_frequencies` | `THE and 123 ab` | No eligible terms |
| `candidate_terms` | Empty hits | Empty list |
| `candidate_terms` | Two hits containing `alpha and beta`, corpus size 4, frequencies 2 and 4 | `alpha` scores `2 × log(2)` and ranks above zero-score `beta` |
| `candidate_terms` | Equal-score `alpha` and `beta` | Alphabetical tie-breaking |
| `candidate_terms` | One versus exactly two matching hits | Default `min_docs=2` excludes one and includes two |
| `candidate_terms` | Query `groups` with candidates containing `group` | Exclude the matching word and phrases containing it |
| `candidate_terms` | Phrase `collective motion` scores above its component words | Select phrase and suppress the component words |
| `candidate_terms` | `top=1` | Only the highest-ranked eligible term, with correct IDs |
| `match_label` | Immediately below, exactly at, and immediately above 0.60 | Strong, moderate, moderate |
| `match_label` | Immediately below, exactly at, and immediately above 0.70 | Moderate, moderate, weak |

Use `math.nextafter` to obtain adjacent floating-point values around a threshold.

Known behaviors to discuss before treating them as requirements: duplicate hit
IDs count multiple times, and `top=0` can still return one candidate. The function
does not validate all inputs; for example, scoring with a nonpositive corpus
size can raise a math-domain error. No production behavior has been changed here.

## Copy the suite into Problem-Solving Lab

Keep the same layout in the destination repository:

```text
2026-10-26_problem-solving-lab/
    concepts.py          Existing production module: keep this version
    tests/
        README.md
        pytest.ini
        requirements-dev.txt
        test_concepts.py
```

1. Write your first test here and run it. Add the remaining tests only after that
   HW9 step is complete.
2. Copy this entire `tests/` folder into the original project's root, beside
   `concepts.py`. All test code, configuration, dependencies, and instructions
   travel together. If a `tests/` folder already exists, merge without replacing
   unrelated files and review any same-name conflicts.
3. Use the explicit `-c tests/pytest.ini` command below to select this suite's
   configuration independently of any existing project configuration. It collects
   this folder and imports from its parent, excluding root-level app smoke tests.
   No destination root config or dependency file needs to be changed. If the
   destination already has tests in this folder, they will also be collected;
   specify `tests/test_concepts.py` to run only this file.
4. Keep the original project's `concepts.py`. Do not copy this snapshot over it.
   Do not copy `.venv`, caches, or `UPSTREAM.txt`; create or reuse an environment
   in the destination and install pytest there.
5. From the original project's root, run the setup commands above if needed,
   then run the copied file explicitly:

   ```powershell
   .\.venv\Scripts\python.exe -m pip install -r tests/requirements-dev.txt
   .\.venv\Scripts\python.exe -m pytest -c tests/pytest.ini tests/test_concepts.py -v
   ```

The parent folder must contain the production `concepts.py`; it intentionally
does not live inside the test bundle. The relative `pythonpath = ..` setting is
resolved from `tests/pytest.ini`, so it works in either repository. Use the
explicit config command above from the project root; a bare root-level `pytest`
command may not discover a nested config. Copy source files only, omitting any
generated `__pycache__` or `.pytest_cache` folders.

No `conftest.py`, mocks, or path-editing code are needed for this layout. If the
copied tests fail against newer source, inspect whether the behavior changed or
the test's expectation is wrong before changing either one.
