import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from stored_procedure.main import parse_csv, normalize_data, generate_payout_report
def test_parse_csv_empty_file(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("")
    with pytest.raises(IndexError): 
        parse_csv(empty_file)

def test_parse_csv_only_headers(tmp_path):
    headers_file = tmp_path / "headers.csv"
    headers_file.write_text("name,department,hours_worked,hourly_rate\n")
    data = parse_csv(headers_file)
    assert data == []
    
def test_parse_csv():
    data = parse_csv('test_data.csv')
    assert len(data) == 3
    assert data[0]['name'] == 'Alice Johnson'
    
def test_normalize_data_invalid_values():
    raw_data = [
        {'name': 'Alice', 'department': 'Marketing', 'hours_worked': 'invalid', 'hourly_rate': '50'},
        {'name': 'Bob', 'department': 'Design', 'hours_worked': '150', 'hourly_rate': 'invalid'},
    ]
    with pytest.raises(ValueError):  
        normalize_data(raw_data)
       
def test_normalize_data():
    raw_data = [
        {'name': 'Alice', 'department': 'Marketing', 'hours_worked': '160', 'hourly_rate': '50'},
        {'name': 'Bob', 'department': 'Design', 'hours_worked': '150', 'rate': '40'},
    ]
    normalized = normalize_data(raw_data)
    assert normalized[0]['hourly_rate'] == 50
    assert normalized[1]['hourly_rate'] == 40
    
def test_normalize_data_invalid_values():
    raw_data = [
        {'name': 'Alice', 'department': 'Marketing', 'hours_worked': 'invalid', 'hourly_rate': '50'},
        {'name': 'Bob', 'department': 'Design', 'hours_worked': '150', 'hourly_rate': 'invalid'},
    ]
    with pytest.raises(ValueError): 
        normalize_data(raw_data)

def test_generate_payout_report():
    data = [
        {'name': 'Alice', 'department': 'Marketing', 'hours_worked': 160, 'hourly_rate': 50},
        {'name': 'Bob', 'department': 'Design', 'hours_worked': 150, 'hourly_rate': 40},
    ]
    report = generate_payout_report(data)
    assert report['Marketing']['total_payout'] == 8000
    assert report['Design']['total_payout'] == 6000
