from dataclasses import dataclass, fields

from rest_framework.exceptions import ValidationError


@dataclass
class DataclassImproved:

    def convert_value(self, value):
        if isinstance(value, DataclassImproved):
            # Рекурсивно сериализируем вложенные датаклассы
            return value.as_dict()
        elif isinstance(value, list):
            # Обрабатываем списки
            return [self.convert_value(item) for item in value]
        else:
            return value

    def as_dict(self) -> dict:
        """Метод для экспорта датакласс в дикт влючая вложенные датаклассы и проперти."""
        obj_dict = {}

        class_keys = set(self.__class__.__dict__.keys())
        for prop in class_keys:
            if isinstance(getattr(self.__class__, prop), property):
                obj_dict[prop] = self.convert_value(getattr(self, prop))

        class_fields = set(fields(self))
        for field in class_fields:
            if field.init:
                obj_dict[field.name] = self.convert_value(getattr(self, field.name))

        return obj_dict

    @classmethod
    def from_dict(cls, dict_data):
        """
        Метод для валидации входящей даты через датакласс

        validated_dataclass = Dataclass.from_dict(dict_data)

        Возвращает провалидированный инстанс датакласса со всеми вложенными датаклассами.
        """

        class_fields = set(fields(cls))
        for field in class_fields:
            if field.name not in dict_data:
                raise ValidationError(f"Field '{field.name}' is missing in the dict data.")

            # Достаем тип поля для параметризованных полей
            field_type = field.type
            if hasattr(field_type, "__origin__"):
                field_type = field_type.__origin__

            field_value = dict_data[field.name]

            # Рекурсивно валидируем поля вложенного датакласса
            if isinstance(field_type, type) and issubclass(field_type, DataclassImproved):
                nested_instance = field_type.from_dict(dict_data[field.name])
                dict_data[field.name] = nested_instance

            elif not isinstance(field_value, field_type):
                raise ValidationError(f"Field '{field.name}' has invalid type in the dict data.")

        return cls(**dict_data)
