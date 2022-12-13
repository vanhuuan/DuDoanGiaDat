import email
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from tensorflow.python.keras.models import load_model
from sklearn.preprocessing import RobustScaler
import numpy as np
import math
from DuDoanGiaDat import settings


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
    print(road, type, width, length, area, bedroom, floor, direct, paper)
    return render(request, 'ketqua.html', {'price': 1000000})
