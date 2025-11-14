from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QListWidgetItem, QPushButton, QLabel, QMessageBox,
                             QInputDialog, QSlider, QTabWidget, QScrollArea,
                             QSpinBox)
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
        title = QLabel("Layer Settings - Rarity, Opacity & Stacking")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; color: #f0f0f0;")
        layout.addWidget(title)

        # Tab widget for artists
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Info label
        self.info_label = QLabel("Configure rarity weights, opacity, and stacking order for each artist's layers.")
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
                self.info_label.setText("Artists added but no layers uploaded. Add layers to configure settings.")
                return

            self.info_label.setText(
                f"Configure settings for {len(artists)} artists. Higher rarity = more common. Lower layer index = rendered first.")

            for artist_name in artists:
                layer_count = self.project_manager.get_artist_layer_count(artist_name)
                if layer_count > 0:
                    artist_tab = self.create_artist_tab(artist_name)
                    tab_name = f"{artist_name} ({layer_count})"
                    self.tab_widget.addTab(artist_tab, tab_name)

    def create_artist_tab(self, artist_name):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(2)

        artist = self.project_manager.get_artist(artist_name)
        if not artist or not artist['layers']:
            no_layers_label = QLabel(f"No layers added for {artist_name} yet.")
            no_layers_label.setStyleSheet("color: #f0f0f0; padding: 10px;")
            layout.addWidget(no_layers_label)
            return tab

        # Add instructions
        instructions = QLabel(f"Configure {artist_name}'s layers:")
        instructions.setStyleSheet(
            "padding: 2px 5px; color: #cccccc; font-weight: bold; font-size: 12px; margin: 0; margin-bottom: 2px;")
        layout.addWidget(instructions)

        # Create scroll area for many layers
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(2)

        for layer in artist['layers']:
            layer_widget = self.create_layer_settings_widget(artist_name, layer)
            scroll_layout.addWidget(layer_widget)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_area.setMaximumHeight(800)

        layout.addWidget(scroll_area)
        return tab

    def create_layer_settings_widget(self, artist_name, layer):
        widget = QWidget()
        widget.setStyleSheet("QWidget { background: #333333; padding: 12px; border-radius: 6px; margin: 4px; }")
        layout = QVBoxLayout(widget)

        # Layer name header
        name_label = QLabel(layer['display_name'])
        name_label.setStyleSheet("color: #f0f0f0; font-weight: bold; font-size: 13px; margin-bottom: 8px;")
        layout.addWidget(name_label)

        # Rarity controls
        rarity_layout = QHBoxLayout()
        rarity_label = QLabel("Rarity:")
        rarity_label.setStyleSheet("color: #cccccc; min-width: 60px;")
        rarity_layout.addWidget(rarity_label)

        # Rarity slider
        rarity_slider = QSlider(Qt.Orientation.Horizontal)
        rarity_slider.setRange(1, 10)
        rarity_slider.setValue(int(layer.get('rarity_weight', 1.0)))
        rarity_slider.valueChanged.connect(lambda value: self.on_rarity_changed(artist_name, layer['file_name'], value))
        rarity_slider.setStyleSheet("""
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

        # Rarity value label
        rarity_value = QLabel(f"{layer.get('rarity_weight', 1.0):.0f}")
        rarity_value.setStyleSheet("color: #f0f0f0; font-weight: bold; min-width: 20px;")
        rarity_slider.valueChanged.connect(lambda value: rarity_value.setText(f"{value}"))

        rarity_layout.addWidget(rarity_slider)
        rarity_layout.addWidget(rarity_value)
        layout.addLayout(rarity_layout)

        # Opacity controls
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel("Opacity:")
        opacity_label.setStyleSheet("color: #cccccc; min-width: 60px;")
        opacity_layout.addWidget(opacity_label)

        # Opacity slider
        opacity_slider = QSlider(Qt.Orientation.Horizontal)
        opacity_slider.setRange(0, 100)
        opacity_value = int(layer.get('opacity', 1.0) * 100)
        opacity_slider.setValue(opacity_value)
        opacity_slider.valueChanged.connect(
            lambda value: self.on_opacity_changed(artist_name, layer['file_name'], value / 100.0))
        opacity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #555555;
                height: 8px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #444477, stop:1 #666699);
                margin: 2px 0;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8888cc, stop:1 #aaaaff);
                border: 1px solid #777799;
                width: 18px;
                margin: -2px 0;
                border-radius: 9px;
            }
        """)

        # Opacity value label
        opacity_value_label = QLabel(f"{layer.get('opacity', 1.0):.1f}")
        opacity_value_label.setStyleSheet("color: #f0f0f0; font-weight: bold; min-width: 30px;")
        opacity_slider.valueChanged.connect(lambda value: opacity_value_label.setText(f"{value / 100.0:.1f}"))

        opacity_layout.addWidget(opacity_slider)
        opacity_layout.addWidget(opacity_value_label)
        layout.addLayout(opacity_layout)

        # Layer Index (z-index) controls
        index_layout = QHBoxLayout()
        index_label = QLabel("Stack Order:")
        index_label.setStyleSheet("color: #cccccc; min-width: 60px;")
        index_layout.addWidget(index_label)

        # Layer index spin box
        index_spin = QSpinBox()
        index_spin.setRange(1, 20)  # Reasonable range for layers
        index_spin.setValue(int(layer.get('layer_index', 1)))
        index_spin.valueChanged.connect(
            lambda value: self.on_layer_index_changed(artist_name, layer['file_name'], value))
        index_spin.setStyleSheet("""
            QSpinBox {
                background: #444444;
                color: #f0f0f0;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 2px;
                min-width: 50px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background: #555555;
                border: 1px solid #666666;
                width: 15px;
            }
        """)

        index_help = QLabel("(Lower = rendered first)")
        index_help.setStyleSheet("color: #888888; font-size: 10px;")

        index_layout.addWidget(index_spin)
        index_layout.addWidget(index_help)
        index_layout.addStretch()
        layout.addLayout(index_layout)

        # Help text
        help_text = QLabel(
            "Rarity: 1-10 (higher = more common) | Opacity: 0.0-1.0 | Stack Order: 1-20 (lower = behind)")
        help_text.setStyleSheet("color: #888888; font-size: 10px; margin-top: 4px;")
        layout.addWidget(help_text)

        return widget

    def on_rarity_changed(self, artist_name, layer_name, rarity_weight):
        if self.project_manager.set_layer_rarity(artist_name, layer_name, float(rarity_weight)):
            self.rarity_changed.emit()

    def on_opacity_changed(self, artist_name, layer_name, opacity):
        if self.project_manager.set_layer_opacity(artist_name, layer_name, opacity):
            self.rarity_changed.emit()

    def on_layer_index_changed(self, artist_name, layer_name, layer_index):
        if self.project_manager.set_layer_index(artist_name, layer_name, layer_index):
            self.rarity_changed.emit()