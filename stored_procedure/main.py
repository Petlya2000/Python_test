import argparse
import os
from tabulate import tabulate


def parse_csv(file_path):
    """
    Парсит CSV-файл и возвращает список словарей с данными сотрудников.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Определяем заголовки
    headers = [header.strip() for header in lines[0].split(',')]
    data = []

    # Читаем строки данных
    for line in lines[1:]:
        values = [value.strip() for value in line.split(',')]
        data.append(dict(zip(headers, values)))

    return data


def normalize_data(data):
    """
    Нормализует данные, приводя названия колонок к стандартным.
    """
    normalized_data = []
    for row in data:
        normalized_row = {
            'name': row.get('name'),
            'department': row.get('department'),
            'hours_worked': int(row.get('hours_worked', 0)),
            'hourly_rate': int(row.get('hourly_rate') or row.get('rate') or row.get('salary', 0)),
        }
        normalized_data.append(normalized_row)
    return normalized_data


def generate_payout_report(data):
    """
    Генерирует отчет по заработной плате.
    """
    report = {}
    for row in data:
        department = row['department']
        if department not in report:
            report[department] = {'employees': [], 'total_hours': 0, 'total_payout': 0}

        payout = row['hours_worked'] * row['hourly_rate']
        report[department]['employees'].append({
            'name': row['name'],
            'hours_worked': row['hours_worked'],
            'hourly_rate': row['hourly_rate'],
            'payout': payout,
        })
        report[department]['total_hours'] += row['hours_worked']
        report[department]['total_payout'] += payout

    return report


def print_payout_report(report):
    """
    Выводит отчет по заработной плате в виде таблицы.
    """
    for department, details in report.items():
        print(department)
        print('-' * len(department))
        
        # Подготовка данных для таблицы
        table_data = [
            [employee['name'], employee['hours_worked'], employee['hourly_rate'], f"${employee['payout']}"]
            for employee in details['employees']
        ]
        
        # Добавление итогов
        table_data.append(['', details['total_hours'], '', f"${details['total_payout']}"])
        
        # Вывод таблицы
        print(tabulate(table_data, headers=["name", "hours", "rate", "payout"], tablefmt="grid"))
        print()


def main():
    print("Скрипт запущен")  # Отладочное сообщение
    parser = argparse.ArgumentParser(description="Генерация отчетов по сотрудникам.")
    parser.add_argument('files', metavar='FILE', type=str, nargs='+') # help='Пути к CSV-файлам с данными сотрудников.')
    parser.add_argument('--report', type=str, required=True) # help='Тип отчета (например, payout).')

    args = parser.parse_args()
    print(f"Полученные аргументы: {args}")  # Отладочное сообщение

    # Читаем и объединяем данные из всех файлов
    all_data = []
    for file_path in args.files:
        print(f"Чтение файла: {file_path}")  # Отладочное сообщение
        if not os.path.exists(file_path):
            print(f"Файл {file_path} не найден.")
            continue
        data = parse_csv(file_path)
        print(f"Данные из файла {file_path}: {data}")  # Отладочное сообщение
        all_data.extend(normalize_data(data))

    # Генерация отчета
    if args.report == 'payout':
        report = generate_payout_report(all_data)
        print(f"Сформированный отчет: {report}")  # Отладочное сообщение
        print_payout_report(report)
    else:
        print(f"Отчет типа {args.report} не поддерживается.")


if __name__ == '__main__':
    main()
