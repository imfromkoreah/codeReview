import csv

def load_csv(file_path):
    """CSV 파일을 읽어 리스트로 반환"""
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def sort_by_flammability(data):
    """Flammability 값을 기준으로 내림차순 정렬"""
    header, *rows = data
    rows.sort(key=lambda x: float(x[-1]) if x[-1].replace('.', '', 1).isdigit() else -1, reverse=True)
    return [header] + rows

def filter_high_flammability(data, threshold=0.7):
    """Flammability 값이 threshold 이상인 항목 필터링"""
    header, *rows = data
    filtered_rows = [row for row in rows if row[-1].replace('.', '', 1).isdigit() and float(row[-1]) >= threshold]
    return [header] + filtered_rows

def main():
    file_path = "Mars_Base_Inventory_List.csv"  # CSV 파일 경로
    data = load_csv(file_path)
    
    if not data:
        print("CSV 파일이 비어 있습니다.")
        return
    
    sorted_data = sort_by_flammability(data)
    print("Sorted Inventory List (by Flammability):")
    for row in sorted_data[:10]:  # 상위 10개만 출력
        print(row)
    
    dangerous_items = filter_high_flammability(sorted_data)
    print("\nHigh Flammability Items (flammability >= 0.7):")
    for row in dangerous_items[:10]:  # 상위 10개만 출력
        print(row)

if __name__ == "__main__":
    main()
