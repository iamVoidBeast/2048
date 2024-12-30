import tkinter as tk
from tkinter import messagebox
import random

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game with AI")
        self.root.configure(bg="black")
        self.grid = [[0] * 4 for _ in range(4)]
        self.ai_mode = tk.BooleanVar()

        self.build_ui()
        self.new_tile()
        self.new_tile()
        self.update_ui()

    def build_ui(self):
        top_frame = tk.Frame(self.root, bg="black")
        top_frame.pack(pady=10)

        ai_checkbox = tk.Checkbutton(
            top_frame, text="AI Mode", variable=self.ai_mode, command=self.toggle_ai_mode,
            bg="black", fg="white", selectcolor="black", font=("Helvetica", 12, "bold"),
            relief="flat"
        )
        ai_checkbox.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(
            top_frame, text="Reset", command=self.reset_game, bg="#444444", fg="white",
            font=("Helvetica", 12, "bold"), relief="flat"
        )
        reset_button.pack(side=tk.LEFT, padx=10)

        self.board_frame = tk.Frame(self.root, bg="black")
        self.board_frame.pack(pady=20)
        
        self.cells = []
        for row in range(4):
            row_cells = []
            for col in range(4):
                cell = tk.Label(
                    self.board_frame, text="", width=6, height=3,
                    font=("Helvetica", 24, "bold"), bg="lightgray", fg="black",
                    relief="flat", bd=3
                )
                cell.grid(row=row, column=col, padx=5, pady=5)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.root.bind("<KeyPress>", self.handle_keypress)

    def new_tile(self):
        empty_tiles = [(r, c) for r in range(4) for c in range(4) if self.grid[r][c] == 0]
        if not empty_tiles:
            return
        r, c = random.choice(empty_tiles)
        self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        colors = {
            0: "#1c1c1c",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32",
            8192: "#776e65",
            16384: "#9c0b08",
            32768: "#7d241e",
            65536: "#5d2e46",
            131072: "#463f59",
            262144: "#2e4e74",
            524288: "#1c5f89",
            1048576: "#0d638e",
            2097152: "#08628b"
        }

        text_colors = {
            0: "#1c1c1c",
            2: "#776e65",
            4: "#776e65",
            8: "#f9f6f2",
            16: "#f9f6f2",
            32: "#f9f6f2",
            64: "#f9f6f2",
            128: "#f9f6f2",
            256: "#f9f6f2",
            512: "#f9f6f2",
            1024: "#f9f6f2",
            2048: "#f9f6f2",
            4096: "#f9f6f2",
            8192: "#f9f6f2",
            16384: "#f9f6f2",
            32768: "#f9f6f2",
            65536: "#f9f6f2",
            131072: "#f9f6f2",
            262144: "#f9f6f2",
            524288: "#f9f6f2",
            1048576: "#f9f6f2",
            2097152: "#f9f6f2"
        }

        for r in range(4):
            for c in range(4):
                value = self.grid[r][c]
                self.cells[r][c].config(
                    text=str(value) if value != 0 else "",
                    bg=colors.get(value, "black"),
                    fg=text_colors.get(value, "white")
                )

    def reset_game(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.new_tile()
        self.new_tile()
        self.update_ui()

    def handle_keypress(self, event):
        if self.ai_mode.get():
            return

        key_moves = {
            "w": self.move_up,
            "s": self.move_down,
            "a": self.move_left,
            "d": self.move_right
        }

        if event.keysym.lower() in key_moves:
            moved = key_moves[event.keysym.lower()]()
            if moved:
                self.new_tile()
                self.update_ui()
                self.check_game_state()

    def toggle_ai_mode(self):
        if self.ai_mode.get():
            self.run_ai()

    def run_ai(self):
        if not self.ai_mode.get():
            return

        if not self.make_ai_move():
            return

        self.new_tile()
        self.update_ui()
        self.check_game_state()
        self.root.after(200, self.run_ai)

    def make_ai_move(self):
        best_move = None
        best_score = -1

        for move, action in enumerate([self.move_up, self.move_down, self.move_left, self.move_right]):
            backup = [row[:] for row in self.grid]
            moved = action()
            if moved:
                score = sum(sum(row) for row in self.grid)
                if score > best_score:
                    best_score = score
                    best_move = move
            self.grid = backup

        if best_move is not None:
            [self.move_up, self.move_down, self.move_left, self.move_right][best_move]()
            return True
        return False

    def compress(self):
        moved = False
        new_grid = [[0] * 4 for _ in range(4)]
        for r in range(4):
            position = 0
            for c in range(4):
                if self.grid[r][c] != 0:
                    new_grid[r][position] = self.grid[r][c]
                    if position != c:
                        moved = True
                    position += 1
        self.grid = new_grid
        return moved

    def merge(self):
        moved = False
        for r in range(4):
            for c in range(3):
                if self.grid[r][c] == self.grid[r][c + 1] and self.grid[r][c] != 0:
                    self.grid[r][c] *= 2
                    self.grid[r][c + 1] = 0
                    moved = True
        return moved

    def reverse(self):
        for r in range(4):
            self.grid[r] = self.grid[r][::-1]

    def transpose(self):
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_left(self):
        moved1 = self.compress()
        moved2 = self.merge()
        self.compress()
        return moved1 or moved2

    def move_right(self):
        self.reverse()
        moved = self.move_left()
        self.reverse()
        return moved

    def move_up(self):
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def check_game_state(self):
        max_tile = max(max(row) for row in self.grid)

        if max_tile == 2048:
            messagebox.showinfo("Congratulations!", "You have won! You got 2048 but you can still play.")
        elif max_tile >= 2097152:
            messagebox.showerror("ERROR", "GAME LIMIT REACHED, YOU ARE GOD")

        elif not any(0 in row for row in self.grid):
            if not any(self.can_merge(r, c) for r in range(4) for c in range(4)):
                messagebox.showinfo("Game Over", "No more moves left! Game over.")

    def can_merge(self, r, c):
        value = self.grid[r][c]
        if r < 3 and self.grid[r + 1][c] == value:
            return True
        if c < 3 and self.grid[r][c + 1] == value:
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
