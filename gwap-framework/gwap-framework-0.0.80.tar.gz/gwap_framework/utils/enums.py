from enum import Enum


class PubSubOperation(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

    def is_create(self) -> bool:
        return self.value == self.CREATE

    def is_update(self) -> bool:
        return self.value == self.UPDATE

    def is_delete(self) -> bool:
        return self.value == self.DELETE
