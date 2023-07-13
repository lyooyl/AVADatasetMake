import pickle
import numpy as np
import csv
import sys

fix_pkl_file = sys.argv[1]

f = open(fix_pkl_file, 'rb')
info = pickle.load(f, encoding='iso-8859-1')
dense_proposals_train = {}

for i in info:
    tempArr = np.array(info[i])
    dicts = []
    for index1, temp in enumerate(tempArr):
        temp = temp.astype(np.float64)
        for index2, x in enumerate(temp):
            if x < 0:
                temp[index2] = 0.0
            if x > 1:
                temp[index2] = 1.0
        dicts.append(temp)
    dense_proposals_train[i] = np.array(dicts)
# 保存为pkl文件
with open(fix_pkl_file, "wb") as pklfile:
    pickle.dump(dense_proposals_train, pklfile)
