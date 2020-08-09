from abc import abstractmethod, ABC


class Animal(ABC):
    body_size_dict = {
        '小': 1,
        '中等:': 2,
        '大': 3,
    }

    def __init__(self, name, animalType, body, characteristic):
        self.name = name
        self.animalType = animalType
        self.body = body
        self.characteristic = characteristic

    @property
    def is_beast(self):
        if self.animalType == '食肉' and self.characteristic == '凶猛':
            body_size = self.body_size_dict[self.body]
            if body_size >= 2:
                return True
        return False

    @abstractmethod
    def cry(self):
        pass


class Cat(Animal):
    def cry(self):
        print('miao')

    @property
    def is_fit_for_pet(self):
        return True


class Zoo:
    def __init__(self, name):
        self.name = name
        self.animals = []

    def _is_in_zoo(self, animal_name):
        for a in self.animals:
            if type(a).__name__ == animal_name:
                return True
        return False

    def add_animal(self, animal: Animal):
        can_add_animal = True
        for a in self.animals:
            if id(a) == id(animal):
                print('同一只动物（同一个动物实例）不能被重复添加')
                can_add_animal = False
        if can_add_animal:
            self.animals.append(animal)

    def __getattr__(self, item):
        return self._is_in_zoo(item)


if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    print(cat1.is_beast)
    print(cat1.cry())
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = getattr(z, 'Cat')
    print(have_cat)
