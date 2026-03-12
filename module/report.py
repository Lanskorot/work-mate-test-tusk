import csv
from typing import Dict, List, Optional
from tabulate import tabulate

from module.models import StudentData


class BaseReport:
    '''Абстрактный базовый класс для отчетов.'''
    
    def read_data(self, file_path: str) -> None:
        '''Читает данные из файла.'''
        raise NotImplementedError
    
    def calculate(self) -> List:
        '''Вычисляет данные для отчета.'''
        raise NotImplementedError
    
    def print_report(self) -> None:
        '''Выводит отчет.'''
        raise NotImplementedError


class CoffeeReport(BaseReport):
    '''Отчет по потреблению кофе.'''
    
    def __init__(self):
        self.students: Dict[str, StudentData] = {}
        self.REQUIRED_COLUMNS = {'student', 'coffee_spent'}

    def _validate_columns(self, fieldnames: Optional[List[str]]) -> bool:
        '''Проверяет наличие необходимых колонок в CSV.'''
        if not fieldnames:
            return False
        return all(col in fieldnames for col in self.REQUIRED_COLUMNS)

    def read_data(self, file_path: str) -> None:
        '''Читает CSV файл с данными о студентах-любителях кофе.
        
        Args:
            file_path: Путь к CSV файлу.
            
        Raises:
            FileNotFoundError: Если файл не существует.
            ValueError: Если отсутствуют необходимые колонки.
        '''
        try:
            with open(file_path, 'r', encoding='UTF-8') as csv_file:
                reader = csv.DictReader(csv_file)
                
                if not self._validate_columns(reader.fieldnames):
                    raise ValueError(
                        f"Файл {file_path} не содержит колонок: "
                        f"{', '.join(self.REQUIRED_COLUMNS)}"
                    )

                for row in reader:
                    try:
                        coffee_val = float(row['coffee_spent'])
                    except ValueError:
                        continue
                        
                    student_name = row['student']
                    if student_name not in self.students:
                        self.students[student_name] = StudentData(name=student_name)
                    
                    self.students[student_name].add_coffee(coffee_val)
                        
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Файл не найден: {file_path}") from e
                    
    def calculate(self) -> List:
        '''Вычисляет среднее потребление кофе для каждого студента.
        
        Returns:
            Отсортированный по убыванию список студентов.
        '''
        table_data = []
        for student in self.students.values():
            table_data.append([student.name, student.average_coffee])
        return sorted(table_data, key=lambda x: x[1], reverse=True)

    def print_report(self) -> None:
        '''Форматирует и выводит отчёт.'''
        table_data = self.calculate()
        if not table_data:
            print("Нет данных для отображения")
            return
            
        print(tabulate(
            table_data,
            headers=['Имя', 'Среднее выпитое кофе'],
            tablefmt='fancy_grid'
        ))