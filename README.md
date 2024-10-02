Here’s a `README.md` file for your automatic screenshot application:

---

# Automatic Screenshot App

## Overview
The **Automatic Screenshot App** is a simple Python GUI application built using `Tkinter`, `PyAutoGUI`, and `PIL` (Pillow) for taking periodic screenshots of your screen. You can specify the interval between screenshots, choose a save directory, and optionally blur the screenshots.

## Features
- **Automatic Screenshots**: Take periodic screenshots at a specified interval.
- **Save Directory**: Choose where to save your screenshots.
- **Optional Blur**: Apply a Gaussian blur filter to screenshots if desired.
- **Start/Stop Functionality**: Easily start and stop the screenshot process.

## Requirements
- Python 3.x
- Required Python libraries:
  - `pyautogui`
  - `tkinter`
  - `threading`
  - `Pillow` (PIL)

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd automatic-screenshot-app
   ```

2. **Install required libraries:**
   Install the required Python packages by running:
   ```bash
   pip install pyautogui Pillow
   ```

3. **Run the app:**
   Execute the script:
   ```bash
   python screenshot_app.py
   ```

## Usage
1. **Save Directory**: Enter the directory where screenshots will be saved. If left blank, the current directory will be used.
   
2. **Screenshot Interval**: Specify the interval between screenshots in seconds. The default value is 30 seconds.

3. **Blur Option**: Check the box to apply a blur effect to the screenshots.

4. **Start/Stop Screenshots**: Click the "Start" button to begin capturing screenshots at the specified interval. The button will change to "Stop" to allow stopping the capture process.

5. **Status Information**: The app will display the current status of the screenshot process, including whether the images are blurred and the screenshot interval.

Here’s how you can create a **Screenshots** section using a table format in your `README.md`:

---

Here's an updated version of the **Screenshots** section that includes an additional column for a non-blurred screenshot:

---

## Screenshots

| **Main Interface**                                   | **Blurred Screenshot Option**                           | **Non-Blurred Screenshot**                            |
|------------------------------------------------------|---------------------------------------------------------|-------------------------------------------------------|
| ![Main Interface](public/interface.png)    | ![Blurred Screenshot](public/screenshot.png) | ![Non-Blurred Screenshot](public/screenshotnoblurr.png) |

---




## Known Issues
- Ensure that the save directory exists or will be created if it doesn't already exist.
- The `Stop` functionality will wait for the ongoing screenshot process to complete its current cycle before stopping.

## Future Enhancements
- Add options to select screenshot formats (e.g., PNG, JPG).
- Allow advanced image filters and transformations.
- Add screenshot area selection functionality.