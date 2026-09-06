# R10A1 local source validation

R10A1 source validation is repo-local and does not require GitHub Actions, a GitHub-hosted runner, or any paid external service.

From a full local checkout at the exact R10A1 receipt-review head, run:

```bash
python tools/validate_r10a1.py
```

The validator uses only Python's standard library and the local `git` executable. It performs the same source/static checks previously embedded in `.github/workflows/r10a1-validation.yml`: exact R10A0 ancestry, predecessor immutability, required frozen cases and owner terms, native-size and manifest pins, Git-blob cross-binding, candidate-core hashing, test-first introduction order, and the one-parent pre-receipt publication binding.

A PASS proves only the source/static contract. It does not establish installation, provider activation, runtime behavioral qualification, BugOps closure, or merge authority.
