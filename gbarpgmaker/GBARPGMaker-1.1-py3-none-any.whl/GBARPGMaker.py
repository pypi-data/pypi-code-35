from xml.dom.minidom import parse
from wand.image import Image
from jinja2 import Environment, FileSystemLoader
import os
from GBARPGMaker.helper_functions import get_lowest_option, SHAPE_SIZE_DICTIONARY


class WrongImageError(Exception):
    def __init__(self, message):
        super(WrongImageError, self).__init__(message)


class WrongConfigError(Exception):
    def __init__(self, message):
        super(WrongConfigError, self).__init__(message)


class GBARPGMaker:
    def __init__(self, config):
        self.config = config

        self.maps = {}
        for map_ in config.maps:
            self.maps[map_] = Map(config.maps[map_])

        self.sprite_graphics = {}
        for sprite_graphic in config.sprite_graphics:
            self.sprite_graphics[sprite_graphic] = SpriteGraphic(config.sprite_graphics[sprite_graphic])

        try:
            if config.targets:
                self.targets = config.targets
            else:
                raise AttributeError
        except AttributeError:
            self.targets = ["imageData.c", "imageData.h", "graphics.c", "graphics.h"]
        try:
            if config.excluded_targets:
                self.targets = [i for i in self.targets if i not in config.excluded_targets]
        except AttributeError:
            pass

        self.jinja_env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.realpath(__file__)), "jinja_templates")))

    def parse(self):
        for map_ in self.maps:
            print("Parsing map:\"" + map_ + "\"")
            self.maps[map_].parse()
        for sprite_graphic in self.sprite_graphics:
            print("Parsing sprite_graphic:\"" + sprite_graphic + "\"")
            self.sprite_graphics[sprite_graphic].parse()

    def write_file(self, filename, output_folder, context):
        print("Making \"" + filename + "\"")

        rendered_file = self.jinja_env.get_template(filename).render(context)

        with open(output_folder + "/" + filename, 'w') as f:
            f.write(rendered_file)

    def make_game(self):
        self.parse()
        context = {
            "maps": self.maps,
            "sprite_graphics": self.sprite_graphics
            }
        output_folder = "./source"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for target in self.targets:
            self.write_file(target, output_folder, context)


class SpriteGraphic:
    def __init__(self, sprite_graphic_config):
        self.image_path = sprite_graphic_config["image_path"]
        self.tiles = []

        try:
            if sprite_graphic_config["size"]:
                self.real_size = sprite_graphic_config["size"]
                if type(self.real_size) is not list:
                    raise WrongConfigError("sprite_graphics size must be a list")
                if len(self.real_size) is not 2:
                    raise WrongConfigError("sprite_graphics size length must be 2")
                if max(self.real_size) > 8:
                    raise WrongConfigError("sprite_graphics size must not be bigger than 8")
        except KeyError:
            self.real_size = []
        self.frame_count = 0
        self.colors = []

        self.gba_size = []
        self.shape_size = []
        self.palette = []
        self.tileset = []

    def parse(self):
        self.parse_image()
        if len(self.colors) > 255:
            raise WrongImageError("Sprite graphic image: \"" + self.image_path + "\" has too many different colors")
        print(len(self.colors), "different colors")
        self.generate_for_gba()

    def generate_for_gba(self):
        for color in self.colors:
            self.palette.append(0)
            for i, part in enumerate(color):
                self.palette[-1] += int(part * (31 / 255)) << (i * 5)

        for tile in self.tiles:
            for pixel in tile:
                self.tileset.append(pixel)

    def parse_image(self):
        image = Image(filename=self.image_path)
        # generate real_size or frame_count if size was specified (multi frame)
        if not self.real_size:
            self.real_size = [min(int(image.size[0] / 8), 8), min(int(image.size[1] / 8), 8)]
            self.frame_count = 1
        else:
            self.frame_count = int(image.size[0] / 8) / self.real_size[0]
            if self.frame_count != int(self.frame_count):
                raise WrongConfigError("Image is not dividable into frames of the provided size")
            self.frame_count = int(self.frame_count)
        # generate gba_size and shape_size
        if self.real_size[0] == 1:
            gba_size = [1, get_lowest_option(self.real_size[1], [1, 2, 4])]
        elif self.real_size[0] == 2:
            gba_size = [2, get_lowest_option(self.real_size[1], [1, 2, 4])]
        elif self.real_size[0] <= 4:
            gba_size = [4, get_lowest_option(self.real_size[1], [1, 2, 4, 8])]
        else:
            gba_size = [8, get_lowest_option(self.real_size[1], [4, 8])]
        self.gba_size = gba_size
        self.shape_size = SHAPE_SIZE_DICTIONARY[str(gba_size)]
        image_pixels = image.export_pixels()
        image_data = []
        for i in range(0, len(image_pixels), 4):
            image_data.append(image_pixels[i:i+4])
        # generate tiles
        for frame_index in range(self.frame_count):
            for yi in range(0, self.real_size[1] * 8, 8):
                for xi in range(frame_index * self.real_size[0] * 8, (frame_index + 1) * self.real_size[0] * 8, 8):
                    tile = []
                    for pixel_index in range(64):
                        pixel = image_data[(pixel_index % 8) + xi + int(pixel_index / 8) * image.size[0] + yi * image.size[0]]
                        if pixel[3] == 0:
                            tile.append(255)
                        else:
                            if pixel[:3] not in self.colors:
                                self.colors.append(pixel[:3])
                            tile.append(self.colors.index(pixel[:3]))
                    self.tiles.append(tile)
                for xfiller in range(gba_size[0] - self.real_size[0]):
                    self.tiles.append([255 for i in range(64)])
            for yfiller in range((gba_size[1] - self.real_size[1]) * gba_size[0]):
                self.tiles.append([255 for i in range(64)])

    def print_tiles(self):
        for o in range(len(self.tiles)):
            for i in range(0, 64, 8):
                print(self.tiles[o][i:i+8])
            print("-"*(8*3))

    def print_sizes(self):
        print(self.gba_size, "--> ", end="")
        print(self.real_size, "--> ", end="")
        print(self.shape_size)


class Map:
    def __init__(self, map_config):
        self.tmx_path = map_config["tmx_path"]
        try:
            self.bottom_layer_name = map_config["bottom_layer_name"]
            if not self.bottom_layer_name or type(self.bottom_layer_name) is not str:
                raise KeyError
        except KeyError:
            raise WrongConfigError("'bottom_layer_name' not defined for map generated from file: \"" + self.tmx_path + "\"")
        try:
            self.middle_layer_name = map_config["middle_layer_name"]
            if not self.middle_layer_name or type(self.middle_layer_name) is not str:
                raise KeyError
        except KeyError:
            raise WrongConfigError("'middle_layer_name' not defined for map generated from file: \"" + self.tmx_path + "\"")
        try:
            self.top_layer_name = map_config["top_layer_name"]
            if not self.top_layer_name or type(self.top_layer_name) is not str:
                raise KeyError
        except KeyError:
            raise WrongConfigError("'top_layer_name' not defined for map generated from file: \"" + self.tmx_path + "\"")
        try:
            self.special_layer_name = map_config["special_layer_name"]
            if type(self.special_layer_name) is not str:
                raise WrongConfigError("'special_layer_name' is not str or None for map generated from file: \"" + self.tmx_path + "\"")
        except KeyError:
            self.special_layer_name = None

        self.tiles = [[0 for i in range(64)]]
        self.colors = [[0, 0, 0]]
        self.size = []

        self.specials_count = 0
        self.specials = []

        self.layer_tile_maps = []
        self.layer_names = []
        self.layer_sizes = []
        self.tile_legend = {0: 0}

        self.palette = []
        self.tileset = []

    def parse(self):
        self.parse_tilemap()
        self.size.append(max([i[0] for i in self.layer_sizes]))
        self.size.append(max([i[1] for i in self.layer_sizes]))
        print(str(len(self.layer_names)) + " layers parsed: " + str(self.layer_names))
        if len(self.colors) > 256:
            raise WrongImageError("Map generated from file: \"" + self.tmx_path + "\" has too many different colors")
        print(len(self.colors), "different colors")
        self.generate_for_gba()
        for i in range(self.size[0] * self.size[1]):
            self.specials.append(0)
        self.parse_walls(self.middle_layer_name)
        self.parse_specials(self.special_layer_name)
        print(str(self.specials_count) + " specials found")

    def generate_for_gba(self):
        for color in self.colors:
            self.palette.append(0)
            for i, part in enumerate(color):
                self.palette[-1] += int(part * (31 / 255)) << (i * 5)

        for tile in self.tiles:
            for i in range(0, 64, 4):
                word = 0
                for o, val in enumerate(tile[i:i+4]):
                    word += val << 8 * o
                self.tileset.append(word)

    def parse_tilemap(self):
        tmx_file_element = parse(self.tmx_path).documentElement
        for tileset_index, tileset_element in enumerate(tmx_file_element.getElementsByTagName("tileset")):
            first_tile_index = int(tileset_element.getAttribute("firstgid"))
            tsx_path = os.path.normpath(os.path.dirname(self.tmx_path) + "/" + tileset_element.getAttribute("source"))
            self.parse_tileset(tsx_path, first_tile_index)

        for layer_index, layer_element in enumerate(tmx_file_element.getElementsByTagName("layer")):
            if layer_element.getAttribute("name") not in [self.bottom_layer_name, self.middle_layer_name, self.top_layer_name]:
                continue
            self.layer_names.append(layer_element.getAttribute("name").replace(" ", "_"))
            self.layer_sizes.append([
                int(layer_element.getAttribute("width")),
                int(layer_element.getAttribute("height"))
                ])
            self.layer_tile_maps.append([])
            data = layer_element.getElementsByTagName("data")[0].firstChild.data.replace('\n', '').split(',')
            for map_entry in data:
                try:
                    self.layer_tile_maps[-1].append(self.tile_legend[int(map_entry)])
                except KeyError:
                    print("Unknown map entry: " + str(map_entry))
                    self.layer_tile_maps[-1].append(0)

    def parse_tileset(self, tsx_path, first_tile_index):
        tile_index = first_tile_index
        tileset_file_element = parse(tsx_path).documentElement
        try:
            properties = tileset_file_element.getElementsByTagName("properties")[0].getElementsByTagName("property")
            for property_ in properties:
                if (property_.getAttribute("name") == "DontParse" and property_.getAttribute("value") == 'true'):
                    print("\"DontParse\" property set to True found for tileset \"" + tsx_path + "\"")
                    return
                if (property_.getAttribute("name") == "SpecialTileset" and property_.getAttribute("value") == 'true'):
                    print("\"SpecialTileset\" property set to True found for tileset \"" + tsx_path + "\"")
                    return
        except IndexError:
            print("No properties were found for tileset \"" + tsx_path + "\"")
        for image_element in tileset_file_element.getElementsByTagName("image"):
            image_path = os.path.normpath(os.path.dirname(tsx_path) + "/" + image_element.getAttribute("source"))
            image = Image(filename=image_path)
            image_pixels = image.export_pixels()
            image_data = []
            for i in range(0, len(image_pixels), 4):
                image_data.append(image_pixels[i:i+4])
            for yi in range(0, image.size[1], 8):
                for xi in range(0, image.size[0], 8):
                    tile = []
                    for pixel_index in range(64):
                        pixel = image_data[(pixel_index % 8) + xi + int(pixel_index / 8) * image.size[0] + yi * image.size[0]]
                        if pixel[3] == 0:
                            tile.append(0)
                        else:
                            if pixel[:3] not in self.colors:
                                self.colors.append(pixel[:3])
                            tile.append(self.colors.index(pixel[:3]))
                    if tile not in self.tiles:
                        self.tile_legend[tile_index] = len(self.tiles)
                        self.tile_legend[tile_index | 2147483648] = len(self.tiles) | 1024
                        self.tile_legend[tile_index | 1073741824] = len(self.tiles) | 2048
                        self.tile_legend[tile_index | 3221225472] = len(self.tiles) | 3072
                        self.tiles.append(tile)
                    tile_index += 1

    def parse_specials(self, layer_name):
        tmx_file_element = parse(self.tmx_path).documentElement
        known_specials = {"0": 0}
        for layer_element in tmx_file_element.getElementsByTagName("layer"):
            if layer_element.getAttribute("name") != layer_name:
                continue
            special_layer_size = [int(layer_element.getAttribute("width")), int(layer_element.getAttribute("height"))]
            data = layer_element.getElementsByTagName("data")[0].firstChild.data.replace('\n', '').split(',')
            for map_entry_index, map_entry in enumerate(data):
                try:
                    self.specials[self.size[0] * int(map_entry_index / special_layer_size[0]) + map_entry_index % special_layer_size[0]] += known_specials[map_entry]
                except KeyError:
                    known_specials[map_entry] = (self.specials_count + 1) << 1
                    self.specials_count += 1
                    self.specials[self.size[0] * int(map_entry_index / special_layer_size[0]) + map_entry_index % special_layer_size[0]] += known_specials[map_entry]

    def parse_walls(self, layer_name):
        layer_index = self.layer_names.index(layer_name)
        for i, t in enumerate(self.layer_tile_maps[layer_index]):
            if t == 0:
                pass
            else:
                self.specials[self.size[0] * int(i / self.layer_sizes[layer_index][0]) + i % self.layer_sizes[layer_index][0]] = 1

    def print_tiles(self):
        for o in range(len(self.tiles)):
            for i in range(0, 64, 8):
                print(self.tiles[o][i:i+8])
            print("-"*(8*3))
