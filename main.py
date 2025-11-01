"""
Main entry point for the calculator application
"""

import sys
from src.core.imports import *


def launch_app():
    """Launch the calculator GUI application."""
    try:
        print("Starting Advanced Scientific Calculator...")
        app = QApplication(sys.argv)
        app.setApplicationName("Advanced Scientific Calculator")
        app.setApplicationVersion("2.0")
        app.setOrganizationName("Scientific Calculator")
        print("QApplication created successfully")

        # Import the main calculator class
        from src.core.calculator import ScientificCalculator
        
        print("Creating main window...")
        main_win = ScientificCalculator()
        print("Main window created successfully")
        
        main_win.show()
        print("Main window shown, starting event loop...")

        # Start the event loop
        result = app.exec()
        print(f"Event loop finished with result: {result}")
        sys.exit(result)
        
    except Exception as e:
        print(f"Error launching application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    launch_app()
