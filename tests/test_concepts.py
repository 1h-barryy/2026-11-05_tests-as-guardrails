"""Unit tests for concepts.py, portable to the Problem-Solving Lab repo.

HW9: write the first test yourself before Codex adds the remaining tests.
This file intentionally contains no test functions or assertions yet.
"""

from concepts import candidate_terms, document_frequencies, match_label


# First test: document_frequencies should count a term once per document.
# Arrange: documents containing "signal and signal" and "signal".
# Act: call document_frequencies with those documents.
# Assert: compare the result with the hand-calculated expected dictionary.
# Write your own test_ function below. See README.md for the remaining plan.
