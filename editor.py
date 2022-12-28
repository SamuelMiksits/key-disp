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
        keyboard_main.Keyboard_class.__init__(self, master) #run the parent class constructor.

        #keyboard.on_press_key("Space", self.getsize)
        

        self.__frame = master
        self.__frame.title("Editor for Key Disp - Keyboard Input Display")
        #framesize = self.__frame.getsize()
        
        self.__frame.geometry("1400x800")

        for i in range(len(self.buttonList)): #Since we inherit the keyboard, we need to move all buttons
            self.move(400,100,i)

        
        #Layout menu items

        self.__layoutRegionLabel = tk.Label(self.__frame, text="Layout options").place(relx=0, rely=0)
        
        self.__keyListbox = tk.Listbox(self.__frame, selectmode=tk.SINGLE)
        self.__keyListbox.place(x=5, y=20, height=345, width=150)
        for i in range(len(self.buttonList)):
            self.__keyListbox.insert(tk.END, self.buttonList[i].lowercase + " \\ " + self.buttonList[i].uppercase)
        
        #For moving items in the listbox (and the layout file) up and down
        self.__layoutMoveItemUpButton = tk.Button(self.__frame, text="Move up", command=self.moveInKeyItemlist(self.__keyListbox.curselection(), -1))
        self.__layoutMoveItemDownButton = tk.Button(self.__frame, text="Move down", command=self.moveInKeyItemlist(self.__keyListbox.curselection(), 1))
        self.__layoutMoveItemUpButton.place(x=160,y=20, width=75)
        self.__layoutMoveItemDownButton.place(x=160,y=50, width=75)

        self.__layoutpreviewButton = tk.Button(self.__frame, text="Preview")
        self.__layoutpreviewButton.place(x=320, y=20, width=70)

        self.__layoutapplyButton = tk.Button(self.__frame, text="Apply")
        self.__layoutapplyButton.place(x=320, y=50, width=70)

        self.__layoutresetButton = tk.Button(self.__frame, text="Reset")
        self.__layoutresetButton.place(x=320, y=80, width=70)

        self.__layoutpreviewButton = tk.Button(self.__frame, text="Add")
        self.__layoutpreviewButton.place(x=242, y=20, width=70)

        self.__layoutapplyButton = tk.Button(self.__frame, text="Remove")
        self.__layoutapplyButton.place(x=242, y=50, width=70)

        self.__scancodeLabel = tk.Label(self.__frame, text="Key/Scan code")
        self.__scancodeLabel.place(x=160, y=130)
        self.__scancodeEntry = tk.Entry(self.__frame)
        self.__scancodeEntry.place(x=160, y=150, width=100)

        self.__lowercaseLabel = tk.Label(self.__frame, text="Lowercase")
        self.__lowercaseLabel.place(x=160, y=175)
        self.__lowercaseEntry = tk.Entry(self.__frame)
        self.__lowercaseEntry.place(x=160, y=195, width=50)

        self.__uppercaseLabel = tk.Label(self.__frame, text="Uppercase")
        self.__uppercaseLabel.place(x=250, y=175)
        self.__uppercaseEntry = tk.Entry(self.__frame)
        self.__uppercaseEntry.place(x=250, y=195, width=50)

        self.__posxLabel = tk.Label(self.__frame, text="Position (x)")
        self.__posxLabel.place(x=160, y=220)
        self.__posxEntry = tk.Entry(self.__frame)
        self.__posxEntry.place(x=160, y=245, width=50)

        self.__posyLabel = tk.Label(self.__frame, text="Position (y)")
        self.__posyLabel.place(x=250, y=220)
        self.__posyEntry = tk.Entry(self.__frame)
        self.__posyEntry.place(x=250, y=245, width=50)

        self.__widthLabel = tk.Label(self.__frame, text="Width")
        self.__widthLabel.place(x=160, y=270)
        self.__widthEntry = tk.Entry(self.__frame)
        self.__widthEntry.place(x=160, y=295, width=50)

        self.__heightLabel = tk.Label(self.__frame, text="Height")
        self.__heightLabel.place(x=250, y=270)
        self.__heightEntry = tk.Entry(self.__frame)
        self.__heightEntry.place(x=250, y=295, width=50)

        self.__presetLabel = tk.Label(self.__frame, text="Preset")
        self.__presetLabel.place(x=160, y=320)
        self.__presetEntry = tk.Entry(self.__frame)
        self.__presetEntry.place(x=160, y=345, width=50)

        #Preset menu items
        self.__presetRegionLabel = tk.Label(self.__frame, text="Preset options").place(relx=0, y=380)

        self.__presetListbox = tk.Listbox(self.__frame, selectmode=tk.SINGLE)
        self.__presetListbox.place(x=5, y=400, height=90, width=150)
        for i in range(len(self._Keyboard_class__presetList)):
            self.__presetListbox.insert(tk.END, i+1)

        self.__presetMoveItemUpButton = tk.Button(self.__frame, text="Move up", command=self.moveInKeyItemlist(self.__keyListbox.curselection(), -1))
        self.__presetMoveItemDownButton = tk.Button(self.__frame, text="Move down", command=self.moveInKeyItemlist(self.__keyListbox.curselection(), 1))
        self.__presetMoveItemUpButton.place(x=160,y=400, width=75)
        self.__presetMoveItemDownButton.place(x=160,y=430, width=75)

        self.__presetpreviewButton = tk.Button(self.__frame, text="Preview")
        self.__presetpreviewButton.place(x=320, y=400, width=70)

        self.__presetapplyButton = tk.Button(self.__frame, text="Apply")
        self.__presetapplyButton.place(x=320, y=430, width=70)

        self.__presetresetButton = tk.Button(self.__frame, text="Reset")
        self.__presetresetButton.place(x=320, y=460, width=70)

        self.__presetpreviewButton = tk.Button(self.__frame, text="Add")
        self.__presetpreviewButton.place(x=242, y=400, width=70)

        self.__presetapplyButton = tk.Button(self.__frame, text="Remove")
        self.__presetapplyButton.place(x=242, y=430, width=70)


        self.__keyBackgroundColorLabel = tk.Label(self.__frame, text="Key color (unpressed)")
        self.__keyBackgroundColorLabel.place(x=5, y=510)
        self.__keyBackgroundColorEntry = tk.Entry(self.__frame)
        self.__keyBackgroundColorEntry.place(x=5, y=530, width=100)

        self.__keyForegroundColorLabel = tk.Label(self.__frame, text="Text color (unpressed)")
        self.__keyForegroundColorLabel.place(x=147, y=510)
        self.__keyForegroundColorEntry = tk.Entry(self.__frame)
        self.__keyForegroundColorEntry.place(x=147, y=530, width=100)

        self.__fontLabel = tk.Label(self.__frame, text="Font (key unpressed)")
        self.__fontLabel.place(x=290, y=510)
        self.__fontEntry = tk.Entry(self.__frame)
        self.__fontEntry.place(x=290, y=530, width=100)


        self.__fontsizeLabel = tk.Label(self.__frame, text="fontsize")
        self.__fontsizeLabel.place(x=5, y=560)
        self.__fontsizeEntry = tk.Entry(self.__frame)
        self.__fontsizeEntry.place(x=5, y=580, width=100)

        self.__boldLabel = tk.Label(self.__frame, text="bold")
        self.__boldLabel.place(x=147, y=560)
        self.__boldEntry = tk.Entry(self.__frame)
        self.__boldEntry.place(x=147, y=580, width=100)

        self.__italicsLabel = tk.Label(self.__frame, text="italics")
        self.__italicsLabel.place(x=290, y=560)
        self.__italicsEntry = tk.Entry(self.__frame)
        self.__italicsEntry.place(x=290, y=580, width=100)


        self.__backgroundColorPressedLabel = tk.Label(self.__frame, text="Key color (pressed) ")
        self.__backgroundColorPressedLabel.place(x=5, y=610)
        self.__backgroundColorPressedEntry = tk.Entry(self.__frame)
        self.__backgroundColorPressedEntry.place(x=5, y=630, width=100)

        self.__foregroundColorPressedLabel = tk.Label(self.__frame, text="Text color (pressed)")
        self.__foregroundColorPressedLabel.place(x=147, y=610)
        self.__foregroundColorPressedEntry = tk.Entry(self.__frame)
        self.__foregroundColorPressedEntry.place(x=147, y=630, width=100)

        self.__fontPressedLabel = tk.Label(self.__frame, text="font (pressed)")
        self.__fontPressedLabel.place(x=290, y=610)
        self.__fontPressedEntry = tk.Entry(self.__frame)
        self.__fontPressedEntry.place(x=290, y=630, width=100)


        self.__fontsizePressedLabel = tk.Label(self.__frame, text="fontsize (pressed) ")
        self.__fontsizePressedLabel.place(x=5, y=660)
        self.__fontsizeEntry = tk.Entry(self.__frame)
        self.__fontsizeEntry.place(x=5, y=680, width=100)

        self.__boldPressedLabel = tk.Label(self.__frame, text="bold (pressed)")
        self.__boldPressedLabel.place(x=147, y=660)
        self.__boldPressedEntry = tk.Entry(self.__frame)
        self.__boldPressedEntry.place(x=147, y=680, width=100)

        self.__italicsPressedLabel = tk.Label(self.__frame, text="italics (pressed)")
        self.__italicsPressedLabel.place(x=290, y=660)
        self.__italicsPressedEntry = tk.Entry(self.__frame)
        self.__italicsPressedEntry.place(x=290, y=680, width=100)


        self.__rgbLabel = tk.Label(self.__frame, text="RGB ")
        self.__rgbLabel.place(x=5, y=710)
        self.__rgbEntry = tk.Entry(self.__frame)
        self.__rgbEntry.place(x=5, y=730, width=100)

        self.__rgbTypeLabel = tk.Label(self.__frame, text="RGB type")
        self.__rgbTypeLabel.place(x=147, y=710)
        self.__rgbTypeEntry = tk.Entry(self.__frame)
        self.__rgbTypeEntry.place(x=147, y=730, width=100)

        self.__rgbSpeedLabel = tk.Label(self.__frame, text="RGB speed")
        self.__rgbSpeedLabel.place(x=290, y=710)
        self.__rgbSpeedEntry = tk.Entry(self.__frame)
        self.__rgbSpeedEntry.place(x=290, y=730, width=100)

        #Keyboard menu items
        self.__keyboardRegionLabel = tk.Label(self.__frame, text="Keyboard preview").place(x=405, rely=0)
        
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

    #loads layout information for a button, given index i
    def loadButton(self, i):
        pass

    #Move button in the layout file up or down
    def moveInKeyItemlist(self, currentPosition, i):
        pass

def main():

    root = tk.Tk()
    Globals.EDITOR = Editor_class(root)

    root.mainloop()


if __name__ == "__main__":
    main()