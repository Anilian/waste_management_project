import shutil
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


def transfer_images(dataset_json,dest_dir,dataset_part_1,dataset_part_2,dataset_part_3):

    for i in range(1,len(listdir(dataset_json))+1):
        if i==1:
            choose_photo=dataset_part_1
        elif i==2:
            choose_photo=dataset_part_2
        else:
            choose_photo=dataset_part_3
            
        path_folder = os.path.join(dataset_json,str(i))
        json_files = os.listdir(path_folder)

        for name in json_files:
            print('json_name',name)
            json_path = os.path.join(path_folder,name)
            folder_name =name.split('.json')[0] 
            src_dir  = os.path.join(choose_photo,folder_name)
            print('src_dir',src_dir)
            
            files=listdir(src_dir)
            print(len(files))
            print('----------')
            for fname in files:
                # copying the files to the
                # destination directory
                shutil.copy2(os.path.join(src_dir,fname), dest_dir)

def count_image_json(file_folder,json_name):
    img_list = []
    with open(join(file_folder,json_name)) as load_f:
        data_json = json.load(load_f)
        print('кол-во изображений в json:', len(data_json['images']))
        for i in range(len(data_json['images'])):
            name = data_json['images'][i]['file_name']
            img_list.append(name)
    return img_list


def cheak_difference(dest_dir,img_list):

    """input: dest_dir - folder with photo, img_list - list of images from json"""
    img_folder_list = listdir(dest_dir)

    difference_1 = set(img_list).difference(set(img_folder_list))
    difference_2 = set(img_folder_list).difference(set(img_list))

    list_difference = list(difference_1.union(difference_2))
    list_difference.sort()
    return list_difference


if __name__ == "__main__":

    dataset_json = r'C:\Personality\Stady\Lab_CV\Create_dataset\train_json'

    dataset_part_1 = r'Z:\Personality\Stady\CV_Lab\Sorted_dataset — копия'
    dataset_part_2 = r'Z:\Personality\Stady\CV_Lab\New_for_dataset_v2'
    dataset_part_3 = r'Z:\Personality\Stady\CV_Lab\!DATASET_28062023_sorted'

    dest_dir = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\train_IMG' #folder with images

    #transfer images from dataset_part_ to dest_dir
    transfer_images(dataset_json,dest_dir,dataset_part_1,dataset_part_2,dataset_part_3)

    json_name = 'train_v2.json'
    file_folder = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2' #where the json file is

    img_list = count_image_json(file_folder,json_name)
    list_difference = cheak_difference(dest_dir,img_list)
    print('number of different files in json and in image_dataset_folder:',len(list_difference))