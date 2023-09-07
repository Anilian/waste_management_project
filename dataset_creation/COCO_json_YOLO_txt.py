
from datetime import datetime, timedelta
import os
import json
from os import listdir
from os.path import isfile, join
import copy
import numpy as np
import os
import json
from tqdm import tqdm
from pylabel import importer


#it use pylabel import importer. Yaml file not correct, becouse it for YOLOv5
def create_txt_detection(path_to_annotations, path_to_images):
    """Create txt file from COCO json file for detection task"""

    path_to_annotations = r'C:\Personality\Stady\Lab_CV\Create_dataset\short_train_utf8.json'
    path_to_images = r'C:\Personality\Stady\Lab_CV\Create_dataset\train_dataset'
    #Import the dataset into the pylable schema 
    dataset = importer.ImportCoco(path_to_annotations, path_to_images=path_to_images, name="result_test")
    dataset.export.ExportToYoloV5()[0]

#for the main dataset (not for labels and lids)
def create_txt_segmentation(dataset_folder, json_name, image_folder, txt_path, H, W):
    """Create txt file from COCO json file for segmentation task"""

    with open(join(dataset_folder,json_name)) as load_f:
        data_json = json.load(load_f)

        id_image = {}
        cat_id_name = {}
        seg_cat_img_id = {}
        
        for i in range(len(data_json['images'])):
            id_image[data_json['images'][i]['file_name']]=data_json['images'][i]['id']
            
        for i in range(len(data_json['categories'])):
            cat_id_name[data_json['categories'][i]['name']]=data_json['categories'][i]['id'] 
        
            
        for i in tqdm(range(len(os.listdir(image_folder)))):
            image_name = os.listdir(image_folder)[i]    
            id_image_json = id_image[image_name]
            # print('img_name',image_name)
            # print('id_image_json',id_image_json) #id image in json
            
            seg_id = []    #получить список seg_id для нужного изображения
            
            for i in range(len(data_json['annotations'])):
                if data_json['annotations'][i]['image_id'] == id_image_json:
                    segmen_id = data_json['annotations'][i]['id']
                    seg_id.append(int(segmen_id))

            txt_name = image_name.split('.')[0] + '.txt'
            

            with open(os.path.join(txt_path,txt_name), "w") as txt_file:  
                for idx in seg_id:
                    # print('seg_id',idx)
                    seg_id = copy.deepcopy(data_json['annotations'][idx-1]['category_id'])
                    txt_file.write(str(seg_id) + ' ')
                    seg_coord = copy.deepcopy(data_json['annotations'][idx-1]['segmentation'])
                    #print(seg_coord)

                    try:  
                        #print(len(seg_coord[0]))
                        for i in range(len(seg_coord[0])):
                            if i % 2 ==0: #четное
                                seg_coord[0][i] =  round(int(seg_coord[0][i])/W,4)
                                txt_file.write(str(seg_coord[0][i])+ ' ')
                            else:
                                seg_coord[0][i] =  round(seg_coord[0][i]/H,4)
                                txt_file.write(str(seg_coord[0][i])+ ' ')
                    except:
                        #print(len(seg_coord))
                        for i in range(len(seg_coord)):
                            if i % 2 ==0: #четное
                                seg_coord[i] =  round(int(seg_coord[i])/W,4)
                                txt_file.write(str(seg_coord[i])+ ' ')
                            else:
                                seg_coord[i] =  round(seg_coord[i]/H,4)
                                txt_file.write(str(seg_coord[i])+ ' ')
                        
                    txt_file.write('\n')                  
            txt_file.close()    




if __name__ == "__main__":

    dataset_folder = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2'
    json_name = 'test_v2_clean.json'
    image_folder = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\test_dataset'
    txt_path = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\test_labels_v2'
    error_image = []
    H = 1024
    W = 1280
    
    create_txt_segmentation(dataset_folder, json_name, image_folder, txt_path, H, W)

    #path_to_annotations = r'C:\Personality\Stady\Lab_CV\Create_dataset\short_train_utf8.json'
    #path_to_images = r'C:\Personality\Stady\Lab_CV\Create_dataset\train_dataset'
    #create_txt_detection(path_to_annotations, path_to_images)


