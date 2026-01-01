# HVAC Duct Calculator v1.4

A **Python-based GUI application** for calculating air velocity and pressure loss in HVAC duct systems, supporting **flexible and rectangular duct calculations** (rectangular duct is a placeholder for future implementation).  

This project uses **Tkinter** for the GUI and performs **precise engineering calculations** for duct systems.

---

## Table of Contents

- [Features](#features)
- [Folder Structure](#folder-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Assets](#assets)
- [Requirements](#requirements)
- [Credits](#credits)

---

## Features

- Flexible duct calculation
- Interactive GUI with Tkinter
- Input validation for all fields
- Real-time calculation of:
  - Air velocity (FPM)
  - Total pressure loss (in.w.g.)
  - Intermediate calculation details
- Safety factor customization
- Full results popup for detailed analysis
- Multi-page interface: Home, Flexible Duct Calculator, Credits

---

## Folder Structure

HVAC_Project/
│
├─ app.py # Main entry point
├─ assets/ # Images and media files
│ ├─ flexduct.png
│ └─ recduct.png
├─ core/ # Core calculation logic
│ └─ calculations.py
├─ ui/ # GUI pages and main app
│ ├─ app_root.py
│ ├─ home_page.py
│ ├─ flexible_duct_page.py
│ └─ credits_page.py
└─ utils/ # Utility modules
└─ resource_path.py # Handles resource paths for dev and PyInstaller

yaml
Copy code

---

## Installation

1. Make sure **Python 3.14** (or compatible) is installed.
2. Install required packages:

```bash
python -m pip install --upgrade pip
python -m pip install pillow
Place the assets/ folder in the project root, containing:

flexduct.png

recduct.png

Usage
Run the application:

bash
Copy code
python app.py
The Home Page lets you select calculators.

Flexible Duct Calculator allows you to input:

Duct diameter (in)

Air flow (CFM)

Duct length (ft)

Number of bends (45°, 90°, 180°)

Duct roughness

Compression factor (%)

Safety factor (%) (optional)

Click Calculate to see results.

Click See Full Results for detailed calculation breakdown.

Use Reset Inputs to restore default values.

How it Works
Gather Inputs: The app collects user input from Tkinter entry fields.

Validation: Positive numbers are enforced.

Core Calculation:
Uses core/calculations.py:

Converts duct diameter to feet

Calculates duct area and air velocity

Calculates Reynolds number

Estimates friction factor

Calculates equivalent length from bends

Computes raw pressure loss, compression factor, and safety factor

Returns final air velocity and total ΔP

Display: Updates results in the GUI in real-time and shows full details in a popup.

Assets
flexduct.png: Image representing flexible duct

recduct.png: Image representing rectangular duct (currently placeholder)

Requirements
Python 3.14+

Tkinter (included with Python)

Pillow (pip install pillow)

Credits
Developed by: Eng. Bashar

Email: basharwmn@gmail.com

All rights reserved ©