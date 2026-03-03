from typing import Dict, List, Any     #type hinting 
from abc import ABC, abstractmethod    #to create ABC 
from contextlib import contextmanager   
import json
from pathlib import Path



# Abstract Base Class

class Person(ABC):

    @abstractmethod
    def get_details(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass


# Student Class


class Student(Person):

    def __init__(self, name: str, roll_number: int, marks: Dict[str, int]):
        self.name = name
        self.roll_number = roll_number
        self.marks = marks   # uses setter validation

    # Encapsulation -> returns private variable
    @property
    def marks(self) -> Dict[str, int]:
        return self.__marks

    @marks.setter # -> returns values when assigned
    def marks(self, value: Dict[str, int]):
        if not isinstance(value, dict):
            raise TypeError("Marks must be in dictionary format.")

        for subject, score in value.items(): # looping through subjects in dict 
            if not isinstance(score, int) or not (0 <= score <= 100):
                raise ValueError(f"Invalid marks for {subject}")

        self.__marks = value

    # Required abstract method implementation 
    def get_details(self) -> str:
        return f"{self.name} ({self.roll_number})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "roll_number": self.roll_number,
            "marks": self.__marks
        }

    # calculating avg marks
    def average(self) -> float:
        if not self.__marks:
            return 0.0
        return sum(self.__marks.values()) / len(self.__marks) # total marks / no. of subject 

    # Dunder methods
    def __len__(self):
        return len(self.__marks)

    def __getitem__(self, subject):
        return self.__marks[subject]

    def __add__(self, other):
        if not isinstance(other, Student):
            raise TypeError("Can only add Student to Student")
        return sum(self.__marks.values()) + sum(other.__marks.values())

    def __gt__(self, other):
        return self.average() > other.average()

    def __str__(self):
        return f"Student: {self.name}, Avg: {self.average():.2f}"

    def __repr__(self):
        return f"Student({self.name}, {self.roll_number})"


# Context Manager


@contextmanager
def file_handler(file_name: str, mode: str):
    f = open(file_name, mode, encoding="utf-8")
    try:
        yield f
    finally:
        f.close()


# JSON Mixin


class JSONMixin: #helper method 

    @staticmethod # method does not depend on class instance
    def load_json(file_path: str) -> List[Dict[str, Any]]:
        path = Path(file_path)

        if not path.exists():
            print(f"{file_path} not found.")
            return []

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file) # reads json content 

            if not isinstance(data, list):
                raise ValueError("JSON must contain a list of students")

            return data

    @staticmethod
    def save_json(file_path: str, data: List[Dict[str, Any]]) -> None:
        path = Path(file_path)

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)   #writes in json format 



# Closure


def make_grader(min_pass: int):
    def grader(student: Student):
        return student.average() >= min_pass
    return grader



# Decorator


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
                raise TypeError(f"Invalid datatype for {field}")

        return result
    return wrapper



# Load Students


def load_students(filename: str) -> List[Student]:

    raw_data = JSONMixin.load_json(filename)

    valid_students: List[Student] = []
    invalid_students: List[Dict[str, Any]] = []

    for entry in raw_data:
        try:
            student = Student(**entry) # unpacking 
            valid_students.append(student)
        except Exception as e:
            print(f"Invalid student: {entry} | Error: {e}")
            invalid_students.append(entry)

    if invalid_students:
        JSONMixin.save_json("invalid_students.json", invalid_students)

    return valid_students


# Transformations


def uppercase_names(students: List[Student]) -> List[Student]:
    for student in students:
        student.name = student.name.upper()
    return students


@validate_output  #decorator function 
def compute_result(student: Student, grader) -> Dict[str, Any]:
    avg = student.average()
    return {
        "name": student.name,
        "roll_number": student.roll_number,
        "average": float(avg),
        "status": "PASS" if grader(student) else "FAIL"  #closure for garding 
    }


# Main


def main() -> None:
    try:
        grader = make_grader(40)  #min marks to pass is 40 

        students = load_students("students.json")

        if not students:
            print("No student data found..........Exiting!...........")
            return

        students = uppercase_names(students)

        results = [compute_result(s, grader) for s in students]

        JSONMixin.save_json("results.json", results)  # saving final result 
        print("...........Final ouput............")
        for r in results:
            print(f"Name : {r['name']}")
            print(f"Roll Number : {r['roll_number']}")
            print(f"Average : {r['average']}")
            print(f"Status : {r['status']}") 
            print("-----------------------------------")   
        print("Processing completed successfully.")

    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    # student = Student("Aana",101,{"maths" : 80 , "science": 70})
    # print("Student object : ", student )
    # print("Average marks : " , student.average())

    # grader = make_grader(40)
    # print("Pass/Fail: " , grader(student))

    # result = compute_result(student, grader)
    # print("Final resut : ", result )

    main()

