import csv #csv 파일 읽고 쓰는 python 표준 라이브러리
            #csv 파일은 데이터가 쉼표로 구분된 텍스트 형식 파일임
            #그래서 csv.reader() 같은 함수 필요ㅇㅇ
import pickle

def load_csv(file_path):
    """CSV 파일을 읽어 리스트로 반환 
    csv.reader는 csv 파일의 각 행을 리스트로 읽어오기 때문
    그래서 list()로 반환해서 전체 데이터를 리스트 형식으로 반환"""   
    with open(file_path, newline='', encoding='utf-8') as file: #with 사용->자동파일닫
        reader = csv.reader(file)
        data = list(reader)
    return data

def sort_by_flammability(data):
    """Flammability 값을 기준으로 내림차순 정렬"""
    header, *rows = data #header를 따로 저장, 나머지행은 rows에 저장
    rows.sort(key=lambda x: float(x[-1]) if x[-1].replace('.', '', 1).isdigit() else -1, reverse=True)
    return [header] + rows

def filter_high_flammability(data, threshold=0.7):
    """Flammability 값이 threshold 이상인 항목 필터링!!!"""
    header, *rows = data
    filtered_rows = [row for row in rows if row[-1].replace('.', '', 1).isdigit() and float(row[-1]) >= threshold]
    return [header] + filtered_rows

def save_to_binary(data, file_path):
    """이진 파일로 데이터 저장"""
    with open(file_path, 'wb') as file: #'write binary (파일을 이진 모드로 엶)
        pickle.dump(data, file)

def load_from_binary(file_path):
    """이진 파일에서 데이터 읽기"""
    with open(file_path, 'rb') as file: #'read binary (파일을 이진 모드로 엶)
        data = pickle.load(file)
    return data

def main():
    file_path = "Mars_Base_Inventory_List.csv"  # CSV 파일 경로
    data = load_csv(file_path)
    
    if not data:
        print("CSV 파일이 비어 있습니다.")
        return
    
    sorted_data = sort_by_flammability(data)
    print("인화성 순으로 정렬된 화물 목록:")
    for row in sorted_data[:10]:  # 상위 10개만 출력
        print(row)
    
    dangerous_items = filter_high_flammability(sorted_data)
    print("\n인화성 지수가 0.7 이상인 화물 목록 (flammability >= 0.7):")
    for row in dangerous_items[:10]:  # 상위 10개만 출력
        print(row)
    
    # 이진 파일로 저장 (데이터를 빠르고 효율적으로 저장)
    save_to_binary(sorted_data, "Mars_Base_Inventory_List.bin")
    print("\n정렬된 데이터가 'Mars_Base_Inventory_List.bin'에 저장되었습니다.")
    
    # 이진 파일에서 읽기
    loaded_data = load_from_binary("Mars_Base_Inventory_List.bin")
    print("\n'Mars_Base_Inventory_List.bin'에서 읽어온 데이터:")
    for row in loaded_data[:10]:  # 상위 10개만 출력
        print(row)

if __name__ == "__main__":
    main()
