from PIL import Image, ImageFont, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import shutil

BACKGROUND_COLOUR = "#D8D2C2"


class WatermarkApp:
    def __init__(self, window):

        # Create the Tkinter window
        self.window = window
        self.window.title("Image Watermarking App")
        self.window.minsize(width=800, height=600)
        self.window.config(padx=10, pady=20)
        self.final_image = None
        self.temp_image_path = None
        self.image_on_canvas = None
        self.image_tk = None

        self.frame = tk.Frame(window, bg=BACKGROUND_COLOUR, width=800, height=600)
        self.frame.grid(row=0, column=2, rowspan=10, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.canvas = tk.Canvas(self.frame, bg="white", width=800, height=600)
        self.canvas.grid(row=0, column=2, rowspan=10, columnspan=2, padx=10, pady=10)

        # Labels

        # Text Label
        self.text_label = tk.Label(window, text="Watermark Text", background=BACKGROUND_COLOUR,
                                   font=("calibri", 18, "underline"))
        self.text_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Watermark entry box
        self.text_box = tk.Entry(window, font=("calibri", 16), width=45)
        self.text_box.grid(row=1, column=0, columnspan=2, sticky="w")

        # Placement Section

        # Placement Label
        self.placement_label = tk.Label(window, text="Placement", background=BACKGROUND_COLOUR,
                                        font=("calibri", 18, "underline"))
        self.placement_label.grid(row=3, column=0, sticky="w")

        # Placement Configuration
        self.place_label = tk.Label(window, text="Placement", bg=BACKGROUND_COLOUR)
        options = [
            "Bottom-right",
            "Bottom-left",
            "Top-left",
            "Top-right",
            "Centre",
            "Centre-left",
            "Centre-right",
            "Custom",
        ]
        self.place_var = tk.StringVar()
        self.place_var.set("Choose Placement")
        self.place_dropdown = ttk.Combobox(window, textvariable=self.place_var, values=options, width=30)
        self.place_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.place_dropdown.grid(row=4, column=1, padx=5, pady=5)
        self.place_var.trace_add("write", self.update_place_dropbox_spinboxes)

        # Delta x configuration
        self.delta_x_label = tk.Label(window, text="Delta X (pixels)", bg=BACKGROUND_COLOUR)
        self.delta_x_spinbox = ttk.Spinbox(window, from_=1, to=100, background=BACKGROUND_COLOUR, width=30)
        self.delta_x_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.delta_x_spinbox.set(1)
        self.delta_x_spinbox.grid(row=5, column=1, padx=5, pady=5)

        # Delta y configuration
        self.delta_y_label = tk.Label(window, text="Delta Y (pixels)", bg=BACKGROUND_COLOUR)
        self.delta_y_spinbox = ttk.Spinbox(window, from_=1, to=100, background=BACKGROUND_COLOUR, width=30)
        self.delta_y_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.delta_y_spinbox.set(1)
        self.delta_y_spinbox.grid(row=6, column=1, padx=10, pady=10)

        # Font Section
        # Font Label
        self.font_label = tk.Label(window, text="Font", background=BACKGROUND_COLOUR,
                                   font=("calibri", 18, "underline"))
        self.font_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        # font type configuration
        self.font_type_label = tk.Label(window, text="Type", background=BACKGROUND_COLOUR)
        fonts = [
            "Arial",
            "Helvetica",
            "Times New Roman",
            "Courier New",
            "Verdana",
            "Georgia",
            "Garamond",
            "Comic Sans MS",
            "Impact",
            "Monaco",
            "Consolas",
            "Calibri",
            "Candara",
            "Optima",
            "Franklin Gothic",
            "Futura"
        ]

        self.font_dropbox = ttk.Combobox(window, values=fonts, width=30)
        self.font_dropbox.set("Choose font")
        self.font_type_label.grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.font_dropbox.grid(row=8, column=1, padx=5, pady=5)

        # font colour configuration
        self.font_colour_label = tk.Label(
            window, text="Colour", background=BACKGROUND_COLOUR
        )
        colours = [
            "AliceBlue",
            "AntiqueWhite",
            "Aqua",
            "Aquamarine",
            "Azure",
            "Beige",
            "Bisque",
            "Black",
            "BlanchedAlmond",
            "Blue",
            "BlueViolet",
            "Brown",
            "BurlyWood",
            "CadetBlue",
            "Chartreuse",
            "Chocolate",
            "Coral",
            "CornflowerBlue",
            "Cornsilk",
            "Crimson",
            "Cyan",
            "DarkBlue",
            "DarkCyan",
            "DarkGoldenRod",
            "DarkGray",
            "DarkGreen",
            "DarkKhaki",
            "DarkMagenta",
            "DarkOliveGreen",
            "DarkOrange",
            "DarkOrchid",
            "DarkRed",
            "DarkSalmon",
            "DarkSeaGreen",
            "DarkSlateBlue",
            "DarkSlateGray",
            "DarkTurquoise",
            "DarkViolet",
            "DeepPink",
            "DeepSkyBlue",
            "DimGray",
            "DodgerBlue",
            "FireBrick",
            "FloralWhite",
            "ForestGreen",
            "Fuchsia",
            "Gainsboro",
            "GhostWhite",
            "Gold",
            "GoldenRod",
            "Gray",
            "Green",
            "GreenYellow",
            "HoneyDew",
            "HotPink",
            "IndianRed",
            "Indigo",
            "Ivory",
            "Khaki",
            "Lavender",
            "LavenderBlush",
            "LawnGreen",
            "LemonChiffon",
            "LightBlue",
            "LightCoral",
            "LightCyan",
            "LightGoldenRodYellow",
            "LightGray",
            "LightGreen",
            "LightPink",
            "LightSalmon",
            "LightSeaGreen",
            "LightSkyBlue",
            "LightSlateGray",
            "LightSteelBlue",
            "LightYellow",
            "Lime",
            "LimeGreen",
            "Linen",
            "Magenta",
            "Maroon",
            "MediumAquaMarine",
            "MediumBlue",
            "MediumOrchid",
            "MediumPurple",
            "MediumSeaGreen",
            "MediumSlateBlue",
            "MediumSpringGreen",
            "MediumTurquoise",
            "MediumVioletRed",
            "MidnightBlue",
            "MintCream",
            "MistyRose",
            "Moccasin",
            "NavajoWhite",
            "Navy",
            "OldLace",
            "Olive",
            "OliveDrab",
            "Orange",
            "OrangeRed",
            "Orchid",
        ]

        self.font_colour_dropbox = ttk.Combobox(window, values=colours, width=30)
        self.font_colour_dropbox.set("Choose colour")
        self.font_colour_label.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.font_colour_dropbox.grid(row=9, column=1, padx=5, pady=5)

        # Configure grid weights to ensure the canvas expands properly
        # for i in range(0, 11):
        #     self.frame.grid_rowconfigure(i, weight=1)
        #     self.window.grid_rowconfigure(i, weight=1)
        #     if i < 4:
        #         self.frame.grid_columnconfigure(2, weight=1)
        #         self.window.grid_columnconfigure(2, weight=1)

        # Button

        # Upload Image Button
        self.upload_button = ttk.Button(window, text="Upload Image", command=self.upload_image, width=40)
        self.upload_button.grid(row=10, column=2, padx=10)

        # Save Button
        self.save_button = ttk.Button(window, text="Save Image", command=self.save_image, width=40)
        self.save_button.grid(row=10, column=3, padx=10)

        # Add text Button
        self.add_text_button = ttk.Button(window, text="Add Watermark", command=self.add_text, width=40)
        self.add_text_button.grid(row=10, column=1, padx=5, pady=10, sticky="w")

        # Reset Button
        self.reset_button = ttk.Button(window, text="Reset", command=self.reset, width=40)
        self.reset_button.grid(row=10, column=0, padx=5, pady=10, sticky="w")

    def upload_image(self):
        """Window popup to choose image to upload"""

        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if file_path:
            self.display_image(file_path)

    def display_image(self, file_path):
        """Displays the image the user chooses to upload"""

        img = Image.open(file_path)
        self.final_image = img
        img_width, img_height = img.size

        frame_width = self.frame.winfo_width()
        frame_height = self.frame.winfo_height()
        ratio = min(frame_width / img_width, frame_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_img)

        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(
            frame_width // 2, frame_height // 2, anchor="center", image=self.image_tk
        )

        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.update_idletasks()

    def add_text(self):
        """Adds the watermark to the image"""

        # catch errors when adding watermark
        if not self.final_image:
            print("No image loaded.")
            messagebox.showerror(
                "No image loaded", "Please upload an image before adding a watermark"
            )
            return

        if self.place_dropdown.get() == "Choose placement":
            messagebox.showerror(
                "No position chosen", "Please choose a placement option"
            )
            return

        if self.font_dropbox.get() == "Choose font":
            messagebox.showerror("No font chosen", "Please choose a font")
            return

        if self.font_colour_dropbox.get() == "Choose colour":
            messagebox.showerror("No font colour chosen", "Please choose a font colour")
            return

        if self.text_box.get() == "":
            messagebox.showerror("No watermark", "Please type in a watermark")
            return

        image = self.final_image.copy()
        img_width, img_height = image.size

        font_name = self.font_dropbox.get().title() + ".ttf"
        font_path = os.path.join("fonts", font_name)

        try:
            # Calculate text size as a percentage of the image height
            text_size = int(img_height * 0.05)
            text_font = ImageFont.truetype(font_path, text_size)
        except OSError:
            print(f"Font file {font_path} not found.")
            messagebox.showwarning(
                "Font doesn't exist",
                f"Font file {self.font_dropbox.get()} not found\nTry a different font.",
            )
            return

        text = self.text_box.get()
        edited_image = ImageDraw.Draw(image)

        # Calculating position based on the image size
        position = self.place_dropdown.get()
        coordinates = {
            "Bottom-right": (int(img_width * 0.7), int(img_height * 0.92)),
            "Bottom-left": (int(img_width * 0.3), int(img_height * 0.92)),
            "Top-left": (int(img_width * 0.1), int(img_height * 0.1)),
            "Top-right": (int(img_width * 0.9), int(img_height * 0.1)),
            "Centre": (int(img_width * 0.31), int(img_height * 0.5)),
            "Centre-left": (int(img_width * 0.1), int(img_height * 0.5)),
            "Centre-right": (int(img_width * 0.9), int(img_height * 0.5)),
        }

        if position in coordinates:
            text_position = coordinates[position]
        else:
            xcor = int(self.delta_x_spinbox.get()) / 100
            ycor = int(self.delta_y_spinbox.get()) / 100
            text_position = (
                int(img_width * xcor),
                int(img_height * ycor),
            )

        edited_image.text(text_position, text, fill=self.font_colour_dropbox.get(), font=text_font)

        # Save the watermarked image temporarily
        self.temp_image_path = os.path.join(os.getcwd(), "temp_image.png")
        image.save(self.temp_image_path)

        # Display the updated image on the canvas
        self.display_temp_image(self.temp_image_path)

    def display_temp_image(self, file_path):
        """Shows a preview of the changes made to the image the user wants to watermark"""

        img = Image.open(file_path)
        img_width, img_height = img.size

        frame_width = self.frame.winfo_width()
        frame_height = self.frame.winfo_height()
        ratio = min(frame_width / img_width, frame_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)

        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_img)

        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(
            frame_width // 2, frame_height // 2, anchor="center", image=self.image_tk
        )

        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def reset(self):
        """Clears the image in the canvas"""

        self.canvas.delete("all")
        self.final_image = None
        if self.temp_image_path and os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)
        self.temp_image_path = None

    def update_place_dropbox_spinboxes(self, *args):
        """activates the placement spinboxes when conditions are satisfied"""

        selected_position = self.place_dropdown.get()
        if selected_position == "Custom":
            self.delta_x_spinbox.configure(state="normal")
            self.delta_y_spinbox.configure(state="normal")
        else:
            self.delta_x_spinbox.configure(state="disabled")
            self.delta_y_spinbox.configure(state="disabled")

    def save_image(self):
        """Saves the watermarked image and opens it to the user"""

        if self.temp_image_path:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
            )
            if save_path:
                shutil.copyfile(self.temp_image_path, save_path)
                os.remove(self.temp_image_path)  # Removes temporary image after saving
                messagebox.showinfo(
                    "Image Saved", f"The image has been saved at:\n{save_path}"
                )
                os.startfile(save_path)
        else:
            messagebox.showwarning(
                "No Watermark", "Please add a watermark before saving the image."
            )

    def run(self):
        self.window.mainloop()
