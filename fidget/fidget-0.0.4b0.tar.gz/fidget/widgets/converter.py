from __future__ import annotations

from typing import TypeVar, Generic, Callable, Optional

from functools import wraps
from fidget.backend.QtWidgets import QHBoxLayout

from fidget.core import Fidget, ParseError, PlaintextParseError, FidgetTemplate

from fidget.widgets.idiomatic_inner import SingleFidgetWrapper
from fidget.widgets.__util__ import is_trivial_printer, only_valid

T = TypeVar('T')
F = TypeVar('F')


class FidgetConverter(Generic[F, T], SingleFidgetWrapper[F, T]):
    """
    A Fidget wrapper that only converts the value to another type
    """

    def __init__(self, inner_template: FidgetTemplate[F] = None,
                 converter_func: Callable[[F], T] = None,
                 back_converter_func: Optional[Callable[[T], F]] = None,
                 **kwargs):
        """
        :param inner_template: the template to wrap
        :param converter_func: a conversion function
        :param back_converter_func: a backwards conversion function
        :param kwargs: forwarded to either the inner template or Fidget
        """

        inner_template = only_valid(inner_template=inner_template, INNER_TEMPLATE=self.INNER_TEMPLATE).template_of()

        template_args = {}

        for key in ('make_plaintext', 'make_indicator', 'make_title'):
            if key in kwargs:
                template_args[key] = kwargs[key]
            else:
                v = getattr(self, key.upper(), None)
                if v is not None:
                    template_args[key] = v
            kwargs[key] = False
        inner_template = inner_template.template(**template_args)

        super().__init__(inner_template.title, **kwargs)

        self.inner_template = inner_template
        self.inner: Fidget[F] = None
        self.converter_func = converter_func
        self.back_converter_func = back_converter_func

        self.init_ui()

    INNER_TEMPLATE: FidgetTemplate[F] = None

    def init_ui(self):
        super().init_ui()
        layout = QHBoxLayout(self)

        self.inner = self.inner_template()
        layout.addWidget(self.inner)
        self.setMinimumSize(self.inner.minimumSize())
        self.setMaximumSize(self.inner.maximumSize())

        if self.inner.title_label:
            self.make_title = True
            self.title_label.linkActivated.disconnect(self.inner._help_clicked)
            self.title_label.linkActivated.connect(self._help_clicked)

        if self.inner.auto_button:
            self.inner.auto_button.clicked.disconnect(self.inner._auto_btn_click)
            self.inner.auto_button.clicked.connect(self._auto_btn_click)
            self.make_auto = True

        if self.inner.plaintext_button:
            self.inner.plaintext_button.clicked.disconnect(self.inner._plaintext_btn_click)
            self.inner.plaintext_button.clicked.connect(self._plaintext_btn_click)

            self._plaintext_widget = self.inner._plaintext_widget
            self._plaintext_widget.owner = self

            self.make_plaintext = True

        if self.inner.indicator_label:
            self.inner.indicator_label.linkActivated.disconnect(self.inner._detail_button_clicked)
            self.inner.indicator_label.linkActivated.connect(self._detail_button_clicked)

            self.indicator_label = self.inner.indicator_label
            self.make_indicator = True

        self.inner.on_change.connect(self.change_value)
        self.setFocusProxy(self.inner)

    def provided_pre(self, *args, **kwargs):
        return self.inner.provided_pre(*args, **kwargs)

    def provided_post(self, *args, **kwargs):
        return self.inner.provided_post(*args, **kwargs)

    def parse(self):
        f = self.inner.parse()
        return self.convert(f)

    def validate(self, value: T):
        if self.back_convert:
            self.inner.validate(self.back_convert(value))
        super().validate(value)

    def convert(self, v: F) -> T:
        if not self.converter_func:
            raise Exception('a converter function must be provided')
        return self.converter_func(v)

    @property
    def back_convert(self):
        return self.back_converter_func

    def plaintext_parsers(self):
        yield from super().plaintext_parsers()
        for parser in self.inner.plaintext_parsers():
            @wraps(parser)
            def p(*args, **kwargs):
                f = parser(*args, **kwargs)
                try:
                    return self.convert(f)
                except ParseError as e:
                    raise PlaintextParseError from e

            yield p

    def plaintext_printers(self):
        if self.back_convert:
            yield from super().plaintext_printers()
            for printer in self.inner.plaintext_printers():
                if is_trivial_printer(printer):
                    continue

                @wraps(printer)
                def p(*args, **kwargs):
                    f = self.back_convert(*args, **kwargs)
                    return printer(f)

                yield p
        else:
            yield from super().plaintext_printers()

    NO_FILL = object()

    def _fill(self, v: T = NO_FILL):
        if v is self.NO_FILL:
            self.inner.fill()
        else:
            f = self.back_convert(v)
            self.inner.fill(f)

    @property
    def fill(self):
        return (self.inner.fill and self.back_convert) and self._fill

    def template_of(self):
        ret = super().template_of()
        template_args = {}
        for key in ('make_plaintext', 'make_indicator', 'make_title'):
            if key in self.inner_template.kwargs:
                template_args[key] = self.inner_template.kwargs[key]
        return ret.template(**template_args)


if __name__ == '__main__':
    from fidget.backend import QApplication
    from fidget import wrap_parser
    from fidget.widgets import FidgetLineEdit, FidgetOptional

    app = QApplication([])
    w = FidgetConverter(FidgetLineEdit('sample', pattern='(1[^1]*1|[^1])*', make_plaintext=True),
                        converter_func=wrap_parser(ValueError, int),
                        back_converter_func=str, make_indicator=True)
    w = FidgetOptional(w, make_title=True)
    w.show()
    res = app.exec_()
    print(w.value())
    exit(res)
