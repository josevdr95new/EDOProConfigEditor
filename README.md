# Configurator GUI ⚙️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

A graphical editor for managing technical configurations, built with Python and Tkinter.

## 🚀 Quick Start

This guide will help you quickly get the Configurator GUI up and running.

## ⚙️ Installation

1.  **Prerequisites:**

    *   Python 3.6+ installed: Download the latest version from [python.org](https://www.python.org/downloads/).
    *   Tkinter:  Tkinter is usually included with Python.  If you encounter issues (particularly on Linux), install it using your system's package manager:

        ```bash
        sudo apt-get install python3-tk
        ```

2.  **Running the application:**

    *   Open a terminal or command prompt.
    *   Navigate to the project directory.  For example:

        ```bash
        cd /path/to/your/project
        ```

    *   Execute the application:

        ```bash
        python run.py
        ```

        or, if you have multiple Python versions installed:

        ```bash
        python3 run.py
        ```

## 💡 Purpose

This application provides a graphical user interface for managing technical configurations. It allows you to define and edit settings for various elements.

*   **Configuration Editor:** Provides a user-friendly GUI for technical settings.

## ✨ Features

*   **Element Management:** Handles four key types of elements:
    1.  **Git Repositories:** Stores names, URLs, and local paths.
    2.  **Resource URLs:**  Categorizes and manages URLs for images, fields, and cover art.
    3.  **Servers:** Defines server addresses, ports, and communication protocols.
    4.  **System Paths:** Manages POSIX-compliant system path configurations.

*   **Key Functionalities:**
    *   **Tabbed Interface:**  Organized interface with tabs for each element type.
    *   **Real-time Translation:** Supports dynamic English/Spanish language switching.
    *   **Automatic Saving:** Configurations are automatically saved to a JSON file.
    *   **Basic Data Validation:** Implements basic validation to ensure data integrity.

## 📖 Usage Examples

The application's user interface is intuitive. Here's a general idea of how to use it:

1.  **Open the application:** Follow the installation and running instructions above.
2.  **Navigate tabs:**  Use the tabs to switch between Git Repositories, Resource URLs, Servers, and System Paths.
3.  **Add/Edit entries:**  Use the provided input fields and buttons to add new entries or modify existing ones.
4.  **Language Switch:** Change the language using the Language selector (if implemented in the UI).

## 🗄️ Data Storage

*   **Configuration File:** `/config/configs.json`
    Stores the application's configuration data.

*   **Language Files:** `/lang/lang_[en|es].json`
    Contains the translation data for English and Spanish.

## 🌐 Offline Functionality

The application does not require an active internet connection to function. It relies on local files for configuration and translation data.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
