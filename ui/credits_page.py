import tkinter as tk
from tkinter import ttk


class CreditsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Credits", font=("Segoe UI", 20, "bold")).pack(pady=(10, 20))

        credits_text = (
            "Developed by Eng. Bashar\n"
            "Email: basharwmn@gmail.com\n\n"
            "All rights reserved ©"
        )
        ttk.Label(main_frame, text=credits_text, font=("Segoe UI", 12), justify="center").pack(pady=10)

        ttk.Button(main_frame, text="Back to Home", width=20,
                   command=lambda: self.controller.show_frame("HomePage")).pack(pady=30)
