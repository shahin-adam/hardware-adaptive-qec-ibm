# V494 systems-result claim card

Status: **validated closure; provisional latency comparison; no accuracy-equivalence claim**  
Date: 1 August 2026

## Claim that is already supported

On 1,536 preserved real-IBM replay shots from Fez and Marrakesh, the corrected
Relay-BP/OSD cascade returned corrections satisfying the exact algebraic
contract `H e = s` on **100% of shots**. This establishes that the earlier
syndrome/correction convention defect has been repaired for this replay set.

The scope is deliberately narrow: algebraic closure does not itself establish
logical improvement, online end-to-end latency, cross-chip transfer, or a
fault-tolerance threshold.

## Provisional systems-performance result

V493 measured 4.4509 ms/shot for a per-shot sequential cascade. V494 measured
1.3940 ms/shot after batching the Relay pass and OSD fallback, a raw ratio of
**3.19x** on the same 1,536-shot contract family. This is a strong systems lead,
but the historical measurements were separate single runs. V497 therefore
repeats sequential and batched paths after warm-up on the same GPU allocation.
The paper will report medians, dispersion, and paired per-contract ratios from
V497 rather than treating 3.19x as finalized.

## Accuracy result

V494's paired logical gain was +1.302 percentage points with a 95% bootstrap
interval of [-2.279,+4.753] pp. V495's best tested operating point was +1.563 pp
with interval [-1.823,+4.948] pp. These intervals include zero.

This supports **no detected accuracy improvement** at the available sample
size. It does not establish equivalent or non-inferior accuracy. An equivalence
claim would require a preregistered clinically/scientifically meaningful margin
and a two-one-sided-test or confidence-interval analysis sized for that margin.

## Routing diagnosis before further decoder tuning

Aggregate V495 results suggest the escalated subgroup sometimes contains more
of the apparent gain than the fast path, but its intervals remain wide and the
route masks were not retained in the first result format. V497 freezes the four
existing operating points, stores per-shot route masks, measures difficulty
enrichment and route stability, and computes only diagnostic—not promotable—
oracle ceilings. No V496/new decoder candidate is authorized until this audit
shows whether routing rather than correction quality is the limiting component.

## Publication-safe wording

> A closure-gated batched Relay-BP/OSD cascade achieved exact syndrome closure
> on all 1,536 preserved real-IBM replay shots. Batching substantially reduced
> decoder wall time in the initial measurement; a same-node repeated benchmark
> is used for the finalized speed ratio. Logical-error-rate differences were
> statistically inconclusive, and no accuracy-equivalence or suppression-factor
> claim is made.

## Evidence required before promotion

1. V497: 100% closure in every repeat and contract.
2. V497: warm-cache sequential/batched distributions and paired ratios.
3. Hardware/software/node metadata sufficient to reproduce the timing context.
4. Separate X/Z, distance, and backend tables; no pooled-only promotion.
5. V12 remains a separate Kingston contract unless a matched head-to-head
   replay is available; cross-experiment percentages must not be called a direct
   V12 comparison.

