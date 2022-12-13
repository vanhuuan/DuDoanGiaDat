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
    print(road, type, width, length, area, bedroom, floor, direct)
    newRc = {
        'Road': road,
        'Type Of Estate': type,
        'Square': area,
        'Width': width,
        'Length': length,
        'Floors': floor,
        'Bedrooms': bedroom,
        'Direction': direct
    }
    df = pd.read_csv('dataclean.csv')
    df = df[['Road','Type Of Estate','Square','Width','Length','Floors','Bedrooms','Direction']]
    df = fixOutlier(df)
    df = df.append(newRc, ignore_index=True)
    df['Type Of Estate'] = le.fit_transform(df['Type Of Estate'])
    df['Direction'] = le.fit_transform(df['Direction'])
    df = ChuanHoa(df)
    # predicted = model.predict(df.iloc[-1])
    # print(predicted)
    return render(request, 'ketqua.html', {'price': 1000000})


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