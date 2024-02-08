"""File to launch the clock application."""

from converter import UnitConverter
from converter_ui import ConverterUI
from unittype import UnitType

if __name__ == '__main__':
 
    # Create a unit converter and give it to the ConverterUI
    # via the constructor. This is called Dependency Injection.
    con = UnitConverter()
    uni = UnitType
    ui = ConverterUI(con, uni)
    ui.run()
