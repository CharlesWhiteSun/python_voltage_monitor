import pytest
from typing import Tuple, Iterable, Type, Any
from src.utils.impl.validators import validate_type


# 測試組 (名稱, 允許型別)
test_suites: Iterable[Tuple[str, Tuple[Type[Any], ...]]] = [
    ("只允許 float", (float,)),
    ("允許 float, int", (float, int)),
    ("允許 str", (str,)),
    ("允許 list, tuple", (list, tuple)),
]

# 測資
test_cases = [
    (220.5, 221.0, 219.8),             # 全 float
    (221, 208, 222),                   # 全 int
    (221.0, 208, 222.5),               # float + int
    ("abc", "def"),                    # 全 str
    (["a", "b"], ["c"]),               # list of str
    ((1, 2), (3, 4)),                  # tuple of int
    ([], ()),                           # 空 list, tuple
    ({'a': 1.0, 'b': 2.0},),           # dict values float
    ({"x": "a", "y": "b"},),           # dict values str
    (1.0, "string", 3),                # 混合型別
    (None,),                            # None
]

def is_valid_case(values: Any, allow_types: Tuple[Type[Any], ...]) -> bool:
    """
    判斷輸入值是否符合 allow_types（只檢查最外層）。
    """
    if not isinstance(values, tuple):
        values = (values,)
    return all(isinstance(v, allow_types) for v in values)


@pytest.mark.parametrize("suite_name, allow_types", test_suites)
@pytest.mark.parametrize("values", test_cases)
def test_validate_type_positive_and_negative(suite_name, allow_types, values):
    expect_pass = is_valid_case(values, allow_types)

    if expect_pass:
        # 正向測試
        try:
            validate_type(values, allow_types=allow_types)
        except TypeError as e:
            pytest.fail(f"Unexpected TypeError: {e}")
    else:
        # 負向測試
        with pytest.raises(TypeError):
            validate_type(values, allow_types=allow_types)
