# Phase 1 Design Notes

This repository contains the Phase 1 scaffold for ScamGraph AI.

Phase 1 is a baseline MVP with a FastAPI backend, SQLAlchemy-ready SQLite storage, a rule-based NLP and evidence layer, and a React TypeScript frontend dashboard for investigation inputs and result display.

The architecture intentionally separates NLP, ML, risk scoring, database, schema, tests, and frontend service flow so future phases can extend the system without rewriting the core pipeline.
