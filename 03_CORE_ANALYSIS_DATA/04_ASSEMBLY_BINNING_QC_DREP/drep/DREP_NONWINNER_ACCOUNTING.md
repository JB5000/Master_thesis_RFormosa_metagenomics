# Non-winner accounting for the 56-input final dRep run

Of 56 CheckM2-selected inputs, 29 are Wdb winners. The remaining 27 inputs split into:

- 9 genomes that passed dRep's internal CheckM filter and were non-winners in secondary clusters;
- 18 genomes that did not appear in Cdb/Wdb because dRep re-ran CheckM internally and did not retain them at its -comp 90 -con 5 filter.

Recorded accounting: 56 inputs = 29 Wdb winners + 9 Cdb non-winners + 18 inputs absent from Cdb/Wdb after the internal dRep CheckM step.
