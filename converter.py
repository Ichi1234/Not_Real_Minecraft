"""This module use for calculate unit and store unit value"""
from unittype import *


class UnitConverter:
    """This class use for calculate the value"""

    def __init__(self):
        """initialize of Converter class"""
        self.initial = None
        self.last_unit = None
        self.strategy = None

    def set_value(self, user_input, user_desired):
        """This method use user input to set value of attribute initial and last_unit"""
        self.initial = user_input
        self.last_unit = user_desired

    def get_units(self, type_of_unit):
        """return units"""
        try:
            val = list(type_of_unit)
            return val
        except TypeError:
            return 0

    @staticmethod
    def class_return(class_name: str):
        # get a class from an Enum

        for unit in list(UnitType):
            if class_name in unit.value:
                return unit.cls

        for length in list(LengthUnit):
            if class_name in length.value:
                return length

        for temp in list(TempUnit):
            if class_name in temp.value:
                return temp

        for money in list(TimeUnit):
            if class_name in money.value:
                return money

        for emerald in list(EmeraldUnit):
            if class_name in emerald.value:
                return emerald

        # unknown class
        return 0

    def calculator(self, value: int or float, strategy):
        """this method return converted value"""
        self.strategy = strategy

        return self.strategy.reality_breaker(self.initial, self.last_unit, value)


if __name__ == '__main__':  # test code
    c = UnitConverter()
    c.class_return("Emerald")
    # print(c.class_return("Kilometer"))

    # c.user_help_function()
