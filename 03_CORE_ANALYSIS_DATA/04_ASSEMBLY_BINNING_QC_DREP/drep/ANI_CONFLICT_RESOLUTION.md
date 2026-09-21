# dRep ANI conflict resolution

## Recorded value

Final secondary ANI: 0.95 (95%), not 0.99 (99%). — PASS

The final MAG29 dRep primary output is institutional HPC run hq56_single_sample_drep_gtdbtk_18330. Its source SLURM command and dRep cluster_arguments.json both record dRep 3.6.2; 56 input genomes; -comp 90, -con 5, -l 50000; primary ANI -pa 0.9; secondary ANI -sa 0.95; -nc 0.1; and --S_algorithm fastANI.

Cdb.csv records a secondary clustering distance threshold of 0.05, equivalent to ANI 0.95. Wdb.csv records 29 winners. The dRep log says the run finished.

## Origin of the 99% conflict

An earlier 99% statement is not supported by the retained MAG29 dRep command or Cdb/Wdb output. The provenance status of that wording is `UNVERIFIABLE`. The recovered MAG29 dRep command and Cdb/Wdb files record 0.95.

No retained later dRep run at 99% links to the 29 representative files. The current bundle dRep parameter field is 0.95.
