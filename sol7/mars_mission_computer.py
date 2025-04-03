import time
import json
import random  # 난수를 생성하기 위한 모듈

class DummySensor:
    def __init__(self):
        """ 센서에서 측정할 환경 변수 초기화 """
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
    
    def set_env(self):
        """ 실시간 센서 데이터가 없는 대신, 랜덤 값을 생성하여 센서 데이터 시뮬레이션 """
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 3)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4.0, 7.0), 2)

    def get_env(self):
        """ 현재 저장된 센서 데이터를 반환 """
        return self.env_values


class MissionComputer:
    def __init__(self):
        """ 센서 객체를 생성하고, 환경 데이터를 저장할 변수를 초기화 """
        self.ds = DummySensor()
        self.env_values = {}
        self.running = True  # 루프 실행 여부
        self.data_log = []  # 최근 5분간의 데이터를 저장하는 리스트
    
    def get_sensor_data(self):
        """ 
        센서 데이터를 5초마다 갱신하여 출력하고, 
        5분(60회)마다 평균 값을 계산하여 출력
        """
        while self.running:
            self.ds.set_env()  # 센서 데이터 갱신
            self.env_values = self.ds.get_env()  # 최신 센서 데이터 가져오기
            print(json.dumps(self.env_values, indent=4))  # JSON 형식으로 보기 좋게 출력
            self.data_log.append(self.env_values.copy())  # 깊은 복사하여 로그 저장

            if len(self.data_log) >= 60:  # 5분(60회)마다 평균값 계산
                self.print_five_min_avg()
                self.data_log.clear()  # 로그 초기화
            
            time.sleep(5)  # 5초 후 반복 실행
    
    def print_five_min_avg(self):
        """ 최근 5분간 수집된 데이터의 평균 값을 계산하고 출력 """
        avg_values = {key: 0 for key in self.data_log[0]}  # 초기화

        for entry in self.data_log:  
            for key in entry:
                avg_values[key] += entry[key]  # 각 센서 값 합산

        for key in avg_values:
            avg_values[key] /= len(self.data_log)  # 평균 계산
        
        print("\n[5분 평균 환경 값]")
        print(json.dumps(avg_values, indent=4))

    def stop_system(self):
        """ 시스템 종료 플래그 설정 """
        self.running = False
        print("System stopped....")


if __name__ == "__main__":
    RunComputer = MissionComputer()
    try:
        RunComputer.get_sensor_data()  # 센서 데이터 수집 시작
    except KeyboardInterrupt:  # Ctrl + C 입력 시 안전하게 종료
        RunComputer.stop_system()
