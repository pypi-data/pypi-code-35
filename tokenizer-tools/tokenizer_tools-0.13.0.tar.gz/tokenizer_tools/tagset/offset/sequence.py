import uuid

from tokenizer_tools.tagset.offset.span_set import SpanSet
from tokenizer_tools.tagset.offset.span import Span


class Sequence(object):
    def __init__(self, text, span_set=None, id=None):
        self.text = text
        self.span_set = span_set or SpanSet()
        self.id = id if id is not None else uuid.uuid4()
        self.label = None  # for feature usage

    def add_span(self, span):
        pass

    def check_span_set(self):
        check_overlap, overlapped_result = self.span_set.check_overlap()
        check_match, mismatch_result = self.span_set.check_match(self.text)

        return check_overlap and check_match, overlapped_result, mismatch_result

    def __eq__(self, other):
        return self.text == other.text and self.span_set == other.span_set


if __name__ == "__main__":
    seq = Sequence("王小明在北京的清华大学读书。")
    seq.span_set.append(Span(0, 3, 'PERSON', '王小明'))
    seq.span_set.append(Span(4, 6, 'GPE', '北京'))
    seq.span_set.append(Span(7, 11, 'ORG', '清华大学'))

    check_result = seq.check_span_set()
    print(check_result)
