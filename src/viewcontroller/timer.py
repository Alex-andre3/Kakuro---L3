# timer found in this website : https://riptutorial.com/tkinter/example/22870/-after--

import tkinter as tk

class Timer:
    def __init__(self, parent):
        # variable storing time
        self.seconds = 0
        # label displaying time
        self.label = tk.Label(parent, text="0 s", font="Arial 10", width=5)
        self.label.pack()
        # start the timer
        self.label.after(1000, self.refresh_label)

    def refresh_label(self):
        """ refresh the content of the label every second """
        # increment the time
        self.seconds += 1
        # display the new time
        self.label.configure(text="%i s" % self.seconds)
        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        self.label.after(1000, self.refresh_label)
