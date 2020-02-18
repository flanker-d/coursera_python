# PyYaml 3.13 required
import yaml

hero_yaml = """
--- !Character
factory:
    !factory assassin
name:
    7NaGiBaToR7
"""

class HeroFactory:
    @classmethod
    def create_hero(Class, name):
        return Class.Hero(name)

    @classmethod
    def create_spell(Class):
        return Class.Spell()

    @classmethod
    def create_weapon(Class):
        return Class.Weapon()

class WarriorFactory(HeroFactory):
    class Hero:
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

    class Weapon:
        def hit(self):
            return "Claymore"

    class Spell:
        def cast(self):
            return "Power"


class MageFactory(HeroFactory):
    class Hero:
        def __init__(self, name):
            self.name = name
            self.spell = None
            self.weapon = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):
            print(f"Mage {self.name} hits with {self.weapon.hit()}")

        def cast(self):
            print(f"Mage {self.name} casts {self.spell.cast()}")

    class Weapon:
        def hit(self):
            return "Staff"

    class Spell:
        def cast(self):
            return "Fireball"


class AssassinFactory(HeroFactory):
    class Hero:
        def __init__(self, name):
            self.name = name
            self.spell = None
            self.weapon = None

        def add_weapon(self, weapon):
            self.weapon = weapon

        def add_spell(self, spell):
            self.spell = spell

        def hit(self):
            print(f"Assasin {self.name} hits with {self.weapon.hit()}")

        def cast(self):
            print(f"Assasin {self.name} casts {self.spell.cast()}")

    class Weapon:
        def hit(self):
            return "Dagger"

    class Spell:
        def cast(self):
            return "Invisibility"

def factory_constructor(loader, node):
    data = loader.construct_scalar(node)
    if data == "assassin":
        return AssassinFactory
    elif data =="mage":
        return MageFactory
    else:
        return WarriorFactory

class Character(yaml.YAMLObject):
    yaml_tag = "!Character"

    def create_hero(self):
        hero = self.factory.create_hero(self.name)

        weapon = self.factory.create_weapon()
        spell = self.factory.create_spell()

        hero.add_weapon(weapon)
        hero.add_spell(spell)

        return hero

loader = yaml.Loader
loader.add_constructor("!factory", factory_constructor)
hero = yaml.load(hero_yaml).create_hero()
hero.hit()
hero.cast()