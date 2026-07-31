# V421 cross-block basis/round guard

IBM-only diagnostic replay of the V420 exact-transpiled router on two Kingston blocks. Wolffe job 64816 reproduced the local metrics exactly.

| Block | Guard gain vs selected MWPM base |
|---|---:|
| Fresh | +0.162500 pp |
| Later | +0.164583 pp |

Leave-one-block-out policy transfer was +0.052083 pp (fresh-trained policy on later) and +0.155208 pp (later-trained policy on fresh). This is not a promotion: the retrospective intersection is not independent, only two blocks are available, and seven-round slices are not universally improved. V12/selected MWPM remains the safety fallback. No cross-vendor claim.
