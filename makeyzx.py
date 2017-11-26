#!/usr/bin/python
#Cause there is no maeket price in our dataset so I will not reallyn make the yzx file
import  utils as ut
import  json
import  operator
import sys

reload(sys)

sys.setdefaultencoding('utf-8')


workspace = '/home/yxsong/Downloads/dataset/data/'
#Campaign = sys.argv[1]
Campaign = '135139'

Train_log = workspace+Campaign+'/'+Campaign+'train_sampling.txt'
Test_log = workspace+Campaign+'/'+Campaign+'test.log.txt'
Feature_file = workspace + Campaign+'/'+Campaign+'featindex.txt'

Train_yzx = workspace+Campaign+'/'+Campaign +'train.yzx.txt'
Test_yzx = workspace+Campaign+'/'+Campaign +'test.yzx.txt'


namecol = {}
featindex = {}

featcount = {}   #filter the unpopular features by  a count dict/  only the features appear more than 10 times will be used for us
Main_schema = [u'ad_call_index', u'placement_id', u'campaign_id', u'is_iframe', u'country_code', u'timezone',  u'page_referrer', u'creative_id', u'charset', u'is_crawler', u'publisher_id',  u'advertiser_id', u'mediation_priority_item_id',  u'tsource', u'session_call_count', u'page_url'] #u'session_call_count',

device_schema = [u'browserVersion', u'screenColors', u'platformName', u'releaseYear',  u'platformVersion', u'browserName', u'priceBand', u'hardwareVendor', u'hardwareFamily', u'browserVendor', u'browserSize', u'screenResolution', u'type', u'hardwareModel']

Modified_schema = ['timestamp']

multi_field = [u'plugins']

fi = open(Train_log,'r')
for line in fi:
    obj = json.loads(line)
    #print len(obj),len(obj['device'])
    for field in Main_schema:
        if field in obj:
        #Newfeat = field +':'+obj[field]
            Newfeat = field + ':' + str(obj[field])
            if Newfeat not in featcount:
                featcount[Newfeat] = 1
            else:
                featcount[Newfeat] = featcount[Newfeat] + 1

    for field in device_schema:
        if field in obj['device']:
            Newfeat = field + ':' + obj['device'][field]
            if Newfeat not in featcount:
                featcount[Newfeat] = 1
            else:
                featcount[Newfeat] = featcount[Newfeat] + 1


    for field in multi_field:
        if 'plugins' in obj['device']:
            featlist = obj['device']['plugins']
            for f in featlist:
                Newfeat = field + ':' + f
                if Newfeat not in featcount:
                    featcount[Newfeat] = 1
                else:
                    featcount[Newfeat] = featcount[Newfeat] + 1


    for field in Modified_schema:
        if field == 'timestamp':
            Newfeat = 'weekday:' + ut.time_modifier(obj[field], obj['timezone'])[0]
            if Newfeat not in featcount:
                featcount[Newfeat] = 1
            else:
                featcount[Newfeat] = featcount[Newfeat] + 1
            Newfeat = 'hour:' + ut.time_modifier(obj[field], obj['timezone'])[1]
            if Newfeat not in featcount:
                featcount[Newfeat] = 1
            else:
                featcount[Newfeat] = featcount[Newfeat] + 1
        else:
            Newfeat = field + ut.FeatureTrans(field, obj[field])
            if Newfeat not in featcount:
                featcount[Newfeat] = 1
            else:
                featcount[Newfeat] = featcount[Newfeat] + 1
fi.close()

maxindex = 0
### truncate/ initialize
featindex['truncate']= maxindex
maxindex = maxindex + 1
#multi field ====> plugins

###initialize the lines
for field in Main_schema:
    featindex[field+':other']= maxindex
    maxindex = maxindex + 1

for field in device_schema:
    featindex[field+':other']= maxindex
    maxindex = maxindex + 1

for field in multi_field:
    featindex[field + ':other'] = maxindex
    maxindex = maxindex + 1

for field in Modified_schema:
    if field == 'timestamp':
        featindex['weekday:other'] = maxindex
        maxindex = maxindex+1
        featindex['hour:other'] = maxindex
        maxindex = maxindex+1

#indexing--------------------------
print "indexing"
fi = open(Train_log,'r')
for line in fi:
    obj = json.loads(line)
    for field in Main_schema:
        if field in obj:
            Newfeat = field + ':' + str(obj[field])
            if Newfeat not in featindex and featcount[Newfeat] >= 10:
                featindex[Newfeat] = maxindex
                maxindex = maxindex + 1

    for field in device_schema:
        if field in obj['device']:
            Newfeat = field + ':' + obj['device'][field]
            if Newfeat not in featindex and featcount[Newfeat]>=10:
                featindex[Newfeat] = maxindex
                maxindex = maxindex + 1

    for field in multi_field:
        if 'plugins' in obj['device']:
            featlist = obj['device']['plugins']
            for f in featlist:
                Newfeat = field + ':' + f
                if Newfeat not in featindex and featcount[Newfeat] >= 10:
                    featindex[Newfeat] = maxindex
                    maxindex = maxindex + 1

    for field in Modified_schema:
        if field == 'timestamp':
            Newfeat = 'weekday:' + ut.time_modifier(obj[field], obj['timezone'])[0]
            if Newfeat not in featindex and featcount[Newfeat] >= 10:
                featindex[Newfeat] = maxindex
                maxindex = maxindex + 1
            Newfeat = 'hour:' + ut.time_modifier(obj[field], obj['timezone'])[1]
            if Newfeat not in featindex and featcount[Newfeat] >= 10:
                featindex[Newfeat] = maxindex
                maxindex = maxindex + 1
        else:
            Newfeat = field + ut.FeatureTrans(field, obj[field])
            if Newfeat not in featindex and featcount[Newfeat] >= 10:
                featcount[Newfeat] = maxindex
                maxindex = maxindex + 1
fi.close()

print 'Feature Size: ' + str(maxindex)
featvalue = sorted(featindex.iteritems(), key=operator.itemgetter(1))
fo = open(Feature_file, 'w')
for fv in featvalue:
    fo.write(fv[0] + '\t' + str(fv[1]) + '\n')
fo.close()


print 'start to index train data'
fi = open(Train_log,'r')
fo = open(Train_yzx,'w')
for line in fi:
    obj = json.loads(line)
    click = obj['click']
    fo.write(str(click)+' '+str(featindex['truncate'])+':1 ')
    for field in Main_schema :
        if field in obj:
            Newfeat = field + ':' + str(obj[field])
            if Newfeat in featindex:
                fo.write(' '+str(featindex[Newfeat]) + ':1' )
            else:
                otherfeat = field + ':other'
                fo.write(' '+str(featindex[otherfeat]) + ':1')

    for field in device_schema:
        if field in obj['device']:
            Newfeat = field + ':' + obj['device'][field]
            if Newfeat in featindex:
                fo.write(' '+str(featindex[Newfeat]) + ':1' )
            else:
                otherfeat = field + ':other'
                fo.write(' '+str(featindex[otherfeat]) + ':1')

    for field in multi_field:
        if 'plugins' in obj['device']:
            featlist = obj['device']['plugins']
            for f in featlist:
                Newfeat = field + ':' + f
                if Newfeat in featindex:
                    fo.write(' ' + str(featindex[Newfeat]) + ':1')
                else:
                    otherfeat = field + ':other'
                    fo.write(' ' + str(featindex[otherfeat]) + ':1')

    for field in Modified_schema:
        if field == 'timestamp':
            Newfeat = 'weekday:' + ut.time_modifier(obj[field], obj['timezone'])[0]
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = 'weekday'+ ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')
            Newfeat = 'hour:' + ut.time_modifier(obj[field], obj['timezone'])[1]
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = 'hour'+ ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')
        else:
            Newfeat = field + ut.FeatureTrans(field, obj[field])
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = field + ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')

    fo.write('\n')
fi.close()
fo.close()


print "start to index test data"

fi = open(Test_log, 'r')
fo = open(Test_yzx, 'w')
for line in fi:
    obj = json.loads(line)
    click = obj['click']
    fo.write(str(click) + ' ' + str(featindex['truncate']) + ':1 ')
    for field in Main_schema:
        if field in obj:
            Newfeat = field + ':' + str(obj[field])
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = field + ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')

    for field in device_schema:
        if field in obj['device']:
            Newfeat = field + ':' + obj['device'][field]
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = field + ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')

    for field in multi_field:
        if field in obj['device']:
            featlist = obj['device']['plugins']
            for f in featlist:
                Newfeat = field + ':' + f
                if Newfeat in featindex:
                    fo.write(' ' + str(featindex[Newfeat]) + ':1')
                else:
                    otherfeat = field + ':other'
                    fo.write(' ' + str(featindex[otherfeat]) + ':1')

    for field in Modified_schema:
        if field == 'timestamp':
            Newfeat = 'weekday:' + ut.time_modifier(obj[field], obj['timezone'])[0]
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = 'weekday'+ ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')
            Newfeat = 'hour:' + ut.time_modifier(obj[field], obj['timezone'])[1]
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = 'hour' + ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')
        else:
            Newfeat = field + ut.FeatureTrans(field, obj[field])
            if Newfeat in featindex:
                fo.write(' ' + str(featindex[Newfeat]) + ':1')
            else:
                otherfeat = field + ':other'
                fo.write(' ' + str(featindex[otherfeat]) + ':1')

    fo.write('\n')
fi.close()
fo.close()
