#!/usr/bin/python
import os
import json
import sys
import  random
import  json


workspace = '/home/yxsong/Downloads/dataset/bebi/'
Campaign = '135139'
nds_ratio = 0.03
# we will use the code to negative downsampling

Trainfile = workspace+Campaign+'/'+Campaign+'train.log.txt'
Sampling_file = workspace+Campaign+'/'+Campaign+'train_sampling.txt'

fi = open(Trainfile,'r')
fo = open(Sampling_file,'w')

for line in fi:
    #obj = json.loads(line)
    if '"click": "1"' in line:
        fo.write(line)
    else:
        Random_number = random.random()
        if Random_number<0.03:
            fo.write(line)

fi.close()
fo.close()






















