import numpy as np
import cv2
import json
import pycocotools.mask as mask_util
from tqdm import tqdm
from os.path import isfile, join

def polygonFromMask(maskedArr): 
    
    # https://github.com/hazirbas/coco-json-converter/blob/master/generate_coco_json.py

    contours, _ = cv2.findContours(maskedArr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    segmentation = []
    for contour in contours:
        if contour.size >= 6:
            segmentation.append(contour.flatten().tolist())

    return segmentation[0] #, [x, y, w, h], area

def RLE_count(file_path):

    """подсчитать файлы, в которых аннотация в виде RLE"""
    
    count_RLE = [] #id annotations
    RLE_image = [] #image id
    with open(file_path, 'r') as f:
        data = json.load(f)
        
        for i in tqdm(range(len(data['annotations']))):
            
            sample_seg = data['annotations'][i]['segmentation']
            
            if len(sample_seg)==2:
                RLE_image.append(data['annotations'][i]['image_id'])
                count_RLE.append(data['annotations'][i]['id'])

    return count_RLE

if __name__ == "__main__":

    file_path = r"C:\Personality\Stady\Lab_CV\Create_dataset\V2\train_v2.json"
    imHeight = 1024
    imWidth = 1280

    c_RLE = RLE_count(file_path)
    
    if len(c_RLE) !=0:

        with open(file_path, 'r') as f:
            data = json.load(f)

        for i in range(len(data['annotations'])):
            sample_seg = data['annotations'][i]['segmentation']
            if len(sample_seg) == 2:
                sample_seg_1 = mask_util.frPyObjects(sample_seg,imHeight,imWidth)
                sample_mask = mask_util.decode(sample_seg_1)
                sample_polygon = polygonFromMask(sample_mask)
                data['annotations'][i]['segmentation']= sample_polygon

        #add new data in json file
        with open(join(r'C:\Personality\Stady\Lab_CV\Create_dataset','train_v2_clean.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)