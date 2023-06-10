import os
import imageio.v2 as imageio
import matplotlib
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
import numpy as np
import os
import pandas as pd
import copy
import os.path

def fname2int(fname):
    int_s = int(fname[9:].replace('.bmp', ''))
    return int_s


def list_images(root):
    filenames = next(os.walk(root), (None, None, []))[2]
    filenames.sort(key=fname2int)
    filenames = [os.path.join(root, f) for f in filenames if '.bmp' in f]
    return filenames


def read_bmp_image(pth):
    img = imageio.imread(pth)
    return img


def find_peaks_value(img, line_length): #на выходе словарь, где ключ - линия, значение - массив[канал пика, высота пика]
    peaks_columns = {} 
    for c in range(line_length): 
        peak_value = []
        line = img[:, c] # все значения на одной линия(значения всех каналов)
        peaks, _ = find_peaks(line, threshold = 6)
        value = line[peaks]
        if peaks.size > 0:
            peak_value.append(peaks)
            peak_value.append(value)
            peaks_columns[c]= peak_value

    return peaks_columns

def denoise(img, peaks_columns): #создает копию изображения, где вместо пиков - среднее значение от соседних каналов

    img_new = copy.copy(img)
    for i in list(peaks_columns.keys()):
        line = img_new[:, i] # все значения на одной линия(значения всех каналов)
        value = peaks_columns[i] #номер канала, где пик и его значение
        if value[0].size > 0:
            channel = value[0][0] #номер канала
            value = value[1][0] #значение пика
            avg_val = (line[channel - 1] + line[channel + 1])/2
            # print('avg_val = ', avg_val)
            # print('before = ', img_new[:, i][channel])
            img_new[:, i][channel] = avg_val
            # print('after = ',avg_val)
            # print('------------------')
        else:
            continue
    return img_new


def visualise(img,line_length):
    previous_line = None
    inline_correlation = list()
    for c in range(line_length): 
        line = img[:, c] 
        if previous_line is not None:
            correlate_result = np.correlate(previous_line-previous_line.mean(), line-line.mean(), 'full')
            max_corr = max(correlate_result)
            inline_correlation.append(max_corr)
        previous_line = line
        
        plt.plot(line, c=cmap(c/line_length))
        
        
    plt.title('Spectras for single line on denoizing image')
    plt.show()


if __name__ == "__main__":

    data_img = input("name of folder with FX files to clean:")
    path_class_0 = 'Z:/CV/light_data/0_class/FX'

    images_names = list_images(data_img)
    images = [read_bmp_image(i) for i in images_names]

    ref_class_0 = list_images(path_class_0)
    ref = [read_bmp_image(i) for i in ref_class_0]
   
    line_length = 640
    gt_line = ref[0][:, 300]
    threshold = 10
    final_count = []
    for i in range(len(images)):

        img_name = images_names[i]
        img_i = images[i]
        line_val = []

        for c in range(line_length):
            line_class = img_i[:, c]
            mse1 = ((line_class - gt_line)**2).mean()
            line_val.append(mse1)

        count_1_class = 0
        for value in line_val:
            if value > threshold: #если расстояние больше 10, то линии не относятся к фону
                count_1_class = count_1_class + 1
                
        final_count.append(count_1_class)

        #print('{}) {}: {}'.format(i, img_name, count_1_class))

        if count_1_class == 0:
            os.remove(images_names[i])

    zero_count = len(final_count) - np.count_nonzero(final_count)
    print('in the end, {} files out of {} were deleted'.format(zero_count,len(images_names)))