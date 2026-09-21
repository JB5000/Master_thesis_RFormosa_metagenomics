#!/usr/bin/env bash
dRep dereplicate "<drep_output_dir>" -g "<56_input_genomes>" -p <cpus> -comp 90 -con 5 -l 50000 -pa 0.9 -sa 0.95 -nc 0.1 --S_algorithm fastANI

