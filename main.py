#Brian Huffman Custom Calculator

import tkinter as tk
from pygame import mixer
from threading import Thread
from tkinter import filedialog, messagebox

class ToolBox:
    def __init__(self, master):

        ###Initialize Instance Variables###
        self.expression = ""
        self.result = ""
        self.current_operation = ""
        self.ejectCount = 0
        self.ejected = False
        self.panelOffsetX = 10
        self.panelOffsetY = 10

        ###Create and Configure Widgets###

        # Set Root Window properties
        self.master = master
        master.geometry("400x400")
        #This keeps the main window above the panel
        master.attributes('-topmost', True)
        master.resizable(0, 0)
        master.title('Toolbox -- by Brian Huffman')
        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)
        master.columnconfigure(0, weight=1)

        #Create the Entry Box Widget to act as a display
        self.TopFrame = tk.Frame(master)
        self.TopFrame.grid(row=0, column=0, sticky="NSEW")
        self.TopFrame.rowconfigure(0, weight=1)
        self.TopFrame.columnconfigure(0, weight=1)
        self.display = tk.Entry(self.TopFrame, font=("arial", 30), justify='right')
        self.display.grid(row=0, column=0, padx=10, pady=10, sticky="S")

        #Create the keypad to hold all the input buttons
        self.keypad = tk.Frame(master)
        self.keypad.grid(row=1, column=0, padx=20, pady=20, sticky="NSEW")
        self.keypad.rowconfigure(1, weight=1)
        self.keypad.rowconfigure(2, weight=1)
        self.keypad.rowconfigure(3, weight=1)
        self.keypad.rowconfigure(4, weight=1)
        self.keypad.rowconfigure(5, weight=1)
        self.keypad.columnconfigure(0, weight=1)
        self.keypad.columnconfigure(1, weight=1)
        self.keypad.columnconfigure(2, weight=1)
        self.keypad.columnconfigure(3, weight=1)

        # create the buttons
        self.create_button("7", 1, 0)
        self.create_button("8", 1, 1)
        self.create_button("9", 1, 2)
        self.create_button("/", 1, 3)
        self.create_button("4", 2, 0)
        self.create_button("5", 2, 1)
        self.create_button("6", 2, 2)
        self.create_button("*", 2, 3)
        self.create_button("1", 3, 0)
        self.create_button("2", 3, 1)
        self.create_button("3", 3, 2)
        self.create_button("-", 3, 3)
        self.create_button("0", 4, 0)
        self.create_button(".", 4, 1)
        self.create_button("C", 4, 2)
        self.create_button("+", 4, 3)
        self.create_button("=", 5, 0, columnspan=4)

        #Create Sliding Panel
        self.Panel = tk.Toplevel(master)
        self.Panel.geometry('390x400')
        #This internal function removes the surrounding window border and title bar with dock, expand, exit buttons
        self.Panel.overrideredirect(True)
        #Bind the <Configure> event which fires when the window is resized or moved
        master.bind("<Configure>", self.sync)
        #Bind the show and hide events of the main window to show and hide the panel as well
        master.bind("<Unmap>", self._hide_panel)
        master.bind("<Map>", self._show_panel)
        #Create Eject button and prepare pygame's mixer to play a sound file when pressed
        mixer.init()
        mixer.music.load('Click.mp3')
        self.ejectButton = tk.Button(self.TopFrame, text='<<', padx=10, pady=10, command= self.panelEject)
        self.ejectButton.grid(row=0, column=0, sticky='NW')

        #Create a new empty Menu Bar object and "configure" it to the panel
        self.menu_bar = tk.Menu(self.master)
        self.Panel.config(menu=self.menu_bar)
        # Add a File drop down button onto the Menu Bar
        file_menu = self.file_menu()
        self.menu_bar.add_cascade(label="File", menu=file_menu)



        #Create Text Box Area
        self.text = tk.Text(self.Panel, bg='white', font=("Consolas", 12))
        self.text.pack(fill="both", expand=True)

        """
        """
        #####################################

    ###Define Class Functions and Events###

    #Button creation function to manage repetitive internal calls required to make similar buttons
    def create_button(self, text, row, col, rowspan = 1, columnspan = 1):
        button = tk.Button(self.keypad, text=text, padx=5, pady=5, command=lambda: self.button_click(text))
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky="NSEW")

    #Event that fires on a button is pressed
    def button_click(self, text):
        if text == "C":
            self.expression = ""
            self.current_operation = ""
            self.result = ""
            self.update_display()
        elif text in ["+", "-", "*", "/"]:
            if self.current_operation:
                self.button_click("=")
            self.current_operation = text
            self.expression += self.result + text
            self.result = ""
            self.update_display()
        elif text == "=":
            if not self.current_operation:
                return
            self.expression += self.result
            self.result = str(eval(self.expression))
            self.current_operation = ""
            self.expression = ""
            self.update_display()
        else:
            self.result += text
            self.update_display()

    # Event that when called will set the top level to the master position so the panel moves with the window
    def sync(self, event=None):
        x = self.master.winfo_x()
        y = self.master.winfo_y()
        self.Panel.geometry("+%d+%d" % (x + self.panelOffsetX, y + self.panelOffsetY))

    def panelEject(self, event=None):
        mixer.music.play()
        Thread(target=self.ejectAnimation(), args=(self,)).start()
        self.ejectCount = 0

    def ejectAnimation(self):
        offset_increment = 39
        frame_delay = 20
        num_frames = 10
        if self.ejected == False and self.ejectCount < num_frames:
            x = self.master.winfo_x()
            y = self.master.winfo_y()
            self.panelOffsetX -= offset_increment
            self.Panel.geometry('+%d+%d' % (x + self.panelOffsetX, y + self.panelOffsetY))
            self.ejectCount += 1
            self.master.after(frame_delay, self.Panel.update())
            self.ejectAnimation()
            self.ejected = True
        elif self.ejected == True and self.ejectCount < num_frames:
            x = self.master.winfo_x()
            y = self.master.winfo_y()
            self.panelOffsetX += offset_increment
            self.Panel.geometry('+%d+%d' % (x + self.panelOffsetX, y + self.panelOffsetY))
            self.ejectCount += 1
            self.master.after(frame_delay, self.Panel.update())
            self.ejectAnimation()
            self.ejected = False

    def _hide_panel(self, event=None):
        self.Panel.withdraw()

    def _show_panel(self, event=None):
        self.Panel.deiconify()

    def file_menu(self):

        def new_file():
            # Clear the text widget
            self.text.delete("1.0", "end")

        def open_file():
            # Use the filedialog module to open a file
            file_path = filedialog.askopenfilename()

            # If a file was selected, read its contents and display them in the text widget
            if file_path:
                with open(file_path, "r") as file:
                    self.text.delete("1.0", "end")
                    self.text.insert("1.0", file.read())

        def save_file():
            # Use the filedialog module to save the contents of the text widget to a file
            file_path = filedialog.asksaveasfilename()

            # If a file was selected, write the contents of the text widget to the file
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.text.get("1.0", "end-1c"))

        def save_file_as():
            # Use the filedialog module to save the contents of the text widget to a new file
            file_path = filedialog.asksaveasfilename(defaultextension='.txt')

            # If a file was selected, write the contents of the text widget to the file
            if file_path:
                with open(file_path, "w") as file:
                    file.write(self.text.get("1.0", "end-1c"))

        def exit_notepad():
            root.destroy()

        #Bind these functions to these drop down buttons and add labels
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=exit_notepad)

        return file_menu

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.result)
        self.master.update()

root = tk.Tk()
app = ToolBox(root)
root.mainloop()
