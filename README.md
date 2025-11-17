# gayy-nft-factory - Multi-Artist NFT Generator

![gayy-nft-factory UI](src/gui_layout.png)

gayy-nft-factory is a powerful desktop application that enables artists to collaborate on NFT collections by combining their individual layers into unique digital assets. Create Solana Metaplex-compatible NFT collections with an intuitive drag-and-drop interface.

## ✨ Features

- **🎨 Multi-Artist Collaboration**: Each artist contributes their own layers
- **🖱️ Drag & Drop Interface**: Easy layer management and upload
- **🎲 Automatic Combination Generation**: Creates unique NFTs from artist layers
- **⚡ Rarity System**: Control how common or rare each layer appears
- **🌊 Opacity Controls**: Adjust layer transparency for artistic effects
- **📐 Layer Stacking**: Control rendering order with layer indexes
- **🎬 GIF Animation Support**: Create animated NFTs with automatic frame synchronization
- **📱 Real-time Animated Preview**: See NFT combinations with full animation playback
- **🖼️ Gallery View**: Browse all generated NFTs with animated previews
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
   - Click "Upload Layers" or drag & drop PNG or GIF files
   - Each artist should upload their transparent PNG/GIF layers

4. **Configure Layer Settings**
   - **Rarity**: 1-10 scale (higher = more common)
   - **Opacity**: 0.0-1.0 scale (0.0 = transparent, 1.0 = fully opaque)
   - **Stack Order**: 1-20 scale (lower = rendered first/behind)
   - Adjust controls in the "Layer Settings" panel

5. **Generate NFTs**
   - **Generate Single**: Test with one NFT
   - **Generate Batch**: Create multiple at once
   - **Generate All Unique**: Create every possible combination

6. **View Your Collection**
   - Switch to "Gallery" tab to see all NFTs
   - Click any NFT to view animated preview and details
   - Copy metadata for marketplace use

### File Requirements

- **Format**: PNG or GIF with transparency
- **Size**: Any size (automatically resized to 2000x2000px)
- **Naming**: Use descriptive names (e.g., "forest_background.png", "sparkle_effect.gif")
- **GIF Frames**: All frames are automatically synchronized

### Project Structure
```
your_project/
├── assets/artists/
│   ├── artist1/
│   │   ├── layer1.png
│   │   ├── layer2.gif
│   │   └── layer3.png
│   └── artist2/
│       ├── layer1.gif
│       └── layer2.png
├── workspace/generated/
│   ├── 1.png
│   ├── 1.json
│   ├── 2.gif
│   ├── 2.json
│   └── ...
└── config/project.json
```

## 🎬 GIF Animation Support

### Automatic GIF Detection & Processing
- **Smart Detection**: System automatically detects when any layer is a GIF
- **Frame Synchronization**: All output NFTs become animated GIFs when any input layer is a GIF
- **Frame Count Matching**: Static PNG layers are converted to match the frame count of the longest GIF
- **Loop Optimization**: Shorter GIFs automatically loop to match longer animations

### How GIF Combinations Work
1. **Mixed Media Support**: Combine PNG and GIF layers in any combination
2. **Automatic Conversion**: When a GIF layer is included, all static layers become animated
3. **Frame Synchronization**: All layers are synchronized to the same frame rate
4. **Quality Preservation**: All frames maintain 2000x2000px resolution

### Example GIF Workflow
- **Background Artist**: Uploads static PNG backgrounds
- **Character Artist**: Uploads PNG character layers  
- **Effects Artist**: Uploads animated GIF overlays (sparkles, glow, etc.)
- **Result**: All generated NFTs become animated GIFs with synchronized effects

### Metadata for Animated NFTs
```json
{
  "name": "Collection Name #1",
  "description": "Collection description",
  "image": "1.gif",
  "animation_url": "1.gif",
  "attributes": [
    {
      "trait_type": "Background Artist",
      "value": "Cosmic Nebula",
      "file_type": "png",
      "layer_index": 1
    },
    {
      "trait_type": "Character Artist",
      "value": "Cyber Warrior", 
      "file_type": "png",
      "layer_index": 3
    },
    {
      "trait_type": "Effects Artist",
      "value": "Magic Sparkles",
      "file_type": "gif",
      "layer_index": 5
    }
  ]
}
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
- **Works with GIFs**: Opacity applies to all frames of animated layers

### Stacking Order (Layer Index)
- **Layer Index**: 1-20 scale (lower = rendered first/behind, higher = rendered last/in front)
- Controls the stacking order of layers in the final NFT
- Layers are automatically sorted by index before composition
- Example: Background layers should have lower indexes (1-3), foreground elements higher indexes (4-6)

### Complete Layer Settings
Each layer has three controls:
- **Rarity**: How often the layer appears (1-10)
- **Opacity**: Layer transparency (0.0-1.0)  
- **Stack Order**: Rendering order (1-20)

## 🎯 Best Practices

### For Artists
- **PNG Layers**: Create layers with transparent backgrounds
- **GIF Layers**: Use for animated effects, transitions, or moving elements
- **Consistent Styles**: Maintain consistent art styles within layers
- **High Quality**: Use high-quality source images (2000x2000px recommended)
- **Clear Naming**: Name files clearly for easy identification
- **Stacking Order**: Consider stacking order when designing layers

### For GIF-Specific Tips
- **Frame Optimization**: Keep GIFs under 50 frames for optimal performance
- **Looping Effects**: Design effects that loop seamlessly
- **File Size**: Optimize GIFs to balance quality and file size
- **Transparency**: Use transparent backgrounds for overlay effects
- **Timing**: Consider animation speed when combining multiple GIFs

### For Project Managers
- **Start Small**: Begin with 2-3 artists for testing
- **Layer Balance**: Each artist should have 3-7 layers
- **Test Batches**: Test combinations with small batches first
- **Rarity Planning**: Use rarity settings to create common and rare traits
- **Opacity Experiments**: Experiment with opacity for unique visual effects
- **Stacking Strategy**: Plan layer stacking order for optimal composition

### Example Animated Collection
- **Background Artist**: 5 environment layers (Layer Index: 1-2)
- **Character Artist**: 4 character designs (Layer Index: 3-4)  
- **Accessory Artist**: 3 item layers (Layer Index: 5-6)
- **Effects Artist**: 2 animated GIF overlays (Layer Index: 7-8)
- **Total Combinations**: 5 × 4 × 3 × 2 = **120 unique animated NFTs**

### Example Stacking Strategy
- **Backgrounds**: Layer Index 1-2 (PNG)
- **Base Characters**: Layer Index 3-4 (PNG)
- **Clothing/Armor**: Layer Index 5-6 (PNG)
- **Accessories**: Layer Index 7-8 (PNG or GIF)
- **Effects/Overlays**: Layer Index 9-10 (GIF for animations)

## 🔧 Troubleshooting

### Common Issues

**Application won't start:**
- Verify Python installation and PATH
- Check all dependencies are installed
- Ensure all project files are present

**Image generation errors:**
- Use PNG or GIF format with transparency
- Check file permissions and paths
- Verify images aren't corrupted

**GIF preview not animating:**
- Check that GIF files are valid and not corrupted
- Ensure PyQt6 is properly installed
- Try generating a single NFT first to test GIF functionality

**No combinations generated:**
- Ensure artists have layers uploaded
- Check that layer files exist in project folder
- Verify at least two artists have layers

**Preview not working:**
- Check console for error messages
- Verify image files are valid PNGs/GIFs
- Try generating a single NFT first

**Layers stacking incorrectly:**
- Check layer index settings for each artist
- Lower numbers render first (behind other layers)
- Higher numbers render last (in front of other layers)

**GIF performance issues:**
- Reduce number of frames in source GIFs
- Optimize GIF file sizes
- Consider using smaller batches for generation

### Getting Help
1. Check the console for error messages
2. Verify all installation steps were followed
3. Test with simple PNG files first, then add GIFs
4. Create a new project if issues persist
5. Review layer index settings if stacking order is wrong
6. For GIF issues, test with smaller GIF files first

## 📊 Understanding Statistics

- **Possible Combinations**: Total unique NFTs possible with current layers
- **Generated Count**: Number of NFTs created so far
- **Unique Combinations**: Actually different NFTs generated
- **Remaining Unique**: How many more unique NFTs can be created
- **File Types**: Track how many PNG vs GIF NFTs were generated

## 🎨 Creative Tips

### Using Opacity Effectively
- **Subtle Overlays**: Use low opacity (0.1-0.3) for texture layers
- **Color Tinting**: Apply colored layers with medium opacity (0.4-0.6)
- **Glow Effects**: Create light effects with high opacity (0.7-0.9)
- **Layering**: Combine multiple transparent layers for complex effects

### GIF Animation Strategies
- **Background Animations**: Use subtle animated backgrounds (water, clouds, stars)
- **Character Effects**: Add blinking eyes, breathing motions, or idle animations
- **Overlay Magic**: Create sparkle, glow, or particle effects as GIF overlays
- **Transition Effects**: Use GIFs for scene transitions or special effects
- **Frame Coordination**: Plan animations that work well together when combined

### Stacking Order Strategies
- **Background First**: Set backgrounds to lowest indexes (1-2)
- **Character Middle**: Place main characters in middle range (3-5)
- **Accessories Forward**: Put hats, glasses, etc. at higher indexes (6-8)
- **Effects on Top**: Reserve highest indexes for overlays and effects (9-10+)

### Rarity Strategies
- **Common Traits**: Set rarity 8-10 for base layers
- **Uncommon Traits**: Set rarity 4-7 for interesting variations  
- **Rare Traits**: Set rarity 1-3 for special, sought-after layers
- **Legendary**: Combine low rarity with unique opacity and animated effects

## 🎉 What's Next?

After generating your collection:
1. Review all NFTs in the Gallery tab with animated previews
2. Check layer stacking and animation synchronization
3. Copy metadata for each NFT as needed
4. Use the numbered files for minting on platforms like Solana
5. Share your unique multi-artist animated creations!

---

**Create something amazing with gayy-nft-factory!** 🚀

*Where artists collaborate and layers unite to create unique digital collectibles - now with animated GIF support!*

**Happy NFT Creating!** 🎨✨🎬

---

### Version 2.0 Highlights
- ✅ **Full GIF Animation Support**
- ✅ **Automatic Frame Synchronization** 
- ✅ **Animated Previews in Gallery**
- ✅ **Mixed PNG/GIF Layer Combinations**
- ✅ **Optimized 2000x2000px Resolution**
- ✅ **Enhanced Metadata for Animated NFTs**

*Upgrade your NFT collections with dynamic animations and bring your digital art to life!*