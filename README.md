# 한국어 방언 분류 시스템 개발

## Skills
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Konlpy-4285F4?style=for-the-badge&logo=python&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white"/>&nbsp;
<img src="https://img.shields.io/badge/KoBERT-2C5BBF?style=for-the-badge&logoColor=white"/>&nbsp;

## 프로젝트 상세

- **진행 기간**: 2024년 9월 25일
- **프로젝트 유형**: 개인 프로젝트
  
## 프로젝트 목표

사용자가 업로드한 텍스트 파일에서 문장 내 특정 단어와 표현을 분석하여 해당 문장이 어느 지역의 방언에 해당하는지 예측

## 사용한 데이터 셋

오픈 소스(AI Hub) 한국어 방언 발화 데이터(Text)

## 워크플로우

- **데이터 수집 및 전처리**
  - JSON 형식의 방언 데이터를 CSV로 변환하여 각 지역별로 분류하고 저장하였습니다.
  - **형태소 분석**을 통해 텍스트 내 단어를 추출하고 방언 단어를 식별합니다.

- **문장 임베딩(KoBERT 모델 사용)**
  - `monologg/kobert` 모델을 사용하여 텍스트를 임베딩 벡터로 변환했습니다.
  - 임베딩은 각 문장을 벡터 표현으로 변환하여 특징을 추출하는 데 사용됩니다.

- **방언 분류 모델 구축**
  - Transformer 기반의 딥러닝 모델(`skt/kobert-base-v1`)을 Fine-Tuning하여 방언 분류 모델을 학습했습니다.
  - 학습된 모델은 문장을 입력받아 방언 지역을 예측할 수 있습니다.

- **방언 예측 및 결과 제공**  
  - 예측된 방언 지역을 사용자에게 제공하여 텍스트가 어느 지역 방언인지 시각적으로 나타냅니다.

## 프로젝트 결과

**구현 기능**
- **파일 업로드 및 세션 관리**: 사용자가 텍스트 파일을 업로드하고, 파일 내용을 세션에 저장하여 방언 분석이 원활하게 이루어지도록 함
- **방언 분석 및 지역 예측 기능**: KoBERT 모델을 통해 문장을 임베딩한 후, Transformer 기반 분류 모델로 방언 지역을 예측

## 트러블 슈팅

- **문제 상황 1**: 초기 모델에서 특정 단어가 부족한 경우 제주도로 예측되는 문제 발생. 이는 제주도 고유 방언 단어가 모델에 강하게 반영되어 예측이 편향된 것으로 판단됨
- **해결 방법**: 지역별 방언 단어 빈도에 따른 가중치를 적용하여 특정 지역에 치우치지 않도록 조정하고 Fine-Tuning을 통해 모델을 최적화

- **문제 상황 2**: 불용어 처리 시 일반적으로 불용어로 간주되는 **부사**, **접속사**, **감탄사** 등을 제거하려 했으나, 방언에서는 이러한 품사가 지역 특유의 말투를 표현하는 중요한 요소가 되기도 함. 단순히 불용어로 처리할 경우 방언의 특색이 손실될 우려가 있어 어려움이 있었음
- **해결 방법**: 방언 특성에 따라 불용어 중에서도 방언의 말투적 특징을 살리는 단어는 유지하고, 의미 없는 단어만 선별적으로 제거하여 방언의 특징을 최대한 보존


## 프로젝트를 통해 얻은 역량

- **형태소 분석 및 텍스트 전처리**: Konlpy의 형태소 분석기를 활용하여 텍스트 데이터를 처리하고, 이를 기반으로 방언 지역을 분류하는 데 적용
- **KoBERT를 이용한 임베딩 및 딥러닝 모델 구축**: KoBERT 모델을 활용하여 문장을 임베딩하고 Transformer 기반의 분류 모델로 방언 분류
- **Django 프레임워크 활용 능력**: Django를 통해 파일 업로드, 세션 관리 및 분석 결과 제공
