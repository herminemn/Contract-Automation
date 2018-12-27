from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from uploads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.files_list, name='files_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload/<int:pk>/', views.delete_file, name='delete_file'),
]
