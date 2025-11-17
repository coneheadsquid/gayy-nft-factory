import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                             QListWidgetItem, QLabel, QScrollArea, QSplitter)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QMovie


class GalleryPanel(QWidget):
    nft_selected = pyqtSignal(dict)  # Emit when NFT is selected

    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.current_movie = None  # Track current GIF movie
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("NFT Gallery")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px; color: #f0f0f0;")
        layout.addWidget(title)

        # Create splitter for gallery and preview
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter)

        # Left side - NFT list
        self.nft_list = QListWidget()
        self.nft_list.itemSelectionChanged.connect(self.on_nft_selected)
        self.nft_list.setStyleSheet("""
            QListWidget {
                background: #2d2d2d;
                color: #f0f0f0;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #3d3d3d;
            }
            QListWidget::item:selected {
                background: #2a82da;
                color: #f0f0f0;
            }
        """)
        splitter.addWidget(self.nft_list)

        # Right side - Preview area
        preview_widget = QWidget()
        preview_layout = QVBoxLayout(preview_widget)

        # Large preview
        self.large_preview = QLabel()
        self.large_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.large_preview.setMinimumSize(400, 400)
        self.large_preview.setStyleSheet("border: 2px solid #444444; background: #1a1a1a; color: #888888;")
        self.large_preview.setText("Select an NFT to preview")

        # NFT info
        self.nft_info = QLabel()
        self.nft_info.setWordWrap(True)
        self.nft_info.setStyleSheet(
            "background: #2d2d2d; padding: 10px; border: 1px solid #444444; border-radius: 4px; color: #f0f0f0;")

        preview_title = QLabel("Preview:")
        preview_title.setStyleSheet("color: #f0f0f0; font-weight: bold;")
        preview_layout.addWidget(preview_title)
        preview_layout.addWidget(self.large_preview)

        info_title = QLabel("Info:")
        info_title.setStyleSheet("color: #f0f0f0; font-weight: bold; margin-top: 10px;")
        preview_layout.addWidget(info_title)
        preview_layout.addWidget(self.nft_info)

        splitter.addWidget(preview_widget)

        # Set splitter proportions
        splitter.setSizes([300, 500])

    def refresh_gallery(self):
        """Refresh the gallery with all generated NFTs"""
        self.nft_list.clear()

        # Stop any currently playing GIF
        if self.current_movie:
            self.current_movie.stop()
            self.current_movie = None

        if not self.project_manager.is_project_loaded():
            self.nft_info.setText("No project loaded")
            return

        nfts = self.project_manager.get_all_generated_nfts()

        for nft in nfts:
            edition = nft['edition']
            metadata = nft['metadata']

            item_text = f"#{edition} - {metadata.get('name', 'Unknown')}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, nft)

            # Try to load thumbnail
            thumb_path = nft['image_path']
            if os.path.exists(thumb_path):
                if thumb_path.lower().endswith('.gif'):
                    # For GIFs, use first frame as thumbnail
                    try:
                        from PIL import Image
                        gif = Image.open(thumb_path)
                        gif.seek(0)
                        thumb = gif.copy()
                        thumb = thumb.convert('RGBA')
                        # Create thumbnail (50x50)
                        thumb = thumb.resize((50, 50), Image.Resampling.LANCZOS)
                        # Convert PIL Image to QPixmap
                        from PIL.ImageQt import ImageQt
                        qim = ImageQt(thumb)
                        pixmap = QPixmap.fromImage(qim)
                        icon = QIcon(pixmap)
                        item.setIcon(icon)
                    except Exception as e:
                        print(f"Error creating GIF thumbnail: {e}")
                else:
                    # For PNGs
                    pixmap = QPixmap(thumb_path)
                    if not pixmap.isNull():
                        # Create thumbnail (50x50)
                        thumb = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                                              Qt.TransformationMode.SmoothTransformation)
                        # Convert QPixmap to QIcon
                        icon = QIcon(thumb)
                        item.setIcon(icon)

            self.nft_list.addItem(item)

        # Update status
        if nfts:
            self.nft_info.setText(f"Loaded {len(nfts)} NFTs")
            # Select the first item if there are NFTs
            if self.nft_list.count() > 0:
                self.nft_list.setCurrentRow(0)
        else:
            self.nft_info.setText("No NFTs generated yet")

    def on_nft_selected(self):
        """When NFT is selected in the list"""
        current_item = self.nft_list.currentItem()
        if current_item:
            nft_data = current_item.data(Qt.ItemDataRole.UserRole)
            self.show_nft_preview(nft_data)
            self.nft_selected.emit(nft_data)

    def show_nft_preview(self, nft_data):
        """Show large preview of selected NFT"""
        image_path = nft_data['image_path']
        metadata = nft_data['metadata']

        # Stop any currently playing GIF
        if self.current_movie:
            self.current_movie.stop()
            self.current_movie = None

        if os.path.exists(image_path):
            if image_path.lower().endswith('.gif'):
                # Handle GIF preview with animation
                self.large_preview.setText("")  # Clear text
                self.current_movie = QMovie(image_path)
                self.current_movie.setScaledSize(self.large_preview.size())
                self.large_preview.setMovie(self.current_movie)
                self.current_movie.start()
            else:
                # Handle PNG preview
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    # Scale to fit preview area while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(380, 380, Qt.AspectRatioMode.KeepAspectRatio,
                                                  Qt.TransformationMode.SmoothTransformation)
                    self.large_preview.setPixmap(scaled_pixmap)
                    self.large_preview.setText("")  # Clear text when image is shown
                else:
                    self.large_preview.clear()
                    self.large_preview.setText("Failed to load image")
        else:
            self.large_preview.clear()
            self.large_preview.setText("Image file not found")

        # Show NFT info
        info_text = f"Edition: #{nft_data['edition']}\n"
        info_text += f"Name: {metadata.get('name', 'Unknown')}\n"
        info_text += f"File Type: {'GIF' if image_path.lower().endswith('.gif') else 'PNG'}\n"
        info_text += f"Attributes: {len(metadata.get('attributes', []))} traits\n"

        # Add attributes
        attributes = metadata.get('attributes', [])
        if attributes:
            info_text += "\nTraits:\n"
            for attr in attributes:
                file_type = attr.get('file_type', 'png')
                info_text += f"• {attr.get('trait_type', 'Unknown')}: {attr.get('value', 'Unknown')} ({file_type})\n"

        self.nft_info.setText(info_text)

    def resizeEvent(self, event):
        """Handle resize events to adjust GIF size"""
        super().resizeEvent(event)
        if self.current_movie:
            self.current_movie.setScaledSize(self.large_preview.size())