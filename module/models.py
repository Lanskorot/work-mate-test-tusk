from typing import Dict, List
from dataclasses import dataclass, field


@dataclass
class StudentData:
    '''Модель данных студента.'''
    name: str
    coffee_spent: List[float] = field(default_factory=list)
    
    def add_coffee(self, value: float) -> None:
        '''Добавляет значение затрат на кофе.'''
        self.coffee_spent.append(value)
    
    @property
    def average_coffee(self) -> float:
        '''Возвращает среднее значение затрат на кофе.'''
        if not self.coffee_spent:
            return 0.0
        return round(sum(self.coffee_spent) / len(self.coffee_spent), 2)