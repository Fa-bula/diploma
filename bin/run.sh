#!/bin/bash
# Script to perform all needed calculations and wait for it finish

ROOT=../lusc/			# Dir with raw_mutations.txt and enrichment.txt
LOGS=$ROOT/logs/		# qsub .log files directory
RESULTS=$ROOT/results/		# Dir used to store interim results
PLOTS=$ROOT/plots/		# Dir for final plots
FREQ=$RESULTS/*/mutation_frequency/

# rm $LOGS/*			# Remove old .log files
clear				# Clear terminal screen
date > $LOGS/exec_time	# Write start time at file

# Python part

# Filtering exome samples
# qsub -sync y -cwd -S /usr/bin/python -e $LOGS -o $LOGS filter.py $ROOT/raw_mutations.txt $ROOT/catalog.txt $ROOT/filtered_mutations.txt

# TODO: Usage of check.py

# Transform .wig to .csv
# qsub -sync y -cwd -S /usr/bin/python -e $LOGS -o $LOGS replication.py $ROOT/rep_time.wig $ROOT/rep_time.csv

# Perform all remaining computations for every mutation signature pair

# for i in {1..96..16}
# do
#     qsub -t $i-$((i + 15)) -sync y -cwd -S /usr/bin/python -e $LOGS -o $LOGS calculate.py $ROOT/filtered_mutations.txt $ROOT/enrichment.txt $ROOT/replicationTiming $RESULTS
# done

for i in {1..96..8}
do
    qsub -t $i-$((i + 7)) -sync y -cwd -S /usr/bin/python -e $LOGS -o $LOGS calculate.py $ROOT/filtered_mutations.txt $ROOT/enrichment.txt $ROOT/replicationTiming $RESULTS
done

# R part
# for dir in $FREQ; do
#     qsub -cwd -S /usr/bin/Rscript -e $LOGS -o $LOGS linearModel.R $dir $ROOT/enrichment.txt $PLOTS $(basename $(dirname $dir))
# done

echo "Calculations, job has been finished!"
date >> $LOGS/exec_time		# Append end time to file
cat $LOGS/exec_time		# Show running start and end times
