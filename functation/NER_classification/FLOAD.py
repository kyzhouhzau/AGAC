import glob
import os
import numpy as np
from sklearn.model_selection import KFold
def change(file,basepath):
    basefile = file.split('/')[-1]
    newpath = basepath+basefile
    with open(file,'r') as rf:
        with open(newpath,'w') as wf:
            for line in rf:
                line = line.strip()
                wf.write(line+'\n')

def fload(num,files):
    for train,test in KFold(n_splits=num ,shuffle=True).split(files):
        oldfiles = glob.glob("./TEST/*")
        oldfiles_ = glob.glob("./train_data/*")
        for n in oldfiles:
            os.remove(n)
        for n in oldfiles_:
            os.remove(n)
        files = np.array(files)
        train_data = files[train]
        test_data = files[test]
        for file in test_data:
            change(file,"TEST/")
        for file in train_data:
            change(file,"train_data/")
        os.system('bash wapiti_agac_fload.sh')

def avg_score(filename):
    with open(filename,'r') as rf:
        line = rf.readline()
        precision = []
        recall= []
        fb1 = []
        while line:
            if line.startswith("accuracy:"):
                precision.append(float(line.split(';')[1].split(':')[1].strip().replace("%",'')))
                recall.append(float(line.split(';')[2].split(':')[1].strip().replace("%",'')))
                fb1.append(float(line.split(';')[3].split(':')[1].strip().replace("%",'')))
                line = rf.readline()
            else:
                line = rf.readline()

        print("##########################################\n")
        
        print("Precision:{:.3f}% Recall:{:.3f}% FB1:{:.3f}% \n".format(sum(precision)/len(precision),sum(recall)/len(recall),sum(fb1)/len(fb1)))
        print("##########################################")


if __name__=="__main__":
    files = glob.glob("./BIO116/*.txt")
    oldmodelfile = glob.glob("./eval/bio/*")
    for n in oldmodelfile:
        os.remove(n)
    fload(10,files)
    file = glob.glob("./eval/bio/*.eval")[0]
    avg_score(file)
    