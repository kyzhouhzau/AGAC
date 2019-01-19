#步骤
* 第一步
	> 下载所有pubmed文本并本地化（/mnt/disk1/Pubtator29/functionpart1/pubtator29）

* 第二步
	> 用2001个基因搜索数据库。(/mnt/disk1/Pubtator29/functionpart1/build_data/2001.txt)
	> 有1951个基因有搜索结果。(/mnt/disk1/Pubtator29/functionpart1/pmid)
	> 共搜索到4791972篇文本。(/mnt/disk1/Pubtator29/functionpart1/pmid) (统计方法：wc -l pmid/*)
	
* 第三步
	> 用突变和癫痫相关名字过滤文本。
	> 965个基因有相关文本。(/mnt/disk1/Pubtator29/functionpart1/Filtered_version2)
	> 有文本共10221篇。(/mnt/disk1/Pubtator29/functionpart1/Filtered_version2)
	
*第四步
	> 切分句子，并将可能得上下句合并,基于规则。(/mnt/disk1/Pubtator29/functionpart1/sentence_level_version2)
	> 有683个基因有相关描述，有10366个句子有相关描述。(/mnt/disk1/Pubtator29/functionpart1/sentence_level_version2)

*第五步
	> 用AGAC语料库训练实体识别模型，提取10366个句子的特征。
	> 用AGAC语料库训练分类模型，对10366个句子做LOF/GOF/Unknown分类。
	> 去除标注为unknown的句子剩下581个句子。(/mnt/disk2/kyzhou/OMIM/AGAC_CRF/predict_result.txt)

*第六步
	> 下载drugbank数据，并本地化到数据库.

*第七步
	> 将581个句子所相关的基因(65个/mnt/disk1/Pubtator29/interractionpart2/genelist65.txt)到drugbank数据库搜索，并限制上下调关系相对应。	
	> 获得药物118个（/mnt/disk1/Pubtator29/interractionpart2/filtered_drugs118.txt），基因34个（/mnt/disk1/Pubtator29/interractionpart2/filtered_genes34.txt）
	> 获得药物基因关系对426对。(/mnt/disk1/Pubtator29/interractionpart2/result426.txt)
*第八步
	> 人工校对426对结果，分类正确率65.49%。删除unknown的修改LOF/GOF预测相反的。(/mnt/disk1/Pubtator29/interractionpart2/result_labeled_0106.txt)
	> 剩余309个关系对。（/mnt/disk1/Pubtator29/interractionpart2）基因29个（/mnt/disk1/Pubtator29/interractionpart2/genelist.txt）
	> 人工矫正后的基因重新在drugbank中搜索。
	> 获得281个关系对。（/mnt/disk1/Pubtator29/interractionpart2/drugbank_result1.txt）
		其中包含基因28个，药物112个。（/mnt/disk1/Pubtator29/interractionpart2/filtered_drugs.txt）（/mnt/disk1/Pubtator29/interractionpart2/filtered_genes.txt）
	
	
代码运行流程：
1、index.py
下载pubtator文本用splitfile.py预处理，并用index.py脚本本地化到elasticsearch数据库中。
2、get_pmid.py
以2001个基因为输入获取对应基因的pmid list。
3、get_abstract.py
用该脚本以突变和癫痫为查询条件搜索出相关文本。
4、sentence_level.py
对搜索出的结果按照一定的规则进行分句（包括上下句逻辑关系，包含突变，包含目标基因）。
5、AGAC_CRF
分句后的数据放在文件夹AGAC_CRF\agac_test中
运行convert2bio.py
运行wapiti_agac.sh（实体识别）
运行Decision_tree.py获得分类结果predict_result.txt
对结果人工矫正
6、下载drubank并本地化
drugbank.py解析drugbank数据并用index.py本地化到数据库
get_drugs.py搜索本地数据库并宇人工矫正后的predict_result配对



















