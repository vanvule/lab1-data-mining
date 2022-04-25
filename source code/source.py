
import pandas as pd
import numpy as np
from sys import argv
import sys
import csv
import math

#1. Liet ke cac cot bi thieu du lieu:
def list_miss_data_column(data):
    # column_name, number_missing_data: ten và so luong cua cot bi thieu du lieu
    x = ['column_name', 'number_missing_data']
    missing_data = pd.DataFrame(columns=x)
    columns = data.columns
    for col in columns:
        icolumn_name = col
        imissing_data = data[col].isnull().sum()#so luong gia tri bi thieu moi cot

        #missing_data.loc[len(missing_data)] = [icolumn_name, imissing_data, imissing_in_percentage]
        if(imissing_data > 0): #neu cot do co gi tri bi thieu thi bo vao missing_data
            missing_data.loc[len(missing_data)] = [icolumn_name, imissing_data]
    missing_data.to_csv("list_miss_data_column.csv")
    return missing_data


#2. Dem so dong bi thieu du lieu
def count_miss_data_rows(data):

    # x la danh sach so luong du lieu bi thieu moi dong
    x=data.isnull().sum(axis=1)

    # so dong bi thieu du lieu
    count = 0
    # data = list(df)
    for i in range(len(data)):
        # neu du lieu bi thieu moi dong >0 thi tang bien dem len 1
        if(x[i]>0):
            count=count+1
    return count


#3. Dien gia tri bi thieu
def FillMissingData(data, attributes):
    for a in attributes:
        if data[a].dtype == "object":  # dữ liệu là categorical
            value = data[a].mode()[0]  # dùng mode
            data1 = list(data[a])
            for i in range(0, len(data)):

                if not isinstance(data[a][i], str) and math.isnan(data[a][i]):
                    data1 = value
            data[a] = data1
        else:  # dữ liệu là numeric
            value = data[a].mean()  # dùng mean
            data1 = list(data[a])
            for i in range(0, len(data)):
                # if not isinstance(a[i],str) and math.isnan(float(a[i])):
                if not isinstance(data[a][i], str) and math.isnan(data[a][i]):
                    data1[i] = value
            data[a] = data1
    data.to_csv("FilledMissingData.csv")

#5. Xoa cac cot bi thieu du lieu
#percentage la ty le do nguoi dung nhap vao (vi du: 50% thi nhap 50)
def remove_miss_data_column(data,percentage):
    x = ['column_name', 'number_missing_data']
    missing_data = pd.DataFrame(columns=x)
    columns = data.columns
    for col in columns:

        #ty le miss data moi cot
        imissing_in_percentage = (data[col].isnull().sum() / data[col].shape[0]) * 100


        if(imissing_in_percentage>percentage):#neu ty le miss > percentage thi xoa cot do
            del data[col]
            #missing_data.loc[len(missing_data)] = [icolumn_name, imissing_data]
    data.to_csv("removed_miss_data_column.csv")
    print(data)

#6. Xoa cac mau bi trung lap
def remove_dedupe(source):
    destination = source.replace('.csv', '_deduped.csv')#file csv ket qua
    data = open(source, 'r')
    target = open(destination, 'w')

    # khoi tao bien va bo dem:
    unique_lines = set()
    source_lines = 0
    duplicate_lines = 0

    # duyet toan bo du lieu
    for line in data:
        source_lines += 1
        # loai bo phan nhieu
        line_to_check = line.strip('\r\n')
        if line_to_check in unique_lines:  # bo qua neu dong du lieu do da duoc thiet lap
            duplicate_lines += 1
            continue
        else:  # them vao danh sach "cac dong da duyet qua"
            target.write(line)
            unique_lines.add(line_to_check)

    target.close()
    data.close()


#7.1. Chuan hoa thuoc tinh numeric bang PP minmax
def MinMaxDataNormalization(dataframe, attributes, newmin, newmax):
    length = len(dataframe)
    for a in attributes:
        maxData = dataframe[a].max()
        minData = dataframe[a].min()

        data = []
        for i in range(0,length):
            data.append((dataframe[a][i]-minData)/(maxData-minData)*(newmax-newmin)+newmin)

        dataframe[a]=data
    dataframe.to_csv("MinMaxDataNormalization.csv")

#7.2. Chuan hoa thuoc tinh numeric bang PP Z-score
def Z_ScoresDataNormalization(dataframe, attributes):
    length = len(dataframe)
    for a in attributes:
         mean = dataframe[a].mean()
         SD = dataframe[a].std()

         data = []
         for i in range(0,length):
             data.append((dataframe[a][i]-mean)/SD)

         dataframe[a]=data
    dataframe.to_csv("Z_ScoresDataNormalization.csv")



missing_value_formats = ["n.a.", "?", "NA", "n/a", "na", "--", " "]
data = pd.read_csv(argv[2], na_values=missing_value_formats, delimiter=",")
    #dataframe = pd.read_csv(str(sys.argv[1]))
attributes = data.columns#danh sach cac thuoc tinh
attr_list = []

if sys.argv[1] == '1':
    list_miss_data_column(data)
    print(list_miss_data_column(data))
elif sys.argv[1] == '2':
    print("So dong bi thieu du lieu la:", count_miss_data_rows(data), "(dong)")
elif sys.argv[1] == '3':
    FillMissingData(data, attributes)
elif sys.argv[1] == '5':
    percentage = float(argv[3])
    remove_miss_data_column(data, percentage)
elif sys.argv[1] == '6':
    remove_dedupe(argv[2])
elif sys.argv[1] == '7.1':
    newmin = int(argv[3])
    newmax = int(argv[4])
    MinMaxDataNormalization(data, attr_list, newmin, newmax)
elif sys.argv[1] == '7.2':
    Z_ScoresDataNormalization(data, attr_list)









