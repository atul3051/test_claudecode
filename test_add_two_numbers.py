"""
test_add_two_numbers.py
=======================
Unit tests for add_two_numbers.py using pytest.

Run with:
    pytest test_add_two_numbers.py -v
"""

# --------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------
import math    # For math.inf and math.nan constants used in edge-case tests
import pytest  # pytest provides the test runner, fixtures, and assertion helpers

# Import the function under test using a direct module import.
# This works when both files are in the same directory (or the package is installed).
from add_two_numbers import add


# --------------------------------------------------------------------------
# Happy-path tests — expected correct behaviour
# --------------------------------------------------------------------------
class TestAddHappyPath:
    """Tests for valid inputs that should return a correct numeric result."""

    def test_two_positive_integers(self):
        # Basic sanity check: 2 + 3 must equal 5
        assert add(2, 3) == 5

    def test_two_positive_floats(self):
        # pytest.approx() handles floating-point precision issues (e.g. 0.1 + 0.2 ≠ 0.3 exactly)
        assert add(1.1, 2.2) == pytest.approx(3.3)

    def test_positive_and_negative(self):
        assert add(10, -4) == 6

    def test_two_negative_numbers(self):
        assert add(-5, -3) == -8

    def test_zeros(self):
        assert add(0, 0) == 0

    def test_integer_and_float_mixed(self):
        # Python promotes int + float → float automatically
        assert add(3, 1.5) == pytest.approx(4.5)

    def test_large_numbers(self):
        assert add(1_000_000, 2_000_000) == 3_000_000

    def test_negative_result(self):
        assert add(-10, 3) == -7

    def test_result_is_float_type(self):
        # When both inputs are int, Python returns int; when either is float, result is float
        result = add(1.0, 2.0)
        assert isinstance(result, float)


# --------------------------------------------------------------------------
# Edge-case / boundary tests
# --------------------------------------------------------------------------
class TestAddEdgeCases:
    """Tests for boundary values that are still valid inputs."""

    def test_very_small_floats(self):
        # 1e-300 is near Python's minimum positive float but still finite
        assert add(1e-300, 1e-300) == pytest.approx(2e-300)

    def test_very_large_floats(self):
        # 1e308 is near Python's maximum float (sys.float_info.max ≈ 1.8e308)
        assert add(1e308, 0) == pytest.approx(1e308)

    def test_add_zero_identity(self):
        # Adding zero should return the original value unchanged
        assert add(42, 0) == 42
        assert add(0, 42) == 42


# --------------------------------------------------------------------------
# Negative tests — invalid inputs that must raise exceptions
# --------------------------------------------------------------------------
class TestAddInvalidInputs:
    """Tests that verify proper exceptions are raised for invalid arguments."""

    # pytest.raises() is a context manager that asserts a specific exception is raised.
    # The test FAILS if the exception is NOT raised.

    def test_string_input_first_arg(self):
        with pytest.raises(TypeError):
            add("5", 3)  # type: ignore[arg-type]  # noqa: intentional bad input

    def test_string_input_second_arg(self):
        with pytest.raises(TypeError):
            add(3, "5")  # type: ignore[arg-type]

    def test_none_input(self):
        with pytest.raises(TypeError):
            add(None, 3)  # type: ignore[arg-type]

    def test_list_input(self):
        with pytest.raises(TypeError):
            add([1, 2], 3)  # type: ignore[arg-type]

    def test_nan_first_arg(self):
        # math.nan is a valid Python float value but not a meaningful number
        with pytest.raises(ValueError, match="NaN"):
            add(math.nan, 3)

    def test_nan_second_arg(self):
        with pytest.raises(ValueError, match="NaN"):
            add(3, math.nan)

    def test_inf_first_arg(self):
        # math.inf represents positive infinity — not a valid operand here
        with pytest.raises(ValueError, match="finite"):
            add(math.inf, 3)

    def test_negative_inf_second_arg(self):
        with pytest.raises(ValueError, match="finite"):
            add(3, -math.inf)

    def test_both_nan(self):
        with pytest.raises(ValueError, match="NaN"):
            add(math.nan, math.nan)

    def test_error_message_contains_types(self):
        # Verify the TypeError message includes the actual bad types for debuggability
        with pytest.raises(TypeError, match="str"):
            add("x", 1)
