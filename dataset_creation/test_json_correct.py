from os import listdir
from os.path import isfile, join
import time
from datetime import datetime, timedelta
import time
import random
import numpy as np
import os
import json
from tqdm import tqdm

def correct_cat_idx(test):

    relevant_id_cat = {} #ключ - старое значение, значение - новое
    for i in range(len(test['categories'])):
        dict_items = names.items()
        print('old value:',test['categories'][i]['name'])
        id_update = [key for key, value in dict_items if value == test['categories'][i]['name']][0]
        print('new value', id_update)
        relevant_id_cat[test['categories'][i]['id']]=id_update
        test['categories'][i]['id'] = id_update
        
    for i in range(len(test['annotations'])):
        test['annotations'][i]['category_id'] = relevant_id_cat[test['annotations'][i]['category_id']]      
          
    return test

if __name__ == "__main__":

    #актуальный список категорий из собранного json (v2)
    names= {0:'films',
    1: 'drug blisters',
    2:'Fe/NFe metal',
    3:'Textiles',
    4:'paper',
    5:'PET food bottle blue+colourless',
    6:'PVC',
    7:'TetraPak and EloPak packaging',
    8:'PET food bottle green+brown',
    9:'bottle non food',
    10: 'non bottle',
    11:'LDPE EPE',
    12:'carton',
    13:'PET food bottle white',
    14:'dispenser/pulveriser',
    15:'PET oil sauce bottle'}

    with open(r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\test_v2.json') as load_f:
        test = json.load(load_f)

    test_new = correct_cat_idx(test)

    #save new data in new json test file
    with open(join(r'C:\Personality\Stady\Lab_CV\Create_dataset\V2','test_v2_clean.json'), 'w', encoding='utf-8') as f:
        json.dump(test, f, ensure_ascii=False, indent=4)