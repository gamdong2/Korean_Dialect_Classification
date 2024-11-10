# 한국어 방언 분류 시스템 개발

## Skills
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Konlpy-4285F4?style=for-the-badge&logo=python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>&nbsp;

## 프로젝트 상세

- **진행 기간**: 2024년 9월 26일
- **프로젝트 유형**: 개인 프로젝트
  
## 프로젝트 목표

사용자가 업로드한 텍스트 파일에서 문장 내 특정 단어와 표현을 분석하여 해당 문장이 어느 지역의 방언에 해당하는지 예측

## 사용한 데이터 셋

오픈 소스(AI Hub) 한국어 방언 발화 데이터(Text)

## 워크플로우

- **텍스트 파일 업로드 및 불용어 처리**  
  사용자가 업로드한 텍스트 파일을 읽고, 불용어 파일을 로드하여 방언 단어를 분석

- **방언 단어 추출 및 분석**  
  형태소 분석기(Okt)를 사용하여 업로드된 텍스트 파일에서 단어를 추출하고, 특정 단어가 방언 단어인지 확인. 이후 방언 단어의 특징에 따라 지역을 예측할 수 있도록 설정

- **방언 예측 및 결과 제공**  
  추출된 단어와 문장을 바탕으로 방언의 지역을 예측하고 결과를 반환

## 프로젝트 결과

**구현 기능**
- **파일 업로드 및 세션 관리**: 사용자가 텍스트 파일을 업로드하고, 파일 내용을 세션에 저장하여 퀴즈가 끊기지 않고 진행될 수 있도록 함
- **방언 분석 및 지역 예측 기능**: 형태소 분석기를 통해 텍스트에서 단어를 추출하고 불용어를 제거한 후, 특정 단어가 어느 지역의 방언인지 분석하여 해당 지역을 예측하는 기능을 구현

## 트러블 슈팅

- **문제 상황**: 초기 모델에서는 방언 단어를 분석하여 지역을 예측하는 과정에서 텍스트가 자꾸 제주도로만 예측되는 문제가 존재. 제주도의 고유 방언 단어가 다른 지역에 비해 강하게 반영되어 특정 단어가 없을 때도 제주도 방언로 예측된 것으로 판단함
- **해결 방법**: 방언 단어 빈도 기반 가중치 부여: 각 지역별 방언 단어에 가중치를 부여하여 특정 지역에 국한되지 않도록 조정

## 프로젝트를 통해 얻은 역량

- **형태소 분석**: 형태소 분석기를 활용하여 텍스트 내 의미 있는 단어를 추출하고, 이를 바탕으로 한국어 지역 방언를 분류
- **딥러닝 기반의 Fine-Tuning**: 방언 단어 분류 과정에서 특정 지역으로 예측이 쏠리는 문제를 해결하기 위해 지역별 가중치 부여 및 Fine-Tuning
- **Django 프레임워크 활용 능력**: Django를 사용해 세션 관리, 파일 업로드 및 처리
