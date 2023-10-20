from classes import Student


class Male(Student):
    def __init__(self, name, power, age):
        super().__init__(name, power, age, 'М')


class Female(Student):
    def __init__(self, name, power, age):
        super().__init__(name, power, age, 'Ж')


class StrongMale(Student):
    def __init__(self, name, power, age):
        super().__init__(name, power, age, 'М')


class StrongFemale(Student):
    def __init__(self, name, power, age):
        super().__init__(name, power, age, 'Ж')


person1 = Male('Тема', 4, 18)
person2 = Female('Маша', 2, 18)
person3 = StrongMale('Гриша', 10, 20)
person4 = StrongFemale('Женя', 9, 17)

person1.fight(person3)
person4.greeting(person2)
person1.greeting(person4)
