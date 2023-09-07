# Create images_dataset and labels_txt
## 1. Original data:
Data partitioning was done on simplified terms and the original json files created in the CVAT tool did not have class names, only names 1 and 2, showing 1 - object is fully visible and object is closed. The class name was reflected in the file name, for example, LDPE_film_test.json. Therefore, it was necessary to create a separate dictionary reflecting which garbage class was labeled in which json file. 
# Preparing json to merging
# Image dataset creation
# Сhange numeration of categories in test json
# Visualize json annotation
# Convert COCO json to YOLO txt
# Visualize txt YOLO annotation
