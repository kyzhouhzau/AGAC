#! -*-coding:utf-8-*-
import glob
import json
import nltk
import codecs
import os
def get_bio(file):
    basename = os.path.basename(file)
    with open(file) as rf:
        lines  = rf.readlines()
        for i,line in enumerate(lines):
            text = line.strip()
            name = basename+"_"+str(i)
            yield text,name

def split_write(text,name):
    sentence_list = nltk.sent_tokenize(text)
    start=0
    for sent in sentence_list:
        sent_lis = nltk.word_tokenize(sent)
        for w in sent_lis:
            end = start+len(w)
            line = "{}\t{}\t{}\t{}\t{}\n".format(w,name,start,end,"O")
            start=end
            yield line
        yield '\n'

def main():
    with open("./agac_test/Test_BIO/testtest2bio.tab",'w') as wf:
        x = []
        for dirname in os.listdir("./agac_test/sentence_level"):
            for file in glob.glob("./agac_test/sentence_level/"+dirname+"/*"):
                x.append(file)
                print(file)
                for text,name in get_bio(file):
                    for line in split_write(text,name):
                        wf.write(line)
        print(len(x))       

if __name__=="__main__":
    main()