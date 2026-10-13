# Base to Base Number

`base_to_base_number` is a lightweight Python package for converting numbers from one base to another. It supports bases from **2 to 36**, handles positive and negative numbers, and processes both integers and fractions.

## Example
A live representation of this package in action is my base number calculator -> [NumberConverter](https://timthewebmaster.com/en/tools/number-converter/)

## Features

- **Wide Base Support**: Convert numbers between any arbitrary bases from 2 up to 36.
- **Signed Numbers**: Fully supports positive (`+`) and negative (`-`) numbers.
- **Fractions Supported**: Handles fractional numbers with customizable precision.
- **Pure Python**: Lightweight implementation with zero external dependencies.

---

## Installation

You can install the package using pip:

```bash
pip install base-to-base-number
```

---

## Usage

Here is a quick example of how to use `BaseNumber` to parse and convert numbers across different bases:

```python
from base_to_base_number.main import BaseNumber

# Initialize a number in base 16 (Hexadecimal)
# You can pass a string representation including signs (+/-) and fractions
num = BaseNumber("-1A.8", base=16)

# Convert to base 10
decimal_result = num.convert_to(10)
print(f"Base 10: {decimal_result}")  # Output: -26.50 (approximate fraction handling)

# Convert to base 2 (Binary)
binary_result = num.convert_to(2, precision=4)
print(f"Base 2: {binary_result}")
```

---

## API Reference

### `BaseNumber(number_str: str, base: int = 10)`
Initializes a number object.
- `number_str`: A string representing the number (e.g., `"1010"`, `"FF.EE"`, `"-45.2"`).
- `base`: The base of the input number (must be between 2 and 36, default is 10).

### Methods
- `convert_to(base: int, precision: int = 2) -> str`: Converts the stored number to a target base with a specified fractional precision.
- `get_number() -> float`: Returns the internal numerical representation (base 10 equivalent).
- `get_integer() -> int`: Returns the integer portion of the number, base 10.
- `get_fraction() -> float`: Returns the fractional portion of the number, base 10.
- `get_integer_raw() -> str`: Returns the origianl integer portion of the number via string.
- `get_fraction_raw() -> str`: Returns the original fractional portion of the number via string.

---

## Requirements

- Python `3.10` or higher.

---

## License

This project is licensed under the terms of the [MIT License](LICENSE).