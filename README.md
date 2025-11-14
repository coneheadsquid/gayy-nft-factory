# gayy-nft-factory - Multi-Artist NFT Generator

![gayy-nft-factory UI](src/gui_layout.png)

gayy-nft-factory is a powerful desktop application that enables artists to collaborate on NFT collections by combining their individual layers into unique digital assets. Create Solana Metaplex-compatible NFT collections with an intuitive drag-and-drop interface.

## ✨ Features

- **🎨 Multi-Artist Collaboration**: Each artist contributes their own layers
- **🖱️ Drag & Drop Interface**: Easy layer management and upload
- **🎲 Automatic Combination Generation**: Creates unique NFTs from artist layers
- **⚡ Rarity System**: Control how common or rare each layer appears
- **🌊 Opacity Controls**: Adjust layer transparency for artistic effects
- **📱 Real-time Preview**: See NFT combinations before generating
- **🖼️ Gallery View**: Browse all generated NFTs with metadata
- **💾 Project Persistence**: Save and resume your work anytime
- **🌙 Dark Theme**: Comfortable dark mode interface
- **📊 Generation Statistics**: Track combinations and uniqueness

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or newer
- Windows, macOS, or Linux

### Installation

1. **Download Python** (if not installed):
   - Visit [python.org](https://www.python.org/downloads/)
   - Download Python 3.8+ and install with "Add to PATH" option

2. **Get the Application**:
   ```bash
   # Download and extract the project files
   cd gayy-nft-factory
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python main.py
   ```

## 📖 User Guide

### Creating Your First Project

1. **Start a New Project**
   - Click "New Project"
   - Choose a folder for your project files
   - Name your collection

2. **Add Artists**
   - Click "Add Artist" for each collaborator
   - Name them clearly (e.g., "Background Artist", "Character Artist")

3. **Upload Layers**
   - Select an artist
   - Click "Upload Layers" or drag & drop PNG files
   - Each artist should upload their transparent PNG layers

4. **Configure Layer Settings**
   - **Rarity**: 1-10 scale (higher = more common)
   - **Opacity**: 0.0-1.0 scale (0.0 = transparent, 1.0 = fully opaque)
   - Adjust sliders in the "Layer Settings" panel

5. **Generate NFTs**
   - **Generate Single**: Test with one NFT
   - **Generate Batch**: Create multiple at once
   - **Generate All Unique**: Create every possible combination

6. **View Your Collection**
   - Switch to "Gallery" tab to see all NFTs
   - Click any NFT to view details and metadata
   - Copy metadata for marketplace use

### File Requirements

- **Format**: PNG with transparency
- **Size**: Any size (automatically resized to 2000x2000px)
- **Naming**: Use descriptive names (e.g., "forest_background.png")

### Project Structure
```
your_project/
├── assets/artists/
│   ├── artist1/
│   │   ├── layer1.png
│   │   └── layer2.png
│   └── artist2/
│       └── layer1.png
├── workspace/generated/
│   ├── 1.png
│   ├── 1.json
│   └── ...
└── config/project.json
```

## 🎛️ Layer Settings

### Rarity Controls
- **Rarity Weight**: 1-10 scale (higher = more common)
- Controls how often each layer appears in generation
- Example: Rarity 10 appears 10x more often than Rarity 1

### Opacity Controls  
- **Opacity**: 0.0-1.0 scale (0.0 = fully transparent, 1.0 = fully opaque)
- Adjust layer transparency for artistic effects
- Perfect for creating overlay effects, glows, and subtle textures

### Metadata Structure
```json
{
  "name": "Collection Name #1",
  "description": "Collection description", 
  "image": "1.png",
  "attributes": [
    {
      "trait_type": "Background Artist",
      "value": "Cosmic Nebula"
      },
    {
      "trait_type": "Character Artist", 
      "value": "Cyber Warrior"
    }
  ]
}
```

## 🎯 Best Practices

### For Artists
- Create layers with transparent backgrounds
- Maintain consistent art styles within layers
- Use high-quality source images (2000x2000px recommended)
- Name files clearly for easy identification

### For Project Managers
- Start with 2-3 artists for testing
- Each artist should have 3-7 layers
- Test combinations with small batches first
- Use rarity settings to create common and rare traits
- Experiment with opacity for unique visual effects

### Example Collection
- **Background Artist**: 5 environment layers
- **Character Artist**: 4 character designs  
- **Effects Artist**: 3 overlay layers with varying opacity
- **Total Combinations**: 5 × 4 × 3 = **60 unique NFTs**

## 🔧 Troubleshooting

### Common Issues

**Application won't start:**
- Verify Python installation and PATH
- Check all dependencies are installed
- Ensure all project files are present

**Image generation errors:**
- Use PNG format with transparency
- Check file permissions and paths
- Verify images aren't corrupted

**No combinations generated:**
- Ensure artists have layers uploaded
- Check that layer files exist in project folder
- Verify at least two artists have layers

**Preview not working:**
- Check console for error messages
- Verify image files are valid PNGs
- Try generating a single NFT first

### Getting Help
1. Check the console for error messages
2. Verify all installation steps were followed
3. Test with simple PNG files first
4. Create a new project if issues persist

## 📊 Understanding Statistics

- **Possible Combinations**: Total unique NFTs possible with current layers
- **Generated Count**: Number of NFTs created so far
- **Unique Combinations**: Actually different NFTs generated
- **Remaining Unique**: How many more unique NFTs can be created

## 🎨 Creative Tips

### Using Opacity Effectively
- **Subtle Overlays**: Use low opacity (0.1-0.3) for texture layers
- **Color Tinting**: Apply colored layers with medium opacity (0.4-0.6)
- **Glow Effects**: Create light effects with high opacity (0.7-0.9)
- **Layering**: Combine multiple transparent layers for complex effects

### Rarity Strategies
- **Common Traits**: Set rarity 8-10 for base layers
- **Uncommon Traits**: Set rarity 4-7 for interesting variations  
- **Rare Traits**: Set rarity 1-3 for special, sought-after layers
- **Legendary**: Combine low rarity with unique opacity effects

## 🎉 What's Next?

After generating your collection:
1. Review all NFTs in the Gallery tab
2. Copy metadata for each NFT as needed
3. Use the numbered files for minting on platforms like Solana
4. Share your unique multi-artist creations!

---

**Create something amazing with gayy-nft-factory!** 🚀

*Where artists collaborate and layers unite to create unique digital collectibles.*

**Happy NFT Creating!** 🎨✨