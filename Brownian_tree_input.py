"""This program takes specific input from the program Brownian Tree
Two Points.py and returns the user input parameters"""

import tkinter

def input_variables(param1, param2, param3):
    master = tkinter.Tk()
    master.resizable(width = True, height = True)
    master.minsize(400, 400)
    master.title('Input Parameters')

    # set with default values from Brownian tree two point
    # basically windowsize, default distance between roots and particle size
    # param1 is WINDOWSIZE
    # param2 is particle SIZE
    # param3 is default distance between roots
    param1 = tkinter.StringVar(master, value = str(param1))
    param2 = tkinter.StringVar(master, value = str(param2))
    param3 = tkinter.StringVar(master, value = str(param3))

    # button_click will do what happens when you click button1
    # in this case, return param as an int and prints it
    def button_click():
        if param1.get() != '':        
            v1 = param1.get()
        
        if param2.get() != '':
            v2 = param2.get()

        if param3.get() != '':
            v3 = param3.get()    

        return (int(v1), int(v2), int(v3))    
    
    def exit_button():
        button_click()
        master.destroy()

    # these three lines call the label, entry, and buttons in that order.
    label = tkinter.Label(master, text = 'window size (pixels)').pack()
    entry1 = tkinter.Entry(master, textvariable = param1).pack()

    # next three
    label2 = tkinter.Label(master, text = 'Particle Size (pixels)').pack()
    entry2 = tkinter.Entry(master, textvariable = param2).pack()

    # last params
    label3 = tkinter.Label(master, text = 'Distance Between Roots' + '\n'
                                  '(will not go over window size)').pack()
    entry3 = tkinter.Entry(master, textvariable = param3).pack()


    # enter button to leave 
    space = tkinter.Label(master, text = '').pack()
    button = tkinter.Button(master, text = "Looks Good!", command = exit_button,
                     fg = 'black', bg = 'white').pack()

    master.mainloop()

    output = button_click()

    return output
