#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
import glob
import os
import numpy as np

class FeatureLabel(object):
    def __init__(self,file):
        self.files = file
        self.tagfile = "./dataforclassfication/name_label.txt"
        self.labelfile = "./dataforclassfication/label_id.txt"
        
    def get_label(self,file):
        with open(file) as rf:
            dom  = rf.read().strip()
            dom = eval(dom)
            return dom

    def load_labe(self,file):
        label_id = {}
        with open(file) as rf:
            for line in rf:
                contents = line.strip().split()
                label_name = contents[0]
                id = contents[-1]
                label_id[label_name]=id
            return label_id

    def features_label(self,flag="train"):
        name_tag = self.get_label(self.tagfile)
        label_id = self.load_labe(self.labelfile)
        feature_label = np.zeros((len(self.files),len(label_id)+1))
        file_names = []
        all_files = []
        for i,file in enumerate(self.files):
            rf = open(file)
            name = os.path.basename(file)
            file_names.append(name)
            tag=None
            sentence = []
            for line in rf:
                contents = line.strip().split('\t')
                w = contents[0]
                sentence.append(w)
                if flag=="train":
                    tag = name_tag[name]
                elif flag=="test":
                    pass
                if contents[-1].startswith("B"):
                    label = contents[-1].split('-')[-1]
                    if label in label_id.keys():
                        lid = label_id[label]
                        feature_label[i,int(lid)]+=1
            if flag=="train":
                feature_label[i, -1] = int(tag)
            elif flag=="test":
                feature_label[i, -1] = -1
            rf.close()
            line = ' '.join(sentence)
            all_files.append(line)
        return feature_label,file_names,all_files

def load_data():
    testfile = glob.glob("./agac_result_bio/*")
    trainfiles = glob.glob("./BIO116/*")
    train = FeatureLabel(trainfiles)
    traindata,_ ,_= train.features_label("train")
    test = FeatureLabel(testfile)
    testdata,file_names,all_files = test.features_label("test")
    return traindata,testdata,file_names,all_files

if __name__=="__main__":
    traindata = load_data()