# Validation Report — 2026-07-23 Sam News batch

**Verdict: PASS**

Validated as fresh-context verifier (did not author analyses). Timestamp of check: 2026-07-23.

## Counts

| Check | Expected | Actual | Result |
|-------|----------|--------|--------|
| Raw articles (`/workspace/data/raw/2026-07-23/*.md`, exclude `._*`, `*_Analysis.md`) | 18 | 18 | PASS |
| Analysis files (`*_Analysis.md`) | 18 | 18 | PASS |
| Raw ↔ analysis ID pairing | 1:1 | 18/18 match | PASS |
| CSV `2026-07-23_articles_yaml.csv` data rows | 18 | 18 | PASS |
| Briefing `/workspace/briefings/2026-07-23.md` | if present: §0–4, table=18, no paths | **absent** | N/A (skipped) |

## Per-analysis mechanical checks (18/18)

For every `*_Analysis.md`:

- Size ≥ 1024 bytes: **PASS** (range 13,127–23,874 bytes)
- Exactly one YAML frontmatter (opening `---` … closing `---` at file start): **PASS**
  - Note: each file also uses `---` as horizontal rules between Phase sections (typically 11 extra `---` lines). These are markdown HRs, not additional YAML frontmatter blocks.
- Phase headings 0–10 each appear exactly once (canonical Chinese titles as specified): **PASS**
- `## Analysis Framework (Structured Data)` present with fenced YAML containing: `summary`, `key_entities`, `trend_signals`, `market_impact`, `monitoring_triggers`, `action_required`, `urgency`, `tags`: **PASS**

## Soft caps

| Cap | Violations |
|-----|------------|
| `key_entities` ≤ 8 | 0 |
| `trend_signals` ≤ 3 | 0 |
| `monitoring_triggers` ≤ 3 | 0 |
| `tags` ≤ 8 | 0 |
| `market_impact.sectors` ≤ 3 | 0 |

No soft-cap violations reported.

## Spot-check grounding (3 analyses)

| File | Result | Notes |
|------|--------|-------|
| `20260723_FT_001` | PASS | Entities (De Gucht, EU/Commission, China, von der Leyen, WTO, Huawei, Sánchez) and figures (€104bn / €360bn) match raw FT piece. |
| `20260723_SCMP_002` | PASS | Compute targets (50k / 130k / 22k / 82k petaflops), RISC-V, token economy grounded; “United States” corresponds to raw “US”. |
| `20260723_UNK_005` | PASS | WAIC scale figures (1,117 / 4,486 / 351), AI Proem, Rachel, Geek+, StepFun, ViTai, Ant Group grounded; `習近平` is the Chinese form of raw “Xi Jinping” (not invented). |

No obvious invention of orgs/numbers detected in spot-checks.

## Briefing

`/workspace/briefings/2026-07-23.md` did not exist at validation time → section-4 table / path / §0–4 checks **not applicable**.

## Fixes applied

None. No clear mechanical defects (missing/typo phase headings, empty framework) found.

## Summary

**PASS** — 18 raw, 18 analyses, 18 CSV rows; all structural and framework checks green; soft caps clean; 3/3 spot-checks grounded; briefing N/A.


## Briefing re-check (post-write)
- File: `briefings/2026-07-23.md`
- Bytes: 29607
- §4 rows: 18 (expect 18)
- Sections 0–4: True
- Path leaks: False
- Result: PASS
