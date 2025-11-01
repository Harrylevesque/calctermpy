"""
Code editor with line numbers and inline results
"""

from ..core.imports import *


class LineNumberArea(QWidget):
    """Widget for displaying line numbers"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.code_editor = editor
        
    def sizeHint(self):
        return QSize(self.code_editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.code_editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    """Custom text editor with line numbers and inline results"""
    
    def __init__(self):
        super().__init__()
        self.line_number_area = LineNumberArea(self)
        self.line_results = {}  # Store results for each line
        
        # Connect signals
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        
        # Set initial width
        self.update_line_number_area_width(0)
        
        # Setup fonts and margins
        font = QFont("Consolas", 12)
        self.setFont(font)
        
    def line_number_area_width(self):
        """Calculate width needed for line number area"""
        digits = 1
        max_block = max(1, self.blockCount())
        while max_block >= 10:
            max_block //= 10
            digits += 1
        
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, new_block_count):
        """Update the viewport margins for line numbers"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """Update the line number area when scrolling"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """Handle resize events"""
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
    
    def line_number_area_paint_event(self, event):
        """Paint the line numbers"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(240, 240, 240))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        height = self.fontMetrics().height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QColor(120, 120, 120))
                painter.drawText(0, int(top), self.line_number_area.width() - 5, height,
                               Qt.AlignmentFlag.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def paintEvent(self, event):
        """Custom paint event to draw inline results"""
        super().paintEvent(event)
        
        # Draw inline results
        painter = QPainter(self.viewport())
        painter.setPen(QColor(0, 150, 0))  # Green for results
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        height = self.fontMetrics().height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                # Draw inline result if available
                if block_number + 1 in self.line_results:
                    result = self.line_results[block_number + 1]
                    result_text = f" = {result}"
                    
                    # Calculate position at end of line text
                    text_width = self.fontMetrics().horizontalAdvance(block.text())
                    result_x = text_width + 20  # Add some padding
                    
                    # Make sure it fits in the viewport
                    if result_x < self.viewport().width() - 200:
                        painter.drawText(int(result_x), int(top + height - 3), result_text)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def set_line_result(self, line_number, result):
        """Set the result for a specific line"""
        self.line_results[line_number] = result
        self.update()  # Trigger repaint
    
    def clear_line_results(self):
        """Clear all inline results"""
        self.line_results.clear()
        self.update()
