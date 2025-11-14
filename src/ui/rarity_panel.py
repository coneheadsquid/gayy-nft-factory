from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QListWidgetItem, QPushButton, QLabel, QMessageBox,
                             QInputDialog, QSlider, QTabWidget)
from PyQt6.QtCore import pyqtSignal, Qt


class RarityPanel(QWidget):
    rarity_changed = pyqtSignal()

    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Rarity Settings & Generation")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; color: #f0f0f0;")
        layout.addWidget(title)

        # Tab widget for artists
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Info label
        self.info_label = QLabel("Add artists and layers, then set rarity weights for each layer.")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("padding: 10px; background: #2d2d2d; color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(self.info_label)

        self.refresh_artists()

    def refresh_artists(self):
        """Refresh the entire rarity panel with current artists and layers"""
        self.tab_widget.clear()

        if self.project_manager.is_project_loaded():
            artists = self.project_manager.get_artists()

            if not artists:
                self.info_label.setText("No artists added yet. Use the Artists panel to add artists and upload layers.")
                return

            # Check if any artist has layers
            has_layers = any(self.project_manager.get_artist_layer_count(artist) > 0 for artist in artists)

            if not has_layers:
                self.info_label.setText("Artists added but no layers uploaded. Add layers to configure rarity.")
                return

            self.info_label.setText(
                f"Configure rarity settings for {len(artists)} artists. Higher weight = more common.")

            for artist_name in artists:
                layer_count = self.project_manager.get_artist_layer_count(artist_name)
                if layer_count > 0:
                    artist_tab = self.create_artist_tab(artist_name)
                    tab_name = f"{artist_name} ({layer_count})"
                    self.tab_widget.addTab(artist_tab, tab_name)

    def create_artist_tab(self, artist_name):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        artist = self.project_manager.get_artist(artist_name)
        if not artist or not artist['layers']:
            no_layers_label = QLabel(f"No layers added for {artist_name} yet.")
            no_layers_label.setStyleSheet("color: #f0f0f0; padding: 10px;")
            layout.addWidget(no_layers_label)
            return tab

        # Add instructions
        instructions = QLabel(f"Drag rarity sliders for {artist_name}'s layers (1-10, higher = more common):")
        instructions.setStyleSheet("padding: 5px; color: #cccccc;")
        layout.addWidget(instructions)

        for layer in artist['layers']:
            layer_widget = self.create_layer_rarity_widget(artist_name, layer)
            layout.addWidget(layer_widget)

        layout.addStretch()
        return tab

    def create_layer_rarity_widget(self, artist_name, layer):
        widget = QWidget()
        widget.setStyleSheet("QWidget { background: #333333; padding: 8px; border-radius: 4px; margin: 2px; }")
        layout = QHBoxLayout(widget)

        # Layer name
        name_label = QLabel(layer['display_name'])
        name_label.setStyleSheet("color: #f0f0f0; font-weight: bold; min-width: 150px;")
        layout.addWidget(name_label)

        # Rarity slider
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(1, 10)  # 1-10 scale for simplicity
        slider.setValue(int(layer.get('rarity_weight', 1.0)))
        slider.valueChanged.connect(lambda value: self.on_rarity_changed(artist_name, layer['file_name'], value))
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #666666, stop:1 #888888);
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #aaaaaa, stop:1 #cccccc);
                border: 1px solid #777777;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)

        # Value label
        value_label = QLabel(f"{layer.get('rarity_weight', 1.0):.0f}")
        value_label.setStyleSheet("color: #f0f0f0; font-weight: bold; min-width: 20px;")
        slider.valueChanged.connect(lambda value: value_label.setText(f"{value}"))

        layout.addWidget(slider)
        layout.addWidget(value_label)

        return widget

    def on_rarity_changed(self, artist_name, layer_name, rarity_weight):
        if self.project_manager.set_layer_rarity(artist_name, layer_name, float(rarity_weight)):
            self.rarity_changed.emit()