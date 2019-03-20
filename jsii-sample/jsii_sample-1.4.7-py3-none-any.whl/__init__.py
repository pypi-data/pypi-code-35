import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty
__jsii_assembly__ = jsii.JSIIAssembly.load("jsii-sample", "1.4.7", __name__, "jsii-sample@1.4.7.jsii.tgz")
class HelloJsii(metaclass=jsii.JSIIMeta, jsii_type="jsii-sample.HelloJsii"):
    def __init__(self, *, goodbye_message: typing.Optional[str]=None) -> None:
        props: HelloJsiiProps = {}

        if goodbye_message is not None:
            props["goodbyeMessage"] = goodbye_message

        jsii.create(HelloJsii, self, [props])

    @jsii.member(jsii_name="sayGoodbye")
    def say_goodbye(self, times: typing.Optional[jsii.Number]=None) -> str:
        return jsii.invoke(self, "sayGoodbye", [times])

    @jsii.member(jsii_name="sayHello")
    def say_hello(self, name: str) -> str:
        return jsii.invoke(self, "sayHello", [name])


@jsii.data_type(jsii_type="jsii-sample.HelloJsiiProps")
class HelloJsiiProps(jsii.compat.TypedDict, total=False):
    goodbyeMessage: str

__all__ = ["HelloJsii", "HelloJsiiProps", "__jsii_assembly__"]

publication.publish()
