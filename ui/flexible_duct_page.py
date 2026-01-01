import tkinter as tk
from tkinter import ttk, messagebox


class FlexibleDuctPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(
            main_frame,
            text="Flexible Duct Calculator",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        left_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="10")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        right_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(10, 0))

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        left_frame.columnconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

        # Input Fields
        labels_entries = [
            ("Duct Diameter (in):", self.controller.duct_diameter_in_var),
            ("Air Flow (CFM):", self.controller.air_flow_cfm_var),
            ("Duct Length (ft):", self.controller.duct_length_ft_var)
        ]

        for i, (label, var) in enumerate(labels_entries):
            ttk.Label(left_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            ttk.Entry(left_frame, textvariable=var, width=15).grid(row=i, column=1, sticky="ew", pady=5, padx=(5, 0))

        # Bends
        ttk.Label(left_frame, text="Bends:").grid(row=3, column=0, sticky="w", pady=5)
        bend_frame = ttk.Frame(left_frame)
        bend_frame.grid(row=3, column=1, sticky="ew", pady=5, padx=(5, 0))

        bends = [("45°:", self.controller.bend_45_count_var),
                 ("90°:", self.controller.bend_90_count_var),
                 ("180°:", self.controller.bend_180_count_var)]
        for j, (txt, var) in enumerate(bends):
            ttk.Label(bend_frame, text=txt).grid(row=0, column=j*2, sticky="w")
            tk.Spinbox(bend_frame, from_=0, to=1000, textvariable=var, width=8).grid(row=0, column=j*2+1, padx=(2, 10))

        # Roughness
        ttk.Label(left_frame, text="Duct Roughness:").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Combobox(
            left_frame,
            textvariable=self.controller.roughness_choice_var,
            values=list(self.controller.roughness_map.keys()),
            state="readonly",
            width=20
        ).grid(row=4, column=1, sticky="w", pady=5, padx=(5, 0))

        # Compression
        ttk.Label(left_frame, text="Compression (%):").grid(row=5, column=0, sticky="w", pady=5)
        comp_frame = ttk.Frame(left_frame)
        comp_frame.grid(row=5, column=1, sticky="ew", pady=5, padx=(5, 0))
        ttk.Entry(comp_frame, textvariable=self.controller.compression_percent_var, width=8).grid(row=0, column=0)
        ttk.Scale(
            comp_frame,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self.controller.compression_percent_var
        ).grid(row=0, column=1, sticky="ew", padx=(5, 0))
        comp_frame.columnconfigure(1, weight=1)

        # Safety Factor
        ttk.Label(left_frame, text="Safety Factor (%):").grid(row=6, column=0, sticky="w", pady=5)
        sf_frame = ttk.Frame(left_frame)
        sf_frame.grid(row=6, column=1, sticky="ew", pady=5, padx=(5, 0))
        self.sf_entry = ttk.Entry(sf_frame, textvariable=self.controller.safety_factor_var, width=10, state="disabled")
        self.sf_entry.grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(sf_frame, text="Enable custom SF", variable=self.controller.sf_enabled_var,
                        command=self.toggle_sf).grid(row=0, column=1, sticky="w", padx=(5, 0))
        sf_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=15)
        ttk.Button(button_frame, text="Calculate", command=self.controller.perform_calculation, width=15)\
            .grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Reset Inputs", command=self._reset_inputs, width=15)\
            .grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Back to Home", command=lambda: self.controller.show_frame("HomePage"))\
            .grid(row=1, column=0, columnspan=2, pady=(10, 0))

        # Results
        ttk.Label(right_frame, text="Air Velocity:").grid(row=0, column=0, sticky="w", pady=8)
        ttk.Entry(right_frame, textvariable=self.controller.result_air_velocity_var,
                  state="readonly").grid(row=0, column=1, sticky="ew", pady=8, padx=(5, 0))
        ttk.Label(right_frame, text="Total Pressure Loss:").grid(row=1, column=0, sticky="w", pady=8)
        ttk.Entry(right_frame, textvariable=self.controller.result_pressure_loss_var,
                  state="readonly").grid(row=1, column=1, sticky="ew", pady=8, padx=(5, 0))
        ttk.Button(right_frame, text="See Full Results", command=self.controller.show_full_results, width=20)\
            .grid(row=2, column=0, columnspan=2, pady=20)
        right_frame.columnconfigure(1, weight=1)

    def toggle_sf(self):
        if self.controller.sf_enabled_var.get():
            self.sf_entry.configure(state="normal")
        else:
            self.sf_entry.configure(state="disabled")

    def _reset_inputs(self):
        self.controller.duct_diameter_in_var.set("6.0")
        self.controller.air_flow_cfm_var.set("1000")
        self.controller.duct_length_ft_var.set("10")
        self.controller.bend_45_count_var.set("0")
        self.controller.bend_90_count_var.set("0")
        self.controller.bend_180_count_var.set("0")
        self.controller.roughness_choice_var.set("Medium (0.009)")
        self.controller.compression_percent_var.set(0.0)
        self.controller.safety_factor_var.set("10")
        self.controller.sf_enabled_var.set(False)
        self.controller.result_air_velocity_var.set("—")
        self.controller.result_pressure_loss_var.set("—")
        self.controller.status_var.set("Inputs reset to default values")
