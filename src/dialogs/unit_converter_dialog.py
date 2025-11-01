"""
Unit converter dialog for the calculator
"""

from ..core.imports import *


class UnitConverterDialog(QDialog):
    """Dialog for unit conversions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Unit Converter")
        self.setModal(True)
        self.resize(400, 300)
        self.setup_ui()
        self.setup_conversions()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Category selection
        self.category_combo = QComboBox()
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_combo)
        
        # From/To selection
        from_layout = QHBoxLayout()
        self.from_combo = QComboBox()
        self.from_value = QLineEdit("1")
        from_layout.addWidget(QLabel("From:"))
        from_layout.addWidget(self.from_combo)
        from_layout.addWidget(self.from_value)
        layout.addLayout(from_layout)
        
        to_layout = QHBoxLayout()
        self.to_combo = QComboBox()
        self.to_value = QLineEdit()
        self.to_value.setReadOnly(True)
        to_layout.addWidget(QLabel("To:"))
        to_layout.addWidget(self.to_combo)
        to_layout.addWidget(self.to_value)
        layout.addLayout(to_layout)
        
        # Convert button
        self.convert_btn = QPushButton("Convert")
        self.convert_btn.clicked.connect(self.convert)
        layout.addWidget(self.convert_btn)
        
        # Insert button
        self.insert_btn = QPushButton("Insert Result")
        self.insert_btn.clicked.connect(self.insert_result)
        layout.addWidget(self.insert_btn)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        # Connect signals
        self.category_combo.currentTextChanged.connect(self.update_units)
        self.from_value.textChanged.connect(self.convert)
        self.from_combo.currentTextChanged.connect(self.convert)
        self.to_combo.currentTextChanged.connect(self.convert)
        
    def setup_conversions(self):
        """Setup conversion factors"""
        self.conversions = {
            "Length": {
                "meter": 1.0,
                "kilometer": 1000.0,
                "centimeter": 0.01,
                "millimeter": 0.001,
                "inch": 0.0254,
                "foot": 0.3048,
                "yard": 0.9144,
                "mile": 1609.344,
            },
            "Mass": {
                "kilogram": 1.0,
                "gram": 0.001,
                "pound": 0.453592,
                "ounce": 0.0283495,
                "ton": 1000.0,
            },
            "Temperature": {
                "celsius": 1.0,
                "fahrenheit": 1.0,
                "kelvin": 1.0,
            },
            "Area": {
                "square_meter": 1.0,
                "square_kilometer": 1000000.0,
                "square_centimeter": 0.0001,
                "square_inch": 0.00064516,
                "square_foot": 0.092903,
                "acre": 4046.86,
            },
            "Volume": {
                "liter": 1.0,
                "milliliter": 0.001,
                "gallon": 3.78541,
                "quart": 0.946353,
                "pint": 0.473176,
                "cup": 0.236588,
                "fluid_ounce": 0.0295735,
            }
        }
        
        # Populate category combo
        self.category_combo.addItems(list(self.conversions.keys()))
        self.update_units()
        
    def update_units(self):
        """Update unit combos based on selected category"""
        category = self.category_combo.currentText()
        if category in self.conversions:
            units = list(self.conversions[category].keys())
            
            self.from_combo.clear()
            self.to_combo.clear()
            
            self.from_combo.addItems(units)
            self.to_combo.addItems(units)
            
            if len(units) > 1:
                self.to_combo.setCurrentIndex(1)
    
    def convert(self):
        """Perform the conversion"""
        try:
            value = float(self.from_value.text())
            category = self.category_combo.currentText()
            from_unit = self.from_combo.currentText()
            to_unit = self.to_combo.currentText()
            
            if category == "Temperature":
                result = self.convert_temperature(value, from_unit, to_unit)
            elif category in self.conversions:
                from_factor = self.conversions[category][from_unit]
                to_factor = self.conversions[category][to_unit]
                result = value * from_factor / to_factor
            else:
                result = value
            
            self.to_value.setText(f"{result:.6g}")
            
        except (ValueError, KeyError):
            self.to_value.setText("Error")
    
    def convert_temperature(self, value, from_unit, to_unit):
        """Convert temperature units"""
        # Convert to Celsius first
        if from_unit == "fahrenheit":
            celsius = (value - 32) * 5/9
        elif from_unit == "kelvin":
            celsius = value - 273.15
        else:  # celsius
            celsius = value
            
        # Convert from Celsius to target
        if to_unit == "fahrenheit":
            return celsius * 9/5 + 32
        elif to_unit == "kelvin":
            return celsius + 273.15
        else:  # celsius
            return celsius
    
    def insert_result(self):
        """Insert conversion result into main editor"""
        if hasattr(self.parent(), 'insert_conversion_result'):
            result = self.to_value.text()
            if result and result != "Error":
                self.parent().insert_conversion_result(result)
