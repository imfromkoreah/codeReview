import random
import time

class DummySensor:
    def __init__(self):
        """DummySensor 클래스는 화성 기지 환경 값을 랜덤으로 생성하는 역할을 한다."""
        # 환경 값을 저장하는 사전 객체 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,  # 화성 기지 내부 온도
            'mars_base_external_temperature': 0,  # 화성 기지 외부 온도
            'mars_base_internal_humidity': 0,  # 화성 기지 내부 습도
            'mars_base_external_illuminance': 0,  # 화성 기지 외부 광량
            'mars_base_internal_co2': 0.0,  # 화성 기지 내부 이산화탄소 농도
            'mars_base_internal_oxygen': 0.0  # 화성 기지 내부 산소 농도
        }
    
    def set_env(self):
        """환경 값을 랜덤으로 설정한다."""
        # 각 환경 변수에 대해 지정된 범위 내의 랜덤 값을 생성하여 설정
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
        with open('sensor_log.txt', 'a') as log_file:
            log_file.write(log_entry + '\n')
        
        # 환경 값 반환
        return self.env_values

# DummySensor 인스턴스 생성
ds = DummySensor()

# 환경 값 설정 및 확인
ds.set_env()  # 환경 값 설정
env_data = ds.get_env()  # 환경 값 가져오기
print(env_data)  # 환경 값 출력
