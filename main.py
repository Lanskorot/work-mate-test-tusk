#!/usr/bin/env python3
'''Модуль для анализа затрат на кофе.'''

import argparse
import sys
from typing import NoReturn

from module import CoffeeReport


def create_parser() -> argparse.ArgumentParser:
    '''Создает парсер аргументов командной строки.'''
    parser = argparse.ArgumentParser(
        description='Анализ затрат на кофе',
        epilog='Пример: %(prog)s -f data1.csv data2.csv'
    )
    
    parser.add_argument(
        '-f', '--files',
        nargs='+',
        required=True,
        help='CSV файлы с данными (минимум 1 файл)'
    )
    
    parser.add_argument(
        '--report',
        default='median-coffee',
        choices=['median-coffee'],
        help='Тип отчета (доступен только median-coffee)'
    )
    
    return parser


def validate_files(file_paths: list) -> None:
    '''Проверяет существование файлов.'''
    import os
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")


def main() -> NoReturn:
    '''Главная функция приложения.'''
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        # Валидация файлов
        validate_files(args.files)
        
        # Создание и запуск отчета
        analyzer = CoffeeReport()
        for file_path in args.files:
            analyzer.read_data(file_path)
        
        analyzer.print_report()
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка валидации: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()