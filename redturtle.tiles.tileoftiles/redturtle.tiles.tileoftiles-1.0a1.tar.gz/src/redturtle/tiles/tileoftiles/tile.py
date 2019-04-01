# -*- encoding:utf-8 *-
from plone import tiles
import base64


class TileOfTiles(tiles.PersistentTile):
    """
    """

    def get_bg_style(self):
        style = ""
        bgcolor = self.data.get("background_color", None)
        if bgcolor:
            style = "background-color: {}".format(bgcolor)
        bgimage = self.data.get("background_image", None)
        if bgimage:
            b64 = base64.b64encode(bgimage.data)
            style = 'background-image: url("data:image/png;base64,{}")'.format(
                b64
            )
        style = style + "; min-height: {}".format(
            self.data.get("min_height", "20px")
        )
        return style
