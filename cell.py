from tkinter import Button, Label
import random

import menu
import settings


class Cell:
    all = []
    cell_count = 0
    mines_count = 0
    speed = 'fast'
    difficulty = 'easy'
    cell_count_number_label_object = None
    mines_count_number_label_object = None
    status_label_object = None
    btn_menu_object = None
    start_button_object = None

    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_opened = False
        self.is_mine_candidate = False
        self.x = x
        self.y = y
        self.cell_btn_object = None

        # Append the object to the Cell.all list
        Cell.all.append(self)

    @staticmethod
    def set_speed(event, speed):
        Cell.speed = speed
        menu.Btn.color_on_parameters(speed)

    @staticmethod
    def set_difficulty(event, difficulty):
        Cell.difficulty = difficulty
        menu.Btn.color_on_parameters(difficulty)

    @staticmethod
    def grid_size():
        size = settings.SPEED[Cell.speed]
        return size

    @staticmethod
    def cell_count_method():
        Cell.cell_count = Cell.grid_size() ** 2

    @staticmethod
    def set_mines_count():
        count = Cell.cell_count // settings.DIFFICULTY[Cell.difficulty]
        return count

    def create_btn_object(self, location):
        btn = Button(
            location,
            width=settings.CELL_WIDTH,
            height=settings.CELL_HEIGHT
        )
        btn.bind('<Button-1>', self.left_click_actions)  # Left click
        btn.bind('<Button-3>', self.right_click_actions)  # Right click
        self.cell_btn_object = btn

    @staticmethod
    def all_mines_checked():
        mines_checked = True
        for cell_object in Cell.all:
            if cell_object.is_mine and not cell_object.is_mine_candidate:
                mines_checked = False
        return mines_checked

    @staticmethod
    def create_cell_count_number_label(location):
        lbl = Label(
            location,
            text=f"{Cell.cell_count}",
            width=12,
            height=2,
            bg='black',
            fg='white',
            font=("", 20)
        )
        Cell.cell_count_number_label_object = lbl

    @staticmethod
    def create_mines_count_number_label(location):
        lbl = Label(
            location,
            text=f"{Cell.mines_count}",
            width=12,
            height=2,
            bg='black',
            fg='white',
            font=("", 20)
        )
        Cell.mines_count_number_label_object = lbl

    @staticmethod
    def create_status_label(location):
        lbl = Label(
            location,
            width=48,
            height=4,
            bg='black',
            fg='white',
            font=('Snacker Comic Personal Use Only', 30)
        )
        Cell.status_label_object = lbl

    @property
    def mine_zone_checked(self):
        zone_checked = True
        for cell_object in self.surrounded_cells:
            if not cell_object.is_opened:
                zone_checked = False
        return zone_checked

    @staticmethod
    def deploy_zone(cell):
        cell_list = [cell]
        check = True
        while check:
            cell_loop = cell_list
            for cell_unit in cell_loop:
                for cell_object in cell_unit.surrounded_cells:
                    cell_object.show_cell()
                    if cell_object.surrounded_cells_mines_length == 0 and not cell_object.mine_zone_checked:
                        cell_list.append(cell_object)
                cell_list.remove(cell_unit)
            if len(cell_list) == 0:
                check = False

    def left_click_actions(self, event):
        if self.is_mine_candidate:
            pass
        elif self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                self.deploy_zone(self)
            self.show_cell()

            # If Mines count is equal to the cells left count, player won
            if Cell.cell_count == Cell.set_mines_count():
                Cell.status_label_object.configure(
                    text='You won! Congratulations!'
                )

            # Cancel left and right click events if cell is already opened
            self.cell_btn_object.unbind('<Button-1>')
            self.cell_btn_object.unbind('<Button-3>')

    @staticmethod
    def get_cell_by_axis(x, y):
        # return a cell object based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x, self.y + 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1)
        ]
        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_number_label_object:
                Cell.cell_count_number_label_object.configure(
                    text=f"{Cell.cell_count}"
                )
            # If this was a mine candidate, then for safety, we should
            # configure the background to SystemButtonFace
            # Modified: mine candidate blocks the cells and prevent it
            # to be left clicked accidentally
            self.cell_btn_object.configure(bg='SystemButtonFace')
        # Mark the cell as opened (Use is a the last line of this method)
        self.is_opened = True

    @staticmethod
    def show_mine():
        # A logic to interrupt the game, display a message that player lost!
        for cell in Cell.all:
            if cell.is_mine:
                if cell.is_mine_candidate:
                    cell.cell_btn_object.configure(bg='green')
                else:
                    cell.cell_btn_object.configure(bg='red')
        Cell.status_label_object.configure(
            text='You lost, You just clicked on a mine.'
        )

    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg="orange")
            self.is_mine_candidate = True
            Cell.mines_count -= 1
            Cell.mines_count_number_label_object.configure(
                text=f"{Cell.mines_count}"
            )
            Cell.cell_count -= 1
            Cell.cell_count_number_label_object.configure(
                text=f"{Cell.cell_count}"
            )
            # If Mines count == 0 and all evaluated_mines are mines then player won
            if Cell.mines_count == 0 and Cell.all_mines_checked():
                Cell.status_label_object.configure(
                    text='You found all mines! Congratulations!'
                )
                for cell in Cell.all:
                    if not cell.is_opened and not cell.is_mine_candidate:
                        cell.show_cell()
        else:
            self.cell_btn_object.configure(
                bg='SystemButtonFace'
            )
            self.is_mine_candidate = False
            Cell.mines_count += 1
            Cell.mines_count_number_label_object.configure(
                text=f"{Cell.mines_count}"
            )
            Cell.cell_count += 1
            Cell.cell_count_number_label_object.configure(
                text=f"{Cell.cell_count}"
            )

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            Cell.set_mines_count()
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x},{self.y})"
