import os
import csv
import speech_recognition as sr

def get_audio_files(directory):
    audio_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.wav'):
            audio_files.append(os.path.join(directory, file_name))
    return audio_files

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file_path)
    segments = []

    with audio_file as source:
        audio = recognizer.record(source)

        try:
            # 전체 음성을 한 번에 처리
            text = recognizer.recognize_google(audio, language='ko-KR')
            segments.append(('0:00', text))  # 시간 정보는 단순 예시로 0:00
        except sr.UnknownValueError:
            print('인식 실패:', file_path)
        except sr.RequestError:
            print('STT 서비스 오류 발생:', file_path)

    return segments

def save_to_csv(segments, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['시간', '텍스트'])
        for time_stamp, text in segments:
            writer.writerow([time_stamp, text])

def process_all_audio_files(directory):
    audio_files = get_audio_files(directory)
    for file_path in audio_files:
        segments = transcribe_audio(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        csv_name = base_name + '.csv'
        csv_path = os.path.join(directory, csv_name)
        save_to_csv(segments, csv_path)
        print('저장 완료:', csv_path)

def search_keyword_in_csv(directory, keyword):
    print(f'키워드 "{keyword}" 검색 결과:')
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            path = os.path.join(directory, file_name)
            with open(path, mode='r', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # 헤더 건너뜀
                for row in reader:
                    time_stamp, text = row
                    if keyword in text:
                        print(f'[{file_name}] {time_stamp}: {text}')

def main():
    directory = '../2-sol7/recoreds'  # 음성 파일 디렉토리
    process_all_audio_files(directory)

    keyword = input('검색할 키워드를 입력하세요 (종료하려면 Enter): ')
    if keyword.strip():
        search_keyword_in_csv(directory, keyword)

if __name__ == '__main__':
    main()
