import keyboard_main #The editor inherits the keyboard class
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import keyboard
import threading
import time
import debug

class Globals:
    EDITOR = None #Hardcoding, uses a globally stored reference for the instance of the keyboard

class Editor_class(keyboard_main.Keyboard_class):

    def __hello(self):
        print("Hello!")

    def __init__(self, master):
        keyboard_main.Keyboard_class.__init__(self, master)

        #keyboard.on_press_key("Space", self.getsize)
        

        self.__frame = master
        self.__frame.title("Editor for Key Disp - Keyboard Input Display")
       #framesize = self.__frame.getsize()
        
        self.__frame.geometry("1400x600")

        for i in range(len(self.buttonList)):
            #self.buttonList[i].move(400,100)
            self.move(400,100,i)

        
        #Layout menu items

        self.__layoutLabel = tk.Label(self.__frame, text="Layout options").place(relx=0, rely=0)
        """

        self.__buttonItemList
        self.__moveItemUpButton
        self.__moveItemDownButton

        self.__sizeLabel
        self.__sizeEntry

        self.__scancodeLabel
        self.__scancodeEntry

        self.__lowercaseLabel
        self.__lowercaseEntry

        self.__uppercaseLabel
        self.__uppercaseEntry

        self.__shiftLabel
        self.__shiftRadio

        self.__capsLabel
        self.__capsRadio

        self.__posxLabel
        self.__posxEntry

        self.__posyLabel
        self.__posyEntry

        self.__widthLabel
        self.__widthEntry

        self.__heightLabel
        self.__heightEntry

        self.__presetLabel
        self.__presetEntry

        """

        #Preset menu items
        self.__presetLabel = tk.Label(self.__frame, text="Preset options").place(relx=0, rely=0.61)


        #Keyboard menu items
        self.__keyboardLabel = tk.Label(self.__frame, text="Keyboard preview").place(x=405, rely=0)

        
        self.__frame.configure(bg="#F0F0F0")
        #self.__separatorKeyboard.config(bg=self.loadBackgroundColor())
        #print()

        """
        #I/O stuff, load, save
        self.__loadLayoutButton
        self.__saveLayoutButton

        #
        self.__loadPresetButton
        self.__savePresetButton
        """

        
        #self.__separatorLayoutPreset = ttk.Separator(self.__frame, orient="horizontal")
        #self.__separatorLayoutPreset.place(relx=0, rely=0.6, width=400, relheight=1)

        #self.__separatorKeyboard = ttk.Separator(self.__frame, orient="vertical")
        #self.__separatorKeyboard.place(x=400, rely=0, relwidth=1, relheight=1)
        

        #

        #file_path = filedialog.askopenfilename()
        #f = filedialog.asksaveasfile(initialfile = 'Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])

        """
        #"File" menu at the top left of the editor
        self.__menubar = tk.Menu(self.__frame)
        self.__menu = tk.Menu(self.__frame, tearoff=0)
        self.__menu.add_command(label="Open", command=self.__hello)
        self.__menu.add_command(label="Save", command=self.__hello)
        self.__menu.add_command(label="Save As", command=self.__hello)
        self.__menu.add_separator()
        self.__menu.add_command(label="Exit", command=self.__frame.quit)
        self.__menubar.add_cascade(label="File", menu=self.__menu)
        self.__frame.config(menu=self.__menubar)
        """
    def getsize(self,x ):
        print("Width: ", self.__frame.winfo_width())
        print("Height: ", self.__frame.winfo_height())

    #Move the key
    def move(self, x, y, i):
        newposx = int(self.buttonList[i]._Key__posx) + int(x) #Manglin, multi-level inheritance
        newposy = int(self.buttonList[i]._Key__posy) + int(y)
        self.buttonList[i].labelFrame.place(x=str(newposx), y=str(newposy))

def main():

    root = tk.Tk()
    Globals.EDITOR = Editor_class(root)

    root.mainloop()


if __name__ == "__main__":
    main()