"""
History panel for the calculator
"""

from ..core.imports import *


class HistoryPanel(QWidget):
    """Widget for displaying calculation history"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_calculator = parent
        self.setup_ui()
        self.history = []
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Header
        header_label = QLabel("Calculation History")
        header_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(header_label)
        
        # History list
        self.history_list = QListWidget()
        self.history_list.itemDoubleClicked.connect(self.restore_calculation)
        layout.addWidget(self.history_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear History")
        clear_btn.clicked.connect(self.clear_history)
        
        export_btn = QPushButton("Export")
        export_btn.clicked.connect(self.export_history)
        
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
    
    def add_calculation(self, expression, result):
        """Add a calculation to the history"""
        timestamp = QTimer().remainingTime()  # Simple timestamp
        history_item = {
            'expression': expression,
            'result': result,
            'timestamp': timestamp
        }
        
        self.history.append(history_item)
        
        # Update list widget
        display_text = f"{expression} = {result}"
        if len(display_text) > 60:
            display_text = display_text[:57] + "..."
            
        list_item = QListWidgetItem(display_text)
        list_item.setData(Qt.ItemDataRole.UserRole, history_item)
        self.history_list.addItem(list_item)
        
        # Keep only last 100 items
        if self.history_list.count() > 100:
            self.history_list.takeItem(0)
            self.history.pop(0)
    
    def restore_calculation(self, item):
        """Restore a calculation from history to the current editor"""
        history_item = item.data(Qt.ItemDataRole.UserRole)
        if history_item and self.parent_calculator:
            self.parent_calculator.restore_from_history(history_item['expression'])
    
    def clear_history(self):
        """Clear all history"""
        self.history.clear()
        self.history_list.clear()
    
    def export_history(self):
        """Export history to a text file"""
        if not self.history:
            QMessageBox.information(self, "Export History", "No calculations to export.")
            return
            
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export History", "calculation_history.txt", "Text Files (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("Calculator History\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for item in self.history:
                        f.write(f"{item['expression']} = {item['result']}\n")
                
                QMessageBox.information(self, "Export Complete", f"History exported to {filename}")
                
            except Exception as e:
                QMessageBox.warning(self, "Export Error", f"Failed to export history: {e}")
