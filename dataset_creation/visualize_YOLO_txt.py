from os import listdir
from os.path import isfile, join
import time
import random
import numpy as np
import os
from PIL import ImageDraw
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from pathlib import Path
from tqdm import tqdm

def visualize_txt_YOLO_segmentation(txt_path, path,names):
    """displays images from the path folder and overlays markup on it from the corresponding txt file. 
    Displays the file name, class id and class name."""

    files = os.listdir(txt_path)
    for idx in range(0,len(files)):
        name = files[idx]
        f = open(join(txt_path,name),'r')
        img_name = name.split('.')[0] + '.jpg'
        img = Image.open(join(path,img_name))
        draw = ImageDraw.Draw(img)
        W, H = img.size
        print('№{}: {}'.format(idx+1,img_name))
        XY= []
        for line in f: 
            data = []
            #print(line)
            data.append([float(x) for x in line.split()])
            if data: #если файл не пустой
                class_id = int(data[0][0])
                print(class_id)
                print(names[class_id])
                XY = data[0][1:] #список - только координаты
                for i in range(len(XY)):
                    if i%2==0:
                        XY[i] = round(XY[i]*W,2)
                    else:
                        XY[i] = round(XY[i]*H,2)
                polygon = XY

                draw.polygon(polygon,outline=(0,255,0), width=5)
            else:
                pass
        plt.imshow(img)

        
        f.close()
        plt.show()

def visualize_txt_YOLO_detect(txt_folder, cat_name, names,images_folder):
    """Takes images that only belong to a specific cat_name class. 
    Displays the file name, class id and class name"""

    for i in tqdm(range(len(os.listdir(txt_folder)))):
        txt = os.listdir(txt_folder)[i]
        txt_file = os.path.join(txt_folder,txt)

        #don't open empy files
        if os.path.getsize(txt_file) < 10:
                continue
        try:        
            f = open(txt_file,'r')
            
        except:
            print('что-то пошло не так', txt)
            
        for line in f:
            stroka = line.split(' ')
            category_id = stroka[0]
            if names[int(category_id)]==cat_name:
        
                x_center,y_center,w,h = float(stroka[1]),float(stroka[2]),float(stroka[3]),float(stroka[4])
                x_center = int(x_center*1280)
                y_center = int(y_center*1024)
                W = int(w*1280)
                H = int(h*1024)
                x = x_center - W/2
                y = y_center - H/2
                img_name = txt.split('.')[0] + '.jpg'
                print(names[int(category_id)])
                print(img_name)
                
                fig, ax = plt.subplots()
                img = mpimg.imread(os.path.join(images_folder,img_name))
                ax.imshow(img)
                rect = patches.Rectangle((x, y), W, H, linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
            else:
                pass
            plt.show()
        f.close()

if __name__ == "__main__":
    #V2
    names= [ "films",
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

    path_seg = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\test_dataset'
    txt_path_seg = r'C:\Personality\Stady\Lab_CV\Create_dataset\V2\test_labels_v2'

    visualize_txt_YOLO_segmentation(txt_path_seg, path_seg, names)

    cat_name = 'PS'
    images_folder_detect = r'C:\Users\annai\Jupyter\create_dataset\training\test\images'
    txt_folder_detect = r'C:\Users\annai\Jupyter\create_dataset\training\labels'
    visualize_txt_YOLO_detect(txt_folder_detect, cat_name, names, images_folder_detect)