import os
import datetime
import wave
import pyaudio

RECORDS_FOLDER = 'records'


class VoiceRecorder:
    def __init__(self, duration = 5):
        self.duration = duration
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

    def record_and_save(self):
        if not os.path.exists(RECORDS_FOLDER):
            os.makedirs(RECORDS_FOLDER)

        now = datetime.datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        filepath = os.path.join(RECORDS_FOLDER, filename)

        audio = pyaudio.PyAudio()
        stream = audio.open(format = self.format,
                            channels = self.channels,
                            rate = self.rate,
                            input = True,
                            frames_per_buffer = self.chunk)

        print('녹음을 시작합니다... 말해주세요.')
        frames = []

        for _ in range(0, int(self.rate / self.chunk * self.duration)):
            data = stream.read(self.chunk)
            frames.append(data)

        print('녹음이 완료되었습니다.')

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))

        print('파일이 저장되었습니다:', filepath)


def list_recordings_by_date(start_date, end_date):
    if not os.path.exists(RECORDS_FOLDER):
        print('녹음된 파일이 없습니다.')
        return

    try:
        start = datetime.datetime.strptime(start_date, '%Y%m%d')
        end = datetime.datetime.strptime(end_date, '%Y%m%d')
    except ValueError:
        print('날짜 형식이 잘못되었습니다. 예: 20250101')
        return

    files = os.listdir(RECORDS_FOLDER)
    print(f'{start_date}부터 {end_date}까지의 녹음 파일 목록:')

    for file in sorted(files):
        if not file.endswith('.wav'):
            continue
        try:
            file_date = datetime.datetime.strptime(file.split('.')[0], '%Y%m%d-%H%M%S')
            if start <= file_date <= end:
                print(file)
        except ValueError:
            continue


def main():
    print('1: 음성 녹음')
    print('2: 날짜별 녹음 파일 보기')
    choice = input('선택하세요 (1 또는 2): ')

    if choice == '1':
        recorder = VoiceRecorder()
        recorder.record_and_save()
    elif choice == '2':
        start = input('시작 날짜를 입력하세요 (예: 20250101): ')
        end = input('종료 날짜를 입력하세요 (예: 20250131): ')
        list_recordings_by_date(start, end)
    else:
        print('잘못된 선택입니다.')


if __name__ == '__main__':
    main()
