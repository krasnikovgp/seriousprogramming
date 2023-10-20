from classes import Student


class Male(Student):
    def __init__(self, name, power, age):
        super().__init__(name, power, age)


class Female(Student):
    def __init__(self, name, power, age):
        super().__init__(name, power, age, 'Ж')


class StrongMale(Student):
    def __init__(self, name, age, power=10):
        super().__init__(name, age, 'М')


class StrongFemale(Student):
    def __init__(self, name, age, power=10):
        super().__init__(name, age, 'Ж')


person1 = Male('Тема', 4, 18)
person2 = Female('Маша', 2, 18)
person3 = StrongMale('Гриша', 20)
person4 = StrongFemale('Женя', 17)
