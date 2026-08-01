# V494 systems-result claim card

Status: **validated closure and offline batching speedup; no accuracy-equivalence claim**  
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

V493 and V494 initially suggested a raw 3.19x ratio, but those were separate
single runs. V497 repeated sequential and batched execution five times on each
of 24 preserved contracts after warm-up on the same Wolffe A30 allocation. The
median paired per-contract speedup was **2.252x**, with a contract-cluster
bootstrap 95% interval of **[2.135x, 2.362x]**. Every one of 24 contract medians
favored batching (range 1.870x--2.856x; two-sided sign-test p=1.19e-7).

The measured median rates were 1.461 ms/shot batched and 3.435 ms/shot
sequential. These are offline CUDA-QX replay timings on one Wolffe A30 node,
not QPU wall-clock latency and not a demonstrated online feedback-loop deadline.
The captured environment is NVIDIA A30 (24,576 MiB), driver 595.71.05,
Python 3.12.3, NumPy 2.4.3, CUDA-Q QEC 0.6.0 at commit `84d18ca`, and
CUDA-Q 0.14.0 at commit `d845683`.

## Accuracy result

V494's paired logical gain was +1.302 percentage points with a 95% bootstrap
interval of [-2.279,+4.753] pp. V495's best tested operating point was +1.563 pp
with interval [-1.823,+4.948] pp. These intervals include zero.

This supports **no detected accuracy improvement** at the available sample
size. It does not establish equivalent or non-inferior accuracy. An equivalence
claim would require a preregistered clinically/scientifically meaningful margin
and a two-one-sided-test or confidence-interval analysis sized for that margin.

## Routing diagnosis before further decoder tuning

V497 shows that the escalation logic is configuration-sensitive. Pairwise route
decisions agree on only 66.0%--72.1% of shots (fast-set Jaccard 0.587--0.678).
The escalated group's raw-failure enrichment ranges from -2.149 to +4.579 pp,
and every bootstrap interval includes zero. Fast/escalated accuracy intervals
also all include zero. The router therefore does not consistently identify a
harder subgroup, and no new decoder candidate is authorized until a routing
score is calibrated on held-out data.

## Publication-safe wording

> A closure-gated batched Relay-BP/OSD cascade achieved exact syndrome closure
> on all 1,536 preserved real-IBM replay shots. In a same-node repeated offline
> benchmark, batching reduced CUDA-QX replay time by a median factor of 2.252
> (contract-cluster 95% interval 2.135--2.362). Logical-error-rate differences were
> statistically inconclusive, and no accuracy-equivalence or suppression-factor
> claim is made.

## Evidence required before promotion

1. Separate X/Z, distance, and backend accuracy tables remain attached; none
   support accuracy promotion.
2. V12 remains a separate Kingston contract unless a matched head-to-head
   replay is available; cross-experiment percentages must not be called a direct
   V12 comparison.
