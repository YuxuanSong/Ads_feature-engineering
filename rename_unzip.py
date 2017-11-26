#!/usr/bin/python
import os
import json
import gzip

workspace = '/home/yxsong/Downloads/dataset/bebi/'
click_space = workspace+'clicks/'
impression_space = workspace+'impressions/'
#all_space = workspace+'all/'
date = ['20170222','20170223','20170224','20170225','20170226','20170227','20170228','20170301','20170302']
#Campaign_Fos={}
#use to store the fout

count = {}

for every_day in date:
    for file in os.listdir(click_space + every_day + '/'):
        os.rename(click_space + every_day + '/'+file,click_space + every_day + '/'+file+'.gz')
    for file in os.listdir(impression_space+every_day+'/'):
        os.rename(impression_space+every_day+'/'+file,impression_space+every_day+'/'+file+ '.gz')


print count



