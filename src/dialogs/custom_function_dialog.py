"""
Custom function dialog for adding/editing functions
"""

from ..core.imports import *


class CustomFunctionDialog(QDialog):
    """Dialog for adding/editing custom functions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Function")
        self.setModal(True)
        self.resize(500, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Form
        form_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Function name (e.g., my_func)")
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Description (optional)")
        
        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("def my_func(x):\n    return x**2 + 1")
        
        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Description:", self.desc_input)
        form_layout.addRow("Code:", self.code_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
