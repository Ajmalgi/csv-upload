"""
URL configuration for csv_upload project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import upload_csv, list_users, delete_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', upload_csv, name='upload_csv'), 
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('list-users/', list_users, name='list_users'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
]
