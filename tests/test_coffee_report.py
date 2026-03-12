import pytest
import csv
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from module import CoffeeReport, StudentData


# === ТЕСТЫ StudentData ===

def test_student_data_creation():
    student = StudentData('Иван')
    assert student.name == 'Иван'
    assert student.coffee_spent == []
    assert student.average_coffee == 0


def test_student_data_add_coffee():
    student = StudentData('Иван')
    student.add_coffee(100)
    student.add_coffee(200)
    assert student.coffee_spent == [100, 200]
    assert len(student.coffee_spent) == 2


def test_student_data_average():
    student = StudentData('Иван')
    assert student.average_coffee == 0
    
    student.add_coffee(100)
    assert student.average_coffee == 100
    
    student.add_coffee(200)
    student.add_coffee(300)
    assert student.average_coffee == 200  # (100+200+300)/3 = 200


# === ТЕСТЫ CoffeeReport ===

def test_read_csv_simple():
    # Создаем простой CSV файл
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f:
        f.write('student,coffee_spent\n')
        f.write('Иван,150.50\n')
        f.write('Мария,200.00\n')
        temp_path = f.name
    
    try:
        report = CoffeeReport()
        report.read_data(temp_path)
        
        assert len(report.students) == 2
        assert 'Иван' in report.students
        assert 'Мария' in report.students
        assert report.students['Иван'].coffee_spent == [150.5]
    finally:
        os.unlink(temp_path)


def test_calculate_averages_simple():
    # Создаем CSV с данными
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f:
        f.write('student,coffee_spent\n')
        f.write('Иван,100\n')
        f.write('Иван,200\n')
        f.write('Мария,300\n')
        temp_path = f.name
    
    try:
        report = CoffeeReport()
        report.read_data(temp_path)
        result = report.calculate()
        
        assert len(result) == 2
        # Проверяем сортировку (по убыванию)
        assert result[0][0] == 'Мария'  # 300
        assert result[1][0] == 'Иван'   # 150
    finally:
        os.unlink(temp_path)


def test_empty_file_simple():
    # Пустой файл (только заголовки)
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f:
        f.write('student,coffee_spent\n')
        temp_path = f.name
    
    try:
        report = CoffeeReport()
        report.read_data(temp_path)
        assert len(report.students) == 0
        assert report.calculate() == []
    finally:
        os.unlink(temp_path)


def test_file_not_found_simple():
    report = CoffeeReport()
    with pytest.raises(FileNotFoundError):
        report.read_data('file_does_not_exist.csv')


def test_invalid_columns_simple():
    # CSV с неправильными колонками
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f:
        f.write('name,age\n')
        f.write('Иван,20\n')
        temp_path = f.name
    
    try:
        report = CoffeeReport()
        with pytest.raises(ValueError):
            report.read_data(temp_path)
    finally:
        os.unlink(temp_path)


def test_invalid_data_simple():
    # CSV с некорректными данными
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f:
        f.write('student,coffee_spent\n')
        f.write('Иван,не число\n')  # Плохое значение
        f.write('Мария,200.00\n')    # Хорошее значение
        temp_path = f.name
    
    try:
        report = CoffeeReport()
        report.read_data(temp_path)
        
        assert len(report.students) == 1
        assert 'Мария' in report.students
        assert 'Иван' not in report.students
    finally:
        os.unlink(temp_path)


def test_multiple_files_simple():
    report = CoffeeReport()
    
    # Первый файл
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f1:
        f1.write('student,coffee_spent\n')
        f1.write('Иван,100\n')
        path1 = f1.name
    
    # Второй файл
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f2:
        f2.write('student,coffee_spent\n')
        f2.write('Иван,200\n')
        f2.write('Мария,300\n')
        path2 = f2.name
    
    try:
        report.read_data(path1)
        report.read_data(path2)
        
        assert len(report.students) == 2
        assert len(report.students['Иван'].coffee_spent) == 2
        assert report.students['Иван'].coffee_spent == [100, 200]
        assert report.students['Мария'].coffee_spent == [300]
    finally:
        os.unlink(path1)
        os.unlink(path2)


def test_print_report_simple(capsys):
    # Создаем отчет с данными
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f:
        f.write('student,coffee_spent\n')
        f.write('Иван,150.50\n')
        temp_path = f.name
    
    try:
        report = CoffeeReport()
        report.read_data(temp_path)
        report.print_report()
        
        output = capsys.readouterr().out
        assert 'Имя' in output
        assert 'Среднее выпитое кофе' in output
        assert 'Иван' in output
        assert '150.5' in output
    finally:
        os.unlink(temp_path)


def test_print_report_empty_simple(capsys):
    report = CoffeeReport()
    report.print_report()
    assert 'Нет данных для отображения' in capsys.readouterr().out


def test_average_rounding_simple():
    # Тест округления до 2 знаков
    with tempfile.NamedTemporaryFile(mode='w', encoding='UTF-8', suffix='.csv', delete=False) as f:
        f.write('student,coffee_spent\n')
        f.write('Иван,100.333\n')
        f.write('Иван,200.667\n')
        temp_path = f.name
    
    try:
        report = CoffeeReport()
        report.read_data(temp_path)
        result = report.calculate()
        
        # (100.333 + 200.667)/2 = 150.5
        assert result[0][1] == 150.5
    finally:
        os.unlink(temp_path)