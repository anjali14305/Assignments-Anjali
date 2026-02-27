'''Build a Student Analytics System that loads student data from students.json, validates it, 
performs calculations (average, pass/fail, comparisons),
and saves results into results.json.




'''

#Abstract Base Class --> Person (ABC) → abstract methods: get_details(), to_dict()


from typing import Dict , List , Any
from abc import ABC, abstractmethod
from contextlib import contextmanager
import json

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
        

    @property
    def marks(self) -> Dict[str,int]:
        return self.__marks
    
    @marks.setter
    def marks(self,value:Dict[str,int]):
        if not isinstance(value,dict):
            raise TypeError("Marks must be dictionary type")
        
        for subject,score in value.items(): 
            if not isinstance(score, int) or not (0 <= score <= 100):
                    raise ValueError(f"Invalid marks for {subject}")
        self.__marks = value

    def get_details(self) -> str:
        return f"{self.name} ({self.roll_number})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "roll_number": self.roll_number,
            "marks": self.__marks
        }

    def average(self) -> float:
        return sum(self.__marks.values()) / len(self.__marks)

    # Dunder Methods
    def __len__(self):
        return len(self.__marks)

    def __getitem__(self, subject):
        return self.__marks[subject]

    def __add__(self, other):
        total_marks = 0
        for key , value in self.__marks.items():
            total_marks += value

        for key , value in other.__marks.items():
            total_marks += value

    def __gt__(self, other):
        return self.average() > other.average()

    def __str__(self):
        return f"Student: {self.name}, Avg: {self.average():.2f}"

    def __repr__(self):
        return f"Student({self.name}, {self.roll_number})"
    

# Context Manager

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


#Decorator --> manual validation 

def validate_output(func):

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        required_fields = {
            "name": str,
            "roll_number": int,
            "average": float,
            "status": str
        }

        for field, field_type in required_fields.items():
            if field not in result:
                raise ValueError(f"Missing field: {field}")
            if not isinstance(result[field], field_type):
                raise TypeError(f"Invalid type for {field}")

        return result

    return wrapper


student1 = Student("kiat",21,{"english":66})
student2 = Student("riat",22,{"english":66})
print(student1.__add__(student2))


