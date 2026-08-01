# Controlled QEC experiments

This directory contains sanitized experiment code and analysis only. Raw
shot-level contracts remain in the private QEC experiment archive.

## V497 routing and latency

- Replays the unchanged Relay-BP/OSD operating points on 1,536 preserved real
  IBM shots.
- Enforces `H e = s` for every final correction.
- Stores route masks privately and publishes aggregate X/Z, distance, backend,
  routing-stability, and repeated timing results.
- Validated systems result: median 2.252x offline A30 batching speedup, cluster
  bootstrap 95% interval [2.135x,2.362x].
- No accuracy or V12 head-to-head claim.

## V498 multi-seed consensus

- Tests whether Relay seed unanimity repairs the unstable route decision.
- Rejected: 2.865% fast-path coverage, 5.797 ms/shot, and 23.633% all-valid
  logical disagreement across seeds.
- Retained as a negative routing result; every required accuracy interval
  includes zero.

