import os
import json
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QLabel, QMessageBox,
                             QFileDialog, QTextEdit, QInputDialog, QProgressDialog,
                             QTabWidget, QApplication)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPalette, QColor, QMovie  # ADD QMovie import
from ..core.project_manager import ProjectManager
from .artist_panel import ArtistPanel
from .rarity_panel import RarityPanel
from .gallery_panel import GalleryPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.project_manager = ProjectManager()
        self.current_preview_movie = None  # Track current preview GIF
        self.apply_dark_theme()
        self.init_ui()

    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        app = QApplication.instance()
        if app:
            # Set dark palette
            dark_palette = QPalette()

            # Base colors
            dark_palette.setColor(QPalette.ColorRole.Window, QColor(35, 35, 35))
            dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(35, 35, 35))
            dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(55, 55, 55))
            dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.Button, QColor(55, 55, 55))
            dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(240, 240, 240))
            dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 255, 255))
            dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
            dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(35, 35, 35))

            # Disabled colors
            dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(127, 127, 127))
            dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(127, 127, 127))
            dark_palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(127, 127, 127))

            app.setPalette(dark_palette)

            # Set stylesheet for additional styling
            app.setStyleSheet("""
                QMainWindow, QWidget {
                    background: #232323;
                    color: #f0f0f0;
                }
                QLabel {
                    color: #f0f0f0;
                }
                QTabWidget::pane {
                    border: 1px solid #444444;
                    background: #232323;
                }
                QTabBar::tab {
                    background: #333333;
                    color: #f0f0f0;
                    padding: 8px 16px;
                    border: 1px solid #444444;
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }
                QTabBar::tab:selected {
                    background: #2a82da;
                }
                QTabBar::tab:hover:!selected {
                    background: #404040;
                }
                QProgressBar {
                    border: 1px solid #444444;
                    border-radius: 4px;
                    text-align: center;
                    color: #f0f0f0;
                    background: #333333;
                }
                QProgressBar::chunk {
                    background: #2a82da;
                    border-radius: 3px;
                }
                QMessageBox {
                    background: #232323;
                    color: #f0f0f0;
                }
                QMessageBox QLabel {
                    color: #f0f0f0;
                }
                QInputDialog {
                    background: #232323;
                    color: #f0f0f0;
                }
                QInputDialog QLabel {
                    color: #f0f0f0;
                }
                QInputDialog QLineEdit {
                    background: #333333;
                    color: #f0f0f0;
                    border: 1px solid #444444;
                    padding: 5px;
                    border-radius: 3px;
                }
            """)

    def init_ui(self):
        self.setWindowTitle("gayy nft factory - Artists collab NFT generator ")
        self.setGeometry(100, 100, 1400, 800)

        # Create tab widget for different views
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Setup tabs
        self.setup_generation_tab()
        self.setup_gallery_tab()

        # Connect signals
        self.artist_panel.artists_changed.connect(self.rarity_panel.refresh_artists)
        self.artist_panel.layers_changed.connect(self.rarity_panel.refresh_artists)

    def setup_generation_tab(self):
        """Setup the generation tab with artists, rarity, and controls"""
        generation_tab = QWidget()
        layout = QHBoxLayout(generation_tab)

        # Left panel - Artists
        self.artist_panel = ArtistPanel(self.project_manager)
        layout.addWidget(self.artist_panel, 1)

        # Center panel - Rarity settings
        self.rarity_panel = RarityPanel(self.project_manager)
        layout.addWidget(self.rarity_panel, 2)

        # Right panel - Controls and preview
        right_panel = self.create_generation_panel()
        layout.addWidget(right_panel, 1)

        self.tab_widget.addTab(generation_tab, "Generation")

    def setup_gallery_tab(self):
        """Setup the gallery tab for viewing generated NFTs"""
        self.gallery_panel = GalleryPanel(self.project_manager)
        self.tab_widget.addTab(self.gallery_panel, "Gallery")

        # Connect gallery signals
        self.gallery_panel.nft_selected.connect(self.on_gallery_nft_selected)

    def create_generation_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Project controls
        project_layout = QHBoxLayout()
        self.btn_new_project = QPushButton("New Project")
        self.btn_load_project = QPushButton("Load Project")
        self.btn_save_project = QPushButton("Save Project")

        # Style buttons
        button_style = """
            QPushButton {
                background: #333333;
                color: #f0f0f0;
                border: 1px solid #444444;
                padding: 8px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #404040;
            }
            QPushButton:pressed {
                background: #505050;
            }
            QPushButton:disabled {
                background: #2d2d2d;
                color: #666666;
            }
        """
        self.btn_new_project.setStyleSheet(button_style)
        self.btn_load_project.setStyleSheet(button_style)
        self.btn_save_project.setStyleSheet(button_style)

        project_layout.addWidget(self.btn_new_project)
        project_layout.addWidget(self.btn_load_project)
        project_layout.addWidget(self.btn_save_project)

        # Generation controls
        generation_layout = QHBoxLayout()
        self.btn_generate_single = QPushButton("Generate Single")
        self.btn_generate_batch = QPushButton("Generate Batch")
        self.btn_generate_full = QPushButton("Generate All Unique")
        self.btn_copy_metadata = QPushButton("Copy Metadata")

        self.btn_generate_single.setStyleSheet(button_style)
        self.btn_generate_batch.setStyleSheet(button_style)
        self.btn_generate_full.setStyleSheet(button_style)
        self.btn_copy_metadata.setStyleSheet(button_style)

        generation_layout.addWidget(self.btn_generate_single)
        generation_layout.addWidget(self.btn_generate_batch)
        generation_layout.addWidget(self.btn_generate_full)
        generation_layout.addWidget(self.btn_copy_metadata)

        # Stats display
        self.stats_label = QLabel("Add artists and layers to see generation stats")
        self.stats_label.setStyleSheet(
            "background: #2d2d2d; padding: 10px; border: 1px solid #444444; border-radius: 4px; color: #f0f0f0;")

        # Preview area
        self.preview_label = QLabel("Combination Preview")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(300, 300)
        self.preview_label.setStyleSheet(
            "border: 2px solid #444444; background: #1a1a1a; color: #888888; font-weight: bold;")
        self.preview_label.setText("Preview will appear here")

        # Preview controls
        preview_controls = QHBoxLayout()
        self.btn_generate_preview = QPushButton("Generate Preview")
        self.btn_clear_preview = QPushButton("Clear Preview")

        self.btn_generate_preview.setStyleSheet(button_style)
        self.btn_clear_preview.setStyleSheet(button_style)

        preview_controls.addWidget(self.btn_generate_preview)
        preview_controls.addWidget(self.btn_clear_preview)

        # Metadata display
        self.metadata_display = QTextEdit()
        self.metadata_display.setPlaceholderText("Metadata will appear here after generation...")
        self.metadata_display.setStyleSheet("""
            QTextEdit {
                background: #2d2d2d;
                color: #f0f0f0;
                border: 1px solid #444444;
                border-radius: 4px;
                padding: 8px;
            }
        """)

        # Project status
        self.project_status_label = QLabel("No project loaded")
        self.project_status_label.setStyleSheet("color: #ff6b6b; font-weight: bold; font-size: 12px; padding: 5px;")

        # Add to main layout
        layout.addWidget(self.project_status_label)
        layout.addLayout(project_layout)
        layout.addWidget(self.stats_label)
        layout.addLayout(generation_layout)
        layout.addLayout(preview_controls)

        preview_title = QLabel("Preview:")
        preview_title.setStyleSheet("color: #f0f0f0; font-weight: bold; margin-top: 10px;")
        layout.addWidget(preview_title)
        layout.addWidget(self.preview_label)

        metadata_title = QLabel("Metadata:")
        metadata_title.setStyleSheet("color: #f0f0f0; font-weight: bold; margin-top: 10px;")
        layout.addWidget(metadata_title)
        layout.addWidget(self.metadata_display)

        # Connect buttons
        self.btn_new_project.clicked.connect(self.new_project)
        self.btn_load_project.clicked.connect(self.load_project)
        self.btn_save_project.clicked.connect(self.save_project)
        self.btn_generate_single.clicked.connect(self.generate_single)
        self.btn_generate_batch.clicked.connect(self.generate_batch)
        self.btn_generate_full.clicked.connect(self.generate_full_collection)
        self.btn_copy_metadata.clicked.connect(self.copy_metadata)
        self.btn_generate_preview.clicked.connect(self.generate_random_preview)
        self.btn_clear_preview.clicked.connect(self.clear_preview)

        return panel

    def check_project_loaded(self, action_name):
        """Check if project is loaded before performing action"""
        if not self.project_manager.is_project_loaded():
            QMessageBox.warning(self, "No Project", f"Please create or load a project before {action_name}!")
            return False
        return True

    def update_project_status(self):
        """Update the project status label"""
        if self.project_manager.is_project_loaded():
            project_name = self.project_manager.project_data['project_info'].get('name', 'Unnamed Project')
            self.project_status_label.setText(f"Project: {project_name}")
            self.project_status_label.setStyleSheet("color: #51cf66; font-weight: bold; font-size: 12px; padding: 5px;")
            self.update_stats_display()
        else:
            self.project_status_label.setText("No project loaded")
            self.project_status_label.setStyleSheet("color: #ff6b6b; font-weight: bold; font-size: 12px; padding: 5px;")
            self.stats_label.setText("Add artists and layers to see generation stats")

    def update_stats_display(self):
        """Update the statistics display"""
        if self.project_manager.is_project_loaded():
            stats = self.project_manager.get_generation_stats()
            artists = self.project_manager.get_artists()

            # Check if we have artists with layers
            has_layers = any(self.project_manager.get_artist_layer_count(artist) > 0 for artist in artists)

            if not has_layers:
                self.stats_label.setText("Artists added but no layers uploaded. Add layers to generate NFTs.")
                return

            stats_text = f"🎨 Artists: {len(artists)} | "
            stats_text += f"🔢 Possible Combinations: {stats['possible_combinations']:,} | "
            stats_text += f"✅ Generated: {stats['generated_count']} | "
            stats_text += f"✨ Unique: {stats['unique_combinations']}"

            if stats['remaining_unique'] > 0:
                stats_text += f" | 📊 Remaining Unique: {stats['remaining_unique']:,}"

            self.stats_label.setText(stats_text)

    def new_project(self):
        project_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if project_path:
            collection_name, ok = QInputDialog.getText(self, "Collection Name", "Enter collection name:")
            if ok and collection_name:
                if self.project_manager.create_new_project(project_path, collection_name):
                    self.artist_panel.refresh_artists()
                    self.rarity_panel.refresh_artists()
                    self.gallery_panel.refresh_gallery()
                    self.update_project_status()
                    QMessageBox.information(self, "Success", f"New project '{collection_name}' created!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to create project")

    def load_project(self):
        project_path = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if project_path:
            if self.project_manager.load_project(project_path):
                self.artist_panel.refresh_artists()
                self.rarity_panel.refresh_artists()
                self.gallery_panel.refresh_gallery()
                self.update_project_status()

                QMessageBox.information(self, "Success", "Project loaded!")
            else:
                QMessageBox.warning(self, "Error", "Failed to load project")

    def save_project(self):
        if not self.check_project_loaded("saving"):
            return

        if self.project_manager.save_project():
            QMessageBox.information(self, "Success", "Project saved!")
        else:
            QMessageBox.warning(self, "Error", "Failed to save project")

    def generate_random_preview(self):
        """Generate a random combination preview"""
        if not self.check_project_loaded("generating preview"):
            return

        # Check if we have artists with layers
        artists = self.project_manager.get_artists()
        has_layers = any(self.project_manager.get_artist_layer_count(artist) > 0 for artist in artists)
        if not has_layers:
            QMessageBox.warning(self, "No Layers", "Please add layers to artists before generating preview!")
            return

        # Stop any currently playing preview GIF
        if self.current_preview_movie:
            self.current_preview_movie.stop()
            self.current_preview_movie = None

        combination, combination_key = self.project_manager.generate_random_combination()
        if combination:
            preview_path = self.project_manager.generate_preview_for_combination(combination)
            if preview_path and os.path.exists(preview_path):
                if preview_path.lower().endswith('.gif'):
                    # Handle GIF preview with animation
                    self.current_preview_movie = QMovie(preview_path)
                    self.current_preview_movie.setScaledSize(self.preview_label.size())
                    self.preview_label.setMovie(self.current_preview_movie)
                    self.current_preview_movie.start()
                    self.preview_label.setText("")  # Clear text
                else:
                    # Handle PNG preview
                    pixmap = QPixmap(preview_path)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio,
                                                      Qt.TransformationMode.SmoothTransformation)
                        self.preview_label.setPixmap(scaled_pixmap)
                        self.preview_label.setText("")  # Clear text when image is shown

            # Show combination info
            combo_text = "Preview Combination:\n"
            for artist, layer in combination.items():
                file_type = "GIF" if layer['file_path'].lower().endswith('.gif') else "PNG"
                combo_text += f"• {artist}: {layer['display_name']} ({file_type})\n"
            self.preview_label.setToolTip(combo_text)

    def clear_preview(self):
        """Clear the preview area"""
        # Stop any currently playing preview GIF
        if self.current_preview_movie:
            self.current_preview_movie.stop()
            self.current_preview_movie = None

        self.preview_label.clear()
        self.preview_label.setText("Preview will appear here")
        self.preview_label.setToolTip("")

    def generate_single(self):
        if not self.check_project_loaded("generating NFTs"):
            return

        # Check if we have artists with layers
        artists = self.project_manager.get_artists()
        has_layers = any(self.project_manager.get_artist_layer_count(artist) > 0 for artist in artists)
        if not has_layers:
            QMessageBox.warning(self, "No Layers", "Please add layers to artists before generating NFTs!")
            return

        if self.project_manager.generate_single_nft():
            # Refresh gallery to show new NFT
            self.gallery_panel.refresh_gallery()

            # Update preview with the newly generated NFT
            nfts = self.project_manager.get_all_generated_nfts()
            if nfts:
                latest_nft = nfts[-1]
                image_path = latest_nft['image_path']
                if os.path.exists(image_path):
                    # Stop any currently playing preview GIF
                    if self.current_preview_movie:
                        self.current_preview_movie.stop()
                        self.current_preview_movie = None

                    if image_path.lower().endswith('.gif'):
                        # Show animated GIF
                        self.current_preview_movie = QMovie(image_path)
                        self.current_preview_movie.setScaledSize(self.preview_label.size())
                        self.preview_label.setMovie(self.current_preview_movie)
                        self.current_preview_movie.start()
                        self.preview_label.setText("")
                    else:
                        # Show static PNG
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            scaled_pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio,
                                                          Qt.TransformationMode.SmoothTransformation)
                            self.preview_label.setPixmap(scaled_pixmap)
                            self.preview_label.setText("")

            # Update metadata display
            metadata = self.project_manager.get_latest_metadata()
            if metadata:
                self.metadata_display.setPlainText(json.dumps(metadata, indent=2))

            self.update_stats_display()
            QMessageBox.information(self, "Success", "Single NFT generated!")
        else:
            QMessageBox.warning(self, "Error", "Failed to generate NFT - may have run out of unique combinations!")

    def generate_batch(self):
        if not self.check_project_loaded("generating NFTs"):
            return

        # Check if we have artists with layers
        artists = self.project_manager.get_artists()
        has_layers = any(self.project_manager.get_artist_layer_count(artist) > 0 for artist in artists)
        if not has_layers:
            QMessageBox.warning(self, "No Layers", "Please add layers to artists before generating NFTs!")
            return

        count, ok = QInputDialog.getInt(self, "Batch Generation", "How many NFTs to generate?", 10, 1, 10000)
        if ok:
            progress = QProgressDialog(f"Generating {count} NFTs...", "Cancel", 0, count, self)
            progress.setWindowTitle("Generating NFTs")
            progress.setStyleSheet("""
                QProgressDialog {
                    background: #232323;
                    color: #f0f0f0;
                }
                QLabel {
                    color: #f0f0f0;
                }
            """)
            progress.show()

            success_count = 0
            for i in range(count):
                if progress.wasCanceled():
                    break

                if self.project_manager.generate_single_nft():
                    success_count += 1
                    progress.setValue(i + 1)
                    QApplication.processEvents()  # Update UI
                else:
                    break

            progress.close()

            # Refresh gallery and update display
            self.gallery_panel.refresh_gallery()
            self.update_stats_display()

            if success_count == count:
                QMessageBox.information(self, "Complete", f"Successfully generated {success_count} NFTs!")
            else:
                QMessageBox.information(self, "Complete",
                                        f"Generated {success_count} out of {count} NFTs. May have run out of unique combinations.")

    def generate_full_collection(self):
        if not self.check_project_loaded("generating full collection"):
            return

        # Check if we have artists with layers
        artists = self.project_manager.get_artists()
        has_layers = any(self.project_manager.get_artist_layer_count(artist) > 0 for artist in artists)
        if not has_layers:
            QMessageBox.warning(self, "No Layers", "Please add layers to artists before generating NFTs!")
            return

        stats = self.project_manager.get_generation_stats()
        remaining = stats['remaining_unique']

        if remaining <= 0:
            QMessageBox.information(self, "Complete", "All unique combinations have already been generated!")
            return

        reply = QMessageBox.question(self, "Generate Full Collection",
                                     f"Generate all {remaining:,} remaining unique combinations?\nThis may take a while.",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            progress = QProgressDialog(f"Generating {remaining} unique NFTs...", "Cancel", 0, remaining, self)
            progress.setWindowTitle("Generating Full Collection")
            progress.setStyleSheet("""
                QProgressDialog {
                    background: #232323;
                    color: #f0f0f0;
                }
                QLabel {
                    color: #f0f0f0;
                }
            """)
            progress.show()

            success_count = 0
            for i in range(remaining):
                if progress.wasCanceled():
                    break

                if self.project_manager.generate_single_nft():
                    success_count += 1
                    progress.setValue(i + 1)
                    QApplication.processEvents()
                else:
                    break

            progress.close()

            # Refresh gallery and update display
            self.gallery_panel.refresh_gallery()
            self.update_stats_display()

            QMessageBox.information(self, "Complete", f"Generated {success_count} new unique NFTs!")

    def copy_metadata(self):
        if not self.check_project_loaded("copying metadata"):
            return

        metadata_text = self.metadata_display.toPlainText()
        if metadata_text and metadata_text.strip():
            try:
                import pyperclip
                pyperclip.copy(metadata_text)
                QMessageBox.information(self, "Success", "Metadata copied to clipboard!")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to copy to clipboard: {e}")
        else:
            QMessageBox.warning(self, "No Metadata", "No metadata to copy. Generate an NFT first!")

    def on_gallery_nft_selected(self, nft_data):
        """When NFT is selected in gallery, update metadata display"""
        if nft_data and 'metadata' in nft_data:
            self.metadata_display.setPlainText(json.dumps(nft_data['metadata'], indent=2))

    def resizeEvent(self, event):
        """Handle resize events to adjust GIF size"""
        super().resizeEvent(event)
        if self.current_preview_movie:
            self.current_preview_movie.setScaledSize(self.preview_label.size())