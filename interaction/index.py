#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
from elasticsearch import Elasticsearch
from config import config as cf
from elasticsearch.helpers import bulk, streaming_bulk
import drugbank
es = Elasticsearch()
def create_index(client,index):
    if not es.indices.exists(index='drugbank_index'):
        client.indices.create(index=index, body=cf.index_mappings)

def main():
    
    create_index(es,"drugbank_index")
    # we load the repo and all commits
#     x = {"target_protein":['HRE & testname','HRN1 & testname2']}
#     es.index(index="drugbank_index",doc_type="drugbank",body = x)
    count=0
    actions=[]
    for json in drugbank.load():
        
        
        action = {"_index":"drugbank_index",
                                "_type":"drugbank",
                                "_id":json["drug_id"],
                                "_source":json
                        }
        
        # with open("ennro.log",'a') as wf:
        #         wf.write(line)
        # continue

        actions.append(action)
        
        if len(actions)==3000:
                success, _ = bulk(es, actions, index = "drugbank_index")
                es.indices.refresh(index='drugbank_index')
                count+=success
                actions=[]
                print("成功插入 {} 篇文本！".format(count))
    success, _ = bulk(es, actions, index = "drugbank_index")
    es.indices.refresh(index='drugbank_index')
    count+=success
    print("成功插入 {} 篇文本！".format(count))
    
if __name__=="__main__":

    main()
    # print(es.count(index='pubmed_index')['count'], 'documents in index')