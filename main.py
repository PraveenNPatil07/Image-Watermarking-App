from tkinter import Tk, PhotoImage
from watermark import WatermarkApp

BACKGROUND_COLOUR = "#D8D2C2"

root = Tk()
icon = PhotoImage(file="Icons/icon.png")
root.iconphoto(False, icon)
root.config(bg=BACKGROUND_COLOUR)

# optional window size
# root.geometry("900x600")

root.resizable(True, True)
app = WatermarkApp(root)
app.run()
