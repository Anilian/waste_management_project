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


def rename_category(json_paths,class_data):

    """changing category names after markup and removing labels for an overlaid class"""
    for k, json_path in enumerate(json_paths):
        print(json_path)
        json_files = [f for f in listdir(json_path) if isfile(join(json_path, f))]

        #получаем json в которых есть название класса и все аннотации с леблом 2 сделаны = 1, и убран их класс при лейбле 2
        for json_file in json_files:
            print(k)
            print(class_data[k])
            class_name = class_data[k][json_file]
            
            #открыть json, заменить значение класса и снова сохранить
            with open(join(json_path,json_file)) as f:
                data = json.load(f)  

            if len(data['categories'])==1:
                data['categories'][0]['name'] = class_name
            else:
                data['categories'][0]['name'] = class_name
                data['categories'].pop(1)

            for i in range(len(data['annotations'])):
                if data['annotations'][i]['category_id'] == 2:
                    data['annotations'][i]['category_id'] = 1

            with open(join(json_path,json_file), 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

def merging_json(json_paths):

    """Combines all json files in these folders, changing class numbering(id) and annotation numbering"""

    #лицензия везде одинаковая
    merged_dict_license =   [{   "name": "",
                "id": 0,
                "url": ""
            }]
    #info везде одинаковое
    merged_dict_info = {
            "contributor": "",
            "date_created": "",
            "description": "",
            "url": "",
            "version": "",
            "year": ""
        }
    

    merged_json = 0
    idx = 0 #номер id для класса
    for path_folder in json_paths:

        json_files = [f for f in listdir(path_folder) if isfile(join(path_folder, f))]
        
        for json_file in json_files:
            
            with open(join(path_folder,json_file)) as load_f:
                data_cur = json.load(load_f)
            print(data_cur['categories'][0]['name'])
            
            if idx==0:#только для самого первого json
                data_cur['categories'][0]['id']=idx
                for i in range(len(data_cur['annotations'])):
                    data_cur['annotations'][i]['category_id'] = idx 
                merged_json = data_cur
                idx += 1
                
            else:
                list_of_categories = {} #список текущих категорий
                for i in range(len(merged_json['categories'])):
                    list_of_categories[merged_json['categories'][i]['name']]=merged_json['categories'][i]['id']
                
                flag=0
                for i in list_of_categories.keys():
                    if data_cur['categories'][0]['name'] == i:
                        flag=1
                        break
                        
                if flag==1:
                    print('если новая категория уже есть')
                    current_id = list_of_categories[data_cur['categories'][0]['name']]
                    data_cur['categories'][0]['id']=current_id

                    #объединенный словарь категорий
                    merged_dict_categories = merged_json['categories']

                    #заменяем в изображении все соответствующие 'id' 
                    cheak_len_id_images = len(merged_json['images'])
                    for i in range(0,len(data_cur['images'])):
                        cur_image_id = cheak_len_id_images + i +1
                        data_cur['images'][i]['id'] = cur_image_id 

                    #заменяем в аннотации все 'id'(порядковый номер аннотации) и 'image_id'(привязка к изображению)
                    cheak_len_id_annot = len(merged_json['annotations']) + 1

                    for i in range(len(data_cur['annotations'])):
                        data_cur['annotations'][i]['id'] = i + cheak_len_id_annot
                        data_cur['annotations'][i]['image_id'] = cheak_len_id_images + data_cur['annotations'][i]['image_id']
                        data_cur['annotations'][i]['category_id'] = current_id


                    #объединенный словарь аннотаций
                    merged_dict_annotations = merged_json['annotations'] + data_cur['annotations']
                    merged_json = {"licenses":merged_dict_license,
                            "info":merged_dict_info,
                        "categories":merged_dict_categories,
                        "images":merged_json['images'] + data_cur['images'],
                        "annotations": merged_dict_annotations
                                    } 

                else:
                    print("новая категория") 
                    #заменяем в категориях номер id класса
                    data_cur['categories'][0]['id']=idx
                    #объединенный словарь категорий
                    merged_dict_categories = merged_json['categories'] + data_cur['categories']

                    #заменяем в изображении все соответствующие 'id' 
                    cheak_len_id_images = len(merged_json['images'])
                    for i in range(0,len(data_cur['images'])):
                        cur_image_id = cheak_len_id_images + i +1
                        data_cur['images'][i]['id'] = cur_image_id 

                    #заменяем в аннотации все 'id'(порядковый номер аннотации) и 'image_id'(привязка к изображению)
                    cheak_len_id_annot = len(merged_json['annotations']) + 1

                    for i in range(len(data_cur['annotations'])):
                        data_cur['annotations'][i]['id'] = i + cheak_len_id_annot
                        data_cur['annotations'][i]['image_id'] = cheak_len_id_images + data_cur['annotations'][i]['image_id']
                        data_cur['annotations'][i]['category_id'] = idx

                    #объединенный словарь аннотаций
                    merged_dict_annotations = merged_json['annotations'] + data_cur['annotations']
                    merged_json = {"licenses":merged_dict_license,
                            "info":merged_dict_info,
                        "categories":merged_dict_categories,
                        "images":merged_json['images'] + data_cur['images'],
                        "annotations": merged_dict_annotations
                                    } 

                    idx += 1
    return merged_json

if __name__ == "__main__":

    #all_classes dataset V2
    names= ['films',      
    'bottle non food',
    'non bottle',       
    'drug blisters',
    'Fe/NFe metal',
    'Textiles',      
    'paper',
    'carton',     
    'PVC',
    'LDPE EPE',
    'TetraPak and EloPak packaging', 
    'PET food bottle blue+colourless',
    'PET food bottle green+brown',
    'PET food bottle white',
    'PET oil sauce bottle',   
    'dispenser/pulveriser']

    #description of which file the debris material class corresponds to
    #V2-dataset
    class_data_3 = {'1.1.json':'PET food bottle blue+colourless',
                '2.1.json':'PET food bottle green+brown',
                '3.1.json':'PET food bottle white',
                '4.1.json':'PET oil sauce bottle',
                '5.1.json':'bottle non food',
                '9.1.json':'non bottle',
                '11.1_1_1.json':'PVC',
                '13.1_1.json':'LDPE EPE',
                '19.1.json':'TetraPak and EloPak packaging',
                '20.1_1.json':'carton',    
                '35.1.json':'dispenser/pulveriser',
                '36.1.json':'dispenser/pulveriser',
                '36.1_7.1.json':'bottle non food',
                '11.1_2_1.json':'PVC',
                '11.1_1_2.json':'PVC',
                '13.1_2.json':'LDPE EPE',    
                '14.1_2.json':'films',
                '20.1_2.json':'carton',    
                '11.1_2_2.json':'PVC'
                }
    class_data_2 = {'1.1.json':'PET food bottle blue+colourless',
                '2.1.json':'PET food bottle green+brown',
                '5.1.json':'bottle non food',
                '6.1.json':'non bottle',
                '7.1.json':'bottle non food',
                '8.1.json':'non bottle',
                '11.1.json':'PVC',
                '12.1.json':'films',
                '14.1.json':'films',
                '19.1.json':'TetraPak and EloPak packaging',
                '20.1.json':'carton',    
                '33.1.json':'Fe/NFe metal'
                }

    #это пойдет на test_dataset
    class_data_1 = {'HDPE_выдувной_test.json':'bottle non food',
                'HDPE_выдувной_test_2ndrun.json':'bottle non food',
                'HDPE_пленки_test.json':'films',
                'LDPE_пленка_test.json':'films',
                'LLDPE_пленка_test.json':'films',
                'LPDE_EPE_test.json':'LDPE EPE',
                'PET_бутылка_белая_test.json':'PET food bottle white',
                'PET_бутылка_не_пищевой_test.json':'bottle non food',
                'PET_бутылки_test.json':'НЕПРАВИЛЬНАЯ РАЗМЕТКА',
                'PET_не_бутылочный_test.json':'non bottle',
                'PP_test.json':'non bottle',    
                'PET_бутылочный_масло_test.json':'PET oil sauce bottle',
                'PS_test.json':'non bottle',
                'PVC_test.json':'PVC',
                'Блистеры_от_лекарств_test.json':'drug blisters',
                'Металл_test.json':'Fe/NFe metal',
                'Текстиль_test.json':'Textiles',
                'Тетрапак_test.json':'TetraPak and EloPak packaging',    
                'Фольга_алюминиевая_test.json':'Fe/NFe metal',
                'Целлюлоза_бумага_белая_test.json':'carton',
                'Целлюлоза_бумага_прочее_test.json':'paper',
                'Целлюлоза_картон_test.json':'carton'
                }

    path_folder_1 = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\train_json\1'
    path_folder_2 = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\train_json\2'
    path_folder_3 = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\train_json\3'

    json_paths = [path_folder_1,path_folder_2,path_folder_3]
    class_data = [class_data_1,class_data_2,class_data_3]

    rename_category(json_paths,class_data)
    merged_json = merging_json(json_paths)   

    #if the path to the folder is saved in the file name, remove it
    for i in range(len(merged_json['images'])):
        try:
            merged_json['images'][i]['file_name'] = merged_json['images'][i]['file_name'].split('/')[1]
        except:
            pass

    #save merged_json in new json file
    new_json_name = 'train_v2.json'
    path_to_save = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2'
    with open(join(path_to_save,new_json_name), 'w', encoding='utf-8') as f:
        json.dump(merged_json, f, ensure_ascii=False, indent=4)

