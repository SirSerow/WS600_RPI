from tkinter import*
import tkinter.font

#GUI DEFINITIONS
win = Tk()
win.title('PWS600 weather sensor')
myFont = tkinter.font.Font(family = 'Helvetica', size = 12, weight = "bold")

#EVENT FUNCTIONS
def close():
	win.destroy()


#WIGETS
exitButton = Button(win, text = 'EXIT', font = myfont, command = close, bg = 'bisque2', height = 1, width = 24)
exitButton.grid(row=0, column=1)


