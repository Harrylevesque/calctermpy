"""
Configuration manager for saving and loading application state
"""

import json
import os
from typing import Dict, Any, Optional
from ..core.imports import QSettings, QColor, QFont


class ConfigManager:
    """Manages application configuration and layout persistence"""
    
    def __init__(self, app_name="ScientificCalculator"):
        self.app_name = app_name
        self.settings = QSettings("ScientificCalculator", "Settings")
        self.config_file = os.path.join(os.path.expanduser("~"), f".{app_name.lower()}_config.json")
        
    def save_window_geometry(self, window):
        """Save window geometry and state"""
        self.settings.setValue("geometry", window.saveGeometry())
        self.settings.setValue("windowState", window.saveState())
        
    def restore_window_geometry(self, window):
        """Restore window geometry and state"""
        geometry = self.settings.value("geometry")
        if geometry:
            window.restoreGeometry(geometry)
            
        state = self.settings.value("windowState")
        if state:
            window.restoreState(state)
    
    def save_dock_layout(self, window):
        """Save dock widget layout"""
        dock_config = {}
        
        # Save dock visibility
        dock_widgets = {
            'history': getattr(window, 'history_dock', None),
            'functions': getattr(window, 'functions_dock', None),
            'graph': getattr(window, 'graph_dock', None),
            'variables': getattr(window, 'variables_dock', None)
        }
        
        for name, dock in dock_widgets.items():
            if dock:
                dock_config[name] = {
                    'visible': dock.isVisible(),
                    'floating': dock.isFloating(),
                    'area': int(window.dockWidgetArea(dock)) if not dock.isFloating() else None,
                    'size': [dock.width(), dock.height()]
                }
        
        # Save tabified dock information
        tabified_docks = []
        for name, dock in dock_widgets.items():
            if dock:
                tabified = window.tabifiedDockWidgets(dock)
                if tabified:
                    tab_group = [name] + [self._dock_name_from_widget(d, dock_widgets) for d in tabified]
                    if tab_group not in tabified_docks and len(tab_group) > 1:
                        tabified_docks.append(tab_group)
        
        dock_config['tabified_groups'] = tabified_docks
        
        self.settings.setValue("dockLayout", json.dumps(dock_config))
    
    def restore_dock_layout(self, window):
        """Restore dock widget layout"""
        dock_config_str = self.settings.value("dockLayout")
        if not dock_config_str:
            return
            
        try:
            dock_config = json.loads(dock_config_str)
            
            dock_widgets = {
                'history': getattr(window, 'history_dock', None),
                'functions': getattr(window, 'functions_dock', None),
                'graph': getattr(window, 'graph_dock', None),
                'variables': getattr(window, 'variables_dock', None)
            }
            
            # Restore individual dock properties
            for name, config in dock_config.items():
                if name == 'tabified_groups':
                    continue
                    
                dock = dock_widgets.get(name)
                if dock and isinstance(config, dict):
                    dock.setVisible(config.get('visible', True))
                    dock.setFloating(config.get('floating', False))
                    
                    if not dock.isFloating() and config.get('area') is not None:
                        from ..core.imports import Qt
                        area_map = {
                            1: Qt.DockWidgetArea.LeftDockWidgetArea,
                            2: Qt.DockWidgetArea.RightDockWidgetArea,
                            4: Qt.DockWidgetArea.TopDockWidgetArea,
                            8: Qt.DockWidgetArea.BottomDockWidgetArea
                        }
                        area = area_map.get(config['area'], Qt.DockWidgetArea.LeftDockWidgetArea)
                        window.addDockWidget(area, dock)
                    
                    # Restore size
                    size = config.get('size', [200, 300])
                    dock.resize(size[0], size[1])
            
            # Restore tabified groups
            tabified_groups = dock_config.get('tabified_groups', [])
            for group in tabified_groups:
                if len(group) > 1:
                    first_dock = dock_widgets.get(group[0])
                    for dock_name in group[1:]:
                        dock = dock_widgets.get(dock_name)
                        if first_dock and dock:
                            window.tabifyDockWidget(first_dock, dock)
                            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error restoring dock layout: {e}")
    
    def _dock_name_from_widget(self, widget, dock_widgets):
        """Get dock name from widget"""
        for name, dock in dock_widgets.items():
            if dock == widget:
                return name
        return None
    
    def save_theme_config(self, theme_data):
        """Save theme configuration"""
        config = {}
        
        if 'colors' in theme_data:
            colors = theme_data['colors']
            config['colors'] = {key: color.name() for key, color in colors.items()}
            
        if 'font' in theme_data:
            font = theme_data['font']
            config['font'] = {
                'family': font.family(),
                'size': font.pointSize(),
                'weight': font.weight(),
                'italic': font.italic()
            }
            
        config['font_size'] = theme_data.get('font_size', 12)
        config['theme_name'] = theme_data.get('theme_name', 'Custom')
        
        self.settings.setValue("themeConfig", json.dumps(config))
    
    def load_theme_config(self):
        """Load theme configuration"""
        config_str = self.settings.value("themeConfig")
        if not config_str:
            return None
            
        try:
            config = json.loads(config_str)
            
            # Restore colors
            if 'colors' in config:
                colors = {}
                for key, color_name in config['colors'].items():
                    colors[key] = QColor(color_name)
                config['colors'] = colors
            
            # Restore font
            if 'font' in config:
                font_config = config['font']
                font = QFont(font_config['family'], font_config['size'])
                font.setWeight(font_config.get('weight', QFont.Weight.Normal))
                font.setItalic(font_config.get('italic', False))
                config['font'] = font
                
            return config
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading theme config: {e}")
            return None
    
    def save_editor_config(self, editor_config):
        """Save editor configuration"""
        config = {
            'font_family': editor_config.get('font_family', 'Consolas'),
            'font_size': editor_config.get('font_size', 12),
            'tab_width': editor_config.get('tab_width', 4),
            'line_numbers': editor_config.get('line_numbers', True),
            'word_wrap': editor_config.get('word_wrap', False),
            'highlight_current_line': editor_config.get('highlight_current_line', True),
            'show_whitespace': editor_config.get('show_whitespace', False)
        }
        
        self.settings.setValue("editorConfig", json.dumps(config))
    
    def load_editor_config(self):
        """Load editor configuration"""
        config_str = self.settings.value("editorConfig")
        if not config_str:
            return {
                'font_family': 'Consolas',
                'font_size': 12,
                'tab_width': 4,
                'line_numbers': True,
                'word_wrap': False,
                'highlight_current_line': True,
                'show_whitespace': False
            }
            
        try:
            return json.loads(config_str)
        except json.JSONDecodeError:
            return {}
    
    def save_calculation_config(self, calc_config):
        """Save calculation configuration"""
        config = {
            'decimal_precision': calc_config.get('decimal_precision', 6),
            'angle_mode': calc_config.get('angle_mode', 'radians'),  # radians or degrees
            'complex_format': calc_config.get('complex_format', 'rectangular'),  # rectangular or polar
            'number_format': calc_config.get('number_format', 'auto'),  # auto, fixed, scientific
            'auto_recalculate': calc_config.get('auto_recalculate', True),
            'recalculate_delay': calc_config.get('recalculate_delay', 500)  # milliseconds
        }
        
        self.settings.setValue("calculationConfig", json.dumps(config))
    
    def load_calculation_config(self):
        """Load calculation configuration"""
        config_str = self.settings.value("calculationConfig")
        if not config_str:
            return {
                'decimal_precision': 6,
                'angle_mode': 'radians',
                'complex_format': 'rectangular',
                'number_format': 'auto',
                'auto_recalculate': True,
                'recalculate_delay': 500
            }
            
        try:
            return json.loads(config_str)
        except json.JSONDecodeError:
            return {}
    
    def save_recent_files(self, files_list):
        """Save list of recent files"""
        # Keep only the last 10 files
        recent_files = files_list[-10:] if len(files_list) > 10 else files_list
        self.settings.setValue("recentFiles", json.dumps(recent_files))
    
    def load_recent_files(self):
        """Load list of recent files"""
        files_str = self.settings.value("recentFiles")
        if not files_str:
            return []
            
        try:
            files = json.loads(files_str)
            # Filter out files that no longer exist
            return [f for f in files if os.path.exists(f)]
        except json.JSONDecodeError:
            return []
    
    def save_panel_config(self, panel_name, config):
        """Save configuration for a specific panel"""
        self.settings.setValue(f"panel_{panel_name}", json.dumps(config))
    
    def load_panel_config(self, panel_name, default_config=None):
        """Load configuration for a specific panel"""
        config_str = self.settings.value(f"panel_{panel_name}")
        if not config_str:
            return default_config or {}
            
        try:
            return json.loads(config_str)
        except json.JSONDecodeError:
            return default_config or {}
    
    def save_custom_functions(self, functions_dict):
        """Save custom functions"""
        # Serialize functions to a safe format
        safe_functions = {}
        for name, func_data in functions_dict.items():
            safe_functions[name] = {
                'code': func_data.get('code', ''),
                'description': func_data.get('description', ''),
                'created': func_data.get('created', ''),
                'modified': func_data.get('modified', '')
            }
        
        self.settings.setValue("customFunctions", json.dumps(safe_functions))
    
    def load_custom_functions(self):
        """Load custom functions"""
        functions_str = self.settings.value("customFunctions")
        if not functions_str:
            return {}
            
        try:
            return json.loads(functions_str)
        except json.JSONDecodeError:
            return {}
    
    def export_config(self, filepath):
        """Export all configuration to a file"""
        config = {
            'theme': self.load_theme_config(),
            'editor': self.load_editor_config(),
            'calculation': self.load_calculation_config(),
            'custom_functions': self.load_custom_functions(),
            'recent_files': self.load_recent_files()
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting config: {e}")
            return False
    
    def import_config(self, filepath):
        """Import configuration from a file"""
        try:
            with open(filepath, 'r') as f:
                config = json.load(f)
            
            if 'theme' in config and config['theme']:
                self.save_theme_config(config['theme'])
            
            if 'editor' in config:
                self.save_editor_config(config['editor'])
            
            if 'calculation' in config:
                self.save_calculation_config(config['calculation'])
            
            if 'custom_functions' in config:
                self.save_custom_functions(config['custom_functions'])
            
            if 'recent_files' in config:
                self.save_recent_files(config['recent_files'])
            
            return True
            
        except Exception as e:
            print(f"Error importing config: {e}")
            return False
    
    def reset_config(self):
        """Reset all configuration to defaults"""
        self.settings.clear()
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
