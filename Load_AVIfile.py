#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 09:21:55 2020

@author: Jaidip Jagtap
"""
import numpy as np
import cv2
from glob import glob
import os
import nibabel as nib

input_dir='Avi_mediafolder/'
files=glob(input_dir+'*.avi')# also take pathname

oldprefix = '.avi' #_mask.npy
strremove = -len(oldprefix)

for each in files:
    cap = cv2.VideoCapture(each)
    frameCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    data= np.empty((frameHeight, frameWidth,frameCount), np.dtype('uint8'))
    k=0
    
    while(k < frameCount  and cap.isOpened()):
      ret, frame = cap.read()
      
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      cv2.imshow('frame',gray)
      
      
      frame1=np.expand_dims(gray, 2)
      data[:,:,k:k+1]=frame1
      k += 1      
      print(np.mean(frame1))
      #np.append(frame1, frame1[:,:,:,0,np.newaxis], axis=3)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 

    data1=data
    # data2=data[:,:,::-1]
    # x1=round(frameCount*(1/3))
    # data1=data2[:,:,x1:frameCount]
    
    cap.release()
    cv2.destroyAllWindows()
    
    data=data.astype('float32')
    nifti2 = nib.Nifti1Image(data1, np.eye(4))
    nifti2.to_filename(each[:strremove]+'.nii.gz')
    #np.save(each[:strremove]+'.npy', data)
