from django.urls import path
from .views import quiz_view, file_upload_view, reset_quiz

urlpatterns = [
    path('', quiz_view, name='quiz_view'),  # 퀴즈 화면
    path('upload/', file_upload_view, name='file_upload_view'),  # 파일 업로드 화면
    path('reset/', reset_quiz, name='reset_quiz'),  # 퀴즈 초기화
]