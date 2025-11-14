import json


class MetadataGenerator:
    @staticmethod
    def generate_metadata(edition_number, layer_composition, project_info):
        attributes = []

        for i, layer in enumerate(layer_composition, 1):
            attributes.append({
                "trait_type": f"Layer {i}",
                "value": layer['display_name']
            })

        return {
            "name": f"{project_info['name']} #{edition_number}",
            "description": project_info['description'],
            "image": f"{edition_number}.png",
            "attributes": attributes
        }