import tkinter as tk
from tkinter import font

class TicTacToeBoard(tk.Tk):
    """A class that creates the game"""
    def __init__(self):
        """The title of the game"""
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._create_board_display()
        self._create_board_grid()
    
    def _create_board_display(self):
        """Function that creates the board's display"""
        display_frame=tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display=tk.Label(
            master=display_frame,
            text="Ready",
            font=font.Font(size=28,weight='bold')
        )
        self.display.pack()
    
    def _create_board_grid(self):
        """Creates the grid, with each square acting as a button"""
        grid_frame=tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row,weight=2,minsize=50)
            self.columnconfigure(row,weight=2,minsize=50)
            for col in range(3):
                button=tk.Button(
                    master=grid_frame,
                    text='',
                    font=font.Font(size=36,weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="black"
                )
                self._cells[button]=(row,col)
                button.grid(
                    row=row,
                    column=col,
                    padx=4,
                    pady=4,
                    sticky="nsew"
                )

def main():
    """Create the game and run its main loop"""
    board=TicTacToeBoard()
    board.mainloop()

if __name__=="__main__":
    main()