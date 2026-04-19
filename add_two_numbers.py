"""
add_two_numbers.py
==================
Production-ready utility for adding two numeric values.

Overview:
    This module provides a validated, logged, and CLI-accessible function
    to add two numbers. It is designed for use both as an importable library
    and as a standalone command-line tool. Suitable for integration into
    larger pipelines, APIs, or automation scripts.

Usage (CLI):
    python add_two_numbers.py --a 5.5 --b 3.2
    python add_two_numbers.py --a 10 --b -4

Usage (library):
    from add_two_numbers import add
    result = add(3, 4.5)
"""

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------
import argparse   # For parsing command-line arguments
import logging    # For structured, configurable logging
import math       # For math utilities like isnan, isinf
import sys        # For sys.exit() to terminate with a non-zero exit code on error

# --------------------------------------------------------------------------
# Logging configuration
# --------------------------------------------------------------------------
# basicConfig sets up the root logger. In production, you would typically
# configure this via a config file or environment variable.
logging.basicConfig(
    level=logging.INFO,                          # Log INFO and above (INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Timestamp + level + message
    datefmt="%Y-%m-%dT%H:%M:%S",                # ISO 8601 timestamp format
)

# Get a named logger for this module (best practice over using root logger directly)
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------------
def add(a: float, b: float) -> float:
    """
    Add two numbers and return the result.

    Args:
        a (float): The first operand. Must be a finite real number.
        b (float): The second operand. Must be a finite real number.

    Returns:
        float: The arithmetic sum of a and b.

    Raises:
        TypeError: If either argument is not an int or float.
        ValueError: If either argument is NaN or infinite.
    """
    # --- Type validation ---
    # isinstance() checks if a variable belongs to a given type or tuple of types.
    # We accept both int and float since int is a subset of numeric types.
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError(
            f"Both arguments must be int or float. Got: a={type(a).__name__}, b={type(b).__name__}"
        )

    # --- Value validation ---
    # math.isnan() returns True if the value is Not a Number (e.g. float('nan')).
    # math.isinf() returns True if the value is positive or negative infinity.
    # Neither can produce a meaningful arithmetic result.
    if math.isnan(a) or math.isnan(b):
        raise ValueError("Arguments must not be NaN.")
    if math.isinf(a) or math.isinf(b):
        raise ValueError("Arguments must be finite numbers, not infinity.")

    result: float = a + b  # Perform addition; Python handles int+float promotion automatically

    logger.info("add(%s, %s) = %s", a, b, result)  # Log the operation for observability

    return result


# --------------------------------------------------------------------------
# CLI argument parser
# --------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the CLI argument parser.

    Returns:
        argparse.ArgumentParser: Configured parser with --a and --b arguments.
    """
    # ArgumentParser generates --help automatically and handles usage errors
    parser = argparse.ArgumentParser(
        prog="add_two_numbers",
        description="Add two numbers and print the result.",
        epilog="Example: python add_two_numbers.py --a 5.5 --b 3.2",
    )

    # add_argument() defines an expected argument.
    # type=float converts the raw string input to a Python float.
    # required=True means the flag must be provided; omitting it raises an error.
    parser.add_argument("--a", type=float, required=True, help="First number (int or float)")
    parser.add_argument("--b", type=float, required=True, help="Second number (int or float)")

    return parser


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
# The `if __name__ == "__main__"` guard ensures this block only runs when the
# script is executed directly (not when imported as a module).
if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()  # Parse sys.argv; exits with usage error if args are missing/invalid

    try:
        result = add(args.a, args.b)
        print(f"Result: {result}")   # Print to stdout for CLI consumers
    except (TypeError, ValueError) as exc:
        # Log the error and exit with code 1 to signal failure to the calling process
        logger.error("Invalid input: %s", exc)
        sys.exit(1)
