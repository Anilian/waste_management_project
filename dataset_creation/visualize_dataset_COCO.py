import json
import pandas as pd
import os
from tqdm import tqdm
from pycocotools.coco import COCO
import os
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


def look_same_class(coco, img_dir, list, class_name):
    """вывести изображения и аннотации к определенному классу class_name"""
    count = 0
    for i in tqdm(range(1,len(list))):
        image_id = i
        try:
            img = coco.imgs[image_id]
        except:
            print('конец класса')
            break
        print(img['file_name'])
        cat_ids = coco.getCatIds(catNms=class_name)
        # display COCO categories
        cats = coco.loadCats(coco.getCatIds(catNms=class_name))
        anns_ids = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
        anns = coco.loadAnns(anns_ids)
        if not anns:
            continue
        else:
            image = np.array(Image.open(os.path.join(img_dir, img['file_name'])))
            plt.imshow(image, interpolation='nearest')
            print('№', i)
            count +=1
            for i in range(len(anns)):
                print('category_id:', anns[i]['category_id'])
                #print(anns[i])
                print('category_name:', cats[0]['name'])
            coco.showAnns(anns)
            plt.show()
    return count

def look_same_image(coco, img_dir, list, start_number, stop_number):
    """вывести изображения и аннотации к определенному диапазону фото из папки"""
    for i in range(start_number,stop_number):
        image_id = i
        try:
            img = coco.imgs[image_id]
        except:
            print('конец класса')
            break
        print(img['file_name'])
        image = np.array(Image.open(os.path.join(img_dir, img['file_name'])))
        plt.imshow(image, interpolation='nearest')
        cat_ids = coco.getCatIds()
        # display COCO categories
        cats = coco.loadCats(coco.getCatIds())
      
        anns_ids = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
        anns = coco.loadAnns(anns_ids)
        if not anns:
            continue
        else:    
            print('№', i)
            for i in range(len(anns)):
                # print()
                print('category_id:', anns[i]['category_id'])
                print('category_name:', cats[int(anns[i]['category_id'])]['name'])
            coco.showAnns(anns)
            plt.show()

def all_image(coco, img_dir, list):

    """вывод всех изображений"""
    for i in range(1,len(list)):
        image_id = i
        img = coco.imgs[image_id]
        image = np.array(Image.open(os.path.join(img_dir, img['file_name'])))
        plt.imshow(image, interpolation='nearest')
        cat_ids = coco.getCatIds()
        anns_ids = coco.getAnnIds(imgIds=img['id'], catIds=cat_ids, iscrowd=None)
        anns = coco.loadAnns(anns_ids)
        print('№', i)
        for i in range(len(anns)):
            print('category_id:', anns[i]['category_id'])
        coco.showAnns(anns)
        plt.show()



if __name__ == "__main__":

    coco = COCO(r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\train_v2_clean.json')
    img_dir = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\train_dataset'
    list = os.listdir(img_dir)

    #V2
    list_classes= [ "films",
    "drug blisters",
    "Fe/NFe metal",
    "Textiles",
    "paper",
    "PET food bottle blue+colourless",
    "PVC",
    "TetraPak and EloPak packaging",
    "PET food bottle green+brown",
    "bottle non food",
    "non bottle",
    "LDPE EPE",
    "carton",
    "PET food bottle white",
    "dispenser/pulveriser",
    "PET oil sauce bottle"]

    class_name = 'drug blisters'
    count = look_same_class(coco, img_dir, list, class_name)

    # start_number = 0
    # stop_number = 10
    # look_same_image(coco, img_dir, list, start_number, stop_number)

    #all_image(coco, img_dir, list)