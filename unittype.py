"""An enumeration of known types of units."""
import enum


class LengthUnit(enum.Enum):
    """This class collect all length unit"""

    # 5 metric unit
    KM = (1, "Kilometer")
    M = (1000, "Meter")
    DM = (10000, "Decimeter")
    CM = (100000, "Centimeter")
    MM = (1000000, "Millimeter")

    # 2 Thai unit
    YOT = (0.0625, "Yot")
    WA = (500, "Wa")

    # 2 Japanese unit
    HIRO = (550, "Hiro")
    SHAKU = (3300, "Shaku")

    def __init__(self, integer, full_unit):
        """initialize of LengthUnit"""
        self.integer = integer
        self.full_unit = full_unit

    @staticmethod
    def reality_breaker(first_unit, desire_unit, user_value):
        """Convert the first value to desired value"""

        if "Kilometer" in first_unit.value:  # KM is default value for convert to other
            return f"{user_value * desire_unit.integer:.5g}"

        value_to_km = user_value / first_unit.integer  # convert this unit to km

        return f"{value_to_km * desire_unit.integer:.5g}"

    def __str__(self):
        return self.full_unit


class TempUnit(enum.Enum):
    """This class collect all temperature unit"""

    CELSIUS = ({"offset": 0, "mul": 1}, "Celsius")
    KELVIN = ({"offset": 273.15, "mul": 1}, "Kelvin")  # K = (C * 1) + 273.15  , C = (K - 273.15)/1
    FAHRENHEIT = ({"offset": 32, "mul": 1.8}, "Fahrenheit")  # F = (C * 1.8) +32 , C = (F - 32)/1.8

    def __init__(self, integer, value_name):
        """initialize of TempUnit"""
        self.integer = integer
        self.value_name = value_name

    @staticmethod
    def reality_breaker(first_unit, desire_unit, user_value):
        """Convert the first value to desired value"""

        if "Celsius" in first_unit.value:  # Celsius is default value
            return f"{(user_value * desire_unit.integer['mul']) + desire_unit.integer['offset']:.5g}"

        # convert this unit to Celsius
        value_to_celsius = (user_value - first_unit.integer['offset']) / first_unit.integer['mul']

        return f"{(value_to_celsius * desire_unit.integer['mul']) + desire_unit.integer['offset'] :.5g}"

    def __str__(self):
        return self.value_name


class TimeUnit(enum.Enum):
    """This class collect all money unit"""

    HOUR = (1, "Hour")
    MINUTE = (60, "Minute")
    SEC = (3600, "Second")


    @staticmethod
    def reality_breaker(first_unit, desire_unit, user_value):
        """Convert the first value to desired value"""

        if "Hour" in first_unit.value:  # Year is default value for convert to other
            return f"{user_value * desire_unit.integer:.5g}"

        value_to_baht = user_value / first_unit.integer  # convert this unit to km

        return f"{value_to_baht * desire_unit.integer:.5g}"

    def __init__(self, integer, full_unit):
        """initialize of LengthUnit"""
        self.integer = integer
        self.full_unit = full_unit

    def __str__(self):
        return self.full_unit


class EmeraldUnit(enum.Enum):
    """This class collect all length unit"""
    # Player can Buy and Sell (Vanilla Minecraft cant do this)
    # info inspired from https://minecraft.fandom.com/wiki/Trading

    EM = (1, "Emerald")
    COAL = (1/15, "Coal")
    FLINT = (1/24, "Flint")
    I_AXE = (3, "Iron Axe")
    I_SWORD = (8, "Iron Sword")
    D_AXE = (18, "Diamond Axe")

    def __init__(self, integer, full_unit):
        """initialize of LengthUnit"""
        self.integer = integer
        self.full_unit = full_unit

    @staticmethod
    def reality_breaker(first_unit, desire_unit, user_value):
        """Convert the first value to desired value"""

        if "Emerald" in first_unit.value:  # Emerald is default value for convert to other
            return f"{(user_value // desire_unit.integer):.5g}"

        value_to_em = user_value * first_unit.integer  # convert this unit to Emerald

        return f"{value_to_em // desire_unit.integer:.5g}"

    def __str__(self):
        return self.full_unit


class UnitType(enum.Enum):
    """Define the unittypes here.  The value is the printable type name."""
    LENGTH = ("Length", LengthUnit)
    TIME = ("Time", TimeUnit)  # you can change Area to some other unittype
    TEMPERATURE = ("Temperature", TempUnit)
    EMERALD = ("Villager", EmeraldUnit)

    def __init__(self, name, cls):
        self.cls_name = name
        self.__cls = cls

    @property
    def cls(self):
        return self.__cls

    def __str__(self):
        """Return the unittype name suitable for printing."""
        return self.cls_name


if __name__ == '__main__':  # test code
    print(LengthUnit["KM"])
    print(LengthUnit)
    print(EmeraldUnit.EM)
    print(EmeraldUnit)
