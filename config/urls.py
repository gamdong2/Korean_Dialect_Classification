from django.contrib import admin
from django.urls import path, include  # include를 통해 앱의 URL을 포함

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('application.urls')),  # 'application/urls.py' 파일의 경로를 포함
]