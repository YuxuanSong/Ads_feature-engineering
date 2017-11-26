#!/usr/bin/python
import os
import json

#workspace = '/home/yxsong/Downloads/dataset/bebi/'
workspace = '/home/yxsong/Dataset/Ads/data/2017.2/'
click_space = workspace+'clicks/'
impression_space = workspace+'impressions/'
#all_space = workspace+'all/'
#date = ['first','second'] #can be changed according to the real situation
date = ['20170222','20170223','20170224','20170225','20170226','20170227','20170228','20170301','20170302']
#Campaign_Fos={}   #use to store the fout

#create the split campaign folder
# for campaign in Split_Campaigns:
#     if not os.path.exists(workspace+campaign):
#         os.makedirs(workspace+campaign)

#os.makedirs(workspace+'all')
dict = {}
Missing_imp = 'miss_clicks'

fo = open(workspace+Missing_imp,'w')

for every_day in date:
    for file in os.listdir(click_space+every_day+'/'):
        infile = open(click_space+every_day+'/'+file,'r')
        for line in infile:
            obj=json.loads(line)
            dict[obj['impression_id']]=0
        infile.close()\
    #make single days dict for the click join operation

    #join every days impression and click
    Click_cnt = 0
    for file in os.listdir(impression_space+every_day+'/'):
        infile = open(impression_space + every_day + '/' + file, 'r')
        for line in infile:
            obj=json.loads(line)
            if obj['impression_id'] in dict:
                Click_cnt = Click_cnt+1
                dict[obj['impression_id']] = dict[obj['impression_id']] + 1
        infile.close()

print len(dict),'   ' ,Click_cnt

for imp in  dict.keys():
    if dict[imp] == 0:
        fo.write(imp+'\n')

fo.close()



