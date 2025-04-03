import random
import time

class DummySensor:
    def set_env(self):
        """환경 값을 랜덤으로 설정한다."""
        self.env_values = {
            'mars_base_internal_temperature': random.randint(18, 30),
            'mars_base_external_temperature': random.randint(0, 21),
            'mars_base_internal_humidity': random.randint(50, 60),
            'mars_base_external_illuminance': random.randint(500, 715),
            'mars_base_internal_co2': round(random.uniform(0.02, 0.1), 3),
            'mars_base_internal_oxygen': round(random.uniform(4.0, 7.0), 2)
        }
    
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

# DummySensor 인스턴스 생성 및 사용
ds1 = DummySensor()
ds2 = DummySensor()

ds1.set_env()
ds2.set_env()

env_data1 = ds1.get_env()
env_data2 = ds2.get_env()

print("ds1 환경 값:")
for key, value in env_data1.items():
    print(f"{key}: {value}")

print("\nds2 환경 값:")
for key, value in env_data2.items():
    print(f"{key}: {value}")
