import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QListWidgetItem, QPushButton, QLabel, QMessageBox,
                             QInputDialog, QFileDialog)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent


class ArtistPanel(QWidget):
    artist_selected = pyqtSignal(dict)
    artists_changed = pyqtSignal()
    layers_changed = pyqtSignal()  # NEW: Signal when layers are added/removed

    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Artists")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title)

        # Artist list
        self.artist_list = QListWidget()
        self.artist_list.itemSelectionChanged.connect(self.on_artist_selected)
        self.artist_list.setStyleSheet("""
            QListWidget {
                background: #2d2d2d;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
            }
            QListWidget::item:selected {
                background: #0078d4;
                color: white;
            }
        """)
        layout.addWidget(self.artist_list)

        # Controls
        controls_layout = QHBoxLayout()
        self.btn_add_artist = QPushButton("Add Artist")
        self.btn_remove_artist = QPushButton("Remove Artist")
        self.btn_upload_layers = QPushButton("Upload Layers")

        # Style buttons for dark mode
        button_style = """
            QPushButton {
                background: #404040;
                color: white;
                border: 1px solid #555555;
                padding: 8px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #505050;
            }
            QPushButton:pressed {
                background: #606060;
            }
            QPushButton:disabled {
                background: #2d2d2d;
                color: #666666;
            }
        """
        self.btn_add_artist.setStyleSheet(button_style)
        self.btn_remove_artist.setStyleSheet(button_style)
        self.btn_upload_layers.setStyleSheet(button_style)

        controls_layout.addWidget(self.btn_add_artist)
        controls_layout.addWidget(self.btn_remove_artist)
        controls_layout.addWidget(self.btn_upload_layers)

        layout.addLayout(controls_layout)

        # Layer list for selected artist
        layer_title = QLabel("Artist Layers:")
        layer_title.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(layer_title)

        self.layer_list = QListWidget()
        self.layer_list.setDragEnabled(True)
        self.layer_list.setStyleSheet("""
            QListWidget {
                background: #2d2d2d;
                color: white;
                border: 1px solid #555555;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #3d3d3d;
            }
        """)
        layout.addWidget(self.layer_list)

        # Connect buttons
        self.btn_add_artist.clicked.connect(self.add_artist)
        self.btn_remove_artist.clicked.connect(self.remove_artist)
        self.btn_upload_layers.clicked.connect(self.upload_layers)

        # Enable drag and drop
        self.setAcceptDrops(True)

        self.refresh_artists()

    def refresh_artists(self):
        self.artist_list.clear()
        if self.project_manager.is_project_loaded():
            artists = self.project_manager.get_artists()
            for artist_name in artists:
                item = QListWidgetItem(artist_name)
                # Show layer count in the item
                layer_count = self.project_manager.get_artist_layer_count(artist_name)
                if layer_count > 0:
                    item.setText(f"{artist_name} ({layer_count} layers)")
                self.artist_list.addItem(item)

    def add_artist(self):
        # Check if project is loaded
        if not self.project_manager.is_project_loaded():
            QMessageBox.warning(self, "No Project", "Please create or load a project first!")
            return

        artist_name, ok = QInputDialog.getText(self, "Add Artist", "Artist Name:")
        if ok and artist_name:
            if artist_name.strip() == "":
                QMessageBox.warning(self, "Invalid Name", "Artist name cannot be empty!")
                return

            if self.project_manager.add_artist(artist_name):
                self.refresh_artists()
                self.artists_changed.emit()
                QMessageBox.information(self, "Success", f"Artist '{artist_name}' added!")
            else:
                QMessageBox.warning(self, "Error", "Failed to add artist - name may already exist!")

    def remove_artist(self):
        if not self.project_manager.is_project_loaded():
            QMessageBox.warning(self, "No Project", "Please create or load a project first!")
            return

        current_item = self.artist_list.currentItem()
        if current_item:
            # Extract artist name (remove layer count if present)
            display_text = current_item.text()
            artist_name = display_text.split(' (')[0]  # Remove layer count from display

            reply = QMessageBox.question(self, "Confirm Delete",
                                         f"Are you sure you want to remove artist '{artist_name}' and all their layers?",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                if self.project_manager.remove_artist(artist_name):
                    self.refresh_artists()
                    self.layer_list.clear()
                    self.artists_changed.emit()
                    QMessageBox.information(self, "Success", f"Artist '{artist_name}' removed!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to remove artist")
        else:
            QMessageBox.warning(self, "No Selection", "Please select an artist to remove!")

    def upload_layers(self):
        if not self.project_manager.is_project_loaded():
            QMessageBox.warning(self, "No Project", "Please create or load a project first!")
            return

        current_item = self.artist_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an artist first")
            return

        # Extract artist name (remove layer count if present)
        display_text = current_item.text()
        artist_name = display_text.split(' (')[0]  # Remove layer count from display

        files, _ = QFileDialog.getOpenFileNames(
            self, f"Select Layer Images for {artist_name}", "", "Images (*.png *.jpg *.jpeg)"
        )

        if files:
            success_count = 0
            failed_files = []

            for file_path in files:
                if self.project_manager.add_layer_to_artist(artist_name, file_path):
                    success_count += 1
                else:
                    failed_files.append(os.path.basename(file_path))

            self.refresh_artist_layers(artist_name)
            self.refresh_artists()  # Refresh to update layer counts
            self.layers_changed.emit()  # NEW: Emit signal when layers change

            if success_count > 0:
                message = f"Added {success_count} layers to {artist_name}"
                if failed_files:
                    message += f"\nFailed to add {len(failed_files)} files: {', '.join(failed_files[:5])}"
                    if len(failed_files) > 5:
                        message += f"... and {len(failed_files) - 5} more"
                QMessageBox.information(self, "Success", message)
            else:
                QMessageBox.warning(self, "Error", f"Failed to add any layers to {artist_name}")

    def on_artist_selected(self):
        if not self.project_manager.is_project_loaded():
            return

        current_item = self.artist_list.currentItem()
        if current_item:
            # Extract artist name (remove layer count if present)
            display_text = current_item.text()
            artist_name = display_text.split(' (')[0]  # Remove layer count from display

            self.refresh_artist_layers(artist_name)
            artist_data = self.project_manager.get_artist(artist_name)
            if artist_data:
                self.artist_selected.emit(artist_data)

    def refresh_artist_layers(self, artist_name):
        self.layer_list.clear()
        artist = self.project_manager.get_artist(artist_name)
        if artist and 'layers' in artist:
            for layer in artist['layers']:
                item_text = f"{layer['display_name']} (Rarity: {layer.get('rarity_weight', 1.0):.1f})"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, layer)
                self.layer_list.addItem(item)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if not self.project_manager.is_project_loaded():
            QMessageBox.warning(self, "No Project", "Please create or load a project first!")
            return

        current_item = self.artist_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select an artist first")
            return

        # Extract artist name (remove layer count if present)
        display_text = current_item.text()
        artist_name = display_text.split(' (')[0]  # Remove layer count from display

        success_count = 0
        failed_files = []

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                if self.project_manager.add_layer_to_artist(artist_name, file_path):
                    success_count += 1
                else:
                    failed_files.append(os.path.basename(file_path))

        self.refresh_artist_layers(artist_name)
        self.refresh_artists()  # Refresh to update layer counts
        self.layers_changed.emit()  # NEW: Emit signal when layers change

        if success_count > 0:
            message = f"Added {success_count} layers to {artist_name} via drag & drop!"
            if failed_files:
                message += f"\nFailed to add {len(failed_files)} files"
            QMessageBox.information(self, "Success", message)
        else:
            QMessageBox.warning(self, "Error", "Failed to add any layers via drag & drop")

        event.acceptProposedAction()

    def get_selected_artist_name(self):
        """Get the currently selected artist name"""
        current_item = self.artist_list.currentItem()
        if current_item:
            display_text = current_item.text()
            return display_text.split(' (')[0]  # Remove layer count from display
        return None