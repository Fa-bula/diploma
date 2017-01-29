# Remove old .log files
rm ../logs/errors.log
rm ../logs/output.log

# Run program with specified destination of errors and output
qsub -cwd -S /usr/bin/python -e ../logs/errors.log -o ../logs/output.log calculate.py ../breast/mutations.txt ../breast/enrichment

# Wait for qsub exit and then show output.log and errors.log
OUTPUT="$(qstat)"
while [ -n "$OUTPUT" ]; do
    sleep 5
    OUTPUT="$(qstat)"
done
echo "Finished!"
less -e ../logs/errors.log ../logs/output.log 

