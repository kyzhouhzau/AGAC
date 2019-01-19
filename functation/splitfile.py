#！-*-coding:utf-8-*-
import sys
import os
import pickle 
inp = sys.argv[1]
rf=open(inp)
json = {}
concepts = []
if not os.path.exists("./pubtator29"):os.mkdir("./pubtator29")
count=0
with open("pubtator29/pubtator_json.txt",'w') as wf:
	for line in rf:
		line_list = line.strip().split("|")
		if len(line_list)>2:
			if line_list[1]=="t":
				filename = line_list[0]
				json["id"]=filename
				json["title"]=line_list[2]
			elif line_list[1]=="a":
				json["text"]=line_list[2]
		elif len(line_list)==1 and line_list[0]!='':
			lsline = line.strip().split('\t')
			start =lsline[1]
			end = lsline[2]
			term = lsline[3]
			concept = lsline[4]
			con= "{} & {} & {} & {}".format(concept,start,end,term)
			concepts.append(con)
			
		else:
			json["denotations"]=', '.join(concepts)
			wf.write(str(json)+'\n')
			json = {}
			concepts = []
			count+=1
			if count%2000==0:
				print("成功的分割了第 {} 个文件。".format(count))		
rf.close()







