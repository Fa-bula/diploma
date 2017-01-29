#!/usr/bin/python
""" Perform all neaded calculations"""
import sys
import os
sys.path.append('/home/fa_bula/diploma/bin/')
import core
import mutations

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit("Usage {0} mutations enrichment".format(sys.argv[0]))
    with open(os.path.join(core.HOME, 'sorted_motifs')) as fin:
        for line in fin:
            core.MOTIFS = [line[:-1]]
            core.INIT_NUCL = [line[1]]
            for i in core.INIT_NUCL:
                print i
            # Create directory for results if needed
            res_dir = os.path.join(core.HOME, 'results', core.MOTIFS[0])
            if not os.path.exists(res_dir):
                os.makedirs(res_dir)
                
            # mutations.py part
            sample_names = mutations.get_sample_names(sys.argv[2])
            for sample in sample_names:
                result = mutations.get_mutation_rep_time(sys.argv[1], sample)
            outFileName = os.path.join(res_dir, sample)
            with open(outFileName, 'w') as fout:
                for repTime in result:
                    fout.write(str(repTime) + '\n')
            
    
