from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QListWidgetItem, QPushButton, QLabel, QMessageBox,
                             QInputDialog, QSlider)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class LayerPanel(QWidget):
    composition_changed = pyqtSignal()

    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        layout.addWidget(QLabel("Layer Stack (Z-Index Order)"))

        # Layer stack list
        self.layer_stack = QListWidget()
        self.layer_stack.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.layer_stack.model().rowsMoved.connect(self.on_layers_reordered)
        layout.addWidget(self.layer_stack)

        # Controls
        controls_layout = QHBoxLayout()
        self.btn_move_up = QPushButton("Move Up")
        self.btn_move_down = QPushButton("Move Down")
        self.btn_remove_layer = QPushButton("Remove Layer")
        self.btn_clear_stack = QPushButton("Clear Stack")

        controls_layout.addWidget(self.btn_move_up)
        controls_layout.addWidget(self.btn_move_down)
        controls_layout.addWidget(self.btn_remove_layer)
        controls_layout.addWidget(self.btn_clear_stack)

        layout.addLayout(controls_layout)

        # Layer properties
        properties_layout = QVBoxLayout()
        properties_layout.addWidget(QLabel("Layer Properties:"))

        # Blend mode
        blend_layout = QHBoxLayout()
        blend_layout.addWidget(QLabel("Blend Mode:"))
        from PyQt6.QtWidgets import QComboBox
        self.blend_combo = QComboBox()
        self.blend_combo.addItems(["normal", "multiply", "screen", "overlay"])
        blend_layout.addWidget(self.blend_combo)
        properties_layout.addLayout(blend_layout)

        # Opacity
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(QLabel("Opacity:"))
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(100)
        self.opacity_label = QLabel("1.0")
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_label)
        properties_layout.addLayout(opacity_layout)

        # Required checkbox
        from PyQt6.QtWidgets import QCheckBox
        self.required_checkbox = QCheckBox("Required")
        properties_layout.addWidget(self.required_checkbox)

        layout.addLayout(properties_layout)

        # Connect buttons and signals
        self.btn_move_up.clicked.connect(self.move_layer_up)
        self.btn_move_down.clicked.connect(self.move_layer_down)
        self.btn_remove_layer.clicked.connect(self.remove_selected_layer)
        self.btn_clear_stack.clicked.connect(self.clear_layer_stack)
        self.blend_combo.currentTextChanged.connect(self.update_layer_properties)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        self.required_checkbox.stateChanged.connect(self.update_layer_properties)
        self.layer_stack.itemSelectionChanged.connect(self.on_layer_selected)

        # Enable drag and drop
        self.setAcceptDrops(True)

        self.refresh_layer_stack()

    def on_artist_selected(self, artist_data):
        # Store current artist for drag and drop
        self.current_artist = artist_data

    def refresh_layer_stack(self):
        self.layer_stack.clear()
        composition = self.project_manager.get_composition()
        for layer in composition:
            item_text = f"{layer['artist']} - {layer['display_name']} (Z: {layer['z_index']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, layer)
            self.layer_stack.addItem(item)

    def move_layer_up(self):
        current_row = self.layer_stack.currentRow()
        if current_row > 0:
            self.layer_stack.insertItem(current_row - 1, self.layer_stack.takeItem(current_row))
            self.layer_stack.setCurrentRow(current_row - 1)
            self.update_z_indices()

    def move_layer_down(self):
        current_row = self.layer_stack.currentRow()
        if current_row < self.layer_stack.count() - 1:
            self.layer_stack.insertItem(current_row + 1, self.layer_stack.takeItem(current_row))
            self.layer_stack.setCurrentRow(current_row + 1)
            self.update_z_indices()

    def remove_selected_layer(self):
        current_row = self.layer_stack.currentRow()
        if current_row >= 0:
            self.layer_stack.takeItem(current_row)
            self.update_z_indices()

    def clear_layer_stack(self):
        self.layer_stack.clear()
        self.project_manager.clear_composition()
        self.composition_changed.emit()

    def update_z_indices(self):
        composition = []
        for i in range(self.layer_stack.count()):
            item = self.layer_stack.item(i)
            layer_data = item.data(Qt.ItemDataRole.UserRole)
            layer_data['z_index'] = i + 1
            composition.append(layer_data)

        self.project_manager.update_composition(composition)
        self.refresh_layer_stack()
        self.composition_changed.emit()

    def on_layers_reordered(self):
        self.update_z_indices()

    def on_opacity_changed(self, value):
        opacity = value / 100.0
        self.opacity_label.setText(f"{opacity:.1f}")
        self.update_layer_properties()

    def on_layer_selected(self):
        current_item = self.layer_stack.currentItem()
        if current_item:
            layer_data = current_item.data(Qt.ItemDataRole.UserRole)
            self.blend_combo.setCurrentText(layer_data.get('blend_mode', 'normal'))
            opacity = int(layer_data.get('opacity', 1.0) * 100)
            self.opacity_slider.setValue(opacity)
            self.required_checkbox.setChecked(layer_data.get('required', False))

    def update_layer_properties(self):
        current_item = self.layer_stack.currentItem()
        if current_item:
            layer_data = current_item.data(Qt.ItemDataRole.UserRole)
            layer_data['blend_mode'] = self.blend_combo.currentText()
            layer_data['opacity'] = self.opacity_slider.value() / 100.0
            layer_data['required'] = self.required_checkbox.isChecked()

            self.project_manager.update_layer_properties(layer_data)
            self.composition_changed.emit()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText() or event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if hasattr(self, 'current_artist') and self.current_artist:
            # Get the layer data from the drag (simplified)
            # In a real implementation, you'd get the specific layer being dragged
            artist_name = self.current_artist['name']
            layers = self.current_artist.get('layers', [])

            if layers:
                # Add the first layer (simplified - in real app, you'd select which layer)
                layer = layers[0]
                new_layer = {
                    'artist': artist_name,
                    'layer_name': layer['file_name'],
                    'display_name': layer['display_name'],
                    'file_path': layer['file_path'],
                    'z_index': self.layer_stack.count() + 1,
                    'blend_mode': 'normal',
                    'opacity': 1.0,
                    'required': False
                }

                self.project_manager.add_layer_to_composition(new_layer)
                self.refresh_layer_stack()
                self.composition_changed.emit()

        event.acceptProposedAction()