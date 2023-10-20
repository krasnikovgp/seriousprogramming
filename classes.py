class Student:
    """
    Класс для представления силы человека.
    """

    def __init__(self, name, power, age, sex='М'):
        self.name = name
        self.sex = sex
        self.power = power
        self.age = age
        self.is_beated = False

    def fight(self, other):
        if other.is_beated:
            print(f'{other.name} уже побит!')
        elif self.is_beated:
            print(f'{self.name} уже побит!')
        if other.power > self.power:
            print(f'{other.name} побил {self.name}!')
            self.is_beated = True
        elif other.power < self.power:
            print(f'{self.name} побил {other.name}!')
            other.is_beated = True
        if self.sex == 'Ж' or other.sex == 'Ж':
            print('Вы не можете драться!')

    def greeting(self, other):
        if self.age < other.age:
            print(f'Здравствуйте, {other.name}!')
        else:
            print('Привет, шкет!')


if __name__ == '__main__':
    human1 = Student('Гоша', 8, 16)
    human2 = Student('Никита', 5, 16)
    human3 = Student('Марь Ивановна', -10, 99, 'Ж')
    human4 = Student('Глеб', 3, 11)

    human1.greeting(human3)
    human1.fight(human3)
    human1.greeting(human2)
    human1.fight(human2)
