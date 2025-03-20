import os

LOG_FILE = "mission_computer_main.log"
REPORT_FILE = "log_analysis.md"

# 로그 파일 읽기 및 출력
def read_log_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            logs = file.readlines()
            for log in logs:
                print(log.strip())
            return logs
    except FileNotFoundError:
        print(f"Error: {filename} 파일을 찾을 수 없습니다.")
        return []
    except Exception as e:
        print(f"Error: 로그 파일을 읽는 중 오류 발생 - {e}")
        return []

# 로그 분석 함수
def analyze_logs(logs):
    errors = []
    warnings = []
    for log in logs:
        parts = log.strip().split(",")
        if len(parts) == 3:
            timestamp, event, message = parts
            if event in ["ERROR", "CRITICAL"] or "unstable" in message.lower() or "explosion" in message.lower():
                errors.append(f"{timestamp} - {event}: {message}")
            elif "warning" in event.lower() or "risk" in message.lower():
                warnings.append(f"{timestamp} - {event}: {message}")
    return errors, warnings

# 보고서 작성 함수
def write_report(errors, warnings, filename):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write("# 사고 분석 보고서\n\n")
            if errors:
                file.write("## 발견된 주요 오류 및 위험 요인\n")
                for error in errors:
                    file.write(f"- {error}\n")
            else:
                file.write("## 주요 오류 없음\n")
            
            if warnings:
                file.write("\n## 발견된 경고\n")
                for warning in warnings:
                    file.write(f"- {warning}\n")
        print(f"보고서가 {filename} 파일로 저장되었습니다.")
    except Exception as e:
        print(f"Error: 보고서 작성 중 오류 발생 - {e}")

# 실행 흐름
if __name__ == "__main__":
    logs = read_log_file(LOG_FILE)
    error_logs, warning_logs = analyze_logs(logs)
    write_report(error_logs, warning_logs, REPORT_FILE)
