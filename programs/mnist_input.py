import tkinter as tk

class MnistInput(tk.Tk):
    """Simple user input for MNIST data."""

    def __init__(self, points):
        tk.Tk.__init__(self)
        self.previous_x = 0
        self.previous_y = 0
        self.x = 0
        self.y = 0
        self.points = points
        self.canvas = tk.Canvas(self,
                                width=280,
                                height=280,
                                bg='black',
                                cursor='cross')
        self.canvas.pack(side='top',
                         fill='both',
                         expand=True)

        self.button_clear = tk.Button(self,
                                      text='Clear',
                                      command=self.clear)
        self.button_clear.pack(side='top',
                               fill='both',
                               expand=True)

        self.button_print = tk.Button(self,
                                      text='Done?',
                                      command=self.destroy)
        self.button_print.pack(side='top',
                               fill='both',
                               expand=True)

        self.canvas.bind('<Motion>', self.motion)
        self.canvas.bind('<B1-Motion>', self.draw_motion)

    def clear(self):
        self.canvas.delete('all')
        self.points.clear()

    def motion(self, event):
        self.previous_x = event.x
        self.previous_y = event.y

    def draw_motion(self, event):
        self.x = event.x
        self.y = event.y
        self.canvas.create_line(self.previous_x,
                                self.previous_y,
                                self.x,
                                self.y,
                                fill="white",
                                width=5)
        self.points.append((self.x, self.y))
        self.previous_x = self.x
        self.previous_y = self.y
