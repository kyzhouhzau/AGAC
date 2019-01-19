#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
from elasticsearch import Elasticsearch
es = Elasticsearch()

def load_genes(path):
    genes = []
    functions = []
    texts = []
    with open(path,'r') as rf:
        for line in rf:
            contents = line.split('\t')
            # gene = contents[0].split('_')[0]
            gene = contents[0]
            function = contents[1]
            text = contents[-1]
            texts.append(text)
            genes.append(gene)
            functions.append(function)
        return genes,functions,texts

def convert2dir(data):
    di = {}
    contents = data.split(',')
    for coup in contents:
        ls = coup.split("#")
        name = ls[0].strip().lower()
        action = ls[1].strip()
        di[name]=action
    return di

def search_elastic(gene):
    _query = {
                'query': {
                        'constant_score': {
                        'filter':{
                                'bool':{
                                        'must':[
                                                {"term":{"target_gene":gene}},
                                                ],
                                        }
                                }
                        }
                }
        }
    _searched = es.search(index='drugbank_index', doc_type='drugbank', body=_query)
    
    for hit in _searched['hits']['hits']:
        
        
        
        json = hit['_source']
        genes = json["target_gene"]
        di = convert2dir(genes)
        try:
            action = di[gene]
        except KeyError:
            action ="None"
        drug = json["drug"]
        indication = json["indication"]
        yield gene,action,drug,indication

def filter_result(action):
    jihuoji = ["partial agonist","potentiator","activator","agonist","inducer"]
    yizhiji = ["blocker","suppressor","aggregation inhibitor","inactivator","antagonist","inhibitor"]
    if action in jihuoji:
        flag = "LOF"
    elif action in yizhiji:
        flag = "GOF"
    else:
        flag=None
    return flag,action

def main():
    # path = "./predict_result.txt"
    path = "result309.txt"
    genes,functions,texts = load_genes(path)
    genew = open("genelist.txt",'w')
    drugw = open("druglist.txt",'w')
    interaction = open("interactions_dict.txt")
    #上面的gene,drug是为了计数和查找，这边的function是为了修改配对
    fw = open("function.txt",'w')
    
    _ = interaction.readline()
    alldrugs = {}
    for line in interaction:
        di = eval(line.strip())
        gene = di["gene"]
        alldrugs[gene]=di
    _gene=[]
    _drug = []
    _function = []
    filteredgene = []
    filtereddrug = []

    all_lines = []
    with open("drugbank_result1.txt",'w') as wf:
        for i,gene in enumerate(genes):

            function = functions[i]
            text = texts[i]
            for gene,action,drug,indication in search_elastic(gene.lower()):
                if action!="None":
                    _gene.append(gene.upper())
                    _drug.append(drug)
                    _function.append(action)
                    flag,action = filter_result(action)
                    if flag=="LOF" and function =="LOF":
                        filteredgene.append(gene.upper())
                        filtereddrug.append(drug)
                    #wf.write("{}\t{}\t{}\t{}\t{}\t[SEP]{}\n".format(gene.upper(),action,function,drug,indication,text))
                        # wf.write("{}\t{}\t{}\t{}\t{}".format(gene.upper(),function,action,drug,text))
                        all_lines.append("{}\t{}\t{}\t{}\t{}".format(gene.upper(),function,action,drug,text))
                    elif flag=="GOF" and function =="GOF":
                        filteredgene.append(gene.upper())
                        filtereddrug.append(drug)
                        # wf.write("{}\t{}\t{}\t{}\t{}".format(gene.upper(),function,action,drug,text))
                        all_lines.append("{}\t{}\t{}\t{}\t{}".format(gene.upper(),function,action,drug,text))
        for line in sorted(list(set(all_lines))):
            wf.write(line)
    

    with open("clinvar_result2.txt",'w') as wf:
        for i,gene in enumerate(genes):
            function = functions[i]
            text = texts[i]
            try:
                wf.write("{}\t{}\t{}\t{}\t[SEP]{}".format(gene.upper(),function,alldrugs[gene.upper()]["interaction"],alldrugs[gene.upper()]["drug_name"],text))
            except KeyError:
                pass
    for d in list(set(_drug)):
        drugw.write(d+'\n')
    for g in list(set(_gene)):
        genew.write(g+'\n')
    for f in list(set(_function)):
        fw.write(f+'\n')
    
    fww = open('filtered_genes.txt','w')
    dww = open('filtered_drugs.txt','w')
    for i in list(set(filteredgene)):
        fww.write(i+'\n')
    for k in list(set(filtereddrug)):
        dww.write(k+'\n')

if __name__=="__main__":
    main()
