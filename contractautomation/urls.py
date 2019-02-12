from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path
from uploads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.files_list, name='files_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload/<int:pk>/', views.delete_file, name='delete_file'),
    path('template/<int:upload_id>/edit/', views.edit_file, name='edit_file'),
    # path('edited_agreements/', views.new_files_list, name='new_files_list'),
    # path('edited_agreements/<int:pk>/', views.delete_new_file, name='delete_new_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
