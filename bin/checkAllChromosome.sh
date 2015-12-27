#!/bin/bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
BIN=$ROOT/bin
DATA=$ROOT/breast_canser_data
for file in /home/bulat/diploma/genome/seq/*; do
    $BIN/checkChromosome.py $DATA/breast_canser_genom_subs_mutations.txt $file ${file:51}
done
