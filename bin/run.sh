# Script to perform all needed calculations and wait for it finish
# Remove old .log files
rm ../logs/errors.log
rm ../logs/output.log
rm ../logs/exec_time

# Run program with specified destination of errors and output
clear
date > ../logs/exec_time	# Write start time at file
qsub -t 1-63 -cwd -S /usr/bin/python -e ../logs/errors.log -o ../logs/output.log calculate.py ../breast/mutations.txt ../breast/enrichment

# Wait for qsub exit and then show output.log and errors.log
OUTPUT="$(qstat)"
while [ -n "$OUTPUT" ]; do
    sleep 5 # Wait 5 sec and then check if calculations finished
    OUTPUT="$(qstat)"
done
echo "Calculations has been finished!"
date >> ../logs/exec_time	# Append end time to file
less -e ../logs/errors.log ../logs/output.log 
