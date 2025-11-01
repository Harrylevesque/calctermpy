"""
Theme customizer dialog for the calculator
"""

from ..core.imports import *


class ThemeCustomizer(QDialog):
    """Dialog for customizing themes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Theme Customizer")
        self.setModal(True)
        self.resize(500, 600)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Preset themes
        layout.addWidget(QLabel("Preset Themes:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "Dark (VS Code)", "Light", "Monokai", "Solarized Dark", 
            "Solarized Light", "GitHub", "Custom"
        ])
        layout.addWidget(self.theme_combo)
        
        # Custom colors section
        colors_group = QGroupBox("Custom Colors")
        colors_layout = QFormLayout(colors_group)
        
        self.bg_color_btn = QPushButton("Background")
        self.text_color_btn = QPushButton("Text")
        self.keyword_color_btn = QPushButton("Keywords")
        self.string_color_btn = QPushButton("Strings")
        self.comment_color_btn = QPushButton("Comments")
        self.number_color_btn = QPushButton("Numbers")
        
        colors_layout.addRow("Background:", self.bg_color_btn)
        colors_layout.addRow("Text:", self.text_color_btn)
        colors_layout.addRow("Keywords:", self.keyword_color_btn)
        colors_layout.addRow("Strings:", self.string_color_btn)
        colors_layout.addRow("Comments:", self.comment_color_btn)
        colors_layout.addRow("Numbers:", self.number_color_btn)
        
        layout.addWidget(colors_group)
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout(font_group)
        
        self.font_btn = QPushButton("Choose Font")
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(12)
        
        font_layout.addRow("Font:", self.font_btn)
        font_layout.addRow("Size:", self.font_size_spin)
        
        layout.addWidget(font_group)
        
        # Preview
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_text = QTextEdit()
        self.preview_text.setPlainText(
            "# Sample Python code\n"
            "import math\n"
            "x = 5\n"
            "y = math.sin(x) * 2.5\n"
            "print(f'Result: {y}')"
        )
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Apply
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply_theme)
        layout.addWidget(buttons)
        
        # Connect signals
        self.theme_combo.currentTextChanged.connect(self.load_preset_theme)
        self.bg_color_btn.clicked.connect(lambda: self.choose_color('bg'))
        self.text_color_btn.clicked.connect(lambda: self.choose_color('text'))
        self.keyword_color_btn.clicked.connect(lambda: self.choose_color('keyword'))
        self.string_color_btn.clicked.connect(lambda: self.choose_color('string'))
        self.comment_color_btn.clicked.connect(lambda: self.choose_color('comment'))
        self.number_color_btn.clicked.connect(lambda: self.choose_color('number'))
        self.font_btn.clicked.connect(self.choose_font)
        
        # Initialize colors
        self.colors = {
            'bg': QColor(30, 30, 30),
            'text': QColor(212, 212, 212),
            'keyword': QColor(86, 156, 214),
            'string': QColor(206, 145, 120),
            'comment': QColor(106, 153, 85),
            'number': QColor(181, 206, 168)
        }
        
        # Initialize font - use system default if Consolas is not available
        self.current_font = QFont("Consolas", 12)
        if not self.current_font.exactMatch():
            self.current_font = QFont("Monaco", 12)  # macOS monospace font
            if not self.current_font.exactMatch():
                self.current_font = QFont("monospace", 12)  # fallback
        
        # Set initial font size in spinner
        self.font_size_spin.setValue(self.current_font.pointSize())
        
        # Connect font size spinner
        self.font_size_spin.valueChanged.connect(self.update_preview)
        
        # Initial preview update
        self.update_preview()
        
    def load_preset_theme(self, theme_name):
        """Load a preset theme"""
        if theme_name == "Dark (VS Code)":
            self.colors.update({
                'bg': QColor(30, 30, 30),
                'text': QColor(212, 212, 212),
                'keyword': QColor(86, 156, 214),
                'string': QColor(206, 145, 120),
                'comment': QColor(106, 153, 85),
                'number': QColor(181, 206, 168)
            })
        elif theme_name == "Light":
            self.colors.update({
                'bg': QColor(255, 255, 255),
                'text': QColor(0, 0, 0),
                'keyword': QColor(0, 0, 255),
                'string': QColor(0, 128, 0),
                'comment': QColor(128, 128, 128),
                'number': QColor(139, 0, 0)
            })
        elif theme_name == "Monokai":
            self.colors.update({
                'bg': QColor(39, 40, 34),
                'text': QColor(248, 248, 242),
                'keyword': QColor(249, 38, 114),
                'string': QColor(230, 219, 116),
                'comment': QColor(117, 113, 94),
                'number': QColor(174, 129, 255)
            })
        # Add more presets as needed
        
        self.update_preview()
    
    def choose_color(self, color_type):
        """Choose a color for a specific element"""
        color = QColorDialog.getColor(self.colors[color_type], self)
        if color.isValid():
            self.colors[color_type] = color
            self.update_preview()
    
    def choose_font(self):
        """Choose font"""
        try:
            font, ok = QFontDialog.getFont(self.current_font, self)
            if ok and isinstance(font, QFont):
                self.current_font = font
                self.font_size_spin.setValue(font.pointSize())
                self.update_preview()
        except Exception as e:
            print(f"Error choosing font: {e}")
            # Fallback to default font
            self.current_font = QFont("Monaco", 12)
    
    def update_preview(self):
        """Update the preview text styling"""
        try:
            if isinstance(self.current_font, QFont):
                font_family = self.current_font.family()
                font_size = self.font_size_spin.value()
            else:
                # Fallback font
                self.current_font = QFont("Monaco", 12)
                font_family = self.current_font.family()
                font_size = 12
                
            self.preview_text.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {self.colors['bg'].name()};
                    color: {self.colors['text'].name()};
                    font-family: {font_family};
                    font-size: {font_size}pt;
                }}
            """)
        except Exception as e:
            print(f"Error updating preview: {e}")
    
    def apply_theme(self):
        """Apply theme to parent"""
        if hasattr(self.parent(), 'apply_custom_theme'):
            # Ensure we have a valid font
            if not isinstance(self.current_font, QFont):
                self.current_font = QFont("Monaco", 12)
                
            theme_data = {
                'colors': self.colors,
                'font': self.current_font,
                'font_size': self.font_size_spin.value()
            }
            self.parent().apply_custom_theme(theme_data)
