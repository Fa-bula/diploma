# Script to perform all needed calculations and wait for it finish
# Remove old .log files
rm ../logs/*

# Run program with specified destination of errors and output
clear
date > ../logs/exec_time	# Write start time at file
# Python part
# FIXME: maybe loop?
qsub -t 1-9 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 10-19 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 20-29 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 30-39 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 40-49 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 50-59 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 60-69 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 70-79 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 80-89 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results
qsub -t 90-96 -sync y -cwd -S /usr/bin/python -e ../logs/ -o ../logs/ calculate.py ../breast/mutations.txt ../breast/enrichment ../breast_results

# R part
RESULTS=../breast_results/*/mutations_frequency/
for dir in $RESULTS; do
    qsub  -cwd -S /usr/bin/Rscript -e ../logs/ -o ../logs/ linearModel.R $dir ../breast/enrichment ../plots $(basename $(dirname $dir))
done
echo "Calculations, job has been finished!"
date >> ../logs/exec_time	# Append end time to file
cat ../logs/exec_time
