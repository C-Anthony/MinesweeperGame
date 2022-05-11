from tkinter import Label

import settings


class Btn:
    speed_btn = []
    difficulty_btn = []
    all = []

    def __init__(self, location, text, text_size):
        self.location = location
        self.text = text
        self.text_size = text_size
        self.btn_menu_object = None

        # Append the object to the correct Btn.all list
        if text in settings.SPEED:
            Btn.speed_btn.append(self)
        elif text in settings.DIFFICULTY:
            Btn.difficulty_btn.append(self)
        else:
            Btn.all.append(self)

    def create_btn_menu_object(self, action, argument):
        lbl = Label(
            self.location,
            text=self.text,
            width=12,
            height=1,
            bg='black',
            fg='white',
            font=("Snacker Comic Personal Use Only", self.text_size)
        )
        lbl.bind('<Button-1>', lambda event, arg=argument: action(event, argument))
        self.btn_menu_object = lbl

    @staticmethod
    def color_on_parameters(text):
        if text in settings.SPEED:
            for btn in Btn.speed_btn:
                if btn.text == text:
                    btn.btn_menu_object.configure(fg='red')
                else:
                    btn.btn_menu_object.configure(fg='white')
        elif text in settings.DIFFICULTY:
            for btn in Btn.difficulty_btn:
                if btn.text == text:
                    btn.btn_menu_object.configure(fg='red')
                else:
                    btn.btn_menu_object.configure(fg='white')
