# Admission KB Project

Pipeline skeleton for parsing admission DOCX files into a normalized knowledge base.

## Overview
- Goal: turn unstructured admission documents into structured KB artifacts for downstream use.
- Pipeline: parse DOCX → extract entities/relations → assemble KB JSON (or other stores).
- Status: scripts are stubs; fill in logic as you grow the pipeline.

## Repository Layout
```
admission_kb_project/
├── data/
│   ├── raw_docs/          # place source .docx files here
│   └── extracted/         # parsed text/JSON produced by parse_docx.py
├── scripts/
│   ├── parse_docx.py      # step 1: DOCX → structured text/JSON
│   ├── extract_entities.py# step 2: text → entities/relations
│   └── build_kb.py        # step 3: aggregate into normalized KB outputs
├── kb/
│   ├── programs.json
│   ├── admission_methods.json
│   ├── requirements.json
│   └── relations.json
└── README.md
```

## Pipeline Steps
1) **Parse DOCX** (`scripts/parse_docx.py`)
   - Read all `.docx` in `data/raw_docs/`.
   - Emit cleaned text and/or structured blocks to `data/extracted/`.

2) **Extract Entities** (`scripts/extract_entities.py`)
   - Transform parsed outputs into entities and relations (IDs, names, scores, methods, etc.).
   - Save intermediate artifacts in `data/extracted/`.

3) **Build KB** (`scripts/build_kb.py`)
   - Normalize and merge entities into final KB artifacts under `kb/`.
   - Extend to emit other targets (SQLite/graph) as needed.

## Quickstart (once implemented)
- Add DOCX files to `data/raw_docs/`.
- Run `python scripts/parse_docx.py` to parse.
- Run `python scripts/extract_entities.py` to extract structured data.
- Run `python scripts/build_kb.py` to refresh `kb/*.json`.

## Notes for Implementers
- Keep intermediate outputs deterministic (use stable ordering for lists/keys).
- Start simple: regex/keyword rules, then iterate with more robust NLP as needed.
- Version your KB outputs if you plan to track changes across document updates.
