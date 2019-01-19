#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
from elasticsearch import Elasticsearch
es = Elasticsearch()
def search_elastic(gene):
        # _query = {
        # 'query': {
        #         'match_all': {
        #                 },
        # }
        # }
        # _query = {
        #         'query': {
        #                 'bool':{
        #                 "must":{
        #                 'match_phrase': {
        #                         'target_protein':"Low affinity immunoglobulin"
        #                 }
        #         }
        #         }}
        # }
        _query = {
                'query': {
                        'constant_score': {
                        'filter':{
                                'bool':{
                                        'must':[
                                                {"term":{"target_gene":gene}},
                                                # {"term":{"target_gene": "hre"}}
                                                ],
                                        }
                                }
                        }
                }
        }
        _searched = es.search(index='drugbank_index', doc_type='drugbank', body=_query)
        for hit in _searched['hits']['hits']:
                print(hit['_source'], flush=True)
                print("Score:>>>>>>>", hit["_score"])
        


if __name__=="__main__":
        gene = "IL2RG"
        search_elastic(gene.lower())
        print(es.count(index='drugbank_index')['count'], 'documents in index')