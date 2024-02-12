import tkinter as tk
import tkinter.messagebox
import platform
from tkinter import ttk, font
from converter import *
from pygame import mixer

FONT = ("Old English Text MT", 18)


class ConverterUI(tk.Tk):
    """User Interface for a unit converter.

    The UI displays units and handles user interaction.  It invokes 
    a UnitConverter object to perform actual unit conversions.
    """

    def __init__(self, kon: UnitConverter, unit_type: UnitType):
        """initialize for ConverterUI"""
        super().__init__()
        self.converter = kon
        self.unit_type = unit_type
        self.title("Not Minecraft")

        # String variable
        self.unit_name1 = tk.StringVar()
        self.unit_name2 = tk.StringVar()

        # Integer variable
        self.user_int_left = tk.IntVar()
        self.user_int_right = tk.IntVar()

        self.strategy = LengthUnit

        # background
        self.bg = tk.PhotoImage(file="wood.png")
        background = tk.Label(self, image=self.bg)
        background.place(x=0, y=0)

        # set default font (Minecraft font work only in windows)
        if platform.system() == "Windows":
            import pyglet
            pyglet.font.add_file('Minecraft_font.otf')
            self.font = font.Font(family="Minecraft", size=18, name="minecraft_font")

        else:
            self.font = FONT

        # user_select_unit
        self.convert_program = tk.Text(self, height=1.3, width=11, font=self.font)
        self.convert_program.insert("1.0", "Length")
        self.convert_program.config(state="disabled")

        self.unit_select1 = ttk.Combobox(self, width=11, textvariable=self.unit_name1, font=self.font)
        self.unit_select2 = ttk.Combobox(self, width=11, textvariable=self.unit_name2, font=self.font)

        # user_input_number
        self.input_left = tk.Entry(self, width=10, font=self.font, textvariable=self.user_int_left, bg="white")
        self.input_right = tk.Entry(self, width=10, font=self.font, textvariable=self.user_int_right, bg="white")

        self.init_components()
        self.load_units(self.strategy)
        self.clear_input()

        # add bgm
        mixer.init()
        mixer.music.load("Wet_Hands.mp3")
        mixer.music.set_volume(0.2)
        mixer.music.play(loops=-1)

    @staticmethod
    def play_click_sound(event):
        """Left mouse click sound"""
        effect = mixer.Sound("Minecraft_Button.mp3")
        effect.set_volume(0.4)
        effect.play()

    def set_strategy(self, unit_type):
        """set strategy"""
        self.strategy = unit_type.cls
        self.load_units(self.strategy)
        self.play_click_sound(self)

        # update current display
        self.convert_program.config(state="normal")
        self.convert_program.delete("1.0", "end")
        self.convert_program.insert("1.0", unit_type.cls_name)
        self.convert_program.config(state="disabled")

        # Update combobox values
        self.unit_select1['value'] = self.converter.get_units(self.strategy)
        self.unit_select1.current(newindex=0)

        self.unit_select2['value'] = self.converter.get_units(self.strategy)
        self.unit_select2.current(newindex=0)

    def init_components(self):
        """Create components and layout the UI."""
        # use a frame as internal container
        # this will help later when the UI gets more complex
        # Add image file
        img = tk.PhotoImage(file="minecraft_logo.png")
        # change icon photo for window user
        self.iconphoto(False, img)

        # menu bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=False)
        for cls_and_name in UnitType:
            file_menu.add_command(label=cls_and_name.cls_name,
                                  command=lambda class_str=cls_and_name: self.set_strategy(class_str))

        # add cascade
        menubar.add_cascade(label="Units", menu=file_menu, underline=0)
        menubar.add_cascade(label='Exit', command=self.destroy)

        # button
        converter_button = tk.Button(self, text="Convert!", font=self.font, command=self.convert_handler)
        clear_button = tk.Button(self, text="Clear", font=self.font, command=self.clear_input)

        # binding
        self.input_left.bind('<Return>', lambda event=None: self.convert_handler())
        self.input_right.bind('<Return>', lambda event=None: self.convert_handler())

        self.input_left.bind("<FocusIn>", self.play_click_sound)
        self.input_right.bind("<FocusIn>", self.play_click_sound)

        self.unit_select1.bind("<Button-1>", self.play_click_sound)
        self.unit_select2.bind("<Button-1>", self.play_click_sound)
        self.unit_select1.bind("<<ComboboxSelected>>", self.play_click_sound)
        self.unit_select2.bind("<<ComboboxSelected>>", self.play_click_sound)

        converter_button.bind("<Button-1>", self.play_click_sound)
        clear_button.bind("<Button-1>", self.play_click_sound)

        # text
        label = tk.Label(self, text="=", font=self.font)

        # Configure columns to expand
        for colum in range(6):
            self.columnconfigure(colum, weight=1)

        # Configure rows to expand
        for row in range(2):
            self.rowconfigure(row, weight=1)

        pad_x = 10
        pad_y = 10
        self.convert_program.grid(row=0, column=0, padx=14, pady=22, sticky="news")
        self.input_left.grid(row=1, column=0, padx=pad_x, pady=pad_y, sticky="news")
        self.unit_select1.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky="news")
        label.grid(row=1, column=2, padx=pad_x, pady=pad_y, sticky="news")

        self.input_right.grid(row=1, column=3, padx=pad_x, pady=pad_y, sticky="news")
        self.unit_select2.grid(row=1, column=4, padx=pad_x, pady=pad_y, sticky="news")
        converter_button.grid(row=1, column=5, padx=pad_x, pady=20, sticky="news")
        clear_button.grid(row=1, column=6, padx=pad_x, pady=20, sticky="news")

    def clear_input(self):
        """This use to clear all input from tk.enry"""
        self.input_left.configure(fg="black")
        self.input_right.configure(fg="black")
        self.input_left.delete(0, tk.END)
        self.input_right.delete(0, tk.END)

    def load_units(self, unit_type):  # self.strategy
        """Load units of the requested unittype into the comboboxes."""
        units = self.converter.get_units(unit_type)

        # show unit in the combo box
        self.unit_select1['value'] = units
        self.unit_select1.current(newindex=0)

        self.unit_select2['value'] = units
        self.unit_select2.current(newindex=0)

    def convert_handler(self):
        """An event handler for conversion actions.
        You should call the unit converter to perform actual conversion.
        """
        self.input_left.configure(fg="black")
        self.input_right.configure(fg="black")

        check_first_val = self.input_left.get()
        check_second_val = self.input_right.get()

        if not check_first_val and not check_second_val:
            tkinter.messagebox.showerror(title="Oi!", message="You should input some value.")
            self.bell()
            return None

        try:

            get_first_unit = self.unit_select1.get()
            get_second_unit = self.unit_select2.get()

            first_unit = self.converter.class_return(get_first_unit)
            second_unit = self.converter.class_return(get_second_unit)

            first_value = float(check_first_val) if check_first_val else 0
            second_value = float(check_second_val) if check_second_val else 0

            if first_value != 0 and second_value == 0:
                self.converter.set_value(first_unit, second_unit)

                # Set the converted value in the right input field
                converted_value = self.converter.calculator(first_value, self.strategy)
                self.input_right.delete(0, tk.END)
                self.input_right.insert(0, str(converted_value))

            elif second_value != 0 and first_value == 0:
                self.converter.set_value(second_unit, first_unit)

                # Set the converted value in the right input field
                converted_value = self.converter.calculator(second_value, self.strategy)
                self.input_left.delete(0, tk.END)
                self.input_left.insert(0, str(converted_value))

            else:
                self.converter.set_value(first_unit, second_unit)

                # Set the converted value in the right input field
                converted_value = self.converter.calculator(first_value, self.strategy)
                self.input_right.delete(0, tk.END)
                self.input_right.insert(0, str(converted_value))

        except ValueError:

            if check_first_val.isalpha():
                self.input_left.configure(fg="red")

            if check_second_val.isalpha():
                self.input_right.configure(fg="red")

            tkinter.messagebox.showerror(title="WHAT", message="Invalid value git gud!.")
            self.bell()
            return None

    def run(self):
        """use to run program"""
        # start the app, wait for events 
        self.mainloop()


if __name__ == "__main__":
    converter = UnitConverter()
    uni = UnitType
    ui = ConverterUI(converter, uni)
    ui.run()
