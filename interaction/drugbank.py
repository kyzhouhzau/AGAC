#!-*-coding:utf-8-*-
import xml.etree.cElementTree as  ET
import re
import glob
def split_data(path):
    name=0
    with open(path) as rf:
        for line in rf:
            if line.startswith("<drug type="):
                name+=1
            with open("./all_drugs/"+str(name)+".xml",'a') as wf:
                wf.write(line)

def process_none(result_dir,name,variable):
    if variable!=None and variable.text!=None:
        result_dir[name]= variable.text.strip()
    else:
         result_dir[name]=''
    return result_dir    
                
def parse_data(xml):
    result_dir = {}
    try:
        tree = ET.parse(xml)
    except Exception:
        print(xml)
    root = tree.getroot()
    _targets=[]
    drug = root.find("name")
    drug_id = root.find("drugbank-id")
    description = root.find("description")
    indication = root.find("indication")
    pharmacodynamics = root.find("pharmacodynamics")
    mechanism_of_action = root.find("mechanism-of-action")
    result_dir = process_none(result_dir,"drug",drug)
    result_dir = process_none(result_dir,"drug_id",drug_id)
    result_dir = process_none(result_dir,"description",description)
    result_dir = process_none(result_dir,"indication",indication)
    result_dir = process_none(result_dir,"pharmacodynamics",pharmacodynamics)
    result_dir = process_none(result_dir,"mechanism_of_action",mechanism_of_action)
    for target in root.iter("target"):
        name = target.find("name")
        proteinname = name.text
        actions = []
        for action in target.iter("actions"):
            _action=action.find("action")
            if _action!=None:
                geneaction = _action.text
                actions.append(geneaction)
            else:
                actions.append('None')
                # print(geneaction)
        gname = ''
        for genename in target.iter("gene-name"):
            if genename!=None:
                gname = genename.text
     
        
        _targets.append((proteinname, gname, ', '.join(actions)))
    try:
        result_dir["target_protein"] = ", ".join([str(x[0]) for x in _targets])
        result_dir["target_gene"] = ", ".join([str(x[1])+" # "+ str(x[2]) for x in _targets])
    except Exception:
        print("#######################")
        print([str(x[1])+" # "+ str(x[2]) for x in _targets])
        print([x[0] for x in _targets])
        exit(0)
    return result_dir
        
def load():
    files = glob.glob("../drug_interaction/all_drugs/*")
    for file in files:
        result_dir = parse_data(file)
        yield result_dir

if __name__=="__main__":
    # split_data("full_database.xml")
   
        for i in load():
            print(i)
