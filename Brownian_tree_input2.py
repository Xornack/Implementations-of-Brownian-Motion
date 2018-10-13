"""
This program takes specific default values returns the user input parameters.
"""

import tkinter

def input_variables(param1, param2, param3, param4, param5, param6, param7):
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
    param4 = tkinter.StringVar(master, value = str(param4))
    param5 = tkinter.StringVar(master, value = str(param5))
    param6 = tkinter.StringVar(master, value = str(param6))
    param7 = tkinter.StringVar(master, value = str(param7))
    # button_click will do what happens when you click button1
    # in this case, return params as an int
    def button_click():
        if param1.get() != '':        
            v1 = param1.get()
        
        if param2.get() != '':
            v2 = param2.get()

        if param3.get() != '':
            v3 = param3.get()    

        if param4.get() != '':
            v4 = param4.get()

        if param5.get() != '':
            v5 = param5.get()            

        if param6.get() != '':
            v6 = param6.get()

        if param7.get() != '':
            v7 = param7.get()

        return [int(v1), int(v2), int(v3),
                int(v4), int(v5), int(v6),
                float(v7)] 
    
    def exit_button():
        button_click()
        master.destroy()

    # these lines call the label, entry, and buttons in that order.
    # window width
    label = tkinter.Label(master, text = 'window width (pixels)').pack()
    entry1 = tkinter.Entry(master, textvariable = param1).pack()

    # window height
    label2 = tkinter.Label(master, text = 'window height (pixels)').pack()
    entry2 = tkinter.Entry(master, textvariable = param2).pack()

    # ellipse width
    label3 = tkinter.Label(master, text = 'ellipse width (pixels)').pack()
    entry3 = tkinter.Entry(master, textvariable = param3).pack()

    # ellipse height
    label4 = tkinter.Label(master, text = 'ellipse height (pixels)').pack()
    entry4 = tkinter.Entry(master, textvariable = param4).pack()

    # particle size
    label5 = tkinter.Label(master, text = 'size of particle (pixels)').pack()
    entry35 = tkinter.Entry(master, textvariable = param5).pack()

    # root increase in size
    label6 = tkinter.Label(master, text = 'root size above' + '\n'
                                        + 'particle size (pixels)').pack()
    entry6 = tkinter.Entry(master, textvariable = param6).pack()

    # shift angle increase (radians)
    label7 = tkinter.Label(master, text = 'shift roots' + '\n'
                                          '(radians)').pack()
    entry7 = tkinter.Entry(master, textvariable = param7).pack()

    # enter button to leave 
    space = tkinter.Label(master, text = '').pack()
    button = tkinter.Button(master, text = "Right On!", command = exit_button,
                     fg = 'black', bg = 'white').pack()

    master.mainloop()

    output = button_click()

    return output
