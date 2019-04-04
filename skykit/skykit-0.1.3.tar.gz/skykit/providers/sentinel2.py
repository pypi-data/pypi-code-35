from .families.sentinel import Sentinel


class Sentinel2(Sentinel):
    def __init__(self, username, password):
        Sentinel.__init__(self, username, password, mission="Sentinel-2")

    def get_s3_location(self, product):
        product_type = product['producttype']
        format_bucket = "sentinel-s2-l{}".format(product_type[5:7].lower())

        title = product['title']
        tileid = title.split("_")[5]
        format_tile = "{}/{}/{}".format(tileid[1:3],
                                        tileid[3], tileid[4:6])
        format_date = "{}/{}/{}".format(title[11:15],
                                        int(title[15:17]), int(title[17:19]))
        format_path = "tiles/{}/{}/0/".format(format_tile, format_date)
        return (format_bucket, format_path)
