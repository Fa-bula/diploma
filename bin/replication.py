#!/usr/bin/python
""" Transforming replication timing .wig file to format:
<chromosome> <position> <replication_timing>"""
import sys
import re
# Information string pattern in .wig file
# Example for this pattern:
# fixedStep chrom=chr1 start=1048500 step=1000 span=1000
PATTERN = r"fixedStep chrom=chr(?P<chromosome>\w+) start=(?P<start>\d+) step=(?P<step>\d+) span=(?P<span>\d+)"

def wig2csv(wig_filename, out_filename):
    """ Transform given .wig file to human-readable format:
    chrNo_position_replicationTime """
    # TODO: Return pandas.DataFrame
    with open(wig_filename, 'r') as wig_file:
        with open(out_filename, 'w') as out_file:
            out_file.write('chromosome position replication_timing\n')
            for line in wig_file:
                if re.match("fixedStep", line):
                    match_results = re.match(PATTERN, line).groupdict()
                    position = int(match_results['start'])
                    chromosome = match_results['chromosome']
                    step = int(match_results['step'])
                else:
                    # rep_time = float(line[:-1])
                    rep_time = line[:-1]
                    out_file.write('{0} {1} {2}\n'.format(chromosome,
                                                          position,
                                                          rep_time))
                    position += step

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('usage: {0} input.wig output.csv'.format(sys.argv[0]))
    wig2csv(sys.argv[1], sys.argv[2])
