#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@Author:zhoukaiyin
"""
class config():
    index_mappings = {
      "mappings": {
        "drugbank": {
          "properties": {
            "drug_id":{
                  "type": "keyword",
              },
            "drug": {
              "type": "keyword",
            },
            "description": {
              "type": "text",
              "analyzer": "standard",
              "search_analyzer": "standard"
            },
             "indication": {
              "type": "text",
              "analyzer": "standard",
              "search_analyzer": "standard"
            },
            "pharmacodynamics": {
              "type": "text",
              "analyzer": "standard",
              "search_analyzer": "standard"
            },
            "mechanism_of_action": {
              "type": "text",
              "analyzer": "standard",
              "search_analyzer": "standard"
            },
            "target_protein": {
              "type": "text",
              "analyzer": "standard",
              "search_analyzer": "standard"
            },
            "target_gene": {
              "type": "text",
              "analyzer": "standard",
              "search_analyzer": "standard"
            },

          }
        }
      }
    }
     