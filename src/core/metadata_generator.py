import json


class MetadataGenerator:
    @staticmethod
    def generate_metadata(edition_number, layer_composition, project_info):
        attributes = []

        # Check if any layer is a GIF
        has_gif = any(layer['file_path'].lower().endswith('.gif') for layer in layer_composition)

        for layer in layer_composition:
            attributes.append({
                "trait_type": layer['artist'],  # Use artist name as trait_type
                "value": layer['display_name'],
                "layer_index": layer.get('z_index', 1),  # Include layer index in metadata
                "file_type": "gif" if layer['file_path'].lower().endswith('.gif') else "png"
            })

        metadata = {
            "name": f"{project_info['name']} #{edition_number}",
            "description": project_info['description'],
            "attributes": attributes
        }

        # Set image field based on file type
        if has_gif:
            metadata["image"] = f"{edition_number}.gif"
            metadata["animation_url"] = f"{edition_number}.gif"
        else:
            metadata["image"] = f"{edition_number}.png"

        return metadata