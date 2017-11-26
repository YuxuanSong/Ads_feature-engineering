#!/usr/bin/python
import os
import json
import sys
import  random
import  json


workspace = '/home/yxsong/Downloads/dataset/data/'
Campaign = '135139'

# we will use the code to shaffle train data

Sampling_file = workspace+Campaign+'/'+Campaign+'train.yzx.txt'
Shaffle_file = workspace+Campaign+'/'+Campaign+'train.yzx.shaffle.txt'

fi = open(Sampling_file,'r')
fo = open(Shaffle_file,'w')
Data_List = []
for line in fi:
    #obj = json.loads(line)
    Data_List.append(line)

Index_list =range(len(Data_List))

random.shuffle(Index_list)

for idx in Index_list:
    fo.write(Data_List[idx])

fi.close()
fo.close()

