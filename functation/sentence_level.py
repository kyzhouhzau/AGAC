#! -*-coding:utf-8-*-
import nltk
import glob
import os
def get_texts(path):
    genename = os.path.basename(path)
    texts = []
    pmids=[]
    with open(path) as rf:
        for line in rf:
            contents = line.strip()
            _dict = eval(contents)
            text = _dict["text"]
            pmid = _dict["id"]
            texts.append(text)
            pmids.append(pmid)
        return texts,pmids,genename

def concat_possible(sens):
    nsens = ['']
    for i,sen in enumerate(sens):
        if sen.startswith("This mutation"):
            nsen = ' '.join([nsens.pop(),sen])
            nsens.append(nsen)
        elif sen.startswith("Those mutations"):
            nsen = ' '.join([nsens.pop(),sen])
            nsens.append(nsen)
        elif sen.startswith("These mutations"):
            nsen = ' '.join([nsens.pop(),sen])
            nsens.append(nsen)
        elif sen.startswith("It"):
            nsen = ' '.join([nsens.pop(),sen])
            nsens.append(nsen)
        elif sen.startswith("The mutation"):
            nsen = ' '.join([nsens.pop(),sen])
            nsens.append(nsen)
        else:
            nsens.append(sen)
    return nsens
        
def filter_text(texts,pmids,genename):
    def filter_sentence(sens,genename):
        sentences = []
        for sentence in sens:
            if sentence.find(genename)!=-1 and sentence.find("mutation")!=-1:
                sentences.append(sentence)
        return sentences
    for text,pmid in zip(texts,pmids):
        sens = nltk.sent_tokenize(text) 
        # 基于规则将可能的上下句相互连接。
        sens = concat_possible(sens)
        #将句子中含有基因名，同时有mutation字样的句子留下来，其他去掉。
        sentences = filter_sentence(sens,genename)
        yield sentences,pmid,genename

def main():
    files = glob.glob("./Filtered_version2/*")
    for file in files:
        print(os.path.getsize(file))
        texts,pmids,genename = get_texts(file)
        for sentences,pmid,genename in filter_text(texts,pmids,genename):
            if len(sentences)!=0:
                if not os.path.exists("./sentence_level_version2/"+genename):os.mkdir("./sentence_level_version2/"+genename)
                with open("./sentence_level_version2/"+genename+'/'+genename+"_"+pmid,'w') as wf:
                    for sentence in sentences:
                        wf.write(sentence+'\n')

if __name__=="__main__":
    main()



