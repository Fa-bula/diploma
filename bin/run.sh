# Script to perform all needed calculations and wait for it finish
# Remove old .log files
rm ../logs/*
# motifs = ../
# Run program with specified destination of errors and output
clear
date > ../logs/exec_time	# Write start time at file

test `tail -c 1 ../sorted_motifs` && { echo "Error: ../sorted_motifs should end with newline"; exit 1; }
a=$((`wc -l ../sorted_motifs | awk '{print $1;}'`-1)) # Number of motifs in file

qsub -t 1-${a} -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment
# Wait for qsub exit and then show output.log and errors.log
OUTPUT="$(qstat)"
while [ -n "$OUTPUT" ]; do
    sleep 5 # Wait 5 sec and then check if calculations finished
    OUTPUT="$(qstat)"
done
echo "Calculations, job has been finished!"
date >> ../logs/exec_time	# Append end time to file
cat ../logs/exec_time
