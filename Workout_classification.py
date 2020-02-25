"""
@author: preethamganesh
@email: preetham.ganesh@mavs.uta.edu
"""
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from sklearn.metrics import explained_variance_score as evs

def minMaxNorm(data):
    poi_rem = [5, 6, 7, 8, 11, 12, 13, 15, 17]
    poi_ori = [l for l in range(18)]
    poi_new = [l for l in poi_ori if l not in poi_rem]
    col_x, col_y, col_c = [], [], [] 
    for l in poi_new: 
        col_x.append('x_'+str(l))
        col_y.append('y_'+str(l))
        col_c.append('c_'+str(l))
    col = col_x + col_y + col_c
    d = {}
    for i in col:
        l = data[i]
        l_n = []
        maxi = max(l) #finding maximum value in the list
        mini = min(l) #finding minimum value in the list
        if maxi - mini == 0:
            l_n = [0 for i in range(len(l))]
	else:
	    for j in l:
                l_n.append((j-mini)/(maxi-mini)) #adding normalized value to a new list
        d[i] = l_n
    df = pd.DataFrame(d, columns=col) #generating normalized dataframe 
    return df

def accuracy(data1, data2):
    poi_rem = [5, 6, 7, 8, 11, 12, 13, 15, 17]
    poi_ori = [l for l in range(18)]
    poi_new = [l for l in poi_ori if l not in poi_rem]
    poi_list = ['Nose', 'Neck', 'Right Shoulder', 'Right Elbow', 'Right Wrist', 'Right Knee', 'Right Ankle', 'Right Eye', 'Right Ear']
    col_x, col_y, col_c = [], [], []
    for i in poi_new:
        col_x.append('x_'+str(i))
        col_y.append('y_'+str(i))
        col_c.append('c_'+str(i))
    col = col_x + col_y + col_c
    d2 = {}
    for i in col:
        if len(data1) > len(data2):
            if (len(data1) - len(data2)) % 2 == 0:
                m = int((len(data1) - len(data2)) / 2) #number of rows to be added at the top of user's dataframe
                n = int((len(data1) - len(data2)) / 2) #number of rows to be added at the bottom of user's dataframe
            else:
                m = int(np.ceil((len(data1) - len(data2)) / 2)) #number of rows to be added at the top of user's dataframe
                n = int(np.floor((len(data1) - len(data2)) / 2)) #number of rows to be added at the bottom of user's dataframe
            l = list(data2[i])
            l_n = []
            for j in range(m):
                l_n.append(np.mean(l)) #adding mean values of the column at the top of list
            l_n = l_n + l #appending the user's list to the new list
            for j in range(n):
                l_n.append(np.mean(l)) #adding mean values of the column at the bottom of list
            d2[i] = l_n #adding list to the dictionary
        else:
            if (len(data2) - len(data1)) % 2 == 0:
                m = int((len(data2) - len(data1)) / 2) #number of rows to be removed from the top of user's dataframe
                n = int((len(data2) - len(data1)) / 2) #number of rows to be removed from the bottom of user's dataframe
            else:
                m = int(np.ceil((len(data2) - len(data1)) / 2)) #number of rows to be removed from the top of user's dataframe
                n = int(np.floor((len(data2) - len(data1)) / 2)) #number of rows to be removed from the bottom of user's dataframe
            l = list(data2[i])
            l1 = l[m:] #removing first m elements from the user's list
            l_n = l1[:-n] #removing last n elements from the user's list
            d2[i] = l_n 
    data2 = pd.DataFrame(d2, columns=col) #converting dictionary to dataframe
    d1 = minMaxNorm(data1)
    d2 = minMaxNorm(data2)
    evs_x = []
    evs_y = []
    for i, j in zip(col_x, col_y):
        evs_x.append(evs(d1[i], d2[i])) #computing accuracy for each joint in x dimension
        evs_y.append(evs(d1[j], d2[j])) #computing accuracy for each joint in y direction
    evs_t = []
    for i, j in zip(evs_x, evs_y):
        evs_t.append(np.mean([i, j])) #computing mean accuracy across x and y dimension
    evs_f = []
    for i in range(len(poi_new)): #categorizing the accuracy
        if evs_t[i] < 0:
            evs_f.append(poi_list[i]+' movement is entirely incorrect')
        elif evs_t[i] < 0.2 and evs_t[i] >= 0:
            evs_f.append(poi_list[i]+' movement is majorly incorrect')
        elif evs_t[i] < 0.4 and evs_t[i] >= 0.2:
            evs_f.append(poi_list[i]+' movement is minorly incorrect')
        elif evs_t[i] < 0.6 and evs_t[i] >= 0.4:
            evs_f.append(poi_list[i]+' movement is minorly correct')
        elif evs_t[i] < 0.8 and evs_t[i] >= 0.6:
            evs_f.append(poi_list[i]+' movement is majorly correct')
        else:
            evs_f.append(poi_list[i]+' Movement is entirely correct')
    return evs_t, evs_f

def workout(data):
    df = minMaxNorm(data)
    ori_data = pd.read_csv('filepath to the combined file')
    model = DecisionTreeClassifier() #ML model used for prediction
    train_x = ori_data.drop(columns=['act']) #independent attributes for the model
    train_y = ori_data['act'] #dependent attribute for the model
    model.fit(train_x, train_y) #fitting the model
    pred = model.predict(df) #prediction for the user's dataframe
    pred_u = np.unique(pred)
    c = [0 for i in range(len(pred_u))]
    for i in pred:
        for j in range(len(pred_u)):
            if i == pred_u[j]:
                c[j] += 1
    a = pred_u[c.index(max(c))]
    a1, a2, a3, a4, a5 = 0, 0, 0, 0, 0
    if a == 1:
        a1 = 1
        d = pd.read_csv('filepath to a1_s4_r1.csv') #obtaining reference file for activity 1
        acc_v, acc_t = accuracy(d, data)
    elif a == 2:
        a2 = 1
        d = pd.read_csv('filepath to a2_s4_r1.csv') #obtaining reference file for activity 2
        acc_v, acc_t = accuracy(d, data)
    elif a == 3:
        a3 = 1
        d = pd.read_csv('filepath to a3_s4_r1.csv') #obtaining reference file for activity 3
        acc_v, acc_t = accuracy(d, data)
    elif a == 4:
        a4 = 1
        d = pd.read_csv('filepath to a4_s4_r1.csv') #obtaining reference file for activity 4
        acc_v, acc_t = accuracy(d, data)
    else:
        a5 = 1
        d = pd.read_csv('filepath to a5_s4_r1.csv') #obtaining reference file for activity 5
        acc_v, acc_t = accuracy(d, data)
    return acc_v, acc_t, a1, a2, a3, a4, a5