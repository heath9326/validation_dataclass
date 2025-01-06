from dataclasses import dataclass
from unittest import TestCase

from rest_framework.exceptions import ValidationError

from validation_dataclass import DataclassImproved


@dataclass
class Datalass_01(DataclassImproved):
    field_01: str
    field_02: int
    field_03: dict
    field_04: list[int]


class TestDataclassImproved(TestCase):

    def test__dataclass_is_serialized__success(self):
        # Dataclass сериализуется и все поля присутстуют
        expected_data = {
            'field_01': 'Example',
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2]
        }

        dataclass_instance = Datalass_01(
            field_01="Example",
            field_02=10,
            field_03={
                "nested_field_01": "Example",
                "nested_field_02": 10
            },
            field_04=[0, 1, 2]
        )
        dataclass_data = dataclass_instance.as_dict()
        self.assertDictEqual(dataclass_data, expected_data)

    def test__nested_dataclass_is_serialized__success(self):
        # Dataclass со вложенным датаклассом успешно сериализуется
        expected_data = {
            'field_01': 'Example',
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2],
            'field_05': {
                'field_01': [0, 1, 2],
                'field_02': {
                    'nested_field_01': 'Example',
                    'nested_field_02': 10
                },
            }
        }

        # region Датаклассы
        @dataclass
        class NestedDatalass_01(DataclassImproved):
            field_01: list[int]
            field_02: dict

        @dataclass
        class Datalass_02(DataclassImproved):
            field_01: str
            field_02: int
            field_03: dict
            field_04: list[int]
            field_05: NestedDatalass_01
        # endregion

        dataclass_instance = Datalass_02(
            field_01="Example",
            field_02=10,
            field_03={
                "nested_field_01": "Example",
                "nested_field_02": 10
            },
            field_04=[0, 1, 2],
            field_05=NestedDatalass_01(
                field_01=[0, 1, 2],
                field_02={
                    "nested_field_01": "Example",
                    "nested_field_02": 10
                },
            )
        )

        dataclass_data = dataclass_instance.as_dict()
        self.assertDictEqual(dataclass_data, expected_data)

    def test__double_nested_dataclass_is_serialized__success(self):
        """Датакласс с двума уровнями вложенности датаклассов успешно сериализуется"""
        expected_data = {
            'field_01': 'Example',
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2],
            'field_05': {
                'field_01': [0, 1, 2],
                'field_02': {
                    'field_02': {
                        'nested_field_01': 'Example',
                        'nested_field_02': 10
                    }
                },
            }
        }
        # region Датаклассы
        @dataclass
        class NestedDatalass_02(DataclassImproved):
            field_02: dict

        @dataclass
        class NestedDatalass_01(DataclassImproved):
            field_01: list[int]
            field_02: NestedDatalass_02

        @dataclass
        class Datalass_02(DataclassImproved):
            field_01: str
            field_02: int
            field_03: dict
            field_04: list[int]
            field_05: NestedDatalass_01
        # endregion

        dataclass_instance = Datalass_02(
            field_01="Example",
            field_02=10,
            field_03={
                "nested_field_01": "Example",
                "nested_field_02": 10
            },
            field_04=[0, 1, 2],
            field_05=NestedDatalass_01(
                field_01=[0, 1, 2],
                field_02=NestedDatalass_02(
                    field_02={
                        "nested_field_01": "Example",
                        "nested_field_02": 10
                    }
                ),
            )
        )

        dataclass_data = dataclass_instance.as_dict()
        self.assertDictEqual(dataclass_data, expected_data)

    def test__list_nested_dataclass_is_serialized__success(self):
        """Датакласс со вложенным списком датаклассов успешно сериализуется"""
        expected_data = {
            'field_01': 'Example',
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2],
            'field_05': [
                {
                'field_01': [0, 1, 2],
                'field_02': {
                    'nested_field_01': 'Example',
                    'nested_field_02': 10
                    }
                },
                {
                'field_01': [0, 1, 2],
                'field_02': {
                    'nested_field_01': 'Example',
                    'nested_field_02': 10
                    },
                }
            ]
        }

        # region Датаклассы
        @dataclass
        class NestedDatalass_01(DataclassImproved):
            field_01: list[int]
            field_02: dict

        @dataclass
        class Datalass_02(DataclassImproved):
            field_01: str
            field_02: int
            field_03: dict
            field_04: list[int]
            field_05: list[NestedDatalass_01]
        #endregion

        dataclass_instance = Datalass_02(
            field_01="Example",
            field_02=10,
            field_03={
                "nested_field_01": "Example",
                "nested_field_02": 10
            },
            field_04=[0, 1, 2],
            field_05=[
                NestedDatalass_01(
                    field_01=[0, 1, 2],
                    field_02={
                        "nested_field_01": "Example",
                        "nested_field_02": 10
                    }
                ),
                NestedDatalass_01(
                    field_01=[0, 1, 2],
                    field_02={
                        "nested_field_01": "Example",
                        "nested_field_02": 10
                    }
                )
            ]
        )
        dataclass_data = dataclass_instance.as_dict()
        self.assertDictEqual(dataclass_data, expected_data)

    def test__dataclass_with_properties_is_serialized__success(self):
        """Датакласс со проперти созданной @property отражается в сериализованном датаклассе"""
        expected_data = {
            'field_01': 'Example',
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2],
            'field_05': 10
        }
        @dataclass
        class Datalass_01(DataclassImproved):
            field_01: str
            field_02: int
            field_03: dict
            field_04: list[int]

            @property
            def field_05(self):
                return self.field_02

        dataclass_instance = Datalass_01(
            field_01="Example",
            field_02=10,
            field_03={
                "nested_field_01": "Example",
                "nested_field_02": 10
            },
            field_04=[0, 1, 2],
        )
        dataclass_data = dataclass_instance.as_dict()
        self.assertDictEqual(dataclass_data, expected_data)

    def test__json_validated_via_dataclass__success(self):
        """Дата успешно валидируется через датакласс и возвращает инстанс этого датакласса."""
        data = {
            'field_01': 'Example',
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2]
        }

        validated_dataclass = Datalass_01.from_dict(data)
        self.assertIsInstance(validated_dataclass, Datalass_01)

    def test__json_validated_via_dataclass__fail_wrong_field_type(self):
        """Дата с полем неправильного типа при валидации через датакласс поднимает ValidationError"""
        data = {
            'field_01': 1,
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2]
        }

        with self.assertRaises(ValidationError) as context:
            validated_data = Datalass_01.from_dict(data)

        self.assertEqual(context.exception.args[0], "Field 'field_01' has invalid type in the dict data.")

    def test__json_validated_via_dataclass__fail_field_type_is_missing(self):
        """Дата с отсутствующим полем при валидации через датакласс поднимает ValidationError"""
        data = {
            'field_02': 10,
            'field_03': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_04': [0, 1, 2]
        }

        with self.assertRaises(ValidationError) as context:
            validated_dataclass = Datalass_01.from_dict(data)
            self.assertIsInstance(validated_dataclass, Datalass_01)

        self.assertEqual(context.exception.args[0], "Field 'field_01' is missing in the dict data.")

    def test__json_validated_via_nested_dataclass__success(self):
        """Дата успешно валидируется через датакласс и возвращает инстанс этого датакласса"""
        data = {
            'field_01': {
                'field_01': [0, 1, 2],
                'field_02': {
                    'nested_field_01': 'Example',
                    'nested_field_02': 10
                },
            },
            'field_02': 'Example',
            'field_03': 10,
            'field_04': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_05': [0, 1, 2],

        }

        # region Датаклассы
        @dataclass
        class NestedDatalass_01(DataclassImproved):
            field_01: list[int]
            field_02: dict

        @dataclass
        class Datalass_02(DataclassImproved):
            field_01: NestedDatalass_01
            field_02: str
            field_03: int
            field_04: dict
            field_05: list[int]
        #endregion

        validated_dataclass = Datalass_02.from_dict(data)
        self.assertIsInstance(validated_dataclass, Datalass_02)

    def test__json_validated_via_nested_dataclass__fail_wrong_field_type_in_nested(self):
        """
        Дата с полем неправильного типа во вложенном поле при валидации через датакласс
        во вложенном датаклассе поднимает ValidationError
        """
        data = {
            'field_01': {
                'field_01': 'Example',
                'field_02': {
                    'nested_field_01': 'Example',
                    'nested_field_02': 10
                },
            },
            'field_02': 'Example',
            'field_03': 10,
            'field_04': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_05': [0, 1, 2],

        }

        # region Датаклассы
        @dataclass
        class NestedDatalass_01(DataclassImproved):
            field_01: list[int]
            field_02: dict

        @dataclass
        class Datalass_02(DataclassImproved):
            field_01: NestedDatalass_01
            field_02: str
            field_03: int
            field_04: dict
            field_05: list[int]
        #endregion

        with self.assertRaises(ValidationError) as context:
            validated_dataclass = Datalass_02.from_dict(data)
            self.assertIsInstance(validated_dataclass, Datalass_02)

        self.assertEqual(
            context.exception.args[0],
            "Field 'field_01' has invalid type in the dict data."
        )

    def test__json_validated_via_nested_dataclass_has__null_value__success(self):
        """Дата успешно валидируется через датакласс и возвращает инстанс этого датакласса"""
        data = {
            'field_01': {
                'field_01': [0, 1, 2],
                'field_02': None,
            },
            'field_02': 'Example',
            'field_03': 10,
            'field_04': {
                'nested_field_01': 'Example',
                'nested_field_02': 10
            },
            'field_05': [0, 1, 2],

        }

        # region Датаклассы
        @dataclass
        class NestedDatalass_01(DataclassImproved):
            field_01: list[int]
            field_02: dict | None

        @dataclass
        class Datalass_02(DataclassImproved):
            field_01: NestedDatalass_01
            field_02: str
            field_03: int
            field_04: dict
            field_05: list[int]
        #endregion

        validated_dataclass = Datalass_02.from_dict(data)
        self.assertIsInstance(validated_dataclass, Datalass_02)
