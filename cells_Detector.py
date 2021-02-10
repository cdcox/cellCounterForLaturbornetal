# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 09:29:07 2020

@author: colorboxy
"""
import skimage.io
import matplotlib.pyplot as plt
import numpy as np
import os
from skimage.filters import threshold_niblack, gaussian, threshold_isodata, threshold_li,threshold_mean,threshold_minimum,threshold_otsu,threshold_triangle,threshold_yen
import skimage.util
import PIL
from skimage.segmentation import watershed
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.measure import label, regionprops
import xlrd
import csv
from skimage import draw

class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def mask_save(thresh,addendum):
    binary = np.array(iamge >=thresh).astype('uint8')*255
    skimage.io.imsave(addendum+'.jpg',binary)

final = AutoVivification()
directory = r'.'
image_dir = os.path.join(directory,'cropped_sample_images')
book = xlrd.open_workbook(os.path.join(directory,r'DonorInformation filtered by availability of ISH.xls'))
xl_sheet = book.sheet_by_index(0)
name_col = xl_sheet.col_values(1)
diagnosis_col = xl_sheet.col_values(17)

file_list = os.listdir(image_dir)
cell_thresh = 10
for file_name in file_list:
    full_path = os.path.join(image_dir,file_name)
    patient_info = file_name.split('_')
    patient_name = patient_info[0]
    antibody = patient_info[1]
    diagnosis_temp = [xn for xn,x in enumerate(name_col) if patient_name in x]
    diagnosis = diagnosis_col[diagnosis_temp[0]]
    PIL.Image.MAX_IMAGE_PIXELS = 933120000
    image = skimage.io.imread(full_path,as_gray=True)
    image = skimage.util.invert(image)
    block_size = 35
    iamge = gaussian(image, sigma = 2)
    iamge = gaussian(image, sigma = 3)
    thresh = threshold_yen(iamge)
    #mask_save(thresh, 'yen3')
    
    binary = iamge >=thresh
    
    labeled_image = label(binary)
    
    region_props = regionprops(labeled_image)
    
    areas = [x.area for x in region_props]
    areas = np.array(areas)
    filt_areas = areas
    filt_areas[filt_areas>200] = 200
    centroid = [x.centroid for x in region_props]
    centroid = np.array(centroid)
    cell_count = np.sum(areas>cell_thresh)
    final[diagnosis][patient_name][antibody]['cell count'] = cell_count
    final[diagnosis][patient_name][antibody]['image area'] = np.shape(image)[0]*np.shape(image)[1]
    '''
    image = skimage.util.invert(image)
    image_red=np.copy(image)
    for inn,i in enumerate(centroid):
        [rr,cc]=draw.circle(i[0],i[1],2,np.shape(image))
        image_red[rr,cc]=1
        image[rr,cc]=0

    outi=np.zeros([np.shape(image)[0],np.shape(image)[1],3])
    outi[:,:,0]=image
    outi[:,:,1]=image_red
    outi[:,:,2]=image_red
    plt.imsave(file_name+'reddot.jpg',outi)
    '''    
    print(file_name)

    
output_file = open("outfile"+str(cell_thresh)+".csv","w",newline='')
writer = csv.writer(output_file)
writer.writerow(['Diagnosis','name','GAT1 count','GAT1 area','vGluT1 count','vGluT1 area'])
for key, value in final.items():
    for key2, value2 in value.items():
        setter = [key, key2, value2['GAT1']['cell count'],value2['GAT1']['image area'],value2['vGluT1']['cell count'],value2['vGluT1']['image area']]
        writer.writerow(setter)
output_file.close()