import random
import time

#코드 개요
'''
이 코드는 화성 기지에서 환경 데이터를 측정하는 더미 센서(DummySensor)를 구현한 것
실제 센서가 없으므로 랜덤한 값을 생성하여(임의로) -> 데이터 제공
생성된 환경 값은 로그파일(sensor_log.txt)에 저장한다 
'''

# 더미클래스 (화성 기지의 환경 데이터 관리)
class DummySensor:
    def __init__(self):
        """DummySensor 클래스는 화성 기지 환경 값을 랜덤으로 생성"""
        
        # 환경 데이터값을 저장하는 딕셔너리 (사전 객체) 초기화 / 초기값은 모든 항목을 0으로 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,  # 화성 기지 내부 온도 int
            'mars_base_external_temperature': 0,  # 화성 기지 외부 온도 int
            'mars_base_internal_humidity': 0,  # 화성 기지 내부 습도 int
            'mars_base_external_illuminance': 0,  # 화성 기지 외부 광량 int
            'mars_base_internal_co2': 0.0,  # 화성 기지 내부 이산화탄소 농도 float
            'mars_base_internal_oxygen': 0.0  # 화성 기지 내부 산소 농도 float
        }
    
    def set_env(self):
        """환경 값을 랜덤으로 설정한다."""
        
        # 각 환경 변수에 대해 지정된 범위 내의 랜덤 값을 생성하여 설정
        '''
        random.randint(a, b): a에서 b 사이의 정수를 랜덤 생성
        random.uniform(a, b): a에서 b 사이의 실수를 랜덤 생성
        round(value, n): 소수점 n번째 자리까지 반올림
        '''
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)
    
    def get_env(self):
        """환경 값을 반환하고 로그 파일에 기록한다."""
        # 현재 시간을 가져와서 로그에 추가
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = (f"{timestamp}, "
                     f"{self.env_values['mars_base_internal_temperature']}, "
                     f"{self.env_values['mars_base_external_temperature']}, "
                     f"{self.env_values['mars_base_internal_humidity']}, "
                     f"{self.env_values['mars_base_external_illuminance']}, "
                     f"{self.env_values['mars_base_internal_co2']}, "
                     f"{self.env_values['mars_base_internal_oxygen']}")
        
        # 로그 파일(sensor_log.txt)에 환경 값 기록
        # open('sensor_log.txt', 'a') 파일을 → 추가(append) 모드로 열어 데이터를 저장
        with open('sensor_log.txt', 'a') as log_file:
            log_file.write(log_entry + '\n')
        
        # 환경 값 반환
        return self.env_values

# DummySensor 인스턴스(객체) 생성
ds = DummySensor()

# 환경 값 설정 및 확인
ds.set_env()  # 환경 값 설정
env_data = ds.get_env()  # 환경 값 가져오기

for key, value in env_data.items():
    print(f"{key}: {value}") # 환경 값 줄바꿈 출력
