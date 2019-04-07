from photospicker.picker.abstract_exif_date_picker import \
    AbstractExifDatePicker
import random
import math


class SmartPicker(AbstractExifDatePicker):
    """
    Pick intelligently photos depending on EXIF DateTimeOriginal
    The chance for a photo to be selected is proportional to its recency.
    Actually, the majority of retrieved photos will be recent and a few old
    photos will be also retrieved.
    """

    def _select(self, to_select):
        """
        Finally select photos

        :param list to_select: list where process selection

        :rtype: list
        """
        for i in range(1, 21):
            ratio = i * .05
            ret = self._compute_packet_extractions(ratio, to_select)
            if ret is not None:
                break  # use the lowest ratio found

        (packet_sizes, extractions) = ret
        current_packet = []
        packet_size = packet_sizes.pop(0)
        selected = []
        for filename in to_select:
            current_packet.append(filename)
            if len(current_packet) == packet_size:
                selected += self._process_packet(current_packet, extractions)
                current_packet = []
                if packet_sizes:
                    packet_size = packet_sizes.pop(0)

        return selected

    @staticmethod
    def _process_packet(current_packet, extractions):
        """
        Randomly select photos inside a packet

        :param list current_packet: packet
        :param list extractions: list of photos count to extract of each packet

        :rtype: list
        """
        random.shuffle(current_packet)
        to_extract = extractions.pop(0)
        return [
            x for key, x in enumerate(current_packet)
            if key < to_extract
        ]

    def _compute_packet_extractions(self, ratio, sorted_filenames):
        """
        Compute the successive photos count to extract from packets
        depending on the given ratio. Returns false if computing is
        not possible with self._photo_count and total photos count.

        :param float ratio: ratio
        :param list sorted_filenames: sorted filenames

        :rtype: None/tuple
        """
        remaining = min(self._photos_count, len(sorted_filenames))
        max_val = None
        extractions = []
        while remaining > 0:
            to_extract = int(max(round(remaining * ratio), 1))
            if max_val is None:
                # the first (and bigger) count
                # to extract must be greater than 1
                if to_extract < 2:
                    return None
                max_val = to_extract
            remaining -= to_extract
            extractions.append(to_extract)

        # Packets count is equal to extractions count
        total = len(sorted_filenames)
        packets_count = len(extractions)
        packet_size_floored = math.floor(total / packets_count)
        rest = total - packet_size_floored * packets_count
        packet_sizes = []
        for i in range(1, packets_count + 1):
            packet_sizes.append(
                packet_size_floored + 1
                if packets_count - i < rest
                else packet_size_floored
            )

        if packet_sizes[0] < max_val:
            return None

        return (packet_sizes, extractions)
