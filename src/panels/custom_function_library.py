"""
Custom function library panel for the calculator
"""

from ..core.imports import *
from datetime import datetime
from ..dialogs.custom_function_dialog import CustomFunctionDialog


class CustomFunctionLibrary(QWidget):
    """Widget for managing custom functions"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.functions = {}
        self.load_functions()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Custom Functions"))
        
        self.add_function_btn = QPushButton("Add Function")
        self.add_function_btn.clicked.connect(self.add_function)
        header_layout.addWidget(self.add_function_btn)
        
        layout.addLayout(header_layout)
        
        # Functions list
        self.functions_list = QListWidget()
        self.functions_list.itemDoubleClicked.connect(self.insert_function)
        layout.addWidget(self.functions_list)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.edit_btn = QPushButton("Edit")
        self.delete_btn = QPushButton("Delete")
        self.insert_btn = QPushButton("Insert")
        
        self.edit_btn.clicked.connect(self.edit_function)
        self.delete_btn.clicked.connect(self.delete_function)
        self.insert_btn.clicked.connect(self.insert_selected_function)
        
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.insert_btn)
        
        layout.addLayout(btn_layout)
        
    def load_functions(self):
        """Load custom functions from configuration"""
        if hasattr(self.parent(), 'config_manager'):
            self.functions = self.parent().config_manager.load_custom_functions()
            self.refresh_list()
    
    def save_functions(self):
        """Save custom functions to configuration"""
        if hasattr(self.parent(), 'config_manager'):
            self.parent().config_manager.save_custom_functions(self.functions)
        
    def add_function(self):
        """Add a new custom function"""
        from ..dialogs.custom_function_dialog import CustomFunctionDialog
        dialog = CustomFunctionDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.name_input.text().strip()
            code = dialog.code_input.toPlainText().strip()
            description = dialog.desc_input.text().strip()
            
            if name and code:
                self.functions[name] = {
                    'code': code, 
                    'description': description,
                    'created': datetime.now().isoformat(),
                    'modified': datetime.now().isoformat()
                }
                self.refresh_list()
                self.save_functions()
    
    def edit_function(self):
        """Edit selected function"""
        current_item = self.functions_list.currentItem()
        if current_item:
            name = current_item.text().split(' - ')[0]
            if name in self.functions:
                from ..dialogs.custom_function_dialog import CustomFunctionDialog
                dialog = CustomFunctionDialog(self)
                dialog.name_input.setText(name)
                dialog.code_input.setPlainText(self.functions[name]['code'])
                dialog.desc_input.setText(self.functions[name]['description'])
                
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    new_name = dialog.name_input.text().strip()
                    code = dialog.code_input.toPlainText().strip()
                    description = dialog.desc_input.text().strip()
                    
                    if new_name and code:
                        if new_name != name:
                            del self.functions[name]
                        self.functions[new_name] = {
                            'code': code, 
                            'description': description,
                            'created': self.functions.get(name, {}).get('created', datetime.now().isoformat()),
                            'modified': datetime.now().isoformat()
                        }
                        self.refresh_list()
                        self.save_functions()
    
    def delete_function(self):
        """Delete selected function"""
        current_item = self.functions_list.currentItem()
        if current_item:
            name = current_item.text().split(' - ')[0]
            if name in self.functions:
                reply = QMessageBox.question(
                    self, "Delete Function",
                    f"Are you sure you want to delete the function '{name}'?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    del self.functions[name]
                    self.refresh_list()
                    self.save_functions()
    
    def insert_selected_function(self):
        """Insert selected function into editor"""
        current_item = self.functions_list.currentItem()
        if current_item:
            name = current_item.text().split(' - ')[0]
            self.insert_function(current_item)
    
    def insert_function(self, item):
        """Insert function into the main editor"""
        name = item.text().split(' - ')[0]
        if name in self.functions and hasattr(self.parent(), 'insert_custom_function'):
            self.parent().insert_custom_function(name, self.functions[name]['code'])
    
    def refresh_list(self):
        """Refresh the functions list"""
        self.functions_list.clear()
        for name, func_data in self.functions.items():
            desc = func_data.get('description', '')
            display_text = f"{name} - {desc}" if desc else name
            item = QListWidgetItem(display_text)
            
            # Add tooltip with function details
            tooltip = f"Name: {name}\n"
            if desc:
                tooltip += f"Description: {desc}\n"
            tooltip += f"Created: {func_data.get('created', 'Unknown')}\n"
            tooltip += f"Modified: {func_data.get('modified', 'Unknown')}\n"
            tooltip += f"Code:\n{func_data.get('code', '')}"
            item.setToolTip(tooltip)
            
            self.functions_list.addItem(item)
