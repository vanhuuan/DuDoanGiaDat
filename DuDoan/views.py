import email
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from tensorflow.python.keras.models import load_model
from sklearn.preprocessing import RobustScaler
import numpy as np
import math
from sklearn import preprocessing
import pandas as pd
import locale

le = preprocessing.LabelEncoder()


# Create your views here.
def index(request):
    return render(request, 'dudoan.html', {})


@require_POST
def ketqua(request):
    model = load_model('model.h5')
    road = request.POST['road']
    type = request.POST['type']
    width = request.POST['width']
    length = request.POST['length']
    area = request.POST['area']
    bedroom = request.POST['bedroom']
    floor = request.POST['floor']
    direct = request.POST['direct']
    paper = request.POST['paper']
    district = request.POST['district']
    print(road, type, width, length, area, bedroom, floor, direct)
    newRc = {
        'Type Of Estate': type,
        'Legal': paper,
        'Square': area,
        'Width': width,
        'Length': length,
        'Floors': floor,
        'Bedrooms': bedroom,
        'Direction': direct,
        'Road': road,
    }
    df = pd.read_csv('dataclean.csv')
    df = df[['Road','Type Of Estate','Square','Width','Length','Floors','Bedrooms','Direction']]
    df = fixOutlier(df)
    df = df.append(newRc, ignore_index=True)
    df = ChuanHoa(df)
    df['Type Of Estate'] = le.fit_transform(df['Type Of Estate'])
    df['Direction'] = le.fit_transform(df['Direction'])
    df['Legal'] = le.fit_transform(df['Legal'])
    last = df[0:1]
    last['Legal'] = int(last['Legal'])
    last['District_Huyện Hòa Vang'] = int(0)
    last['District_Quận Cẩm Lệ'] = int(0)
    last['District_Quận Hải Châu'] = int(0)
    last['District_Quận Liên Chiểu'] = int(0)
    last['District_Quận Ngũ Hành Sơn'] = int(0)
    last['District_Quận Sơn Trà'] = int(0)
    last['District_Quận Thanh Khê'] = int(0)
    match district:
        case 'Huyện Hòa Vang': last['District_Huyện Hòa Vang'] = int(1)
        case 'Quận Cẩm Lệ': last['District_Quận Cẩm Lệ'] = int(1)
        case 'Quận Hải Châu': last['District_Quận Hải Châu'] = int(1)
        case 'Quận Liên Chiểu': last['District_Quận Liên Chiểu'] = int(1)
        case 'Quận Ngũ Hành Sơn': last['District_Quận Ngũ Hành Sơn'] = int(1)
        case 'Quận Sơn Trà': last['Quận Sơn Trà'] = int(1)
        case 'Quận Thanh Khê': last['District_Quận Thanh Khê'] = int(1)
    predicted = model.predict(last)
    locale.setlocale(locale.LC_ALL, 'vi_VN.UTF-8')
    
    return render(request, 'ketqua.html', {'price': locale.currency(float(predicted[0]), grouping=True)})


def fixOutlier(train_df):
    index = []
    for i in range(train_df.shape[0]):
        if i == 0:
            continue
        if train_df['Square'].iloc[i] >= 450:
            if i not in index:
                index.append(i)
        elif train_df['Length'].iloc[i] > 60:
            if i not in index:
                index.append(i)
        elif train_df['Width'].iloc[i] > 50:
            if i not in index:
                index.append(i)
        elif train_df['Floors'].iloc[i] > 18:
            if i not in index:
                index.append(i)
        elif train_df['Road'].iloc[i] > 100:
            if i not in index:
                index.append(i)
        elif train_df['Bedrooms'].iloc[i] > 40:
            if i not in index:
                index.append(i)
    train_df = train_df.drop(index)
    return train_df


def ChuanHoa(train_df):
    scaler = RobustScaler()
    num_cols = ['Road','Square','Width','Length','Floors','Bedrooms']
    train_df[num_cols] = scaler.fit_transform(train_df[num_cols])
    return train_df