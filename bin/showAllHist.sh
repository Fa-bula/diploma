#!/bin/bash
ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )"/.. && pwd )"
BIN=$ROOT/bin
DATA=$ROOT/breast_canser_data/mutation_replication_time
for file in $DATA/*; do
    $BIN/showHistogram.py $file
done
