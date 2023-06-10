from torchvision import datasets, transforms, models
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import pandas as pd
from torchvision.io import read_image
from PIL import Image
import torchvision.transforms as transforms
import os
from os import listdir
import time



def predict(img, model):
    img = transform(img).to(device)
    img = torch.unsqueeze(img, 0)
    yhat = model(img)
    index = yhat.data.cpu().numpy().argmax()

    return index  



if __name__ == "__main__":

    #load the model
    clf = models.resnet18(pretrained = False)
    num_ftrs = clf.fc.in_features 
    clf.fc = nn.Linear(num_ftrs, 2) 

    clf = clf.to('cuda')
    opt = torch.optim.SGD(clf.parameters(),  lr=0.001, momentum=0.9, nesterov=True,)
    criterion = nn.CrossEntropyLoss()

    #load weight for model
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    file_path = '/content/drive/MyDrive/CV/weight_model_18_10.pth'
    clf.load_state_dict(torch.load(file_path))
    clf.eval()


    transform = transforms.Compose([
    transforms.Resize(256),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    folder_dir = input("name of folder with GP files to clean:")
    
    for images in os.listdir(folder_dir):
        if images not in list_images:
        list_images.append(images)
        file_path = os.path.join(folder_dir, images)
        image = Image.open(file_path)
        image = image.resize((256,256))
        label = predict(image,clf)
        if label == 0:
            os.remove(file_path)