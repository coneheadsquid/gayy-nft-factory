import os
import json
import shutil
import random
from datetime import datetime
from ..utils.file_utils import ensure_directory
from ..utils.image_utils import compose_layers, resize_image_to_2000x2000
from .metadata_generator import MetadataGenerator


class ProjectManager:
    def __init__(self):
        self.project_path = None
        self.project_data = {
            'project_info': {},
            'artists': {},
            'artist_order': [],  # Track the order artists are added
            'generation_settings': {},
            'generation_state': {}
        }
        self.generated_combinations = set()

    def create_new_project(self, project_path, collection_name):
        self.project_path = project_path
        self.project_data = {
            'project_info': {
                'name': collection_name,
                'symbol': collection_name[:10].upper(),
                'description': f'A collaborative NFT collection by multiple artists',
                'total_size': 10000,
                'created_date': datetime.now().isoformat(),
                'last_modified': datetime.now().isoformat()
            },
            'artists': {},
            'artist_order': [],  # Track the order artists are added
            'generation_settings': {
                'auto_generate': True,
                'max_attempts': 1000,
                'ensure_uniqueness': True
            },
            'generation_state': {
                'current_edition': 0,
                'generated_count': 0,
                'total_required': 10000,
                'unique_combinations': 0
            }
        }

        # Create directory structure
        ensure_directory(os.path.join(project_path, 'config'))
        ensure_directory(os.path.join(project_path, 'assets', 'artists'))
        ensure_directory(os.path.join(project_path, 'workspace', 'generated'))
        ensure_directory(os.path.join(project_path, 'workspace', 'previews'))

        return self.save_project()

    def load_project(self, project_path):
        self.project_path = project_path
        config_file = os.path.join(project_path, 'config', 'project.json')

        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.project_data = json.load(f)
                # Load existing combinations for uniqueness checking
                self.load_generated_combinations()
                return True
            except Exception as e:
                print(f"Error loading project: {e}")
                return False
        return False

    def save_project(self):
        if not self.project_path:
            return False

        try:
            self.project_data['project_info']['last_modified'] = datetime.now().isoformat()

            config_file = os.path.join(self.project_path, 'config', 'project.json')
            with open(config_file, 'w') as f:
                json.dump(self.project_data, f, indent=2)

            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False

    def add_artist(self, artist_name):
        if not self.project_path:
            return False

        if artist_name in self.project_data['artists']:
            return False

        self.project_data['artists'][artist_name] = {
            'name': artist_name,
            'display_name': artist_name,
            'layers': [],
            'rarity_weights': {},
            'layer_index': len(self.project_data['artist_order']) + 1  # Auto-assign layer index
        }

        # Add to artist order
        self.project_data['artist_order'].append(artist_name)

        # Create artist directory
        artist_dir = os.path.join(self.project_path, 'assets', 'artists', artist_name)
        ensure_directory(artist_dir)

        return self.save_project()

    def remove_artist(self, artist_name):
        if not self.project_path:
            return False

        if artist_name in self.project_data['artists']:
            # Remove from artist order
            if artist_name in self.project_data['artist_order']:
                self.project_data['artist_order'].remove(artist_name)

            # Update layer indexes for remaining artists
            for i, remaining_artist in enumerate(self.project_data['artist_order']):
                self.project_data['artists'][remaining_artist]['layer_index'] = i + 1
                # Update all layers for this artist
                for layer in self.project_data['artists'][remaining_artist]['layers']:
                    layer['layer_index'] = i + 1

            del self.project_data['artists'][artist_name]

            # Remove artist directory
            artist_dir = os.path.join(self.project_path, 'assets', 'artists', artist_name)
            if os.path.exists(artist_dir):
                shutil.rmtree(artist_dir)

            return self.save_project()
        return False

    def add_layer_to_artist(self, artist_name, source_file_path):
        if not self.project_path:
            return False

        if artist_name not in self.project_data['artists']:
            return False

        try:
            # Validate the image file
            try:
                from PIL import Image
                with Image.open(source_file_path) as img:
                    img.verify()  # Verify it's a valid image
            except Exception as e:
                print(f"Invalid image file: {source_file_path}, error: {e}")
                return False

            # Copy file to artist directory
            file_name = os.path.basename(source_file_path)
            artist_dir = os.path.join(self.project_path, 'assets', 'artists', artist_name)
            dest_path = os.path.join(artist_dir, file_name)

            shutil.copy2(source_file_path, dest_path)

            # Get the artist's layer index for default
            artist_index = self.project_data['artists'][artist_name].get('layer_index', 1)

            # Add to project data with default settings
            layer_data = {
                'file_name': file_name,
                'display_name': os.path.splitext(file_name)[0].replace('_', ' ').title(),
                'file_path': dest_path,
                'rarity_weight': 1.0,  # Default rarity
                'opacity': 1.0,  # Default opacity (fully opaque)
                'layer_index': artist_index  # Use artist's layer index as default
            }

            self.project_data['artists'][artist_name]['layers'].append(layer_data)
            self.project_data['artists'][artist_name]['rarity_weights'][file_name] = 1.0

            return self.save_project()

        except Exception as e:
            print(f"Error adding layer: {e}")
            return False

    def set_layer_rarity(self, artist_name, layer_name, rarity_weight):
        """Set rarity weight for a specific layer"""
        if artist_name in self.project_data['artists']:
            self.project_data['artists'][artist_name]['rarity_weights'][layer_name] = rarity_weight
            # Update the layer data as well
            for layer in self.project_data['artists'][artist_name]['layers']:
                if layer['file_name'] == layer_name:
                    layer['rarity_weight'] = rarity_weight
            return self.save_project()
        return False

    def set_layer_opacity(self, artist_name, layer_name, opacity):
        """Set opacity for a specific layer"""
        if artist_name in self.project_data['artists']:
            # Update the layer data
            for layer in self.project_data['artists'][artist_name]['layers']:
                if layer['file_name'] == layer_name:
                    layer['opacity'] = opacity
            return self.save_project()
        return False

    def set_layer_index(self, artist_name, layer_name, layer_index):
        """Set layer index (z-index) for a specific layer - override the default"""
        if artist_name in self.project_data['artists']:
            # Update the layer data
            for layer in self.project_data['artists'][artist_name]['layers']:
                if layer['file_name'] == layer_name:
                    layer['layer_index'] = layer_index
            return self.save_project()
        return False

    def get_layer_opacity(self, artist_name, layer_name):
        """Get opacity for a specific layer"""
        artist = self.get_artist(artist_name)
        if artist:
            for layer in artist['layers']:
                if layer['file_name'] == layer_name:
                    return layer.get('opacity', 1.0)
        return 1.0

    def get_layer_index(self, artist_name, layer_name):
        """Get layer index for a specific layer"""
        artist = self.get_artist(artist_name)
        if artist:
            for layer in artist['layers']:
                if layer['file_name'] == layer_name:
                    return layer.get('layer_index', 1)
        return 1

    def get_artist_layer_index(self, artist_name):
        """Get the default layer index for an artist"""
        artist = self.get_artist(artist_name)
        if artist:
            return artist.get('layer_index', 1)
        return 1

    def set_artist_layer_index(self, artist_name, layer_index):
        """Set the default layer index for an artist and update all their layers"""
        if artist_name in self.project_data['artists']:
            self.project_data['artists'][artist_name]['layer_index'] = layer_index

            # Update all layers for this artist
            for layer in self.project_data['artists'][artist_name]['layers']:
                layer['layer_index'] = layer_index

            return self.save_project()
        return False

    def get_artists(self):
        return list(self.project_data['artists'].keys())

    def get_artist(self, artist_name):
        return self.project_data['artists'].get(artist_name)

    def get_artist_layer_count(self, artist_name):
        """Get number of layers for an artist"""
        artist = self.get_artist(artist_name)
        return len(artist['layers']) if artist else 0

    def generate_random_combination(self):
        """Generate a random combination of layers (one per artist)"""
        if not self.project_path or not self.project_data['artists']:
            return None, None

        combination = {}
        combination_key_parts = []

        # Filter artists that actually have layers
        artists_with_layers = {
            name: data for name, data in self.project_data['artists'].items()
            if data['layers']
        }

        if not artists_with_layers:
            return None, None

        for artist_name, artist_data in artists_with_layers.items():
            layers = artist_data['layers']
            if layers:
                # Select random layer based on rarity weights
                weights = [layer.get('rarity_weight', 1.0) for layer in layers]
                selected_layer = random.choices(layers, weights=weights)[0]

                # Include all settings in the combination
                combination[artist_name] = {
                    'file_name': selected_layer['file_name'],
                    'display_name': selected_layer['display_name'],
                    'file_path': selected_layer['file_path'],
                    'opacity': selected_layer.get('opacity', 1.0),
                    'layer_index': selected_layer.get('layer_index', 1)  # Include layer index
                }
                combination_key_parts.append(f"{artist_name}:{selected_layer['file_name']}")

        combination_key = "|".join(sorted(combination_key_parts))
        return combination, combination_key

    def is_combination_unique(self, combination_key):
        """Check if combination has been used before"""
        return combination_key not in self.generated_combinations

    def register_combination(self, combination_key, edition_number):
        """Register a combination as used"""
        self.generated_combinations.add(combination_key)
        # Save to file for persistence
        combinations_file = os.path.join(self.project_path, 'workspace', 'generated_combinations.txt')
        ensure_directory(os.path.dirname(combinations_file))
        with open(combinations_file, 'a') as f:
            f.write(f"{combination_key}|{edition_number}\n")

    def load_generated_combinations(self):
        """Load previously generated combinations from file"""
        combinations_file = os.path.join(self.project_path, 'workspace', 'generated_combinations.txt')
        self.generated_combinations = set()

        if os.path.exists(combinations_file):
            with open(combinations_file, 'r') as f:
                for line in f:
                    combination_key = line.split('|')[0]
                    self.generated_combinations.add(combination_key)

    def generate_single_nft(self):
        if not self.project_path:
            return False

        try:
            # Get next edition number
            edition = self.project_data['generation_state']['current_edition'] + 1

            # Generate unique combination
            max_attempts = self.project_data['generation_settings'].get('max_attempts', 1000)
            ensure_uniqueness = self.project_data['generation_settings'].get('ensure_uniqueness', True)

            combination = None
            combination_key = None

            # Check if we have any artists with layers
            artists_with_layers = {
                name: data for name, data in self.project_data['artists'].items()
                if data['layers']
            }

            if not artists_with_layers:
                print("No artists with layers found!")
                return False

            for attempt in range(max_attempts):
                combination, combination_key = self.generate_random_combination()

                if combination is None:
                    print("Failed to generate combination")
                    return False

                # Verify all layer files exist
                all_files_exist = all(os.path.exists(layer_data['file_path']) for layer_data in combination.values())
                if not all_files_exist:
                    print("Some layer files are missing, trying another combination...")
                    continue

                if not ensure_uniqueness or self.is_combination_unique(combination_key):
                    break
            else:
                print(f"Failed to generate unique combination after {max_attempts} attempts")
                return False

            # Generate NFT files
            nft_path = os.path.join(self.project_path, 'workspace', 'generated', f'{edition}.png')
            metadata_path = os.path.join(self.project_path, 'workspace', 'generated', f'{edition}.json')

            ensure_directory(os.path.dirname(nft_path))

            # Convert combination to layer composition format
            layer_composition = []
            for artist_name, layer_data in combination.items():
                layer_composition.append({
                    'artist': artist_name,
                    'layer_name': layer_data['file_name'],
                    'display_name': layer_data['display_name'],
                    'file_path': layer_data['file_path'],
                    'z_index': layer_data.get('layer_index', 1),  # Use layer index for z-index
                    'blend_mode': 'normal',
                    'opacity': layer_data.get('opacity', 1.0)
                })

            # Sort by layer index (z-index) - lower numbers rendered first
            layer_composition.sort(key=lambda x: x['z_index'])

            # Generate image
            print(f"Generating NFT #{edition} with {len(layer_composition)} layers...")
            nft_image = compose_layers(layer_composition)
            nft_image.save(nft_path, 'PNG')
            print(f"Successfully saved NFT image to {nft_path}")

            # Generate metadata
            metadata = MetadataGenerator.generate_metadata(
                edition,
                layer_composition,
                self.project_data['project_info']
            )

            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            # Register combination and update state
            if ensure_uniqueness:
                self.register_combination(combination_key, edition)

            self.project_data['generation_state']['current_edition'] = edition
            self.project_data['generation_state']['generated_count'] += 1
            self.project_data['generation_state']['unique_combinations'] = len(self.generated_combinations)
            self.save_project()

            return True

        except Exception as e:
            print(f"Error generating single NFT: {e}")
            import traceback
            traceback.print_exc()
            return False

    def generate_batch_nfts(self, count):
        if not self.project_path:
            return False

        success_count = 0
        for i in range(count):
            if self.generate_single_nft():
                success_count += 1
            else:
                break

        return success_count

    def get_possible_combinations_count(self):
        """Calculate total possible unique combinations"""
        if not self.project_data['artists']:
            return 0

        total_combinations = 1
        for artist_name, artist_data in self.project_data['artists'].items():
            layer_count = len(artist_data['layers'])
            if layer_count > 0:
                total_combinations *= layer_count

        return total_combinations

    def get_generation_stats(self):
        """Get generation statistics"""
        possible = self.get_possible_combinations_count()
        generated = self.project_data['generation_state']['generated_count']
        unique = self.project_data['generation_state']['unique_combinations']

        return {
            'possible_combinations': possible,
            'generated_count': generated,
            'unique_combinations': unique,
            'remaining_unique': possible - unique if possible > unique else 0
        }

    def generate_preview_for_combination(self, combination):
        """Generate preview for a specific combination"""
        if not self.project_path:
            return None

        try:
            preview_path = os.path.join(self.project_path, 'workspace', 'previews', 'combination_preview.png')
            ensure_directory(os.path.dirname(preview_path))

            # Convert combination to layer composition format
            layer_composition = []
            for artist_name, layer_data in combination.items():
                # Check if file exists before adding to composition
                if os.path.exists(layer_data['file_path']):
                    layer_composition.append({
                        'artist': artist_name,
                        'layer_name': layer_data['file_name'],
                        'display_name': layer_data['display_name'],
                        'file_path': layer_data['file_path'],
                        'z_index': layer_data.get('layer_index', 1),  # Use layer index for z-index
                        'blend_mode': 'normal',
                        'opacity': layer_data.get('opacity', 1.0)
                    })

            if not layer_composition:
                print("No valid layers found for preview")
                return None

            # Sort by layer index (z-index) - lower numbers rendered first
            layer_composition.sort(key=lambda x: x['z_index'])

            # Compose image
            result_image = compose_layers(layer_composition)
            result_image.save(preview_path, 'PNG')

            return preview_path
        except Exception as e:
            print(f"Error generating preview: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_all_generated_nfts(self):
        """Get list of all generated NFTs with their metadata"""
        if not self.project_path:
            return []

        generated_dir = os.path.join(self.project_path, 'workspace', 'generated')
        if not os.path.exists(generated_dir):
            return []

        nfts = []
        # Get all PNG files
        for file_name in os.listdir(generated_dir):
            if file_name.endswith('.png'):
                edition = file_name.split('.')[0]
                metadata_path = os.path.join(generated_dir, f"{edition}.json")
                image_path = os.path.join(generated_dir, file_name)

                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        nfts.append({
                            'edition': edition,
                            'image_path': image_path,
                            'metadata': metadata
                        })
                    except Exception as e:
                        print(f"Error loading metadata for {edition}: {e}")

        # Sort by edition number
        nfts.sort(key=lambda x: int(x['edition']))
        return nfts

    def get_latest_preview(self):
        if not self.project_path:
            return None
        preview_path = os.path.join(self.project_path, 'workspace', 'previews', 'current_preview.png')
        return preview_path if os.path.exists(preview_path) else None

    def get_latest_metadata(self):
        if not self.project_path:
            return {}
        edition = self.project_data['generation_state']['current_edition']
        if edition > 0:
            metadata_path = os.path.join(self.project_path, 'workspace', 'generated', f'{edition}.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    return json.load(f)
        return {}

    def is_project_loaded(self):
        """Check if a project is currently loaded"""
        return self.project_path is not None

    def resize_all_layers_to_2000x2000(self):
        """Resize all existing layer images to 2000x2000px"""
        if not self.project_path:
            return False

        try:
            from PIL import Image

            resized_count = 0
            for artist_name, artist_data in self.project_data['artists'].items():
                for layer in artist_data['layers']:
                    file_path = layer['file_path']
                    if os.path.exists(file_path):
                        try:
                            with Image.open(file_path) as img:
                                if img.size != (2000, 2000):
                                    resized_img = resize_image_to_2000x2000(img)
                                    resized_img.save(file_path, 'PNG')
                                    resized_count += 1
                                    print(f"Resized {file_path} to 2000x2000")
                        except Exception as e:
                            print(f"Error resizing {file_path}: {e}")

            print(f"Resized {resized_count} images to 2000x2000px")
            return True

        except Exception as e:
            print(f"Error in resize_all_layers_to_2000x2000: {e}")
            return False

    def validate_all_layer_files(self):
        """Validate that all layer files exist and are accessible"""
        if not self.project_path:
            return False

        missing_files = []
        corrupted_files = []

        for artist_name, artist_data in self.project_data['artists'].items():
            for layer in artist_data['layers']:
                file_path = layer['file_path']
                if not os.path.exists(file_path):
                    missing_files.append(file_path)
                else:
                    try:
                        from PIL import Image
                        with Image.open(file_path) as img:
                            img.verify()
                    except Exception as e:
                        corrupted_files.append((file_path, str(e)))

        if missing_files:
            print(f"Missing files: {missing_files}")
        if corrupted_files:
            print(f"Corrupted files: {corrupted_files}")

        return len(missing_files) == 0 and len(corrupted_files) == 0

    def get_artist_layer_info(self, artist_name):
        """Get detailed information about an artist's layers"""
        artist = self.get_artist(artist_name)
        if not artist:
            return []

        layer_info = []
        for layer in artist['layers']:
            layer_info.append({
                'file_name': layer['file_name'],
                'display_name': layer['display_name'],
                'rarity_weight': layer.get('rarity_weight', 1.0),
                'opacity': layer.get('opacity', 1.0),
                'layer_index': layer.get('layer_index', 1),
                'file_path': layer['file_path'],
                'file_exists': os.path.exists(layer['file_path'])
            })

        return layer_info