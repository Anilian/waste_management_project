# Create images_dataset and labels_txt
## 1. Original data:
Data partitioning was done on simplified terms and the original json files created in the CVAT tool did not have class names, only names 1 and 2, showing 1 - object is fully visible and object is closed. The class name was reflected in the file name, for example, LDPE_film_test.json. 
```bush                           
$ folder 1
.
├── images
│   ├── Металл_test
│   ├── PET_бутылочный_масло_test
│   ├── LLDPE_пленка_test
│   └── Тетрапак_test
│   └── ...
│
├── json
│   ├── Металл_test.json
│   ├── PET_бутылочный_масло_test.json
│   ├── LLDPE_пленка_test.json
│   └── Тетрапак_test.json
│   └── ...

```

## 2. Preparing json to merging
Therefore, it was necessary to create a separate dictionary reflecting which garbage class was labeled in which json file. 
In the [prepare_data_merging.py](https://github.com/Anilian/waste_management_project/blob/main/dataset_creation/prepare_data_merging.py) presents such a dictionary, which is accessed by the **rename_category** function. It changes category names after labeling and deleting labels for a overlapping category category. After that, the **merging_json** function is passed the path to the folder where the json files lie and it will merge them into one, creating a new numbering in the categories and annotations. The code also takes into account that the path to the folder may have been saved in the file description in json, which you need to get rid of, as it will interfere with the opening of files
## 3. Image dataset creation
The **transfer_images** function transfers images from the original split folders to one final folder. To check if all images are counted in the final json file, the def count_image_json function passes a list of all images. This list will be compared with the list of images from the folder by the **cheak_difference** function. [generate_image_dataset_from_json.py](https://github.com/Anilian/waste_management_project/blob/main/dataset_creation/generate_image_dataset_from_json.py)
## 4. Сhange numeration of categories in test json
According to the code from point 2, you can make merged json for test and for train, but the numbering of classes will be different in them, to fix this, you need a [test_json_correct.py](https://github.com/Anilian/waste_management_project/blob/main/dataset_creation/test_json_correct.py). The actual dictionary with idx of categories as key and name as value is passed to it. Using the **correct_cat_idx** function in the current json, the numbering of categories in the catherogy section and in the annotation section is changed.

## 5. Visualize json annotation
[visualize_dataset_COCO.py](https://github.com/Anilian/waste_management_project/blob/main/dataset_creation/visualize_dataset_COCO.py)
Using pycocotools library you can display markup on images from a json file. This is necessary to check if the json is merged into one (correct file numbering, correct category id, and correct markup). There are three functions in the code: **look_same_class**, to which you need to pass the name of a certain class; **look_same_image**, which displays images from a certain range and also a function displaying all images **all_image**.
## 6. Convert COCO json to YOLO txt
Before translating COCO annotations to YOLO txt, we need to get rid of the RLE encoding of the annotations. They occur intermittently in the markup and make coordinate translation to txt impossible.  Therefore it is necessary to clean json from such annotations using the script [RLE_COCO.py](https://github.com/Anilian/waste_management_project/blob/main/dataset_creation/RLE_COCO.py)
After that you can translate COCO annotations to txt. If there was a sigmentation task, you should use the **create_txt_segmentation** function from the file [COCO_json_YOLO_txt.py](https://github.com/Anilian/waste_management_project/blob/main/dataset_creation/COCO_json_YOLO_txt.py). If the task is detection, then in the same script there is a function **create_txt_detection**, which uses the pylabel library to generate txt. Also Yaml file is generated for dataset, which is not correct for YOLOv8 becouse it is for YOLOv5. However, you can get the list of categories from there.

## 7. Visualize txt YOLO annotation
The txt labels obtained in the previous step are also worth visualizing and verifying. The code [visualize_YOLO_txt.py](https://github.com/Anilian/waste_management_project/blob/main/dataset_creation/visualize_YOLO_txt.py) with two functions **visualize_txt_YOLO_segmentation** and **visualize_txt_YOLO_detect** is intended for this purpose.  The first one displays all images, while the second one displays a certain category. Both functions require the dataset img path and txt labels folder path as input. 
