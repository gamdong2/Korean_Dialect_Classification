import random
import time
import os
from django.conf import settings
from django.shortcuts import render, redirect
from konlpy.tag import Okt

# 한국어 형태소 분석기 (Okt)
okt = Okt()

# 불용어 파일을 불러오는 함수
def load_stopwords():
    stopwords_path = os.path.join(settings.BASE_DIR, 'application/data/stopwords.txt')  # 불용어 파일 경로
    with open(stopwords_path, 'r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()  # 한 줄씩 불용어를 읽어서 리스트로 변환
    return stopwords

# 영어 POS 태그를 한글로 변환하는 함수
def convert_pos_to_korean(pos):
    pos_mapping = {
        'Noun': '명사',
        'Adjective': '형용사',
        'Verb': '동사'
    }
    return pos_mapping.get(pos, "")

# 문제 생성 함수 (불용어 처리 포함)
def generate_problem(text, stopwords):
    sentences = text.split('.')  # 마침표를 기준으로 문장 분리
    sentence = random.choice(sentences).strip()  # 랜덤으로 문장을 선택

    # 문장 형태소 분석
    morphs_with_pos = okt.pos(sentence)

    # 불용어 제외 후 명사, 형용사, 동사만 필터링
    candidates = [word for word in morphs_with_pos if word[1] in ['Noun', 'Adjective', 'Verb'] and word[0] not in stopwords]

    if not candidates:
        return generate_problem(text, stopwords)

    # 정답과 오답 선택
    selected_word, selected_pos = random.choice(candidates)
    pos_types = ['Noun', 'Adjective', 'Verb']
    
    return sentence, selected_word, selected_pos, pos_types

# 파일 업로드 처리 함수
def file_upload_view(request):
    if request.method == 'POST':
        if 'text_file' in request.FILES:
            text_file = request.FILES['text_file']
            file_content = text_file.read().decode('utf-8')  # 파일 내용을 읽어서 utf-8로 디코딩
            file_name = text_file.name  # 파일 이름 저장

            # 세션에 파일 내용과 파일 이름 저장
            request.session['uploaded_text'] = file_content
            request.session['uploaded_file_name'] = file_name  # 파일 이름을 세션에 저장

            return redirect('quiz_view')  # 퀴즈 화면으로 리디렉션
    return render(request, 'upload.html')

# 퀴즈 초기화 함수 (처음으로 돌아가기 버튼 클릭 시 실행)
def reset_quiz(request):
    # 세션 초기화
    request.session.flush()  # 모든 세션 데이터 삭제 (점수, 문제 상태 초기화)
    return redirect('file_upload_view')  # 파일 업로드 화면으로 이동

# 퀴즈 뷰 함수
def quiz_view(request):
    stopwords = load_stopwords()  # 불용어 파일 로드

    # 세션에 업로드된 텍스트 파일이 없을 경우 업로드 화면으로 리디렉션
    if 'uploaded_text' not in request.session:
        return redirect('file_upload_view')

    # 업로드된 텍스트 파일을 세션에서 로드
    text_data = request.session['uploaded_text']
    file_name = request.session.get('uploaded_file_name', '알 수 없는 파일')  # 파일 이름 가져오기, 없으면 기본값

    # 초기 설정 (세션 시작 시)
    if 'quiz_index' not in request.session:
        request.session['quiz_index'] = 0
        request.session['score'] = 0
        request.session['questions'] = []
        request.session['start_time'] = time.time()

    quiz_index = request.session['quiz_index']
    
    # 모든 문제를 풀면 종료
    if quiz_index >= 10:
        total_time = sum(float(question['time_taken']) for question in request.session['questions'])
        final_score = request.session['score']
        
        if final_score <= 29:
            feedback = "걸음마 수준이네요!"
        elif 30 <= final_score <= 59:
            feedback = "조금 더 연습이 필요해요!"
        elif 60 <= final_score <= 79:
            feedback = "좋아요, 조금만 더 힘내세요!"
        elif 80 <= final_score <= 99:
            feedback = "훌륭해요! 거의 만점이에요!"
        else:
            feedback = "완벽해요! 만점입니다!"

        return render(request, 'quiz_done.html', {
            'final_score': final_score,
            'total_time': total_time,
            'questions': request.session['questions'],
            'feedback': feedback
        })

    # 문제를 생성
    if request.method == 'GET':
        sentence, selected_word, correct_pos, pos_options = generate_problem(text_data, stopwords)

        # 문장의 앞뒤 공백을 완전히 제거 (특히 문장 첫머리의 공백)
        sentence = sentence.lstrip().rstrip()  # 앞뒤 공백 모두 제거

        # 문장에서 selected_word를 굵게 표시하고 색상 추가 (빨간색)
        sentence = sentence.replace(selected_word, f'<strong style="color:red;">{selected_word}</strong>')
        sentence = f'“{sentence.strip()}”'

        # 문장 내 모든 따옴표(작은따옴표 및 큰따옴표)를 제거
        sentence = sentence.replace("'", "").replace('"', "").replace('“', "").replace('”', "")
        
        # 문장을 큰따옴표로 무조건 감싸기
        sentence = f'“{sentence}”'

        # 문제에서 selected_word를 빨간색으로 강조하여 출력
        question_text = f'다음 문장에서 "<strong style="color:red;">{selected_word}</strong>"는 어떤 품사일까요?'

        # 문제를 세션에 저장 (문제와 정답 정보)
        request.session['current_question'] = {
            'sentence': sentence,
            'selected_word': selected_word,
            'correct_pos': correct_pos  # 정답 저장
        }

        # correct_pos_korean을 세션에 저장해서 POST 요청 시 활용
        request.session['correct_pos_korean'] = convert_pos_to_korean(correct_pos)

        return render(request, 'quiz.html', {
            'sentence': sentence,
            'selected_word': selected_word,
            'pos_options': [convert_pos_to_korean(pos) for pos in pos_options],
            'current_score': request.session['score'],
            'previous_questions': request.session['questions'],
            'current_question_number': quiz_index + 1,
            'file_name': file_name  # 파일 이름을 템플릿에 전달
        })

    elif request.method == 'POST':
        current_question = request.session['current_question']
        correct_pos = current_question['correct_pos']

        # 라디오 버튼에서 선택한 답안 가져오기
        user_answer = request.POST.get('answer')

        # 선택한 답안이 없는 경우 (예외 처리)
        if not user_answer:
            return redirect('quiz_view')

        # 정답 여부 확인
        correct = check_answer(user_answer, correct_pos)

        # 소요 시간을 POST에서 가져오기
        time_taken = request.POST.get('time_taken', 0)

        # 결과를 세션에 저장하여 자바스크립트로 전달할 수 있게 준비
        request.session['answer_correct'] = correct
        request.session['correct_pos_korean'] = convert_pos_to_korean(correct_pos)

        if correct:
            request.session['score'] += 10

        previous_questions = request.session['questions']
        previous_questions.append({
            'question': current_question['sentence'],
            'selected_word': current_question['selected_word'],
            'user_answer': user_answer,
            'correct_pos': convert_pos_to_korean(correct_pos),
            'correct': correct,
            'time_taken': time_taken
        })
        request.session['questions'] = previous_questions

        del request.session['current_question']
        request.session['quiz_index'] += 1

        return redirect('quiz_view')

# 정답 확인 함수 (한글 입력을 영어 POS 태그와 매핑)
def check_answer(user_answer, correct_pos):
    pos_mapping = {
        '명사': 'Noun',
        '형용사': 'Adjective',
        '동사': 'Verb'
    }
    return pos_mapping.get(user_answer.strip(), "") == correct_pos

# 영어 POS 태그를 한글로 변환하는 함수
def convert_pos_to_korean(pos):
    pos_mapping = {
        'Noun': '명사',
        'Adjective': '형용사',
        'Verb': '동사'
    }
    return pos_mapping.get(pos, "")
