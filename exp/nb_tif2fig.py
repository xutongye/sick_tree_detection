
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###
#################################################
# file to edit: dev_nb/tif2fig.ipynb

#================================================
import numpy as np


#================================================
import tifffile as tiff


#================================================
import cv2


#================================================
def to_8bit(x):
    '''
    把x内的像素值转换到[0,255]范围。
    --------------------
    input:
    x: 一个array，维度为[h,w,3]，其中最后一个维度的三个通道为 R,G,B
    --------------------
    return: 一个array，维度与x一致，但是像素值被转换到了[0,255]范围
    --------------------
    '''
    chmax = x.max(axis=(0,1))
    chmin = x.min(axis=(0,1))
    x = (x-chmin)/(chmax-chmin)*255
    x = x.astype(np.uint)
    return x


#================================================
def tif2rgb(x,rgb=[2,1,0]):
    '''
    把x转换为rgb图像。
    -----------------------
    input:
    x: 一个array，维度为[c,h,w]，其中第一个维度的通道数c>=3
    rgb: 把x的哪3个通道作为rgb通道来可视化，[2,1,0] or [3,2,1]
    -----------------------
    return: 一个array，维度为[h,w,3]，通道为R,G,B，且像素值在[0,255]范围
    '''
    x = x.transpose((1,2,0))
    x = x[...,rgb]
    x = to_8bit(x)
    x = x.astype(np.uint)
    return x


#================================================
def tif2mask(x,mask_value=255):
    '''
    把x转换为单通道mask.
    --------------------------
    input:
    x: 一个array，维度为[c,h,w]，其中第一个维度的通道数c>=1，其中值>0的像素为mask
    mask_value：在输出中，mask像素的值设置为mask_value
    --------------------------
    return: 一个array，维度为[h,w]，mask像素值为mask_value，其它像素值为0
    '''
    x = x.transpose((1,2,0))
    x = x[...,0]
    x[x>0] = mask_value
    x = x.astype(np.uint)
    return x


#================================================
def save_tif_as_fig(tif_fn, fig_fn, rgb=[2,1,0], is_mask=False, mask_value=255):
    '''
    把tif文件转换并保存为图像文件。
    ------------------------------------
    input:
    tif_fn: tif文件的路径
    fig_fn：要保存的图像文件的路径
    rgb: 把tif中的哪3个通道作为rgb通道来可视化，[2,1,0] or [3,2,1]
    is_mask：是否mask
    mask_value：若is_mask=True，则mask像素值设置为mask_value
    '''
    tif = tiff.imread(tif_fn)
    if is_mask:
        fig = tif2mask(tif, mask_value)
    else:
        fig = tif2rgb(tif, rgb=[2,1,0])
    cv2.imwrite(fig_fn, fig)
