import xgboost as xgb
# read in data

workspace = '/home/yxsong/Downloads/dataset/data/'

Campaign = '135059'

Train_file = workspace+Campaign+'/'+Campaign+'train.yzx.shaffle.txt'
Test_file = workspace+Campaign+'/'+Campaign +'test.yzx.txt'

dtrain = xgb.DMatrix(Train_file)
dtest = xgb.DMatrix(Test_file)

Xgbresult_file = workspace+Campaign+'/'+Campaign +'test.yzx.txt'
# specify parameters via map


#param = {'max_depth':2, 'eta':1, 'silent':1, 'objective':'binary:logistic' }

param = {
            #'subsample': 0.6,
            'eta': 0.01,
            'gamma': 0.5,
            'min_child_weight': 1,
            'max_depth': 20,
            'silent': 1,
            'scale_pos_weight': 0.7,
            'eval_metric': 'auc',
            #'eval_metric': 'rmse',
            'booster':'gbtree',
            # 'eval_metric': 'error',
            'objective': 'binary:logistic',
            # 'objective':'multi:softmax', 'num_class':2,
            'nthread':4
        }

watch_list =[(dtrain,'train'),(dtest,'test')]


num_round = 100

bst = xgb.train(param,dtrain,evals=watch_list, num_boost_round=num_round,early_stopping_rounds=15)

bst.save_model(workspace+Campaign+'/'+Campaign + 'xgb.model')#preds = bst.predict(dtest)
