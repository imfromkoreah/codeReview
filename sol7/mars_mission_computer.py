import time
import json

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
    
    def set_env(self):
        import random
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)
    
    def get_env(self):
        return self.env_values

class MissionComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_values = {}
        self.running = True
        self.data_log = []
    
    def get_sensor_data(self):
        start_time = time.time()
        while self.running:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print(json.dumps(self.env_values, indent=4))
            self.data_log.append(self.env_values.copy())
            
            # 5분 평균 출력
            if len(self.data_log) >= 60:  # 5분(60회) 데이터 수집 후 평균 출력
                self.print_five_min_avg()
                self.data_log = []  # 로그 초기화
            
            # 5초마다 데이터 갱신
            time.sleep(5)
    
    def print_five_min_avg(self):
        avg_values = {key: 0 for key in self.data_log[0]}
        for entry in self.data_log:
            for key in entry:
                avg_values[key] += entry[key]
        for key in avg_values:
            avg_values[key] /= len(self.data_log)
        print("\n[5분 평균 환경 값]")
        print(json.dumps(avg_values, indent=4))
    
    def stop_system(self):
        self.running = False
        print("System stopped....")

# 실행 코드
if __name__ == "__main__":
    RunComputer = MissionComputer()
    try:
        RunComputer.get_sensor_data()
    except KeyboardInterrupt:
        RunComputer.stop_system()
