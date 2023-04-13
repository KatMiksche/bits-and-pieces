# Exploratory Data Analysis - dataset

import multiprocessing as mp
from multiprocessing import pool
import os
from os import listdir, walk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skimage.io import imread, imshow
from skimage import filters, feature
from skimage.util import compare_images
from skimage.transform import resize
import imagehash
from PIL import Image

from datetime import datetime

def read_files(folder, NamesOnly=False):
    subdir=False
    if (input('Do you want to read all subdirectories as well? y/n   ')=='y'): subdir=True
    res = []
    for (dir_path, dir_names, file_names) in walk(folder):
        if dir_path[-1]!='/': dir_path+='/'
        for item in file_names: 
            type=item[item.find('.')+1:len(item)].upper()
            if type in ('JPEG', 'BMP', 'TIFF', 'JPG', 'PNG'): 
                if NamesOnly==False: res.append(dir_path+item)
                else: res.append(item)
        if subdir!=True: break
    #print(res)
    return res

def hash_image(full_path):
    hash_value=str(imagehash.phash(Image.open(full_path)))
    return [full_path, hash_value]

def pool_hashing(folder):
    print(datetime.now(), 'Reading files')
    files=read_files(folder)
    print(datetime.now(), 'Initiating pool of hashing')
    pool = mp.Pool(mp.cpu_count()-1)
    hashes = pool.map(hash_image, files) #(os.path.join(folder, image) for image in os.listdir(folder)))
    pool.close()
    pool.join()
    print(datetime.now(),'pool finished, ',len(hashes), 'hashes generated')
    return hashes

def pool_load_compare_images(duplicates):
    print(datetime.now(), 'Initiating pool of loading and comparing images')
    pool = mp.Pool(mp.cpu_count()-1)
    lst_of_arrays = pool.map(load_compare_images, duplicates)
    pool.close()
    pool.join()
    print(datetime.now(),'pool finished')
    return lst_of_arrays

def load_compare_images(lst):
    #print('list compared:',lst)
    lst_images=[]
    duplicates=[]
    for i in range(0,len(lst)):
        temp_image=imread(lst[i])
        temp_image=resize(temp_image,(512, 496))
        duple=False
        for picture in lst_images:
            difference = compare_images(temp_image, picture, method='diff')
            if difference.mean()==0:
                duple=True
                break
        if duple==True: duplicates.append(lst[i])
        else: lst_images.append(temp_image)
        if len(lst_images)>2: print('len of unique images',len(lst_images))
        #print ('iteration',i,'identified duplicates',duplicates)
    return duplicates

def clear_hashes(hashes):

    print(datetime.now(), 'Sorting hashes')
    sorted_hashes=sorted(hashes, key=lambda x: x[1])

    print(datetime.now(), 'Finding duplicate hashes')   
    for i in range(0,len(sorted_hashes)):
        
        duple=False
        
        try: 
            if sorted_hashes[i][1]==sorted_hashes[i+1][1]: duple=True
        except: pass
        else: pass
                    
        try: 
            if sorted_hashes[i][1]==sorted_hashes[i-1][1]: duple=True
        except: pass
        else: pass
        
        if duple==False: sorted_hashes[i][0]=0
    
    for i in range(len(sorted_hashes) - 1, -1, -1):
        if sorted_hashes[i][0]==0: del sorted_hashes[i]
    print(len(sorted_hashes),'hashes with duplicity')
    
    return sorted_hashes

def solve_duplicates(hashes):
        
    hashes=clear_hashes(hashes)
    
    print(datetime.now(), 'Generating list of duplicate files as per hashes')
    duplicates=[]
    currenthash=''
    for item in hashes:
        if item[1]!=currenthash:
            currenthash=item[1]
            duplicates.append([item[0]])
        else:
            duplicates[len(duplicates)-1].append(item[0])
 
    duplicate_images=pool_load_compare_images(duplicates)
    
    count=0
    for item in duplicate_images: count+=len(item)
    if input('{} duplicate images found. Do you want to see the list? y/n    '.format(count))=='y':
        for item in duplicate_images:
           for member in item: print(member)
           print('///')
    
    if input('Do you want to delete duplicate files? y/n     ')=='y':
        for lst in duplicates:
            for item in lst: os.remove(item)
        duplicates=[]
    return duplicate_images
    


def duplicates_check(folder):
    print(datetime.now(),'Initiating duplicates check for image files in folder',folder)
    hashes=pool_hashing(folder)
       
    
    if len(hashes)==len(set([i[1] for i in hashes])):                                     
        print('No duplicates found')
    else: 
        print('Duplicates in dataset!')
        duplicates=solve_duplicates(hashes)

        



 
# get number of cases and histogram of groups
def case_statistics(folder):
    print(datetime.now(),'Initiating case statistics for image files in folder',folder)
    files=read_files(folder, NamesOnly=True)
    groups=[]
    for image in files:
        groups.append(image[0:image.find('-')])
    plt.hist(groups)
    plt.title("Histogram of groups - {} files".format(len(groups)))
    plt.show()


if __name__ == '__main__':
    #duplicates_check('C:/Users/Kat/Desktop/New folder/')
    duplicates_check('dataset/train-test/')
    #duplicates_check('dataset/validation/')
    #case_statistics('dataset/validation/')
    #case_statistics('dataset/train-test/')