import re
from dataclasses import fields
from typing import Tuple

def camel_to_snake(name: str) -> str:
    # Convert CamelCase to snake_case
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    snake = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    return snake

def pluralize(name: str) -> str:
    # Simple pluralizer, can be improved or replaced with external libs
    if name.endswith('s'):
        return name
    if name.endswith('y'):
        return name[:-1] + 'ies'
    return name + 's'

def class_to_table_name(cls_name: str) -> str:
    snake = camel_to_snake(cls_name)
    return pluralize(snake)

def primary_key_by_class(kls: "BaseDT") -> str:
    return f"{camel_to_snake(kls.__name__)}_id"

def data_class_fields_names(kls: "BaseDT") -> Tuple[str]:
    return tuple(f.name for f in fields(kls))