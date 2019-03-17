class Util:
    """
    Utility functions
    """
    @staticmethod
    def split_string(text_block, max_segment_len):
        """
        Splits a string into segments such that each segment fits into the
        passed maximum segment length. Splits on space only. If any segment
        of the passed string cannot be split on space, then chops that
        segment at the passed length. E.g.:

        print(Util.split_string("this is a test of stringsplitting", 10))
        Produces: '["this is a", "test of", "stringspli", "tting"]'

        In all cases, trims trailing spaces on all segments but - within a
        segment interior - does not alter spaces. Honors leading spaces at
        the start of a string (or after a newline embedded in a string) but
        left-justifies if a string was split to fit within the passed width.
        Nuances arise based on the yaml flow operator (pipe, or greater-than)
        provided in the yaml.

        :param text_block: the string the split into segments
        :param max_segment_len: the maximum length of any segment

        :return: a List of the segments created by the function. If 'None'
        is passed in 'text_block', or the empty string is passed, or a string
        of all spaces is passed, then an empty List is returned.
        """
        segments = []
        if not text_block or len(text_block.strip()) == 0:
            return segments
        lines = text_block.split('\n')
        for line in lines:
            if len(line.strip()) == 0:
                segments.append("")
                continue
            cur = 0
            while True:
                end = cur + max_segment_len
                if end >= len(line):
                    if len(line[cur:].strip()) > 0:
                        # don't add an empty segment at the end
                        segments.append(line[cur:])
                    break
                for i in range(end, cur - 1, -1):
                    if line[i] == ' ':
                        end = i
                        break
                segments.append(line[cur: end].rstrip())
                # advance, ignoring leading spaces
                cur = end + len(line[end:]) - len(line[end:].lstrip())
        return segments
