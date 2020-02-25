"""
@author: preethamganesh
@email: preetham.ganesh@mavs.uta.edu
"""
import numpy as np

def dataCleaning(data):
    poi_rem = [5, 6, 7, 8, 11, 12, 13, 15, 17]
    poi_ori = [l for l in range(18)]
    poi_new = [l for l in poi_ori if l not in poi_rem] #selecting points which belong to the right hand side of the body
    col_x, col_y, col_c = [], [], [] 
    for l in poi_new: #creating columns for final dataframe
        col_x.append('x_'+str(l))
        col_y.append('y_'+str(l))
        col_c.append('c_'+str(l))
    col = col_x + col_y + col_c
    for l in col:
        col_l = list(data[l])
        for m in range(len(col_l)):
            if col_l[m] == 0:
                col_l[m] = np.mean(col_l) #imputing null values with mean value of the corresponding column
        data[l] = col_l
    col_xy = col_x + col_y
    for l in col_xy:
        col_l = list(data[l])
        for m in range(len(data)):
            col_l[m] = int(col_l[m]) #converting imputed float values to the integer values for the x and y columns
        data[l] = col_l
    new_col = ['frame']
    col = col + new_col
    data = data[col]
    return data