# ui/app_root.py
import tkinter as tk
from tkinter import ttk, messagebox
from ui.home_page import HomePage
from ui.flexible_duct_page import FlexibleDuctPage
from ui.credits_page import CreditsPage
from core.calculations import calculate_flexible_duct
from utils.resource_path import resource_path
import math


class FlexibleDuctApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HVAC Duct Calculator v1.4")
        self.geometry("900x650")
        self.minsize(800, 550)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Menu
        self.create_menu()

        # Shared variables
        self.duct_diameter_in_var = tk.StringVar(value="6.0")
        self.air_flow_cfm_var = tk.StringVar(value="1000")
        self.duct_length_ft_var = tk.StringVar(value="10")

        self.bend_45_count_var = tk.StringVar(value="0")
        self.bend_90_count_var = tk.StringVar(value="0")
        self.bend_180_count_var = tk.StringVar(value="0")

        self.roughness_choice_var = tk.StringVar()
        self.roughness_map = {
            "Low (0.003)": 0.003,
            "Medium (0.009)": 0.009,
            "High (0.015)": 0.015,
        }
        self.roughness_choice_var.set("Medium (0.009)")

        self.compression_percent_var = tk.DoubleVar(value=0.0)
        self.sf_enabled_var = tk.BooleanVar(value=False)
        self.safety_factor_var = tk.StringVar(value="10")  # %

        self.result_pressure_loss_var = tk.StringVar(value="—")
        self.result_air_velocity_var = tk.StringVar(value="—")
        self.last_inputs = None
        self.last_details = None

        # Pages container
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        # Initialize all pages
        self.frames = {}
        for Page in (HomePage, FlexibleDuctPage, CreditsPage):
            frame = Page(self.container, self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    # -----------------------------
    # Menu methods
    # -----------------------------
    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label="About", command=self.show_about)
        info_menu.add_command(label="Credits", command=self.show_credits)
        menubar.add_cascade(label="Info", menu=info_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Preferences", command=self.show_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.show_help)
        help_menu.add_command(label="FAQ", command=self.show_faq)
        menubar.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        messagebox.showinfo("About", "HVAC Duct Calculator\nVersion 1.4\n\nA tool for calculating pressure loss in duct systems.")

    def show_credits(self):
        self.show_frame("CreditsPage")

    def show_settings(self):
        messagebox.showinfo("Settings", "Settings options will be available in a future version.")

    def show_help(self):
        messagebox.showinfo("Help", "User guide documentation will be available soon.")

    def show_faq(self):
        messagebox.showinfo("FAQ", "Frequently Asked Questions will be added in a future update.")

    def show_frame(self, page_name: str):
        self.frames[page_name].tkraise()
        self.status_var.set(f"Viewing {page_name.replace('Page', '')}")

    # -----------------------------
    # Input & calculation helpers
    # -----------------------------
    def _parse_positive_float(self, value_str: str, field_name: str) -> float:
        try:
            value = float(value_str)
        except ValueError:
            raise ValueError(f"{field_name} must be a number.")
        if value < 0:
            raise ValueError(f"{field_name} must be non-negative.")
        return value

    def gather_inputs(self):
        duct_diameter_in = self._parse_positive_float(self.duct_diameter_in_var.get(), "Duct Diameter (in)")
        air_flow_cfm = self._parse_positive_float(self.air_flow_cfm_var.get(), "Air Flow (CFM)")
        duct_length_ft = self._parse_positive_float(self.duct_length_ft_var.get(), "Duct Length (ft)")
        bend_45 = int(self.bend_45_count_var.get())
        bend_90 = int(self.bend_90_count_var.get())
        bend_180 = int(self.bend_180_count_var.get())
        roughness_value = self.roughness_map[self.roughness_choice_var.get()]
        compression_percent = float(self.compression_percent_var.get())
        if self.sf_enabled_var.get():
            sf_percent = self._parse_positive_float(self.safety_factor_var.get(), "Safety Factor (%)")
        else:
            sf_percent = 10.0
        safety_factor = 1.0 + (sf_percent / 100.0)
        inputs = {
            "Duct Diameter (in)": duct_diameter_in,
            "Air Flow (CFM)": air_flow_cfm,
            "Duct Length (ft)": duct_length_ft,
            "Bends": {"45": bend_45, "90": bend_90, "180": bend_180},
            "Roughness": self.roughness_choice_var.get(),
            "Compression (%)": compression_percent,
            "Safety Factor (%)": sf_percent,
        }
        return inputs, {
            "duct_diameter_in": duct_diameter_in,
            "air_flow_cfm": air_flow_cfm,
            "duct_length_ft": duct_length_ft,
            "bend_counts": {"45": bend_45, "90": bend_90, "180": bend_180},
            "roughness_value": roughness_value,
            "compression_percent": compression_percent,
            "safety_factor": safety_factor,
        }

    def perform_calculation(self):
        try:
            inputs, params = self.gather_inputs()
            self.status_var.set("Calculating...")
            self.update_idletasks()
            v, dp, details = calculate_flexible_duct(**params)
            self.last_inputs = inputs
            self.last_details = details
            self.result_air_velocity_var.set(
                "Invalid (zero area)" if math.isinf(v) else f"{v:,.1f} FPM"
            )
            self.result_pressure_loss_var.set(f"{dp:.4f} in. w.g.")
            self.status_var.set("Calculation completed successfully")
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))
            self.status_var.set("Error in calculation")

    # -----------------------------
    # Full results popup
    # -----------------------------
    def show_full_results(self):
        if not self.last_details:
            messagebox.showinfo("No results", "Please run a calculation first.")
            return
        popup = tk.Toplevel(self)
        popup.title("Full Calculation Results")
        popup.geometry("500x550")
        frame = ttk.Frame(popup, padding=10)
        frame.pack(fill="both", expand=True)
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        row = 0
        ttk.Label(scrollable_frame, text="--- INPUTS ---", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, columnspan=2, sticky="w", pady=(0, 6))
        row += 1
        for k, v in self.last_inputs.items():
            if k == "Bends":
                bends = ", ".join(f"{ang}°: {cnt}" for ang, cnt in v.items())
                ttk.Label(scrollable_frame, text=f"{k}:").grid(row=row, column=0, sticky="w")
                ttk.Label(scrollable_frame, text=bends).grid(row=row, column=1, sticky="e")
            else:
                ttk.Label(scrollable_frame, text=f"{k}:").grid(row=row, column=0, sticky="w")
                ttk.Label(scrollable_frame, text=str(v)).grid(row=row, column=1, sticky="e")
            row += 1
        ttk.Label(scrollable_frame, text="").grid(row=row, column=0)
        row += 1
        ttk.Label(scrollable_frame, text="--- CALCULATED ---", font=("Segoe UI", 10, "bold")).grid(row=row, column=0, columnspan=2, sticky="w", pady=(6, 6))
        row += 1
        for k, v in self.last_details.items():
            ttk.Label(scrollable_frame, text=f"{k}:").grid(row=row, column=0, sticky="w")
            ttk.Label(scrollable_frame, text=f"{v:,.5g}").grid(row=row, column=1, sticky="e")
            row += 1
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
