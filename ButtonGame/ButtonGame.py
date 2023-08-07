import tkinter as tk
#import winsound
import random

#############################################################################
#############################################################################
def control_Panel():
    global controlPanel
    controlPanel = tk.Tk()
    controlPanel.geometry("300x500")
    controlPanel.title("Button Control Panel")
    
    global gameWindowOpened
    gameWindowOpened = False

    # Create an Start Game Window button
    def openGame():
        global gameSettings, gameWindowOpened, gameWindow
        gameSettings = createGameSettings()
        print(gameSettings)
        if not gameWindowOpened:
            gameWindow = createGameWindow()
            gameWindowOpened = True
            gameWindow.protocol("WM_DELETE_WINDOW", on_game_window_closed)
        else:
            open_popup("Game Window is already running.", 
                       "The game window is already running, please close the previous game window.")
        
    # Create Label and Entry
    durationLabel = tk.Label(controlPanel, text="Color Change Duration (ms):")
    durationLabel.pack()
    durationEntry = tk.Entry(controlPanel)
    durationEntry.pack()

    intermissionLabel = tk.Label(controlPanel, text="Intermission Duration (ms):")
    intermissionLabel.pack()
    intermissionEntry = tk.Entry(controlPanel)
    intermissionEntry.pack()

    posXLabel = tk.Label(controlPanel, text="X Position of Circle (pixels):")
    posXLabel.pack()
    posXEntry = tk.Entry(controlPanel)
    posXEntry.pack()

    posYLabel = tk.Label(controlPanel, text="Y Position of Circle (pixels):")
    posYLabel.pack()
    posYEntry = tk.Entry(controlPanel)
    posYEntry.pack()

    circleSizeLabel = tk.Label(controlPanel, text="Circle Size (pixels):")
    circleSizeLabel.pack()
    circleSizeEntry = tk.Entry(controlPanel)
    circleSizeEntry.pack()

    # Create checkbox
    duraCheckBoxState = tk.IntVar(value=0)
    duraCheckBox = tk.Checkbutton(controlPanel, \
                                  text="Manual Reset", variable=duraCheckBoxState)
    duraCheckBox.pack()
    
    soundCheckBoxState = tk.IntVar(value=1)
    soundCheckBox = tk.Checkbutton(controlPanel, \
                                   text="Sound Effects", variable=soundCheckBoxState)
    soundCheckBox.pack()

    randMoveCircleState = tk.IntVar(value=0)
    randMoveCircleButton = tk.Checkbutton(controlPanel, \
                                     text="Randomly Move Circle", variable=randMoveCircleState)
    randMoveCircleButton.pack()

    newWindowButton = tk.Button(controlPanel, text="Start Game", command=openGame)
    newWindowButton.pack()

    
    # Creating Apply Settings button
    def applySettings():
        # Apply the settings to the game
        global gameSettings
        global canvas
        if durationEntry.get() != '':
            gameSettings["duration"] = int(durationEntry.get())
        if intermissionEntry.get() != '':
            gameSettings["intermissionTime"] = int(intermissionEntry.get())

        try:
            canvas.delete(circle)
            canvas.delete(outer_ring)
        finally:
            if posXEntry.get() != '':
                gameSettings["posX"] = int(posXEntry.get())
            if posYEntry.get() != '':
                gameSettings["posY"] = int(posYEntry.get())
            if circleSizeEntry.get() != '':
                gameSettings["circleSize"] = int(circleSizeEntry.get())
            
        drawCircle(gameSettings["posX"], gameSettings["posY"], gameSettings["circleSize"])
                
        gameSettings["duraCheckBox"] = duraCheckBoxState.get()
        gameSettings["soundCheckBox"] = soundCheckBoxState.get()
        gameSettings["randMoveCircleCheckBox"] = randMoveCircleState.get()
        print(gameSettings)
        
    applyButton = tk.Button(controlPanel, text="Apply", command=applySettings)
    applyButton.pack()

    def on_game_window_closed():
        resetButton.destroy()
        gameWindow.destroy()
        global gameWindowOpened
        gameWindowOpened = False


    # Creating Exit button
    def exitGame():
        try:
            global gameWindow
            gameWindow.destroy()
        finally:
            controlPanel.destroy()

    exitButton = tk.Button(controlPanel, text="Exit", command=exitGame)
    exitButton.pack()

    # Error Prompt function. could be moved to another script if needed
    def open_popup(title, reason):
        popup_window = tk.Toplevel(controlPanel)
        popup_window.title(title)
        popup_window.geometry("500x100")
        # popup_window.protocol("WM_DELETE_WINDOW", popup_window.on_popup_close)

        # Content of the popup window
        popup_label = tk.Label(popup_window, text=reason)
        popup_label.pack()


#############################################################################
#############################################################################
def drawCircle(posXEntry, posYEntry, circleSizeEntry):
    # Calculate the center coordinates of the canvas
    center_x = gameSettings["posX"]
    center_y = gameSettings["posY"]
    
    cSize = gameSettings["circleSize"]
    
    # Draw the outer circle
    global outer_ring
    outer_ring = canvas.create_oval(center_x-cSize, center_y-cSize,\
                                    center_x+cSize, center_y+cSize,\
                                    outline="black", width=10)

    # Draw the inner circle
    global circle
    circle = canvas.create_oval(center_x-cSize, center_y-cSize,\
                                center_x+cSize, center_y+cSize,\
                                fill="#990000")

def randDrawCircle():
    # Calculate the center coordinates of the canvas
    cSize = random.randint(20, 200)
    center_x = random.randint(cSize, 1600-cSize)
    print(center_x)
    center_y = random.randint(cSize, 900-cSize)
    print(center_y)
    
    
    # Draw the outer circle
    global outer_ring
    outer_ring = canvas.create_oval(center_x-cSize, center_y-cSize,\
                                    center_x+cSize, center_y+cSize,\
                                    outline="black", width=10)

    # Draw the inner circle
    global circle
    circle = canvas.create_oval(center_x-cSize, center_y-cSize,\
                                center_x+cSize, center_y+cSize,\
                                fill="#990000")
    
#############################################################################
#############################################################################        
def createGameWindow():
    gameWindow = tk.Tk()
    gameWindow.geometry("1600x900")
    gameWindow.title("Button Game")

    global controlPanel
    # Create a white canvas to draw the circle
    global canvas
    canvas = tk.Canvas(gameWindow, width=1600, height=900, bg="white")
    canvas.pack()

    if gameSettings["randMoveCircleCheckBox"] == 0:
        drawCircle(gameSettings["posX"], gameSettings["posY"], gameSettings["circleSize"])
    else:
        randDrawCircle()
    
    def play_audio():
        if gameSettings["soundCheckBox"] == 1:
            print("DING!")
            #winsound.PlaySound("rewardSound.wav", winsound.SND_ASYNC)
            # Only can use WAV files            

    def reset_color():
        if gameSettings["intermissionTime"] != 0:
            canvas.delete(circle)
            canvas.delete(outer_ring)
            if gameSettings["randMoveCircleCheckBox"] == 1:
                gameWindow.after(gameSettings["intermissionTime"], randDrawCircle)
            else:
                gameWindow.after(gameSettings["intermissionTime"], 
                                 lambda: drawCircle(gameSettings["posX"], gameSettings["posY"], gameSettings["circleSize"]))
        else:
            canvas.itemconfig(circle, fill="#990000")
       
    # Main functions
    def on_key_press(event):
        if event.keysym == "space" and canvas.itemcget(circle, "fill") == "#990000":
            # Change the color to green when spacebar is pressed
            canvas.itemconfig(circle, fill="green")
            play_audio()
            
            if gameSettings["duraCheckBox"] == 0:
                # Reset color after 3 seconds
                gameWindow.after(gameSettings["duration"], reset_color)

    global resetButton
    resetButton = tk.Button(controlPanel, text="Reset Button", command=reset_color)
    resetButton.pack()
    
    # Bind the key press event to the window
    gameWindow.bind("<KeyPress>", on_key_press)
    return gameWindow


#############################################################################
#############################################################################
def createGameSettings():
    # Initialising Settings Dictionary
    gameSettings = {
        "duration" : 3000, # Default 3000ms
        "posX" : 800,
        "posY" : 450,
        "circleSize" : 200,
        "duraCheckBox" : 0,
        "soundCheckBox" : 1,
        "randMoveCircleCheckBox" : 0,
        "intermissionTime" : 0
    }
    return gameSettings


#############################################################################
#############################################################################

##Main Loop##
control_Panel()
controlPanel.mainloop()