"""
.. Note::
   This plugin is scalable, as long as the minimums/maximums of the manialink ID and action ID do
   not overlap between the instances.

Provides a manialink GUI generator from pure Python code, allocates manialink and action IDs
automatically and handles responses thereof.

Layout system
-------------
The window represents the entire Trackmania client window. It must contain a layout that may
contain multiple widgets and other nested layouts. Absolute positions are discourages.The ingame
position is calculated relatively to the respective margins, paddings and sizes. Every of these
measurements range from zero to hundred, essentially specifying the percentage of the size of the
parent to consume. Warnings are raised if any of the provided measurements are invalid.

Visualized:
::

    +-----------------------------------------------------------+
    | Margin.left                                               |
    | <---------> +========================================+    |
    |             | Padding.left <----- Size.width ----->  |    |
    |             | <----------> +======================+  |    |
    |             |              |        Widget        |  |    |
    |             |              +======================+  |    |
    |             |                 Layout                 |    |
    |             +----------------------------------------+    |
    |                          Window                           |
    +-----------------------------------------------------------+
"""

import collections
import logging
import math
import random
import xml.etree.cElementTree as ET

#: Defines the margin between the layout's border and its parent.
Margin = collections.namedtuple('Margin', ['top', 'right', 'bottom', 'left'])
#: Defines the padding between the layout's border and its widgets.
Padding = collections.namedtuple('Padding', ['top', 'right', 'bottom', 'left'])
#: Defines the spacing between the widgets in the layout.
Spacing = collections.namedtuple('Spacing', ['vertical', 'horizontal'])
#: Defines the position of a widget. For internal use only.
Point = collections.namedtuple('Point', ['x', 'y'])
#: Defines the size of a widget.
Size = collections.namedtuple('Size', ['width', 'height'])
#: Defines the range of an axis, for example.
Range = collections.namedtuple('Range', ['min', 'max'])
#: Defines the coordinate system to map to. Each member except for size is a :class:`Range` object.
#: `size` is just a :class:`Size` object, since sizes cannot be negative anyway.
Coordinates = collections.namedtuple('Coordinates', ['x_axis', 'y_axis', 'depth', 'size'])

pos_attribute = 'posn'
size_attribute = 'sizen'
depth_reduce_factor = 0.1

class VerticalAlign:
    """ Defines all vertical alignments """
    TOP = 'top'
    CENTER = 'center'
    BOTTOM = 'bottom'

class HorizontalAlign:
    """ Defines all horizontal alignments """
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'

class InvalidLayout(Exception):
    """ Raised if any widget of the layout goes out of bounds """
    def __init__(self, current, limit, size):
        super().__init__(f'Invalid layout. {current} + {size} exceeds {limit}')

tmuf_coordinates = Coordinates(
    x_axis=Range(min=-64, max=64),
    y_axis=Range(min=48, max=-48),
    depth=Range(min=-32, max=32),
    size=Size(width=128, height=96)
)

def tmuf_coordinate_transform(old, rel_size, _pos, size, _depth):
    """
    :param Coordinates old: Old coordinates
    :param Size rel_size: Amount of space the children should get
    :param Point _pos: New ingame position of the layout
    :param Size size: New ingame size of the layout
    :param float _depth: New ingame depth of the layout
    """
    # in TMUF, <frame> elements change the origin to bottom-left
    return Coordinates(
        x_axis=Range(0, (-old.x_axis.min + old.x_axis.max) * rel_size.width / 100.0),
        y_axis=Range(0, (-old.y_axis.min + old.y_axis.max) * rel_size.height / 100.0),
        depth=old.depth, # does not change
        size=size # restrict maximum possible size to the new layout
    )

def _map_range(value, new_min, new_max, old_min=0, old_max=100):
    old_range = float(old_max - old_min)
    new_range = float(new_max - new_min)
    return (((value - old_min) * new_range) / old_range) + new_min

def _map_frame(coordinates, position, size, depth):
    # returns (real_pos, real_size, real_depth)
    return (
        Point(
            _map_range(position.x, coordinates.x_axis.min, coordinates.x_axis.max),
            _map_range(position.y, coordinates.y_axis.min, coordinates.y_axis.max),
        ),
        Size(
            _map_range(size.width, 0, coordinates.size.width),
            _map_range(size.height, 0, coordinates.size.height),
        ),
        _map_range(depth, coordinates.depth.min, coordinates.depth.max)
    )

def _get_layout(padding, spacing, items):
    # generator that emits multiple (widget, position) tuples
    start = Point(padding.left, padding.top)
    end = Point(100 - padding.right, 100 - padding.bottom)
    best_height = 0
    current_x = start.x
    current_y = start.y

    for item in items:
        if current_x + item.size.width > end.x:
            current_x = start.x
            current_y += spacing.vertical + best_height
            best_height = 0
        if current_x + item.size.width > end.x or current_y + item.size.height > end.y:
            raise InvalidLayout(Point(current_x, current_y), end, item.size)
        if item.absolute_pos is not None:
            yield item, item.absolute_pos
            continue

        yield item, Point(current_x, current_y)
        best_height = max(best_height, item.size.height)
        current_x += item.size.width + spacing.horizontal

# pylint: disable=too-many-locals
def pretty_print_layout(layout, width, height):
    """ Returns a string that represents a generated layout. """
    char_buffer = [' '] * (width * height)
    for item, pos in _get_layout(layout.padding, layout.spacing, layout.items):
        rel_x = 0 if pos.x == 0 else math.ceil(width * pos.x / 100)
        rel_y = 0 if pos.y == 0 else math.ceil(height * pos.y / 100)
        rel_w = math.ceil(width * item.size.width / 100)
        rel_h = math.ceil(height * item.size.height / 100)
        for xx in range(rel_w):
            for yy in range(rel_h):
                index = (yy + rel_y) * width + xx + rel_x
                side_x = xx in (0, rel_w - 1)
                side_y = yy in (0, rel_h - 1)
                if side_x and side_y:
                    char_buffer[index] = '+'
                elif side_x:
                    char_buffer[index] = '|'
                elif side_y:
                    char_buffer[index] = '-'

    result = '+' + ('-' * width) + '+\n'
    for y in range(height):
        scanline = y * width
        result += '|' + ''.join(char_buffer[scanline:scanline+width]) + '|\n'
    return result + '+' + ('-' * width) + '+'

class Widget:
    """ Defines a manialink widget having a size and defining some attributes. """
    __slots__ = 'size', 'absolute_pos', 'attribs'

    element_name = None

    def __init__(self, **kwargs):
        """
        :param Size size: Size of the widget relative to its parent (required)
        :param Point absolute_pos: Discouraged, but sets the absolute position of the widget
        :param kwargs: Optional attributes to inject into the generated XML element
        """
        self.size = kwargs.pop('size')
        self.absolute_pos = kwargs.pop('absolute_pos', None)
        self.attribs = kwargs

    # pylint: disable=too-many-arguments
    def build(self, parent_tree, position, depth, coordinates, transform):
        """ Builds the widget and returns its cElementTree.Element. """
        del transform # widgets by default do not transform the coordinates
        if self.element_name is None:
            raise NotImplementedError(f'{self.__class__.__name__} needs to override element_name')

        real_pos, real_size, real_depth = _map_frame(coordinates, position, self.size, depth)
        attributes = self.attribs
        attributes.update({
            pos_attribute: f'{real_pos.x} {real_pos.y} {real_depth}',
            size_attribute: f'{real_size.width} {real_size.height}',
        })

        if parent_tree is None:
            return ET.Element(self.element_name, attrib=attributes)
        return ET.SubElement(parent_tree, self.element_name, attrib=attributes)

    def generate_actions(self, _generator):
        """ Generates an action ID from the given generator. """

class Layout(Widget):
    """Defines a layout that holds many widgets and calculates their bounds automatically."""
    element_name = 'frame'

    __slots__ = (
        'background',
        'padding',
        'margin',
        'spacing',
        'items',
        'format',
        'orientation'
    )

    def __init__(self, **kwargs):
        """
        :param Image background: Element to use as background
        :param Padding padding: Layout padding (visual example above)
        :param Margin margin: Layout margin (visual example above)
        :param Spacing spacing: Layout spacing (visual example above)
        :param Size size: Base size of the layout
        :param list[Element] items: Items of the layout. Ordering is taken as-is
        :param dict format: Format attributes to apply to all children
        :param kwargs: Optional attributes to inject into the generated XML element
        """
        self.padding = kwargs.pop('padding', Padding(0, 0, 0, 0))
        self.margin = kwargs.pop('margin', Margin(0, 0, 0, 0))
        self.spacing = kwargs.pop('spacing', Spacing(0, 0))
        self.background = kwargs.pop('background', None)
        self.items = kwargs.pop('items', [])
        self.format = kwargs.pop('format', None)
        super().__init__(**kwargs)

    # pylint: disable=too-many-arguments
    def build(self, parent_tree, position, depth, coordinates, transform):
        """ Builds the layout and all its items. """
        # reduces the relative size according to the layout's margin
        old_size = self.size
        self.size = Size(
            self.size.width - self.margin.left - self.margin.right,
            self.size.height - self.margin.top - self.margin.bottom
        )

        # calculates fake positons and sizes for the full-sized BG image
        fake_coords = transform(
            coordinates, old_size, *_map_frame(coordinates, position, self.size, depth)
        )

        position = Point(position.x + self.margin.left, position.y + self.margin.top)
        parent_tree = super().build(parent_tree, position, depth, coordinates, transform)
        real_pos, real_size, real_depth = _map_frame(coordinates, position, self.size, depth)
        coordinates = transform(coordinates, self.size, real_pos, real_size, real_depth)

        self.size = old_size
        if self.format is not None:
            ET.SubElement(parent_tree, 'format', attrib=self.format)
        if self.background is not None:
            self.background.build(
                parent_tree=parent_tree,
                position=Point(0, 0),
                depth=depth,
                coordinates=fake_coords,
                transform=transform
            )

        for item, pos in _get_layout(self.padding, self.spacing, self.items):
            item.build(parent_tree, pos, depth + depth_reduce_factor, coordinates, transform)
        return parent_tree

    def generate_actions(self, generator):
        for item in self.items:
            item.generate_actions(generator)

class Window:
    """ Represents the entire ingame screen. """
    __slots__ = (
        'base_depth',
        'cached_actions',
        'cached_xml',
        'manialink_id',
        'recipients',
        'coordinates',
        'transform',
        'layouts'
    )

    def __init__(self, base_depth=None, coordinates=tmuf_coordinates,
                 transform=tmuf_coordinate_transform):
        """
        :param base_depth: Base depth of the window (0-100). Each layout reduces the depth
        :param coordinates: Coordinate system of the window (default = TMUF)
        :param transform: Coordinate transform function for widgets in a layout (default = TMUF)
        """
        self.base_depth = base_depth or 0
        self.cached_actions = False
        self.cached_xml = None
        self.coordinates = coordinates
        self.transform = transform
        self.layouts = []
        # these cache certain properties when the window is shown to one or multiple players, for
        # convenience purposes
        self.manialink_id = 0
        self.recipients = None

    def add_layout(self, layout):
        """ Adds the given layout to the window. """
        self.layouts.append(layout)

    def clear_layouts(self):
        """ Clears all layouts of the window. """
        self.layouts.clear()

    def invalidate(self, invalidate_actions=False, invalidate_xml=True):
        """ Invalidates the cache, effectively regenerating the XML when showing the window.

        :param bool invalidate_actions: True to regenerate the action IDs
        :param bool invalidate_xml: True to regenerate the XML
        """
        if invalidate_actions:
            self.cached_actions = False
        if invalidate_xml:
            self.cached_xml = None

    def generate_actions(self, generator):
        """
        Generates action IDs for widgets with actions and caches them. Warning: This must be done
        before generating the XML, since the XML ultimately contains the action IDs! This is
        usually not to be called by user code.

        :param generator: Generator for generating IDs. Takes the action handler, returns an ID
        """
        if not self.cached_actions:
            for layout in self.layouts:
                layout.generate_actions(generator)
            self.cached_actions = True

    def generate_xml(self):
        """
        Generates an XML representation of the window, caches it and returns it. This is usually not
        to be called by user code.
        """
        if self.cached_xml is not None:
            return self.cached_xml
        return ET.tostring(
            Layout(size=Size(100, 100), items=self.layouts).build(
                parent_tree=None,
                position=Point(0, 0),
                depth=self.base_depth,
                coordinates=self.coordinates,
                transform=self.transform
            ),
            encoding='utf-8',
            method='xml'
        )

class Image(Widget):
    """
    Defines a <quad> holding an image or an image generated from a predefined style. It might also
    define an action when it is being clicked on.

    TMUF attributes:
    - style (predefined style category e.g. Bgs1)
    - substyle (predefined style in category e.g. BgList)
    - url
    - bgcolor (4-byte RGBA, e.g. f008)
    - image (permalink to image)
    """
    element_name = 'quad'

    __slots__ = {'action'}

    def __init__(self, **kwargs):
        """
        :param action: Action to execute when the image is clicked (takes player instance)
        """
        self.action = kwargs.pop('action', None)
        super().__init__(**kwargs)

    def generate_actions(self, generator):
        self.attribs['action'] = str(generator(self.action))

class Label(Widget):
    """ Defines a <label> holding text.

    TMUF attributes:
    - halign (left/center/right) (e.g. center makes top-left edge the h-center of the text)
    - valign (top/center/bottom) (e.g. center makes top-left edge the v-center of the text)
    - text
    - autonewline (0/1) (e.g. 1 automatically word-wraps your text)
    - maxnumber (maximum amount of lines to be displayed)
    - url
    - textsize (size of text)
    - textcolor (4-byte RGBA, e.g. f008)
    - style (predefined label style name, e.g. TextPlayerCardName)
    """
    element_name = 'label'

class GuiPlugin:
    """ Shows/hides manialink GUIs and handles their actions """
    version = '1.0.0'
    name = 'gui'
    depends = 'remote', 'players', 'chat'
    logger = logging.getLogger(__name__)

    __slots__ = 'remote', 'players', 'minmax_manialinks', 'minmax_actions', 'manialinks', 'actions'

    def __init__(self):
        self.remote = None
        self.players = None
        self.minmax_manialinks = None
        self.minmax_actions = None
        self.manialinks = []
        self.actions = {}

    async def show(self, window, recipients=None, timeout=0, hide_on_action=True):
        """ Shows the given window to the specified recipients.

        :param Window window: Window to show
        :param list[login] recipients: Recipients or None for everyone
        :param int timeout: Seconds to show the window
        :param bool hide_on_action: True to hide window if the player clicks something
        """
        def _generate_action(handler):
            while True:
                # this may seem inefficient, but since we have such a huge range (0-int32_t.max)
                # the loop will only run once most of the time
                action_id = random.randint(self.minmax_actions[0], self.minmax_actions[1])
                if action_id not in self.actions:
                    self.actions[action_id] = handler
                    return action_id

        def _generate_manialink():
            if window.manialink_id:
                # reuse manialink ID
                return window.manialink_id
            while True:
                m_id = random.randint(self.minmax_manialinks[0], self.minmax_manialinks[1])
                if m_id not in self.manialinks:
                    self.manialinks.append(m_id)
                    return m_id

        if recipients is None or len(recipients) > 1:
            # share actions between multiple recipients to save IDs
            window.generate_actions(_generate_action)
            manialink = _generate_manialink()
        else:
            player = self.players.get(recipients[0])
            def _generator(handler):
                action_id = _generate_action(handler)
                try:
                    player.action_ids.append(action_id)
                except AttributeError:
                    player.action_ids = []
                    player.action_ids.append(action_id)
                return action_id
            window.generate_actions(_generator)
            manialink = _generate_manialink()
            try:
                player.manialink_ids.append(manialink)
            except AttributeError:
                player.manialink_ids = []
                player.manialink_ids.append(manialink)

        xml = window.generate_xml()
        xml = f'<?xml version="1.0" encoding="utf-8"?><manialink id="{manialink}">{xml}</manialink>'

        if recipients is None:
            await self.remote.execute('SendDisplayManialinkPage', xml, timeout, hide_on_action)
        else:
            await self.remote.execute(
                'SendDisplayManialinkPageToLogin',
                ','.join(recipients),
                xml,
                timeout,
                hide_on_action
            )

    async def hide(self, window, recipients=None):
        """ Hides the given window for the specified recipients. """
        # TMUF never intended to show multiple manialinks at once, therefore 'HideManialinkPageXYZ'
        # does not take a manialink ID, but instead hides everything on the screen. As a workaround,
        # we show an empty GUI with the very same manialink ID and treat it as 'hidden' internally.
        xml = f'<?xml version="1.0" encoding="utf-8"?><manialink id="{window.manialink_id}"/>'
        if recipients is None:
            await self.remote.execute('SendDisplayManialinkPage', xml, 1, False)
        else:
            # pylint: disable=line-too-long
            await self.remote.execute('SendDisplayManialinkPageToLogin', ','.join(recipients), xml, 1, False)

    async def load(self, config, dependencies):
        """ Intercepts the PlayerManialinkPageAnswer callback. """
        self.players = dependencies['players']
        self.remote = dependencies['remote']
        self.minmax_manialinks = config['minmax_manialinks']
        self.minmax_actions = config['minmax_actions']

        @self.remote.callback('TrackMania.PlayerManialinkPageAnswer')
        async def _manialink_answer(_uid, login, action_id):
            player = self.players.get(login)
            try:
                handler = player.manialink_actions[action_id]
            except AttributeError:
                # could potentially happen if the player answers and manages to leave immediately
                logging.warning('Player %s is not on the server anymore', login)
                return
            except KeyError as exc:
                logging.error('Action ID %s does not exist for player %s', action_id, login)
                raise exc
            await handler(player)

        @self.remote.callback('TrackMania.PlayerDisconnect')
        async def _player_quit(login):
            # prevent ID starvation by cleaning up the GUIs when the player leaves
            player = self.players.get(login)
            try:
                for m_id in player.manialink_ids:
                    self.manialinks.remove(m_id)
                for a_id in player.action_ids:
                    self.action_ids.remove(a_id)
            except ValueError as exc:
                self.logger.error(
                    'Unable to remove action or manialink ID\n%s -> %s\n%s -> %s',
                    player.manialink_ids, self.manialinks,
                    player.action_ids, self.actions
                )
                raise exc # that should never happen unless the controller has a bug
            except AttributeError:
                pass # o.k. player did not show a GUI

        # FIXME: TEST
        chat = dependencies['chat']
        import argparse
        parser = argparse.ArgumentParser('test', description='Test command')
        @chat.command(parser)
        async def _test(from_):
            window = Window()
            window.add_layout(Layout(
                margin=Margin(10, 10, 10, 10),
                padding=Padding(5, 5, 5, 5),
                size=Size(100, 100),
                background=Image(style='Bgs1', substyle='BgList', size=Size(100, 100)),
                items=[
                    Label(text='Top-left', size=Size(45, 45)),
                    Label(text='Top-right', size=Size(45, 45)),
                    Label(text='Bottom-left', size=Size(45, 45)),
                    Label(text='Bottom-right', size=Size(45, 45)),
                ]
            ))
            await self.show(window, [from_.login])

    async def unload(self):
        """ Hide all GUIs currently visible for all players. """
        if self.remote is not None:
            await self.remote.execute('SendHideManialinkPage')
