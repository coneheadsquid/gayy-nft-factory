from PIL import Image, ImageChops
import os


def compose_layers(layer_composition):
    """
    Compose multiple layers into a single image or GIF based on z-index order
    All images are resized to 2000x2000px to ensure compatibility
    """
    if not layer_composition:
        # Return transparent canvas if no layers
        return Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))

    # Check if any layer is a GIF
    gif_layers = [layer for layer in layer_composition if layer['file_path'].lower().endswith('.gif')]

    if gif_layers:
        frames, durations = compose_gif_layers(layer_composition, gif_layers)
        return frames, durations
    else:
        return compose_static_layers(layer_composition)


def compose_static_layers(layer_composition):
    """Compose static PNG layers"""
    # Sort by z-index (lowest first)
    sorted_layers = sorted(layer_composition, key=lambda x: x['z_index'])

    # Start with transparent canvas
    canvas = Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))

    # Composite all layers
    for layer_config in sorted_layers:
        layer_image = load_and_prepare_layer(layer_config)
        canvas = apply_blend_mode(canvas, layer_image, layer_config)

    return canvas


def compose_gif_layers(layer_composition, gif_layers):
    """
    Compose layers where at least one is a GIF
    All output frames will be GIFs with the same number of frames as the longest GIF
    """
    # Find the maximum number of frames among all GIF layers
    max_frames = 1
    gif_data = {}

    for layer in gif_layers:
        try:
            gif = Image.open(layer['file_path'])
            frames = 0
            while True:
                frames += 1
                try:
                    gif.seek(frames)
                except EOFError:
                    break
            max_frames = max(max_frames, frames)
            gif_data[layer['file_path']] = frames
        except Exception as e:
            print(f"Error reading GIF {layer['file_path']}: {e}")
            gif_data[layer['file_path']] = 1

    # Sort all layers by z-index
    sorted_layers = sorted(layer_composition, key=lambda x: x['z_index'])

    # Create frames
    frames = []
    durations = []

    for frame_num in range(max_frames):
        # Start with transparent canvas for this frame
        canvas = Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))

        for layer_config in sorted_layers:
            layer_image = load_and_prepare_layer_for_frame(layer_config, frame_num, max_frames)
            if layer_image:
                canvas = apply_blend_mode(canvas, layer_image, layer_config)

        frames.append(canvas)
        # Use a default duration of 100ms for GIFs
        durations.append(100)

    return frames, durations


def load_and_prepare_layer_for_frame(layer_config, frame_num, max_frames):
    """Load appropriate frame for GIF layers, or static image for PNG layers"""
    file_path = layer_config['file_path']

    if file_path.lower().endswith('.gif'):
        return load_gif_frame(layer_config, frame_num, max_frames)
    else:
        return load_and_prepare_layer(layer_config)


def load_gif_frame(layer_config, frame_num, max_frames):
    """Load specific frame from GIF, handling looping for shorter GIFs"""
    try:
        gif = Image.open(layer_config['file_path'])

        # Get total frames in this GIF
        total_frames = 0
        while True:
            total_frames += 1
            try:
                gif.seek(total_frames)
            except EOFError:
                break

        # Calculate which frame to use (loop if necessary)
        frame_to_use = frame_num % total_frames

        # Seek to the appropriate frame
        gif.seek(frame_to_use)
        frame = gif.convert('RGBA')

        # Resize to 2000x2000
        frame = resize_image_to_2000x2000(frame)

        # Apply opacity
        opacity = layer_config.get('opacity', 1.0)
        if opacity < 1.0:
            alpha = frame.split()[3]
            alpha = alpha.point(lambda p: p * opacity)
            frame.putalpha(alpha)

        return frame

    except Exception as e:
        print(f"Error loading GIF frame {layer_config['file_path']}: {e}")
        return Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))


def load_and_prepare_layer(layer_config):
    """Load layer image, resize to 2000x2000, and apply opacity"""
    try:
        image = Image.open(layer_config['file_path']).convert('RGBA')

        # Resize image to 2000x2000 while maintaining aspect ratio
        image = resize_image_to_2000x2000(image)

        # Apply opacity
        opacity = layer_config.get('opacity', 1.0)
        if opacity < 1.0:
            # Create new image with adjusted alpha
            alpha = image.split()[3]
            alpha = alpha.point(lambda p: p * opacity)
            image.putalpha(alpha)

        return image
    except Exception as e:
        print(f"Error loading layer {layer_config['file_path']}: {e}")
        # Return transparent image as fallback
        return Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))


def resize_image_to_2000x2000(image):
    """
    Resize image to fit within 2000x2000 while maintaining aspect ratio
    and centering the image on a transparent background
    """
    if image.size == (2000, 2000):
        return image

    # Calculate the scaling factor to fit within 2000x2000
    original_width, original_height = image.size
    scale_x = 2000 / original_width
    scale_y = 2000 / original_height
    scale = min(scale_x, scale_y)  # Use the smaller scale to fit within bounds

    # Calculate new dimensions
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)

    # Resize the image
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Create a new 2000x2000 transparent canvas
    canvas = Image.new('RGBA', (2000, 2000), (0, 0, 0, 0))

    # Calculate position to center the image
    x_offset = (2000 - new_width) // 2
    y_offset = (2000 - new_height) // 2

    # Paste the resized image onto the canvas
    canvas.paste(resized_image, (x_offset, y_offset), resized_image)

    return canvas


def apply_blend_mode(background, foreground, layer_config):
    """Apply blend mode to combine layers"""
    blend_mode = layer_config.get('blend_mode', 'normal')

    if blend_mode == 'normal':
        return Image.alpha_composite(background, foreground)
    elif blend_mode == 'multiply':
        return multiply_blend(background, foreground)
    elif blend_mode == 'screen':
        return screen_blend(background, foreground)
    elif blend_mode == 'overlay':
        return overlay_blend(background, foreground)
    else:
        # Default to normal composite
        return Image.alpha_composite(background, foreground)


def multiply_blend(background, foreground):
    """Multiply blend mode"""
    # Ensure both images are the same size
    if background.size != foreground.size:
        foreground = foreground.resize(background.size, Image.Resampling.LANCZOS)
    return ImageChops.multiply(background, foreground)


def screen_blend(background, foreground):
    """Screen blend mode"""
    # Ensure both images are the same size
    if background.size != foreground.size:
        foreground = foreground.resize(background.size, Image.Resampling.LANCZOS)
    return ImageChops.screen(background, foreground)


def overlay_blend(background, foreground):
    """Overlay blend mode (simplified implementation)"""
    # Ensure both images are the same size
    if background.size != foreground.size:
        foreground = foreground.resize(background.size, Image.Resampling.LANCZOS)

    # This is a simplified overlay - for production use a proper implementation
    # Convert to RGB for blending, then back to RGBA
    bg_rgb = background.convert('RGB')
    fg_rgb = foreground.convert('RGB')

    # Simple overlay using Image.blend
    blended_rgb = Image.blend(bg_rgb, fg_rgb, 0.5)

    # Convert back to RGBA and preserve alpha from foreground
    alpha = foreground.split()[3]
    blended_rgba = blended_rgb.convert('RGBA')
    blended_data = blended_rgba.getdata()
    alpha_data = alpha.getdata()

    # Combine RGB from blended image with alpha from foreground
    final_data = [
        (r, g, b, a)
        for (r, g, b, _), a in zip(blended_data, alpha_data)
    ]

    result = Image.new('RGBA', background.size)
    result.putdata(final_data)

    return result


def get_gif_frame_count(file_path):
    """Get number of frames in a GIF file"""
    try:
        if file_path.lower().endswith('.gif'):
            gif = Image.open(file_path)
            frame_count = 0
            while True:
                frame_count += 1
                try:
                    gif.seek(frame_count)
                except EOFError:
                    break
            return frame_count
        else:
            return 1
    except Exception as e:
        print(f"Error getting GIF frame count for {file_path}: {e}")
        return 1