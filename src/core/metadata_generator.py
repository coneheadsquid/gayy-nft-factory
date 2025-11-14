import json


class MetadataGenerator:
    @staticmethod
    def generate_metadata(edition_number, layer_composition, project_info):
        attributes = []

        for layer in layer_composition:
            attributes.append({
                "trait_type": layer['artist'],  # Use artist name as trait_type
                "value": layer['display_name'],
                "opacity": layer.get('opacity', 1.0)  # Include opacity in metadata
            })

        return {
            "name": f"{project_info['name']} #{edition_number}",
            "description": project_info['description'],
            "image": f"{edition_number}.png",
            "attributes": attributes
        }