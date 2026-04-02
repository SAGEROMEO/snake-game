import tkinter as tk
import random

GRID  = 20
CELL  = 24
SIZE  = GRID * CELL
DELAY = 130  # ms per tick

class Snake(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake")
        self.resizable(False, False)

        self.score    = 0
        self.hi       = 0
        self.running  = False
        self.dir      = (1, 0)
        self.next_dir = (1, 0)

        # Score labels
        top = tk.Frame(self)
        top.pack()
        self.score_lbl = tk.Label(top, text="Score: 0", font=("Courier", 12, "bold"))
        self.score_lbl.pack(side="left", padx=20, pady=6)
        self.hi_lbl = tk.Label(top, text="Best: 0", font=("Courier", 12, "bold"))
        self.hi_lbl.pack(side="right", padx=20)

        # Canvas
        self.cv = tk.Canvas(self, width=SIZE, height=SIZE, bg="#1a1a1a")
        self.cv.pack()
        self.cv.create_text(SIZE//2, SIZE//2 - 20, text="SNAKE",
                            font=("Courier", 24, "bold"), fill="green", tags="msg")
        self.cv.create_text(SIZE//2, SIZE//2 + 20, text="Press Enter to start",
                            font=("Courier", 11), fill="gray", tags="msg")

        # Key bindings
        self.bind("<Up>",     lambda e: self._turn(0, -1))
        self.bind("<Down>",   lambda e: self._turn(0,  1))
        self.bind("<Left>",   lambda e: self._turn(-1, 0))
        self.bind("<Right>",  lambda e: self._turn(1,  0))
        self.bind("<Return>", lambda e: self._start())

    def _start(self):
        mid = GRID // 2
        self.snake    = [(mid, mid), (mid-1, mid), (mid-2, mid)]
        self.dir      = (1, 0)
        self.next_dir = (1, 0)
        self.score    = 0
        self.score_lbl.config(text="Score: 0")
        self.food     = self._new_food()
        self.running  = True
        self._tick()

    def _turn(self, dx, dy):
        if (dx, dy) != (-self.dir[0], -self.dir[1]):
            self.next_dir = (dx, dy)

    def _new_food(self):
        taken = set(self.snake)
        while True:
            pos = (random.randint(0, GRID-1), random.randint(0, GRID-1))
            if pos not in taken:
                return pos

    def _tick(self):
        if not self.running:
            return
        self.dir = self.next_dir
        hx, hy = self.snake[0]
        nx, ny = hx + self.dir[0], hy + self.dir[1]

        if nx < 0 or nx >= GRID or ny < 0 or ny >= GRID or (nx, ny) in self.snake:
            self.running = False
            self._draw()
            self.cv.create_text(SIZE//2, SIZE//2 - 16, text="GAME OVER",
                                font=("Courier", 22, "bold"), fill="red", tags="msg")
            self.cv.create_text(SIZE//2, SIZE//2 + 16,
                                text=f"Score: {self.score}  |  Press Enter to retry",
                                font=("Courier", 10), fill="gray", tags="msg")
            return

        self.snake.insert(0, (nx, ny))
        if (nx, ny) == self.food:
            self.score += 1
            if self.score > self.hi:
                self.hi = self.score
                self.hi_lbl.config(text=f"Best: {self.hi}")
            self.score_lbl.config(text=f"Score: {self.score}")
            self.food = self._new_food()
        else:
            self.snake.pop()

        self._draw()
        self.after(DELAY, self._tick)

    def _draw(self):
        self.cv.delete("game")
        self.cv.delete("msg")

        # Snake (green gradient head to tail)
        n = max(len(self.snake) - 1, 1)
        for i, (x, y) in enumerate(self.snake):
            t = i / n
            g = int(220 - t * 120)
            color = f"#00{g:02x}00"
            p = 2
            self.cv.create_rectangle(
                x*CELL+p, y*CELL+p, x*CELL+CELL-p, y*CELL+CELL-p,
                fill=color, outline="", tags="game"
            )

        # Food
        fx, fy = self.food
        r = CELL // 2 - 3
        cx, cy = fx*CELL + CELL//2, fy*CELL + CELL//2
        self.cv.create_oval(cx-r, cy-r, cx+r, cy+r,
                            fill="red", outline="", tags="game")

if __name__ == "__main__":
    Snake().mainloop()