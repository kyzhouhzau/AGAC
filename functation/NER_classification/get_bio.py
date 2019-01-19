#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
import glob
import json
import nltk
import codecs
import os

start = 0
def get_bio(files):
    for file in files:
        print(file)
        dirs={}
        n_dir={}
        rf=codecs.open(file,'r',encoding='utf-8')
        name = os.path.basename(file)
        wf=open("./BIO/"+name.split('.')[0]+".txt",'w')
        dom = rf.read()
        jsondom = json.loads(dom)
        span_type = jsondom["denotations"]
        text = jsondom["text"]
        text_list = nltk.word_tokenize(text)
        for id in span_type:
            length = []
            offset = id["span"]
            label = id["obj"]
            flag_start = offset["begin"]
            flag_end = offset["end"]
            length.append(flag_end)
            length.append(label)
            dirs[flag_start]=length
        end=0
        for w in text_list:
            index = text.index(w,end)
            end = index+len(w)
            for key,value in dirs.items():
                lower = key
                high = value[0]
                label = value[1]
                # if label not in ["Enzyme","Protein","Gene"]:
                if index+1>=lower and index+1<=high:
                    if index==lower:
                        n_dir[w+str(index)]="B-"+label
                    else:
                        n_dir[w+str(index)]="I-"+label
            print(w)
            if w not in [".", "!", "?"]:
                if w+str(index) in n_dir:
                    line = "{}\t{}\t{}\t{}\n".format(w,str(index),str(end),n_dir[w+str(index)])
                    wf.write(line)
                else:
                    line = "{}\t{}\t{}\t{}\n".format(w,str(index),str(end),"O")
                    wf.write(line)
            else:
                wf.write("{}\t{}\t{}\t{}\n".format(w,str(index),str(end),"O"))
                wf.write('\n')
        rf.close()
        wf.close()
if __name__=="__main__":
    files = glob.glob("./AGAC_raw_data/*")
    get_bio(files)