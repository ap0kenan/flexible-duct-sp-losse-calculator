import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from utils.resources import resource_path


class HomePage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame,
            text="HVAC Duct Calculator",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(10, 20))

        ttk.Label(
            main_frame,
            text="Select a calculator to begin",
            font=("Segoe UI", 12)
        ).pack(pady=(0, 30))

        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill="both", expand=True, pady=10)

        # Flexible Duct Calculator
        flex_frame = ttk.LabelFrame(options_frame, text="Flexible Duct Calculator", padding="10")
        flex_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        try:
            flex_img_path = resource_path("flexduct.png")
            flex_img = Image.open(flex_img_path)
            flex_img = flex_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.flex_photo = ImageTk.PhotoImage(flex_img)
            ttk.Label(flex_frame, image=self.flex_photo).pack(pady=(0, 10))
        except Exception as e:
            print(f"Error loading flexduct.png: {e}")
            ttk.Label(flex_frame, text="Flexible Duct Image", foreground="gray").pack(pady=(0, 10))

        ttk.Button(
            flex_frame,
            text="Open Calculator",
            command=lambda: self.controller.show_frame("FlexibleDuctPage"),
            width=20
        ).pack(pady=5)

        # Rectangular Duct Calculator (Placeholder)
        rect_frame = ttk.LabelFrame(options_frame, text="Rectangular Duct Calculator", padding="10")
        rect_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        try:
            rect_img_path = resource_path("recduct.png")
            rect_img = Image.open(rect_img_path)
            rect_img = rect_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.rect_photo = ImageTk.PhotoImage(rect_img)
            ttk.Label(rect_frame, image=self.rect_photo).pack(pady=(0, 10))
        except Exception as e:
            print(f"Error loading recduct.png: {e}")
            ttk.Label(rect_frame, text="Rectangular Duct Image", foreground="gray").pack(pady=(0, 10))

        ttk.Button(
            rect_frame,
            text="Coming Soon",
            command=lambda: messagebox.showinfo(
                "Placeholder", "Rectangular Duct Calculator will be added later."
            ),
            width=20,
            state="disabled"
        ).pack(pady=5)

        options_frame.columnconfigure(0, weight=1)
        options_frame.columnconfigure(1, weight=1)

        ttk.Button(main_frame, text="Exit", command=self.controller.quit, width=15).pack(pady=(30, 10))
