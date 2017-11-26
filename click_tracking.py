#!/usr/bin/python
import os
import json

#workspace = '/home/yxsong/Downloads/dataset/bebi/'
workspace = '/home/yxsong/Dataset/Ads/bebi/2017.2/'
click_space = workspace+'clicks/'
impression_space = workspace+'impressions/'
all_space = workspace+'all/'
#date = ['first','second'] #can be changed according to the real situation
date = ['20170222','20170223','20170224','20170225','20170226','20170227','20170228','20170301','20170302']
Split_Campaigns=['3','135139','135059','134848']

Testdate = '20170302'

Campaign_Fos={}   #use to store the fout

#create the split campaign folder
for campaign in Split_Campaigns:
    if not os.path.exists(workspace+campaign):
        os.makedirs(workspace+campaign)

os.makedirs(workspace+'all')

for every_day in date:
    dict ={}
    for file in os.listdir(click_space+every_day+'/'):
        infile = open(click_space+every_day+'/'+file,'r')
        for line in infile:
            obj=json.loads(line)
            dict[obj['impression_id']]=1
        infile.close()\
    #make single days dict for the click join operation
    if every_day!='20170302':
        #last day to test
        train_test = 'train'
    else:
        train_test = 'test'
    all_outfile = 'all'+train_test
    if all_outfile not in Campaign_Fos:
        Campaign_Fos[all_outfile] = open(all_space+all_outfile+'.log.txt','w')
    #join every days impression and click
    Click_cnt = 0
    for file in os.listdir(impression_space+every_day+'/'):
        infile = open(impression_space + every_day + '/' + file, 'r')
        for line in infile:
            obj=json.loads(line)
            if obj['campaign_id'] in  Split_Campaigns:
                Current_File = obj['campaign_id']+train_test
                if Current_File not in Campaign_Fos:
                    Campaign_Fos[Current_File] = open(workspace+'/'+obj['campaign_id']+'/'+Current_File+'.log.txt','w')
            if obj['impression_id'] in dict:
                obj['click']='1'
                Click_cnt = Click_cnt+1
            else:
                #print "none"
                obj['click']='0'
            String_obj = json.dumps(obj)
            Campaign_Fos[all_outfile].write(String_obj+'\n')
            if obj['campaign_id'] in Split_Campaigns:
                Campaign_Fos[Current_File].write(String_obj+'\n')
        infile.close()
    print len(dict),'   ' ,Click_cnt

for output in Campaign_Fos.keys():
    Campaign_Fos[output].close()