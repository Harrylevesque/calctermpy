"""
Python syntax highlighter for the code editor
"""

from ..core.imports import *


class PythonSyntaxHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter with VS Code-like colors"""
    
    def __init__(self, document: QTextDocument):
        super().__init__(document)
        self.setup_highlighting_rules()
    
    def setup_highlighting_rules(self):
        """Setup the highlighting rules for Python syntax"""
        self.highlighting_rules = []
        
        # VS Code-like color scheme
        # Keywords (purple/magenta)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(86, 156, 214))  # Light blue
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Built-in functions (yellow)
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(220, 220, 170))  # Light yellow
        
        builtins = [
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'enumerate', 'eval', 'exec', 'filter', 'float', 'format',
            'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
            'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
            'iter', 'len', 'list', 'locals', 'map', 'max', 'min',
            'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
            'range', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'str', 'sum', 'super', 'tuple', 'type',
            'vars', 'zip'
        ]
        
        for builtin in builtins:
            pattern = QRegularExpression(f'\\b{builtin}\\b')
            self.highlighting_rules.append((pattern, builtin_format))
        
        # Numbers (light green)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(181, 206, 168))  # Light green
        
        # Integer and float patterns
        number_pattern = QRegularExpression(r'\b\d+\.?\d*([eE][+-]?\d+)?\b')
        self.highlighting_rules.append((number_pattern, number_format))
        
        # Hex, oct, bin numbers
        hex_pattern = QRegularExpression(r'\b0[xX][0-9a-fA-F]+\b')
        self.highlighting_rules.append((hex_pattern, number_format))
        
        oct_pattern = QRegularExpression(r'\b0[oO][0-7]+\b')
        self.highlighting_rules.append((oct_pattern, number_format))
        
        bin_pattern = QRegularExpression(r'\b0[bB][01]+\b')
        self.highlighting_rules.append((bin_pattern, number_format))
        
        # Strings (orange/salmon)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(206, 145, 120))  # Orange/salmon
        
        # Single quoted strings
        single_quote_pattern = QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        self.highlighting_rules.append((single_quote_pattern, string_format))
        
        # Double quoted strings
        double_quote_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.highlighting_rules.append((double_quote_pattern, string_format))
        
        # Triple quoted strings (multiline)
        triple_quote_format = QTextCharFormat()
        triple_quote_format.setForeground(QColor(206, 145, 120))  # Orange/salmon
        triple_single_pattern = QRegularExpression(r"'''.*?'''", QRegularExpression.PatternOption.DotMatchesEverythingOption)
        triple_double_pattern = QRegularExpression(r'""".*?"""', QRegularExpression.PatternOption.DotMatchesEverythingOption)
        self.highlighting_rules.append((triple_single_pattern, triple_quote_format))
        self.highlighting_rules.append((triple_double_pattern, triple_quote_format))
        
        # Comments (green)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(106, 153, 85))  # Green
        comment_format.setFontItalic(True)
        
        comment_pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((comment_pattern, comment_format))
        
        # Function definitions (yellow)
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(220, 220, 170))  # Light yellow
        function_format.setFontWeight(QFont.Weight.Bold)
        
        function_pattern = QRegularExpression(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((function_pattern, function_format))
        
        # Class definitions (light blue)
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(78, 201, 176))  # Cyan/turquoise
        class_format.setFontWeight(QFont.Weight.Bold)
        
        class_pattern = QRegularExpression(r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((class_pattern, class_format))
        
        # Mathematical module names (light purple)
        module_format = QTextCharFormat()
        module_format.setForeground(QColor(156, 220, 254))  # Light blue
        module_format.setFontWeight(QFont.Weight.Bold)
        
        math_modules = ['math', 'np', 'numpy', 'sp', 'scipy', 'sym', 'sympy']
        for module in math_modules:
            pattern = QRegularExpression(f'\\b{module}\\.')
            self.highlighting_rules.append((pattern, module_format))
        
        # Operators (white/light gray)
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(212, 212, 212))  # Light gray
        
        operators = [
            '=', '==', '!=', '<', '<=', '>', '>=',
            '\\+', '-', '\\*', '/', '//', '%', '\\*\\*',
            '\\+=', '-=', '\\*=', '/=', '//=', '%=', '\\*\\*=',
            '&', '\\|', '\\^', '~', '<<', '>>', '&=', '\\|=', '\\^=',
            '<<=', '>>=', 'and', 'or', 'not', 'in', 'is'
        ]
        
        for op in operators:
            pattern = QRegularExpression(f'\\s*{op}\\s*')
            self.highlighting_rules.append((pattern, operator_format))
        
        # Parentheses, brackets, braces (light gray)
        bracket_format = QTextCharFormat()
        bracket_format.setForeground(QColor(255, 215, 0))  # Gold
        bracket_format.setFontWeight(QFont.Weight.Bold)
        
        bracket_pattern = QRegularExpression(r'[\(\)\[\]\{\}]')
        self.highlighting_rules.append((bracket_pattern, bracket_format))
        
        # Self keyword (purple)
        self_format = QTextCharFormat()
        self_format.setForeground(QColor(86, 156, 214))  # Light blue
        self_format.setFontWeight(QFont.Weight.Bold)
        
        self_pattern = QRegularExpression(r'\bself\b')
        self.highlighting_rules.append((self_pattern, self_format))
    
    def setup_light_theme(self):
        """Setup highlighting rules for light theme"""
        self.highlighting_rules = []
        
        # Light theme colors (darker colors for better visibility on light background)
        # Keywords (dark blue)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(0, 0, 255))  # Blue
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Built-in functions (dark orange)
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(128, 0, 128))  # Purple
        
        builtins = [
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'enumerate', 'eval', 'exec', 'filter', 'float', 'format',
            'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help',
            'hex', 'id', 'input', 'int', 'isinstance', 'issubclass',
            'iter', 'len', 'list', 'locals', 'map', 'max', 'min',
            'next', 'object', 'oct', 'open', 'ord', 'pow', 'print',
            'range', 'repr', 'reversed', 'round', 'set', 'setattr',
            'slice', 'sorted', 'str', 'sum', 'super', 'tuple', 'type',
            'vars', 'zip'
        ]
        
        for builtin in builtins:
            pattern = QRegularExpression(f'\\b{builtin}\\b')
            self.highlighting_rules.append((pattern, builtin_format))
        
        # Numbers (dark red)
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(139, 0, 0))  # Dark red
        
        number_pattern = QRegularExpression(r'\b\d+\.?\d*([eE][+-]?\d+)?\b')
        self.highlighting_rules.append((number_pattern, number_format))
        
        hex_pattern = QRegularExpression(r'\b0[xX][0-9a-fA-F]+\b')
        self.highlighting_rules.append((hex_pattern, number_format))
        
        oct_pattern = QRegularExpression(r'\b0[oO][0-7]+\b')
        self.highlighting_rules.append((oct_pattern, number_format))
        
        bin_pattern = QRegularExpression(r'\b0[bB][01]+\b')
        self.highlighting_rules.append((bin_pattern, number_format))
        
        # Strings (dark green)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(0, 128, 0))  # Dark green
        
        single_quote_pattern = QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        self.highlighting_rules.append((single_quote_pattern, string_format))
        
        double_quote_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.highlighting_rules.append((double_quote_pattern, string_format))
        
        triple_quote_format = QTextCharFormat()
        triple_quote_format.setForeground(QColor(0, 128, 0))  # Dark green
        triple_single_pattern = QRegularExpression(r"'''.*?'''", QRegularExpression.PatternOption.DotMatchesEverythingOption)
        triple_double_pattern = QRegularExpression(r'""".*?"""', QRegularExpression.PatternOption.DotMatchesEverythingOption)
        self.highlighting_rules.append((triple_single_pattern, triple_quote_format))
        self.highlighting_rules.append((triple_double_pattern, triple_quote_format))
        
        # Comments (gray)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(128, 128, 128))  # Gray
        comment_format.setFontItalic(True)
        
        comment_pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((comment_pattern, comment_format))
        
        # Function definitions (dark blue)
        function_format = QTextCharFormat()
        function_format.setForeground(QColor(0, 0, 139))  # Dark blue
        function_format.setFontWeight(QFont.Weight.Bold)
        
        function_pattern = QRegularExpression(r'\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((function_pattern, function_format))
        
        # Class definitions (dark cyan)
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(0, 139, 139))  # Dark cyan
        class_format.setFontWeight(QFont.Weight.Bold)
        
        class_pattern = QRegularExpression(r'\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)')
        self.highlighting_rules.append((class_pattern, class_format))
        
        # Mathematical module names (dark blue)
        module_format = QTextCharFormat()
        module_format.setForeground(QColor(0, 0, 139))  # Dark blue
        module_format.setFontWeight(QFont.Weight.Bold)
        
        math_modules = ['math', 'np', 'numpy', 'sp', 'scipy', 'sym', 'sympy']
        for module in math_modules:
            pattern = QRegularExpression(f'\\b{module}\\.')
            self.highlighting_rules.append((pattern, module_format))
        
        # Operators (black)
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor(0, 0, 0))  # Black
        
        operators = [
            '=', '==', '!=', '<', '<=', '>', '>=',
            '\\+', '-', '\\*', '/', '//', '%', '\\*\\*',
            '\\+=', '-=', '\\*=', '/=', '//=', '%=', '\\*\\*=',
            '&', '\\|', '\\^', '~', '<<', '>>', '&=', '\\|=', '\\^=',
            '<<=', '>>=', 'and', 'or', 'not', 'in', 'is'
        ]
        
        for op in operators:
            pattern = QRegularExpression(f'\\s*{op}\\s*')
            self.highlighting_rules.append((pattern, operator_format))
        
        # Parentheses, brackets, braces (dark orange)
        bracket_format = QTextCharFormat()
        bracket_format.setForeground(QColor(255, 140, 0))  # Dark orange
        bracket_format.setFontWeight(QFont.Weight.Bold)
        
        bracket_pattern = QRegularExpression(r'[\(\)\[\]\{\}]')
        self.highlighting_rules.append((bracket_pattern, bracket_format))
        
        # Self keyword (blue)
        self_format = QTextCharFormat()
        self_format.setForeground(QColor(0, 0, 255))  # Blue
        self_format.setFontWeight(QFont.Weight.Bold)
        
        self_pattern = QRegularExpression(r'\bself\b')
        self.highlighting_rules.append((self_pattern, self_format))
    
    def setup_custom_theme(self, colors):
        """Setup highlighting rules with custom colors"""
        self.highlighting_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(colors['keyword'])
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        keywords = [
            'and', 'as', 'assert', 'break', 'class', 'continue', 'def',
            'del', 'elif', 'else', 'except', 'exec', 'finally', 'for',
            'from', 'global', 'if', 'import', 'in', 'is', 'lambda',
            'not', 'or', 'pass', 'print', 'raise', 'return', 'try',
            'while', 'with', 'yield', 'True', 'False', 'None'
        ]
        
        for keyword in keywords:
            pattern = QRegularExpression(f'\\b{keyword}\\b')
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(colors['number'])
        
        number_pattern = QRegularExpression(r'\b\d+\.?\d*([eE][+-]?\d+)?\b')
        self.highlighting_rules.append((number_pattern, number_format))
        
        # Strings
        string_format = QTextCharFormat()
        string_format.setForeground(colors['string'])
        
        single_quote_pattern = QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'")
        self.highlighting_rules.append((single_quote_pattern, string_format))
        
        double_quote_pattern = QRegularExpression(r'"[^"\\]*(\\.[^"\\]*)*"')
        self.highlighting_rules.append((double_quote_pattern, string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(colors['comment'])
        comment_format.setFontItalic(True)
        
        comment_pattern = QRegularExpression(r'#.*$')
        self.highlighting_rules.append((comment_pattern, comment_format))
        
        # Rehighlight the document
        self.rehighlight()
    
    def highlightBlock(self, text):
        """Apply syntax highlighting to a block of text"""
        # Apply all highlighting rules
        for pattern, format in self.highlighting_rules:
            expression = pattern
            match_iterator = expression.globalMatch(text)
            
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
