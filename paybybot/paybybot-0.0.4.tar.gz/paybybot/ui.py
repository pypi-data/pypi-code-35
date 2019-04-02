from flexx import flx, app
from . import config


class GUI(flx.PyComponent):
    pbp_account = flx.StringProp(config.CONFIG["paybyphone"]["login"], settable=True)
    sessions = flx.ListProp(settable=True)
    email = flx.StringProp(settable=True)

    def init(self):
        View()

    @flx.action
    def _refresh(self):
        config.CONFIG = config.get_config()
        self._mutate_pbp_account(config.CONFIG["paybyphone"]["login"])


class View(flx.JsComponent):
    def init(self):
        with flx.VBox():
            with flx.HBox():
                self.refresh = flx.Button(text="refresh")
                flx.Widget(flex=1)
            with flx.HFix():
                with flx.FormLayout():
                    flx.LineEdit(
                        title="User account",
                        text=lambda: self.root.pbp_account,
                        disabled=True,
                    )
                flx.Widget(flex=1)

            flx.Widget(flex=1)

    @flx.reaction("refresh.pointer_click")
    def _refresh(self, *events):
        self.root._refresh()


if __name__ == "__main__":
    m = app.launch(GUI, "app")
    # m.pbp_account.    set_text("coucou")
    app.run()
