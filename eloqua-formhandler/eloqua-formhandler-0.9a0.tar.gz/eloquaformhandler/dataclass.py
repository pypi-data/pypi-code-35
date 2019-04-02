from datetime import date
from datetime import timedelta
from typing import Any
from typing import Dict

import attr

API_VERSION = '2.0'


@attr.s(auto_attribs=True)
class FieldConverter:
    """
    The FieldConverters responsibility is to convert the form data to the
    format that the eloqua api needs.
    This is the right location to inject information that were not provided by
    forms
    """

    form_id: str = attr.ib()
    field_mapping: Dict[str, str] = attr.ib()

    @classmethod
    def from_schema(cls, schema: Dict):
        form_id = schema["id"]
        field_mapping = {x["htmlName"]: x["id"] for x in schema["elements"]}
        return cls(form_id, field_mapping)

    def __call__(self, user_input: Dict[str, str]) -> Dict[str, Any]:
        return {
            "fieldValues": [{
                "type": "FieldValue",
                "id": self.field_mapping[x[0]],
                "value": x[1],
            } for x in user_input.items()]
        }


@attr.s
class Schema:
    """
    The Schemas Responsibility is to retrieve the schema for the form
    We pass on what we get from eloqua and assume that the consumer knows how
    to handle this.
    The Schema is also responsible for caching.
    We cache 24 hours, non persistent.
    """

    form_id: str = attr.ib()
    last_retrieved: date = attr.ib()
    base_url: str = attr.ib()
    session = attr.ib()

    @classmethod
    def from_id(cls, form_id: str, base_url: str, session):
        yesterday = date.today() - timedelta(days=1)
        return Schema(
            form_id=form_id,
            last_retrieved=yesterday,
            base_url=base_url,
            session=session,
        )

    def __call__(self):
        if self.last_retrieved != date.today():
            self._cached_schema = self.retrieve()
        return self._cached_schema

    def retrieve(self):
        url = "{base}/api/REST/{version}/assets/form/{id}".format(
            base=self.base_url, id=self.form_id, version=API_VERSION
        )
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()


@attr.s
class Transmit:
    """
    The Transmit responsibility is to transmit the data.
    It will throw an exceptions if the data is not the way it needs it to be.
    """

    form_id: str = attr.ib()
    base_url: str = attr.ib()
    session = attr.ib()

    @classmethod
    def from_id(cls, form_id: str, base_url: str, session):
        return cls(form_id=form_id, base_url=base_url, session=session)

    def __call__(self, form_data):
        url = "{base}/api/REST/{version}/data/form/{id}".format(
            base=self.base_url, id=self.form_id, version=API_VERSION
        )
        resp = self.session.post(url, json=form_data)
        resp.raise_for_status()
        assert resp.status_code == 201
        return resp.status_code
