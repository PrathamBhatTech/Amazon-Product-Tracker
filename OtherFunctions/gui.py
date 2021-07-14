from tkinter import *

root = Tk()
title = root.title('Amazon Tracker')
main_label = Label(root, text = 'Amazon Tracker').place(x = 120, y = 0) #to make bold & color maybe

settings_button = Button(root, text = '⚙️').place(x = 400, y = 0)
root.mainloop()
