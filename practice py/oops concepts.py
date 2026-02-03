# oop_examples.py
from abc import ABC, abstractmethod

# Abstraction & Polymorphism: Animal is abstract
class Animal(ABC):
    def __init__(self, name):
        self._name = name  # encapsulation (protected attribute convention)

    @abstractmethod
    def speak(self):
        pass

    def describe(self):
        print(f"I am {self._name} and I can {self._capability()}")

    def _capability(self):
        return "do something"

# Inheritance & Polymorphism
class Dog(Animal):
    def speak(self):
        return "Woof!"

    def _capability(self):
        return "bark"

class Cat(Animal):
    def speak(self):
        return "Meow!"

    def _capability(self):
        return "meow"

# Encapsulation example with getters/setters
class Person:
    def __init__(self, name, age):
        self.__name = name      # private attribute (name mangling)
        self.__age = age

    # getter
    def get_age(self):
        return self.__age

    # setter with validation
    def set_age(self, new_age):
        if new_age < 0:
            raise ValueError("Age cannot be negative")
        self.__age = new_age

    def __str__(self):
        return f"{self.__name} ({self.__age})"

if __name__ == "__main__":
    animals = [Dog("Rex"), Cat("Luna")]
    for a in animals:
        print(a._name, "says", a.speak())
        a.describe()

    p = Person("Kunal", 21)
    print(p)
    p.set_age(22)
    print("After birthday:", p)