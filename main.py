# Imports
from tkinter import *

from cell import Cell
from menu import Btn
import settings
import utils


# Instantiation of the window
root = Tk()

#  Override the settings of the window
root.configure(bg='black')  # background color of the window
root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')  # size of the window : Width x Height
root.title('MineSweeper Game')  # Title of the window
root.resizable(False, False)  # Window not resizable

# Creation of the top frame
top_frame = Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height=utils.height_prct(25)
)
top_frame.place(
    x=0, y=0
)

game_title = Label(
    top_frame,
    bg='black',
    fg='white',
    text='Minesweeper Game',
    font=('Snacker Comic Personal Use Only', 75)
)
game_title.place(x=utils.width_prct(50), y=utils.height_prct(25)/2, anchor=CENTER)

# Creation of the center Frame
center_frame = Frame(
    root,
    bg='black',  # Change to black later
    width=utils.width_prct(50),
    height=utils.height_prct(50)
)
center_frame.place(
    x=utils.width_prct(50),
    y=utils.height_prct(50),
    anchor=CENTER
)

# Creation of the left frame
left_frame = Frame(
    root,
    bg='black',
    width=utils.width_prct(25),
    height=utils.height_prct(50)
)
left_frame.place(
    x=0,
    y=utils.height_prct(25)
)

speed_label = Label(
        left_frame,
        width=12,
        height=1,
        bg='black',
        fg='white',
        font=('Snacker Comic Personal Use Only', 40),
        text='Speed'
    )
speed_label.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*1/12, anchor=CENTER)
fast_speed = Btn(left_frame, 'fast', 25)
fast_speed.create_btn_menu_object(Cell.set_speed, argument='fast')
fast_speed.btn_menu_object.place(x=utils.width_prct(25) / 2, y=utils.height_prct(50) * 2 / 12, anchor=CENTER)
normal_speed = Btn(left_frame, 'normal', 25)
normal_speed.create_btn_menu_object(Cell.set_speed, argument='normal')
normal_speed.btn_menu_object.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*3/12, anchor=CENTER)
long_speed = Btn(left_frame, 'long', 25)
long_speed.create_btn_menu_object(Cell.set_speed, argument='long')
long_speed.btn_menu_object.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*4/12, anchor=CENTER)

difficulty_label = Label(
        left_frame,
        width=12,
        height=1,
        bg='black',
        fg='white',
        font=('Snacker Comic Personal Use Only', 40),
        text='Difficulty'
    )
difficulty_label.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*6/12, anchor=CENTER)
easy_difficulty = Btn(left_frame, 'easy', 25)
easy_difficulty.create_btn_menu_object(Cell.set_difficulty, argument='easy')
easy_difficulty.btn_menu_object.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*7/12, anchor=CENTER)
medium_difficulty = Btn(left_frame, 'medium', 25)
medium_difficulty.create_btn_menu_object(Cell.set_difficulty, argument='medium')
medium_difficulty.btn_menu_object.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*8/12, anchor=CENTER)
hard_difficulty = Btn(left_frame, 'hard', 25)
hard_difficulty.create_btn_menu_object(Cell.set_difficulty, argument='hard')
hard_difficulty.btn_menu_object.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*9/12, anchor=CENTER)

# Creation of the right frame
right_frame = Frame(
    root,
    bg='black',
    width=utils.width_prct(25),
    height=utils.height_prct(50)
)
right_frame.place(x=utils.width_prct(75), y=utils.height_prct(25))

cell_count_label = Label(
        right_frame,
        text="Cells left:",
        width=12,
        height=2,
        bg='black',
        fg='white',
        font=("Snacker Comic Personal Use Only", 40)
    )
cell_count_label.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*2/8, anchor=CENTER)

# Call the labels from the Cell class
Cell.create_cell_count_number_label(right_frame)
Cell.cell_count_number_label_object.place(
    x=utils.width_prct(25)/2,
    y=utils.height_prct(50)*3/8,
    anchor=CENTER
)

mines_count_label = Label(
            right_frame,
            text="Mines left:",
            width=12,
            height=2,
            bg='black',
            fg='white',
            font=("Snacker Comic Personal Use Only", 40)
        )
mines_count_label.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*5/8, anchor=CENTER)

# Call the labels from the Cell class
Cell.create_mines_count_number_label(right_frame)
Cell.mines_count_number_label_object.place(
    x=utils.width_prct(25)/2,
    y=utils.height_prct(50)*6/8,
    anchor=CENTER
)

# Creation of the bottom side bar Frame
bottom_frame = Frame(
    root,
    bg='black',
    width=settings.WIDTH,
    height=utils.height_prct(25)
)
bottom_frame.place(
    x=0,
    y=utils.height_prct(75)
)

# Call the labels from the Cell class
Cell.create_status_label(bottom_frame)
Cell.status_label_object.place(
    x=utils.width_prct(50),
    y=utils.height_prct(25)/2,
    anchor=CENTER
)


def restart_game(event=None, location=center_frame):
    # Erase cells
    for c in Cell.all:
        c.cell_btn_object.destroy()
    Cell.all = []
    # Erase text from bottom frame
    Cell.status_label_object.configure(text='')
    # Initialize counters (cells and mines) and reset counter labels
    Cell.cell_count_method()
    Cell.mines_count = Cell.set_mines_count()
    Cell.cell_count_number_label_object.configure(text=f"{Cell.cell_count}")
    Cell.mines_count_number_label_object.configure(text=f"{Cell.mines_count}")
    # Creation of the grid game
    for x in range(Cell.grid_size()):
        for y in range(Cell.grid_size()):
            c = Cell(x, y)
            c.create_btn_object(location)
            c.cell_btn_object.grid(column=x, row=y)
    # Creation of the mines
    Cell.randomize_mines()
    Btn.color_on_parameters(Cell.speed)
    Btn.color_on_parameters(Cell.difficulty)


# Restart button
restart_button = Btn(left_frame, 'Restart', 50)
restart_button.create_btn_menu_object(restart_game, argument=center_frame)
restart_button.btn_menu_object.place(x=utils.width_prct(25)/2, y=utils.height_prct(50)*11/12, anchor=CENTER)

# Creation of the grid game
restart_game()

# Run the window
root.mainloop()
