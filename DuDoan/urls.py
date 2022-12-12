from django.urls import path

from . import views

app_name = 'DuDoan'
urlpatterns = [
    path('', views.index, name='index'),
    path('ketqua/', views.ketqua, name="ketqua")
]