"""
Variable inspector panel for the calculator
"""

from ..core.imports import *


class VariableInspector(QWidget):
    """Widget for inspecting and managing variables"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Variable Inspector"))
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_variables)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Variables tree
        self.variables_tree = QTreeWidget()
        self.variables_tree.setHeaderLabels(["Name", "Type", "Value"])
        self.variables_tree.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.variables_tree)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.delete_btn = QPushButton("Delete Selected")
        self.edit_btn = QPushButton("Edit Value")
        self.copy_btn = QPushButton("Copy Name")
        
        self.delete_btn.clicked.connect(self.delete_variable)
        self.edit_btn.clicked.connect(self.edit_variable)
        self.copy_btn.clicked.connect(self.copy_variable_name)
        
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.copy_btn)
        
        layout.addLayout(btn_layout)
    
    def update_variables(self, variables):
        """Update the variables display"""
        self.variables_tree.clear()
        
        for name, value in variables.items():
            item = QTreeWidgetItem([
                name,
                type(value).__name__,
                str(value)[:100] + ("..." if len(str(value)) > 100 else "")
            ])
            self.variables_tree.addTopLevelItem(item)
    
    def refresh_variables(self):
        """Refresh variables from parent"""
        if hasattr(self.parent(), 'get_current_variables'):
            variables = self.parent().get_current_variables()
            self.update_variables(variables)
    
    def delete_variable(self):
        """Delete selected variable"""
        current_item = self.variables_tree.currentItem()
        if current_item and hasattr(self.parent(), 'delete_variable'):
            var_name = current_item.text(0)
            self.parent().delete_variable(var_name)
            self.refresh_variables()
    
    def edit_variable(self):
        """Edit selected variable value"""
        current_item = self.variables_tree.currentItem()
        if current_item and hasattr(self.parent(), 'edit_variable'):
            var_name = current_item.text(0)
            current_value = current_item.text(2)
            
            new_value, ok = QLineEdit().text(), True  # Simplified for now
            if ok and hasattr(self.parent(), 'edit_variable'):
                self.parent().edit_variable(var_name, new_value)
                self.refresh_variables()
    
    def copy_variable_name(self):
        """Copy variable name to clipboard"""
        current_item = self.variables_tree.currentItem()
        if current_item:
            var_name = current_item.text(0)
            QApplication.clipboard().setText(var_name)
