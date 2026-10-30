# CIOS LinkedIn Research Demo — Evidence Ledger

This demo is a presentation layer. It performs no scientific inference, graph mutation, training, threshold tuning, or competition submission.

## Baseline
- Visible train-copy adjusted edge Jaccard: 0.922257744071071
- Node recall: 0.9982
- Visible annotated divisions: TP=0, FP=0, FN=3
- Scope warning: train-copy / visible evidence, not embryo-independent generalization.

## AVG3 pseudo-gap diagnostics
- Formula: `v_AVG3(t) = (p_t - p_(t-3)) / 3`
- 36,641 pseudo-gap scenarios
- RAW_V1 Hit@1: 0.6841789252476733
- AVG3 Hit@1: 0.8475478289347999
- RAW_V1 MRR: 0.8025169631088711
- AVG3 MRR: 0.9111782449307692
- Boundary RAW Hit@1: 0.6883949054663396
- Boundary AVG3 Hit@1: 0.8519895577881497
- AVG3 rescue/harm vs raw: 7,287 / 1,301; net +5,986

These are continuation diagnostics, not hidden-test results.

## Independent final D comparison
- A baseline: 0.883068265992445
- D ownership-safe: 0.889646579924952
- Delta: +0.006578313932507
- All per-FOV safeguards: PASS
- A-selected edges removed in D: 0
- Target-parent swaps: 0

## Kaggle
Earlier baseline: public 0.868, private 0.860
Final D: public 0.870, private 0.863
Final candidate: `D_OWNERSHIP_SAFE_EXPANSION_v0.3.0`

## ATR
- midpoint geometry hits: 21/21 overall
- midpoint geometry hits: 7/7 A-unobserved hard subset
- detector support / gated success: 19/21 overall
- gated midpoint success: 5/7 hard subset
- predeclared performance gate: FAIL
- disposition: HOLD
- synthetic node insertion: NOT AUTHORIZED

## Known open limitations
- division reconstruction
- embryo-independent / out-of-fold validation
- candidate-edge coverage
- re-entry / identity continuity
- interaction between locally plausible links and global graph optimization
