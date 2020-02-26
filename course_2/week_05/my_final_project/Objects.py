from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite

class AbstractObject(ABC):

    def __init__(self, icon, position):
        self.sprite = icon
        self.position = position

    def draw(self, display):
        display.draw_object(self.sprite, self.position)


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        super().__init__(icon, position)
        self.action = action

    def interact(self, engine, hero):
        self.action(engine, hero)

class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        super().__init__(icon, position)
        self.stats = stats
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass

# class Berserk(AbstractPositive):
#
#     def get_positive_effects(self):
#         return self.prepare_effects('Berserk')
#
#     def get_stats(self):
#         stats = self.base.get_stats()
#         stats["Strength"] += 7
#         stats["Endurance"] += 7
#         stats["Agility"] += 7
#         stats["Luck"] += 7
#         stats["Perception"] -= 3
#         stats["Charisma"] -= 3
#         stats["Intelligence"] -= 3
#         stats["HP"] += 50
#         return stats
#
#
# class Blessing(AbstractPositive):
#
#     def __init__(self, base):
#         self.base = base
#
#     def get_positive_effects(self):
#         return self.prepare_effects('Blessing')
#
#     def get_stats(self):
#         stats = self.base.get_stats()
#         stats["Strength"] += 2
#         stats["Perception"] += 2
#         stats["Endurance"] += 2
#         stats["Charisma"] += 2
#         stats["Intelligence"] += 2
#         stats["Agility"] += 2
#         stats["Luck"] += 2
#         return stats
#
#
# class Weakness(AbstractNegative):
#
#     def __init__(self, base):
#         self.base = base
#
#     def get_negative_effects(self):
#         return self.prepare_effects('Weakness')
#
#     def get_stats(self):
#         stats = self.base.get_stats()
#         stats["Strength"] -= 4
#         stats["Endurance"] -= 4
#         stats["Agility"] -= 4
#
#         return stats
#
# class EvilEye(AbstractNegative):
#
#     def __init__(self, base):
#         self.base = base
#
#     def get_negative_effects(self):
#         return self.prepare_effects('EvilEye')
#
#     def get_stats(self):
#         stats = self.base.get_stats()
#         stats["Luck"] -= 10
#         return stats
#
# class Curse(AbstractNegative):
#
#     def __init__(self, base):
#         self.base = base
#
#     def get_negative_effects(self):
#         return self.prepare_effects('Curse')
#
#     def get_stats(self):
#         stats = self.base.get_stats()
#         stats["Strength"] -= 2
#         stats["Perception"] -= 2
#         stats["Endurance"] -= 2
#         stats["Charisma"] -= 2
#         stats["Intelligence"] -= 2
#         stats["Agility"] -= 2
#         stats["Luck"] -= 2
#         return stats


# FIXME
# add classes