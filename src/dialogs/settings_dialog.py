"""
Settings dialog for the calculator
"""

from ..core.imports import *


class SettingsDialog(QDialog):
    """Dialog for customizing text appearance and calculator settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator Settings")
        self.setModal(True)
        self.resize(400, 350)
        self.setup_ui()
        
        # Initialize values
        self.current_font = QFont("Consolas", 12)
        self.text_color = QColor(0, 0, 0)
        self.bg_color = QColor(255, 255, 255)
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Create form layout
        form_layout = QFormLayout()
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout(font_group)
        
        self.font_btn = QPushButton("Choose Font")
        self.font_btn.clicked.connect(self.choose_font)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(12)
        
        font_layout.addRow("Font:", self.font_btn)
        font_layout.addRow("Font Size:", self.font_size_spin)
        
        layout.addWidget(font_group)
        
        # Color settings
        color_group = QGroupBox("Color Settings")
        color_layout = QFormLayout(color_group)
        
        self.text_color_btn = QPushButton("Text Color")
        self.text_color_btn.clicked.connect(self.choose_text_color)
        
        self.bg_color_btn = QPushButton("Background Color")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        
        color_layout.addRow("Text:", self.text_color_btn)
        color_layout.addRow("Background:", self.bg_color_btn)
        
        layout.addWidget(color_group)
        
        # Other settings
        other_group = QGroupBox("Other Settings")
        other_layout = QFormLayout(other_group)
        
        self.precision_spin = QSpinBox()
        self.precision_spin.setRange(1, 15)
        self.precision_spin.setValue(6)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark", "Light"])
        
        other_layout.addRow("Decimal Precision:", self.precision_spin)
        other_layout.addRow("Theme:", self.theme_combo)
        
        layout.addWidget(other_group)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def choose_font(self):
        font, ok = QFontDialog.getFont(self.current_font, self)
        if ok:
            self.current_font = font
            self.font_size_spin.setValue(font.pointSize())
            
    def choose_text_color(self):
        color = QColorDialog.getColor(self.text_color, self)
        if color.isValid():
            self.text_color = color
            
    def choose_bg_color(self):
        color = QColorDialog.getColor(self.bg_color, self)
        if color.isValid():
            self.bg_color = color
