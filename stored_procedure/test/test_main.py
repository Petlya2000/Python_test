import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from stored_procedure.main import parse_csv, normalize_data, generate_payout_report

def test_parse_csv():
    data = parse_csv('test_data.csv')
    assert len(data) == 3
    assert data[0]['name'] == 'Alice Johnson'

def test_normalize_data():
    raw_data = [
        {'name': 'Alice', 'department': 'Marketing', 'hours_worked': '160', 'hourly_rate': '50'},
        {'name': 'Bob', 'department': 'Design', 'hours_worked': '150', 'rate': '40'},
    ]
    normalized = normalize_data(raw_data)
    assert normalized[0]['hourly_rate'] == 50
    assert normalized[1]['hourly_rate'] == 40


def test_generate_payout_report():
    data = [
        {'name': 'Alice', 'department': 'Marketing', 'hours_worked': 160, 'hourly_rate': 50},
        {'name': 'Bob', 'department': 'Design', 'hours_worked': 150, 'hourly_rate': 40},
    ]
    report = generate_payout_report(data)
    assert report['Marketing']['total_payout'] == 8000
    assert report['Design']['total_payout'] == 6000
