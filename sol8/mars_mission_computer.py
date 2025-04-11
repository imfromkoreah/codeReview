import platform
import os
import json
import time


class MissionComputer:
    def __init__(self):
        # setting.txt 파일을 불러와 출력 항목 설정을 로드
        self.settings = self.load_settings()

    def load_settings(self):
        # 출력 항목 기본값 정의
        settings = {
            'os': True,
            'os_version': True,
            'cpu_type': True,
            'cpu_cores': True,
            'memory': True,
            'cpu_usage': True,
            'memory_usage': True
        }

        try:
            # setting.txt 파일에서 사용자 설정 읽기
            with open('setting.txt', 'r') as file:
                for line in file:
                    if '=' in line:
                        key, value = line.strip().split('=')
                        key = key.strip()
                        value = value.strip().lower()
                        if key in settings:
                            settings[key] = (value == 'true')
        except FileNotFoundError:
            # 설정 파일이 없으면 기본값 사용
            pass

        return settings

    def get_mission_computer_info(self):
        try:
            info = {}

            # 운영체제 정보
            if self.settings.get('os'):
                info['os'] = platform.system()

            # 운영체제 버전
            if self.settings.get('os_version'):
                info['os_version'] = platform.version()

            # CPU 종류
            if self.settings.get('cpu_type'):
                info['cpu_type'] = platform.processor()

            # CPU 코어 수
            if self.settings.get('cpu_cores'):
                info['cpu_cores'] = os.cpu_count()

            # 메모리 크기
            if self.settings.get('memory'):
                if platform.system() == 'Windows':
                    # Windows: wmic 명령어 사용
                    command = 'wmic computersystem get TotalPhysicalMemory'
                    output = os.popen(command).read().split()
                    if output[-1].isdigit():
                        memory_bytes = int(output[-1])
                        info['memory'] = str(round(memory_bytes / (1024 ** 3), 2)) + ' GB'
                    else:
                        info['memory'] = 'Unknown'
                else:
                    # Linux/macOS: sysconf 사용
                    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
                    info['memory'] = str(round(mem_bytes / (1024 ** 3), 2)) + ' GB'

            # JSON 형식으로 출력
            print('[MissionComputer Info]')
            print(json.dumps(info, indent=4))
            return info

        except Exception as e:
            print('시스템 정보 가져오기 중 오류 발생:', e)
            return {}

    def get_mission_computer_load(self):
        try:
            load = {}

            # CPU 실시간 사용량
            if self.settings.get('cpu_usage'):
                if platform.system() == 'Windows':
                    # Windows: wmic 명령어 사용
                    cpu_usage = os.popen('wmic cpu get loadpercentage').read().split()
                    cpu_percent = next((int(x) for x in cpu_usage if x.isdigit()), None)
                else:
                    # Linux/macOS: load average 기반 계산
                    load1, load5, load15 = os.getloadavg()
                    cpu_percent = round((load1 / os.cpu_count()) * 100, 2)
                load['cpu_usage'] = f'{cpu_percent}%'

            # 메모리 실시간 사용량
            if self.settings.get('memory_usage'):
                if platform.system() in ('Linux', 'Darwin'):
                    # /proc/meminfo 사용
                    with open('/proc/meminfo', 'r') as meminfo:
                        mem_data = meminfo.readlines()
                        mem_total = int(next(line for line in mem_data if 'MemTotal' in line).split()[1])
                        mem_free = int(next(line for line in mem_data if 'MemAvailable' in line).split()[1])
                        mem_used = mem_total - mem_free
                        mem_percent = round((mem_used / mem_total) * 100, 2)
                        load['memory_usage'] = f'{mem_percent}%'
                else:
                    # Windows에서는 사용량 계산 불가
                    load['memory_usage'] = 'Not Available'

            # JSON 형식으로 출력
            print('[MissionComputer Load]')
            print(json.dumps(load, indent=4))
            return load

        except Exception as e:
            print('부하 정보 가져오기 중 오류 발생:', e)
            return {}


if __name__ == '__main__':
    # MissionComputer 인스턴스 생성
    runComputer = MissionComputer()

    # 시스템 정보 출력
    runComputer.get_mission_computer_info()
    print()

    # 부하 정보 출력 (1초 대기 후)
    time.sleep(1)
    runComputer.get_mission_computer_load()
