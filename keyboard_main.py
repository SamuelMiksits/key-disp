import tkinter as tk
import keyboard
import mouse
import threading
import time

#When errors are present in a layout file
class LayoutError(Exception):
    pass

#Error in preset file
class PresetError(Exception):
    pass

class Globals:
    KB = None #Hardcoding, uses a globally stored reference for the instance of the keyboard
    mousebuttons = ["mouse.LEFT", "mouse.RIGHT", "mouse.MIDDLE"]
    mousedict = {"mouse.LEFT" : mouse.LEFT, #jank solution, string parsing by "dictionary casting"
                 "mouse.RIGHT" : mouse.RIGHT,
                 "mouse.MIDDLE" : mouse.MIDDLE}
    mouseindicatorIndex = 0

#RGB color wheel. This color wheel is looped through to determine the color of the RGB enabled keys
#The file rgb.txt is generated through a program called devtools/generatecolorwheel. The program outputs the rgb.txt file created in the devtools folder
def readrgbwheel():
    wheelList = list()

    with open("rgb.txt", "r", encoding="utf-8") as lines:
        for line in lines:
            wheelList.append(line.strip())

    return wheelList

rgbwheel = readrgbwheel()

#Thread function for handling RGB
def rgb_thread(e):
    i = 0
    #Bad hard coding, should check rgb type in the preset file *or somewhere else
    #* if the code is written such as to check the preset file with this loop, then the program will be "clamped into"
    #only allowing a keyboard to have 1 type of RGB enabled at a time, is this a compromise that should be made?
    if Globals.KB.buttonList[0].rgbtype == "0": #First RGB mode, cycles color on every key at the same time
        while True:
            time.sleep(1/(60*float(Globals.KB.buttonList[0].rgbspeed)))
            for j in range(len(Globals.KB.buttonList)):
                if Globals.KB.buttonList[j].isPressed == False:
                    Globals.KB.buttonList[j].label.config(bg=rgbwheel[i])
                    Globals.KB.buttonList[j].labelFrame.config(bg=rgbwheel[i])
            i += 1
            if i == len(rgbwheel) - 1:
                i = 0

    #See comment above
    if Globals.KB.buttonList[0].rgbtype == "1": #Second RGB mode, Color "moves" across the keyboard, 
        while True:                             #only works properly if the "layout" file has the keys in order on each row and has a row per row order
            time.sleep(1/(60*float(Globals.KB.buttonList[0].rgbspeed)))
            for j in range(len(Globals.KB.buttonList)):
                if Globals.KB.buttonList[j].isPressed == False:
                    Globals.KB.buttonList[j].label.config(bg=rgbwheel[(j+i)%len(rgbwheel)])
                    Globals.KB.buttonList[j].labelFrame.config(bg=rgbwheel[(j+i)%len(rgbwheel)])
            i += 1
            if i == len(rgbwheel) - 1:
                i = 0

def mouseind_thread(e):

    #lowercase = sensitivity
    #uppercase = limit
    sensitivity = float(Globals.KB.buttonList[Globals.mouseindicatorIndex].lowercase)
    limit = int(Globals.KB.buttonList[Globals.mouseindicatorIndex].uppercase)
    posx = int(Globals.KB.buttonList[Globals.mouseindicatorIndex].mouseindicatorx)
    posy = int(Globals.KB.buttonList[Globals.mouseindicatorIndex].mouseindicatory)

    oldx = 0
    oldy = 0
    x = 0
    y = 0
    while True:
        (oldx, oldy) = (x,y)
        (x,y) = mouse.get_position()

        dx = x - oldx
        dy = y - oldy

        dx = dx/sensitivity #change to sensitivity in the future
        dy = dy/sensitivity

        if dx > limit:
            dx = limit
        if dx < -limit:
            dx = -limit
        if dy > limit:
            dy = limit
        if dy < -limit:
            dy = -limit

        #print("dx: ", dx, " dy: ", dy)
        stringdx = str(posx + dx)
        stringdy = str(posy + dy)

        Globals.KB.buttonList[Globals.mouseindicatorIndex].mouseindicatorframe.place(x=stringdx, y=stringdy)

        time.sleep(1/60)

#Keyboard object has a list of presets, and then a key will belong to one of the presets defined in the preset file
class Preset:

    def __init__(self, keybackgroundcolor, keyforegroundcolor, font, fontsize, bold, italics,\
    backgroundcolorPressed, foregroundcolorPressed, fontPressed, fontsizePressed, boldPressed, italicsPressed, rgb, rgbtype = None, rgbspeed = None):

        self.keybackgroundcolor = keybackgroundcolor #Background color of the key when unpressed
        self.keyforegroundcolor = keyforegroundcolor #Foreground color (aka text color) when unpressed
        self.font = font #Font of the text when the key is unpressed
        self.fontsize = fontsize #Size of the key text font when the key is unpressed
        self.bold = bold #Is the font bold when key is unpressed? (bool)
        self.italics = italics #Is the font in italics when key is unpressed? (bool)
        self.backgroundcolorPressed = backgroundcolorPressed #Background color of the key when pressed
        self.foregroundcolorPressed = foregroundcolorPressed #Foreground color (aka text color) when the key is pressed
        self.fontPressed = fontPressed #Font of the text when the key is unpressed
        self.fontsizePressed = fontsizePressed #Size of the key text font when the key is unpressed
        self.boldPressed = boldPressed #Is the font bold when key is pressed? (bool)
        self.italicsPressed = italicsPressed #is the font in italics when key is pressed? (bool)
        self.rgb = rgb #Does the key have RGB? "1" = Yes, any other value = No
        self.rgbtype = rgbtype #Which algorithm will be used for determining key color? (currently 0 and 1 are supported, see rgb_thread())
        self.rgbspeed = rgbspeed #Speed multiplier for the rbg algorithm

#Layout information, what key is it (scan code/text expression), lower and uppercase text that appear on the key, geometry and which preset it adheres to.
class Layout:
    
    def __init__(self, scancode, lowercase, uppercase, shift, caps, posx, posy, width, height, presetNumber):

        try: #The contstructor supports using either scancode number or text version of key
            self.scancode = int(scancode)
        except:
            self.scancode = scancode

        self.lowercase = lowercase #The letter that will appear when the keyboard is in *lower* case mode (shift or caps lock)
        self.uppercase = uppercase #The letter that wiil appear when the keyboard is in *upper* case mode
        self.shift = shift #if the key should be modified when pressing shift
        self.caps = caps #if the key should be modified with caps lock
        self.posx = posx #x-coordinate for the key
        self.posy = posy #y-coordinate for the key
        self.width = width #width of the key
        self.height = height #height of the key
        self.presetNumber = presetNumber #Which preset in the preset list this key uses

#Class for the key, attributes depend on the layout and preset from the 
class Key:

    def __init__(self, layout, preset, i):

        #Key based information (key scan code, key text, key position)
        self.__scancode = layout.scancode
        self.lowercase = layout.lowercase
        self.uppercase = layout.uppercase
        self.shift = layout.shift
        self.caps = layout.caps
        self.__posx = layout.posx
        self.__posy = layout.posy
        self.__width = layout.width
        self.__height = layout.height

        #Preset based information (color, font, position, size)

        self.__keybackgroundcolor = preset.keybackgroundcolor
        self.__keyforegroundcolor = preset.keyforegroundcolor
        self.__font = preset.font
        self.__fontsize = preset.fontsize
        self.__bold = preset.bold
        self.__italics = preset.italics
        self.__backgroundcolorPressed = preset.backgroundcolorPressed
        self.__foregroundcolorPressed = preset.foregroundcolorPressed
        self.__fontPressed = preset.fontPressed
        self.__fontsizePressed = preset.fontsizePressed
        self.__boldPressed = preset.boldPressed
        self.__italicsPressed = preset.italicsPressed
        self.rgb = preset.rgb
        self.rgbtype = preset.rgbtype
        self.rgbspeed = preset.rgbspeed

        self.isPressed = False

        self.labelFrame = tk.Frame(Globals.KB, width=self.__width, height=self.__height,bg=self.__keybackgroundcolor) #Place the label itself on a frame. This way we can use pixel based label size instead of
        self.labelFrame.pack_propagate(0)                                                                     #char based sizing, which will screw up the size of the frame if we change font size

        self.label = tk.Label(self.labelFrame, text=self.lowercase, font=self.getfont())
        self.label.configure(bg=self.__keybackgroundcolor, fg=self.__keyforegroundcolor)
        self.label.place(relx=0.5,rely=0.5, anchor=tk.CENTER)

        self.labelFrame.place(y=self.__posy, x=self.__posx)
        
        if self.__scancode not in Globals.mousebuttons and self.__scancode != "mouseindicator": # If it is not a mouse button, it is a keyboard button
            keyboard.on_press_key(self.__scancode, self.hotkeyPress)
            keyboard.on_release_key(self.__scancode, self.hotkeyRelease)

        elif self.__scancode in Globals.mousebuttons:
            mouse.on_button(self.hotkeyPress, (self,), Globals.mousedict[self.__scancode], (mouse.DOWN))
            mouse.on_button(self.hotkeyRelease, (self,), Globals.mousedict[self.__scancode], (mouse.UP))

        if self.__scancode == "mouseindicator":
            self.label.configure(text="") #It puts the "sensitivity" as the text, this just blanks it out
            Globals.mouseindicatorIndex = i
            self.mouseindicatorframe = tk.Frame(Globals.KB, width=self.__width, height=self.__height,bg=self.__keybackgroundcolor)
            self.mouseindicatorframe.pack_propagate(0)
            self.mouseindicator = tk.Label(self.mouseindicatorframe, text="",bg="grey")
            self.mouseindicator.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
            self.mouseindicatorframe.place(x=self.__posx, y=self.__posy)
            self.mouseindicatorx = self.__posx
            self.mouseindicatory = self.__posy

    #Change key color when you press a key
    def hotkeyPress(self,e):
        self.label.configure(bg=self.__backgroundcolorPressed,fg=self.__foregroundcolorPressed, font=self.getfontPressed()) #Change background color on label
        self.labelFrame.configure(bg=self.__backgroundcolorPressed)                                                                                     #You also need to change the color on the label frame
        self.isPressed = True

    #Change key color back to the unpressed key color when you release it
    def hotkeyRelease(self,e):
        self.label.configure(bg=self.__keybackgroundcolor,fg=self.__keyforegroundcolor, font=self.getfont())
        self.labelFrame.configure(bg=self.__keybackgroundcolor)
        self.isPressed = False

    #Method that returns font tuple used for the text on the label: (font, fontsize, bold/italics), for unpressed key state
    def getfont(self):
        if self.__bold and not self.__italics:
            return (self.__font, int(self.__fontsize), "bold")
        if self.__bold and self.__italics:
            return (self.__font, int(self.__fontsize), "bold italic")
        if not self.__bold and self.__italics:
            return (self.__font, int(self.__fontsize), "italic")
        else:
            return (self.__font, int(self.__fontsize))
            

    #Method that returns font tuple used for the text on the label: (font, fontsize, bold/italics), for pressed key state
    def getfontPressed(self):
        if self.__boldPressed and not self.__italicsPressed:
            return (self.__fontPressed, int(self.__fontsizePressed), "bold")
        if self.__boldPressed and self.__italicsPressed:
            return (self.__fontPressed, int(self.__fontsizePressed), "bold italic")
        if not self.__boldPressed and self.__italicsPressed:
            return (self.__fontPressed, int(self.__fontsizePressed), "italic")
        else:
            return (self.__fontPressed, int(self.__fontsizePressed))

#Class for the keyboard container
class Keyboard_class:

    def __init__(self, master):

        self.__frame = master #Reference to the main window
        self.__frame.title("Key Disp - Keyboard Input Display")

        self.__layoutList = self.__getLayout() #List of layouts, unprocessed
        self.__presetList = self.__getPreset() #List of presets, unprocessed

        self.__frame.configure(bg=self.__loadBackgroundColor())
        self.__frame.geometry(self.__getSize()) #first row in layout contains size
        self.__frame.protocol("WM_DELETE_WINDOW", self.__shutdown)

        self.buttonList = list()

        self.y = threading.Thread(target=mouseind_thread, args=(self,), daemon=True) #Daemon makes the thread stop when the (keyboard) window is closed, the program would otherwise run perpetually
        
        for i in range(len(self.__layoutList)):
            self.buttonList.append(Key(self.__layoutList[i], self.__presetList[self.__layoutList[i].presetNumber-1],i))

        if self.buttonList[0].rgb == "1":
            self.x = threading.Thread(target=rgb_thread, args=(self,), daemon=True) #Daemon makes the thread stop when the (keyboard) window is closed, the program would otherwise run perpetually

        #Attributes for determining whether the keys should be in lowercase or uppercase

        keyboard.on_press_key(42, self.__leftShiftPress) #Add left shift events
        keyboard.on_release_key(42, self.__leftShiftRelease)

        keyboard.on_press_key(54, self.__rightShiftPress) #Add right shift events
        keyboard.on_release_key(54, self.__rightShiftRelease)
        
        keyboard.on_press_key(58, self.__capslock) #Caps lock event

        self.capslockPressed = False
        self.leftshiftPressed = False
        self.rightshiftPressed = False

    def left_mouse_press(self):
        self.buttonList[0].label.configure(bg="white")
        self.buttonList[0].labelFrame.configure(bg="white")
        self.buttonList[0].isPressed = True

    def left_mouse_release(self):
        self.buttonList[0].label.configure(bg="grey")
        self.buttonList[0].labelFrame.configure(bg="grey")
        self.buttonList[0].isPressed = False
        
    #Reads layout on startup from the file \settings.txt
    def __getLayout(self):

        layout = self.__layoutPath()
        layoutList = list()

        #Pre-processing, create a list of all buttons to be parsed
        with open(layout, "r", encoding="utf-8") as lines:
            for line in lines:
                if line[0] == "#" or line.split("=")[0] == "size":
                    continue
                layoutList.append(line.strip())

        #Replace every entry with a layout object
        for i in range(len(layoutList)):
            listObjectRaw = list()
            tmp = layoutList[i].split(":")
            emptyStringError = False #: and = are string tokens, so they will cause an empty string error
            for j in range(len(tmp)):
                line = tmp[j].split("=")
                if line == [""]:
                    listObjectRaw.append(":")
                    emptyStringError = True
                elif len(line) == 3:
                    listObjectRaw.append("=")

                elif line[1] == "IGNORE": #IGNORE can be used as a keyword to get the parser to "ignore" the entry and replace it with an empty string (empty string in the parser = error)
                    listObjectRaw.append("")
                else:
                    listObjectRaw.append(line[1])

            if emptyStringError:
                listObjectRaw.remove("")

            li = listObjectRaw #shorthand so the constructor call doesnt span 3 lines

            #Constructor call with expanded variables, so it is easier to know what variable goes where
            scancode = li[0]
            lowercase = li[1]
            uppercase = li[2]
            shift = li[3] == "True" #Typecasting from string to bool, bool() function is weird
            caps = li[4] == "True"
            posx = li[5]
            posy = li[6]
            width = li[7]
            height = li[8]
            presetNumber = int(li[9])
            layoutList[i] = Layout(scancode, lowercase, uppercase, shift, caps, posx, posy, width, height, presetNumber)

        return layoutList

    #A function which checks if the loaded keyboard has RGB. If either a preset has RGB=1 or 
    def hasRGB(self):

        RGB = False

        for i in range(len(self.__presetList)):
            if self.__presetList[i].rgb == "1":
                RGB = True

        return RGB

    #Loads the path for the layout file
    def __layoutPath(self):

        layout = ""

        with open("settings.txt", "r", encoding="utf-8") as lines: #Loop through all lines in settings folder, break when you reach the layout entry
            for line in lines:
                tmp = line.split(":")
                if tmp[0] == "layout":
                    try: #If non-windows, path will use forward slash instead
                        layout = "Layouts\\" + tmp[1].strip() + ".txt"
                        f = open(layout)
                        f.close()
                        break
                    except:
                        try: #If non windows and "non-non-windows", the file probably doesn't exist
                            layout = "Layouts/" + tmp[1].strip() + ".txt"
                            f = open(layout)
                            f.close()
                            break
                        except:
                            raise LayoutError("Error opening layout file, file does not exist!")
                        
        return layout

    #Reads the preset on startup from the file \settings.txt
    def __getPreset(self):

        preset = self.__presetPath()
        presetListRaw = list()

        #Pre-processing, create a list of all presets properties
        with open(preset, "r", encoding="utf-8") as lines:
            for line in lines:
                if line[0] == "#" or line.split(":")[0] == "backgroundcolor": #ignore comments and the backgroundcolor property
                    continue
                presetListRaw.append(line.strip())

        i = 0 #Current item in the full list of parameters
        j = 0 #Current preset
        presetList = list()
        preset = list() #The current preset 

        while i < len(presetListRaw):
            line = presetListRaw[i].split(":")
            if line[0] == "preset" and len(preset) != 0:
                if j == 0:
                    preset.pop(0)
                presetList.append(self.__createPreset(preset, j))
                preset = list()
                j += 1
            else:
                preset.append(line[1])
            i += 1

        preset.pop(0)
        presetList.append(self.__createPreset(preset, j))

        return presetList

    #Helper method for creating the preset, to make the code less bloated
    def __createPreset(self, preset, num):

        keybackgroundcolor = preset[0]
        keyforegroundcolor = preset[1]
        font = preset[2]
        fontsize = preset[3]
        bold = preset[4] == "True" #Cast to bool
        italics = preset[5] == "True"
        backgroundcolorPressed = preset[6]
        foregroundcolorPressed = preset[7]
        fontPressed = preset[8]
        fontsizePressed = preset[9]
        boldPressed = preset[10] == "True"
        italicsPressed = preset[11] == "True"
        rgb = preset[12]

        if len(preset) == 13:
            return Preset(keybackgroundcolor, keyforegroundcolor, font, fontsize, bold, italics, backgroundcolorPressed, foregroundcolorPressed, fontPressed, fontsizePressed, bold, italics, rgb)
        elif len(preset) > 13: 
            rgbtype = preset[13]
            rgbspeed = preset[14]
            return Preset(keybackgroundcolor, keyforegroundcolor, font, fontsize, bold, italics, backgroundcolorPressed, foregroundcolorPressed, fontPressed, fontsizePressed, boldPressed, italicsPressed, rgb, rgbtype, rgbspeed)
        else:
            raise PresetError("Invalid amount of preset parameters in preset " + str(num+1))


    #Loads the path for the preset file
    def __presetPath(self):

        preset = ""

        settingList = list()
        with open("settings.txt", "r", encoding="utf-8") as lines: #Loop through all lines in settings folder, break when you reach the layout entry
            for line in lines:
                tmp = line.split(":")
                if tmp[0] == "preset":
                    try: #If non-windows, path will use forward slash instead
                        preset = "Presets\\" + tmp[1].strip() + ".txt"
                        f = open(preset)
                        f.close()
                        break
                    except:
                        try: #If non windows and "non-non-windows", the file probably doesn't exist
                            preset = "Presets/" + tmp[1].strip() + ".txt"
                            f = open(preset)
                            f.close()
                            break
                        except:
                            raise PresetError("Error opening preset file, file does not exist!")
                        
        return preset

    #Load the keyboard window size (from the layout file)
    def __getSize(self):

        layout = self.__layoutPath()
        size = None

        f = open(layout, "r", encoding="utf-8")
        lines = f.readlines()
        for line in lines: #The file can have multiple comment lines.
            tmp = line.split("=")
            if tmp[0] == "size":
                size = tmp[1].strip()

        if size == None:
            raise LayoutError("Invalid Layout file! 'size' entry either missing or incorrect!")

        return size

    #Reads background color (from the layout file)
    def __loadBackgroundColor(self):

        f = open(self.__presetPath(), "r", encoding="utf-8")
        tmp = f.readlines()
        f.close()
        tmp = tmp[0].split(":")[1].strip()
        return tmp

    #Run process during shutdown, terminates the 
    def __shutdown(self):
        #To be added:
        # Save current active layout to settings.txt (so that the current setups gets remembered for next startup)
        # Save current active preset to settings.txt
        self.__frame.destroy()

    #Handle lower/uppercase when left shift is pressed
    def __leftShiftPress(self, e):

        if self.leftshiftPressed == True: #If you hold a key it will register multiple of the same event, dont need to do anything
            return

        self.leftshiftPressed = True #If shiftPressed is already True, then both shifts are now pressed 

        #For keys that are affected by shift only

        if self.leftshiftPressed and not self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift:
                    self.buttonList[i].label.configure(text=self.buttonList[i].uppercase)

        #For keys that are affected by both caps lock and shift

        #2 cases
        #if shift is pressed and not caps lock => set keys to upper case
        #else if shift is pressed and caps lock => set keys to lower

        if self.leftshiftPressed and not self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].uppercase)

        elif self.leftshiftPressed and self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].lowercase)

    #Handle lower/uppercase when left shift is released
    def __leftShiftRelease(self, e):

        self.leftshiftPressed = False

        #For keys that are affected by shift only

        if not (self.leftshiftPressed or self.rightshiftPressed):
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift:
                    self.buttonList[i].label.configure(text=self.buttonList[i].lowercase)

        #For keys that are affected by both caps lock and shift

        if not (self.leftshiftPressed or self.rightshiftPressed) and not self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].lowercase)
                
        if not (self.leftshiftPressed or self.rightshiftPressed) and self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].uppercase)
    
    #Handle lower/uppercase when right shift is pressed
    def __rightShiftPress(self, e):

        if self.rightshiftPressed == True: #If you hold a key it will register multiple of the same event, dont need to do anything
            return

        self.rightshiftPressed = True #If shiftPressed is already True, then both shifts are now pressed 

        #For keys that are affected by shift only

        if self.rightshiftPressed and not self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift:
                    self.buttonList[i].label.configure(text=self.buttonList[i].uppercase)

        #For keys that are affected by both caps lock and shift

        #2 cases
        #if shift is pressed and not caps lock => set keys to upper case
        #else if shift is pressed and caps lock => set keys to lower

        if self.rightshiftPressed and not self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].uppercase)

        elif self.rightshiftPressed and self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].lowercase)

    #Handle lower/uppercase when right shift is released
    def __rightShiftRelease(self, e):

        self.rightshiftPressed = False

        #For keys that are affected by shift only

        if not (self.leftshiftPressed or self.rightshiftPressed):
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift:
                    self.buttonList[i].label.configure(text=self.buttonList[i].lowercase)

        #For keys that are affected by both caps lock and shift

        if not (self.leftshiftPressed or self.rightshiftPressed) and not self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].lowercase)

        if not (self.leftshiftPressed or self.rightshiftPressed) and self.capslockPressed:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].uppercase)

    #Handle lower/uppercase when caps lock is toggled
    def __capslock(self,e):

        self.capslockPressed = not self.capslockPressed

        if (not (self.leftshiftPressed or self.rightshiftPressed) and self.capslockPressed) or ((self.leftshiftPressed or self.rightshiftPressed) and not self.capslockPressed):
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].uppercase)

        else:
            for i in range(len(self.buttonList)):
                if self.buttonList[i].shift and self.buttonList[i].caps:
                    self.buttonList[i].label.configure(text=self.buttonList[i].lowercase)

def main():

    root = tk.Tk()
    Globals.KB = Keyboard_class(root)

    #If it has RGB, start it here
    if Globals.KB.hasRGB():
        Globals.KB.x.start()

    #Check if the index index has mouseindicatorframe attribute 
    try:
        if Globals.KB.buttonList[Globals.mouseindicatorIndex].mouseindicatorframe != None:
            Globals.KB.y.start()
    except:
        pass
    
    #Globals.KB.thready.start()
    root.mainloop()

if __name__ == "__main__":
    main()