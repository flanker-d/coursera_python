from abc import ABC, abstractmethod

class HeroFactory(ABC):
    @abstractmethod
    def create_hero(self, name):
        pass

    @abstractmethod
    def create_spell(self):
        pass

    @abstractmethod
    def create_weapon(self):
        pass

class WarriorFactory(HeroFactory):
    def create_hero(self, name):
        return Warrior(name)

    def create_spell(self):
        return Power()

    def create_weapon(self):
        return Claymore()

class Warrior:
    def __init__(self, name):
        self.name = name
        self.spell = None
        self.weapon = None

    def add_weapon(self, weapon):
        self.weapon = weapon

    def add_spell(self, spell):
        self.spell = spell

    def hit(self):
        print(f"Warrior {self.name} hits with {self.weapon.hit()}")

    def cast(self):
        print(f"Warrior {self.name} casts {self.spell.cast()}")

class Claymore:
    def hit(self):
        return "Claymore"

class Power:
    def cast(self):
        return "Power"


def create_hero(factory):
    hero = factory.create_hero("Nagibator")

    weapon = factory.create_weapon()
    spell = factory.create_spell()

    hero.add_weapon(weapon)
    hero.add_spell(spell)

    return hero


player = create_hero(WarriorFactory())
player.hit()
player.cast()