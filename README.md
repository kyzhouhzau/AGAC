#Steps
* step1
	> Download all pubmed texts and localize them（functionpart/pubtator29）

* step2
	> Search the database with 2001 genes.(2001.txt)
	> There are 1951 genes with search results.(functionpart/pmid)
	> A total of 479,1972 texts were searched out.(functionpart/pmid) (wc -l pmid/*)
	
* step3
	> Filter text with mutation and epilepsy-related names.
	> 965 genes have related texts.(functionpart/Filtered_version2)
	> There are a total of 10,221 articles.(functionpart/Filtered_version2)
	
* step4
	> Split the sentences and merge the upper and lower sentences, based on the rules.(functionpart/sentence_level_version2)
	> There are 683 genes with related descriptions and 10,366 sentences with related descriptions.(functionpart/sentence_level_version2)

* step5
	> The AGAC corpus is used to train the entity recognition model to extract the features of 10,366 sentences.
	> The classification model was trained with the AGAC corpus and the LOF/GOF/Unknown classification was performed on 10366 sentences.
	> Remove the sentence labeled unknown with 581 sentences left.(NER_classification/predict_result.txt)

* step6
	> Download the drugbank data and localize it to the database.

* step7
	> The genes related to 581 sentences were searched in the drugbank database, and the up-and-down relationship was restricted.(65个/mnt/disk1/Pubtator29/interractionpart2/genelist65.txt)
	> Obtained 118 drugs（/mnt/disk1/Pubtator29/interractionpart2/filtered_drugs118.txt) and 34 genes（/mnt/disk1/Pubtator29/interractionpart2/filtered_genes34.txt）
	> Obtained a drug genetic relationship of 426 pairs.(interaction/result426.txt)
* step8
	> The result of manual proofreading 426 pairs was 65.49%. Remove the unknown modified LOF/GOF predictions instead.(interaction/result_labeled_0106.txt)
	> There are 309 remaining pairs（interaction）and 29 genes.（interaction/genelist.txt）
	> The artificially corrected gene was searched again in the drugbank.
	> Get 281 relationship pairs.（interaction/drugbank_result1.txt）It contains 28 genes and 112 drugs.（interaction/filtered_drugs.txt）（interaction/filtered_genes.txt）
	
	
Run：

1.python splitfile.py and python index.py
The download pubtator text is preprocessed with splitfile.py and localized to the elasticsearch database using the index.py script.

2.python get_pmid.py
The pmid list of the corresponding gene was obtained by inputting 2001 genes.

3.python get_abstract.py
Use this script to search for relevant texts with mutations and epilepsy as query conditions.

4.python sentence_level.py
The search results are divided according to certain rules (including the logical relationship between the upper and lower sentences, including mutations, including the target gene).

5.AGAC_CRF
* The data after the clause is placed in the folder NER_classification\agac_test
* python convert2bio.py
* bash wapiti_agac.sh(NER part)
* Run Decision_tree.py to get the classification result predict_result.txt
* Manual correction of results.

6.Download drubank and localize
* Drugbank.py parses the drugbank data and localizes it to the database with index.py
* Get_drugs.py searches the local database and compares the predicted_result pair after manual correction



















