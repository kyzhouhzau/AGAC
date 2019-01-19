#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""

def get_result(filename,basename):
    with open(filename,'r') as rf:
        for line in rf:
            contents = line.strip().split('\t')
            if len(contents)>1:
                word = contents[0]
                name = contents[1]
                start = contents[2]
                end = contents[3]
                tag = contents[-1]
                wf = open(basename+name,'a')
                wf.write("{}\t{}\t{}\t{}\t{}\n".format(word,name,start,end,tag))
                # if word in ['.','!','?']:
            else:
               
                wf.write('\n')
        wf.close()



if __name__=="__main__":
    filename = "./eval/bio/Tok.pat_agac116-train-test-BIO116.tab"
    basename = "./agac_result_bio/"
    get_result(filename,basename)