#!-*-coding:utf-8-*-
import os
import glob
from elasticsearch import Elasticsearch

es = Elasticsearch()

def get_gene_pmids(genepath):
    
    # pmids = []
    with open(genepath) as rf:
        for line in rf:
            pmid = line.strip()
            # pmids.append(pmid)
            yield pmid

def search(id,denoattions="mutation"):
    query = {
                'query': {
                        'constant_score': {
                        'filter':{
                                'bool':{
                                        'must':[
                                                {"term":{"id":id}},
                                                {"terms":{"text": ["mutation","mutations"]}},
                                                {"terms":{"text":["epilepticus","epilaps","epilepsy","epileptic","seizures","epilepsia"]}}
                                                ],
                                        }
                                }
                        }
                }
        }
    searched = es.search(index='pubmed_index', doc_type='PubMed', body=query)
    for hit in searched['hits']['hits']:
        hit = hit['_source']
        return hit

def main():
    files = glob.glob("./pmid/*")
    for file in files:
        genename = os.path.basename(file).split(".")[0]
        with open("./Filtered_version2/"+genename,'w') as wf:
            for pmid in get_gene_pmids(file):
                if id!=None:
                    hit = search(pmid)
                    if hit != None:
                        wf.write(str(hit)+'\n')
            print("完成基因 {} 的搜索！".format(genename))

if __name__=="__main__":
    main()

        



