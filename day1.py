'''Build a Student Analytics System that loads student data from students.json, validates it, 
performs calculations (average, pass/fail, comparisons),
and saves results into results.json.




'''

#Abstract Base Class --> Person (ABC) → abstract methods: get_details(), to_dict()

from abc import ABC, abstractmethod

class Person(ABC):

    @abstractmethod
    def get_details(self) -> str:
        pass

    def to_dict(self) -> dict:
        pass 

'''
Inherits Person
Attributes: name: str, roll_number: int, marks: dict[str, int]
Encapsulation: private __marks + @property validation (0–100)
'''

# Student Class

class Student(Person):
    def __init__(self,name: str, roll_number: int, marks: dict[str, int]):
        self.name = name
        self.roll_number = roll_number
        self.marks = marks

# Context Manager

from contextlib import contextmanager

@contextmanager
def file_handler(file_name:str, mode:str):
    try:
        f = open(file_name,mode)
        yield f
    finally:
        f.close()

'''
JsonMixin → save/load data (students.json, results.json) file operation 
handled through context manager
'''

# Mixins - define






# Closure: make_grader(min_pass) → pass/fail checker

def make_grader(min_pass:int):
    def grader(student:Student):
        return student.average() >= min_pass
    return grader


