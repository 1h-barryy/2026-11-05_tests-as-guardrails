# Tests as Guardrails

A pytest learning project using data-processing logic from
[Problem-Solving Lab](https://github.com/1h-barryy/2026-10-26_problem-solving-lab).

All test files, pytest configuration, development dependencies, and detailed
instructions are bundled in [`tests/`](tests/README.md). Copy that folder directly
into the original project's root, beside its existing `concepts.py`.

## Run from the project root

Use an existing `.venv`, or create one with `py -m venv .venv`, then:

```powershell
.\.venv\Scripts\python.exe -m pip install -r tests/requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -c tests/pytest.ini -q
```

The current workspace already has pytest installed. No tests have been written:
HW9 requires me to write the first test in `tests/test_concepts.py` myself.
Until then, pytest reports no tests collected (exit code 5), not a passing suite.

See [the test guide](tests/README.md) for setup alternatives, function behavior,
the proposed test cases, and transfer instructions.

The root `concepts.py` is an unchanged upstream snapshot with its provenance in
`UPSTREAM.txt`. When transferring `tests/`, keep the destination project's own
`concepts.py` so the suite tests its actual production code.
