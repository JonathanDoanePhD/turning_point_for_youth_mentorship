# The Turning Point Project

**When, how, and for whom do supportive relationships and developmental experiences shape young
people's future trajectories?**

A research program, with analysis plans frozen locally before data access (not externally preregistered), on the developmental timing of supportive adult
relationships and educational attainment. Principal investigator: Jonathan Doane, Ph.D.
([research portfolio](https://jonathandoanephd.github.io/research-portfolio/)).

**Website:** https://jonathandoanephd.github.io/turning_point_for_youth_mentorship/ (built from `website/` by
`.github/workflows/pages.yml`).

> **Status (2026-11-13): working paper v4, approved by the author.** Nine observational analyses in six U.S. cohorts. Not peer reviewed.
>
> - **Paper:** `manuscripts/working_paper_v4.md`.
> - **Results:** `outputs/primary_estimands.csv` (estimates) and `docs/results_*.md`.
> - **Audit:** `docs/independent_review_response.md`. It was accepted, the survey estimates were reproduced in R (`crosscheck/`), and a
>   second analyst confirmed the results.
>
> In brief:
> - Reported support from parents, and from grade-11 math teachers, was modestly associated with later education.
> - No comparison across ages, grades or mentor start ages was statistically significant.
> - Within families (a sibling comparison), praise at ages 6–9 and 10–14 carried the same weight.
> - Cumulative effects are not demonstrated, and these data cannot show that timing is irrelevant. All results are observational
>   associations.

## What is here

| Area | Contents |
|---|---|
| Literature | `docs/literature_review.md` (abstract-level critical review), `docs/evidence_matrix.csv` (87 works), `docs/references.bib`, `docs/citation_verification_log.jsonl` (Crossref record for every DOI), `docs/references_unverified.md` |
| Data feasibility | `docs/dataset_audit.md` (NLSY97, Add Health, HSLS:09, ELS:2002), `docs/dataset_audit_early_childhood.md` (PSID-CDS/TAS, NLSY79 CYA, FFCWS, ECLS-K, ECLS-K:2011, SECCYD, UK cohorts), comparison CSVs, `docs/variable_dictionary*.{md,csv}` (150 documented variables), `config/datasets.yaml` |
| Design | `docs/research_questions.md`, `docs/conceptual_framework.md`, `docs/causal_framework.md` + `causal_dag.dot`, `docs/statistical_analysis_plan.md`, `docs/preregistration_draft.md`, `docs/ethics_and_limitations.md`, `docs/research_decision_log.md` |
| Code | `src/turning_point/`: ingestion with provenance manifests, validation (ranges, identifiers, microdata-in-git guard), missing-code recoding that keeps reasons, scale scoring/reliability, survey-weighted GLMs (Taylor linearization and replicate weights), restricted cubic splines, age-moderation models, equivalence tests, Rubin pooling, Holm/BH, E-values, life-course structured-approach model comparison, guarded change-point estimation, grouped CV and subgroup calibration, provenance-stamped Plotly figures, CLI |
| Tests | `tests/`: 48 tests incl. agreement with statsmodels' cluster-robust variance, a Monte Carlo bias/coverage check of the primary estimator, life-course model recovery, and site/citation integrity |
| Website | `website/`: dependency-free static site, published to GitHub Pages by `.github/workflows/pages.yml` via `scripts/build_pages.py`; generated data in `website/data/site.js` and `website/data/findings.js` |
| Planning | `scripts/power_age_interaction.py` → `outputs/design_power_age_interaction.csv` (assumed inputs, not data) |

## Key decisions (details in `docs/research_decision_log.md`)

- **Plans:** frozen locally as hashed commits before each dataset was opened (`docs/PLAN_FREEZE*.md`). They are not external
  preregistrations.
- **Data restrictions:** Add Health, PSID and Future of Families restrict AI processing of their data. Their analyses (Studies 5–7 and 9)
  were planned from documentation, run by the author outside AI tools, and are reported qualitatively only.
- **Origin of the project:** it began inside another repository (`ai-incident-atlas`) and was moved here, with its full history, on
  2026-11-13 (D-050).

## Setup and reproduction

```bash
cd turning-point-project
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,stata]"
```

```bash
pytest                                   # 38 tests, synthetic data only
```

```bash
python scripts/power_age_interaction.py --simulate
```

```bash
python scripts/build_site_data.py        # regenerate website/data/site.js from docs/
python -m http.server 8000               # then open http://localhost:8000/website/
```

```bash
tpp paths                                # resolved data/output folders
tpp check-repo                           # fails if any microdata are tracked by git
tpp validate nlsy97 data/raw/nlsy97/extract.csv   # after filling config/mappings/nlsy97.yaml
```

Data paths come from `TPP_DATA_DIR`, then `config/local.yaml` (copy `config/paths.example.yaml`),
then `data/`. Microdata never enter git (`.gitignore`, `tpp check-repo`, and a unit test).

## Reproduce paper 1

```bash
# download https://nlsinfo.org/cohort-data/nlsy97_all_1997-2023.zip, then stream the 24 mapped
# columns into data/raw/nlsy97/paper1_extract.csv (see docs/results_paper1.md, Verification)
python scripts/run_paper1.py --m 40          # ~10 min; writes outputs/paper1_results.json
python scripts/report_paper1.py              # figures + website/data/findings.js
python scripts/crosscheck_variance.py        # jackknife check of standard errors
python scripts/render_manuscript.py manuscripts/working_paper_v1.src.md manuscripts/working_paper_v1.md
python scripts/run_b2_hsls.py --m 20          # study B2 (HSLS:09 extract in data/raw/hsls09/)
python scripts/extract_nls.py <cya zip> nlscya_all_1979-2020.csv config/mappings/nlsy79cya_spec.json cya data/raw/nlsy79cya/cya_extract.csv
python scripts/extract_nls.py <nlsy79 zip> nlsy79_all_1979-2022.csv config/mappings/nlsy79cya_spec.json n79 data/raw/nlsy79cya/n79_extract.csv
python scripts/run_p2_cya.py --m 20           # paper 2
python scripts/run_p1e_accumulation.py        # NLSY97 accumulation addendum
python scripts/render_manuscript.py manuscripts/working_paper_v2.src.md manuscripts/working_paper_v2.md
```

## Open items

Prepared and waiting on someone else (see `docs/human_run_checklist.md`):

| Item | What is ready | Who acts |
|---|---|---|
| A3 Add Health: age a mentor became important | plan, script, checklist | human analyst, outside AI tools |
| R1 PSID: closeness at 8–11 vs 12–15 (mother, teachers, other adults) | plan, script | human analyst, outside AI tools |
| R2 FFCWS: closeness at 9 vs 15 | plan, script | human analyst (or Claude, with ICPSR's written permission) |
| Paper 1 S6b: NLS custom weights | ID list `data/processed/nlsy97_s6b_ids.txt`, script `scripts/run_paper1_s6b.py` | PI downloads weights at nlsinfo.org/weights/nlsy97; Claude runs |
| Closed articles (Fruiht & Wray-Lake 2013, Christensen et al. 2020, and others) | `docs/article_retrieval_protocol.md`, extraction form, email template | PI obtains legal copies; Claude extracts |

## License and citation

Code: MIT (`LICENSE`). Cite via `CITATION.cff`. Survey data are © their stewards and are not redistributed.
