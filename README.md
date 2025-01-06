# validation_dataclass
### Simple json validation though dataclass.
- validates field types
- validated field optionality
- validates fields assigned through @property
- validates nested dataclasses

If data not valid class raises ValidationError, else as_dict() will return validated dict.

### Usage:
1. Create dataclass inheriting from ValidationDataclass with all field restriction required:
```
      @dataclass
      class NestedDatalass_01(ValidationDataclass):
          field_01: list[int]
          field_02: dict

      @dataclass
      class Datalass_02(ValidationDataclass):
          field_01: str | None
          field_02: int
          field_03: dict
          field_04: list[int]
          field_05: NestedDatalass_01
```
2. Validate incoming json data through Dataclass_02
```
   Datalass_02.from_dict(json_data).as_dict()
```
