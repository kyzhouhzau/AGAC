#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
import logging
from sklearn.tree import DecisionTreeClassifier
import data_process
import numpy as np

##Leave One Out
def decisiontree(traindata,testdata,file_names,all_files):
    train_X= traindata[:,:-1]
    train_y=traindata[:,-1]
    test_x = testdata[:,:-1] 
    clf = DecisionTreeClassifier()
    clf.fit(train_X, train_y)
    predict = clf.predict(test_x)
    # print(predict)
    with open("./predict_result.txt",'w') as wf:
        
        for i,name in enumerate(file_names):
            num = predict[i]
            file = all_files[i]
            if int(num)==0:
                label = "GOF"
            elif int(num)==1:
                label="LOF"
            elif int(num)==2:
                label="Unknown"
            if label!="Unknown":
                wf.write("{}\t{}\t{}\n".format(name,label,file))

if __name__=="__main__":
    traindata,testdata,file_names,all_files= data_process.load_data()
    decisiontree(traindata,testdata,file_names,all_files)
    print(traindata[1:4,:-1])
    print(testdata[1:4,:9])
    # decisiontree(traindata,testdata)