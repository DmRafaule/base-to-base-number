import re
from .alphabet import CHAR_TO_DIGIT_MAP, DIGIT_TO_CHAR_MAP


def get_base_regex(base: int) -> str:
    """
    Generates a regular expression for detecting any base (2 to 36).
    """
    if not (2 <= base <= 36):
        raise ValueError("Base must be between 2 and 36 inclusive.")

    if base <= 10:
        max_digit = str(base - 1)
        char_class = f"0-{max_digit}" if base > 1 else "0"
    else:
        max_letter_code = ord('A') + (base - 11)
        max_letter = chr(max_letter_code)
        char_class = f"0-9A-{max_letter}a-{max_letter.lower()}"

    sign = r"[+-]?"
    fraction_delimeter = "[.,]"
    body = f"[{char_class}]+"
    fraction = f"(?:{fraction_delimeter}[{char_class}]+)?"

    return f"^{sign}{body}{fraction}$"

class BaseNumber:

    def __init__(self, number_str: str, base: int = 10):
        """Initializes the BaseNumber.

        :param number_str: String representation of the number (can include '+' or '-')
        """
        self.base = base
        # Check if it is a right number for particular base
        if not re.match(get_base_regex(self.base), number_str):
            raise ValueError(f"'{number_str}' is not a valid number for base {self.base}.")
        # Extract the sign
        cleaned_str = number_str.strip()
        if cleaned_str.startswith(("-", "+")):
            self.sign_provided = True
            self.sign = cleaned_str[0]
            cleaned_str = cleaned_str[1:]
        else:
            self.sign_provided = False
            self.sign = "+"

        self.number_str = cleaned_str
        delimeter_pos_match = re.search(r"[.,]", self.number_str)
        # Divide a number into two parts if needed
        if delimeter_pos_match:
            self.integer_str = cleaned_str[:delimeter_pos_match.start()]
            self.fraction_str = cleaned_str[(delimeter_pos_match.start() + 1):]
        else:
            self.integer_str = cleaned_str
            self.fraction_str = None

        # Save the dict with raw values instead of digits
        self.digit_dict_raw = {}
        for power, char in enumerate(reversed(self.integer_str)):
            self.digit_dict_raw.update({power: char})
        if self.fraction_str:
            for power, char in enumerate(reversed(self.fraction_str), start=len(self.fraction_str) * -1):
                self.digit_dict_raw.update({power: char})

        # Save the dict with only digits in base10
        self.digit_dict_base10 = {}
        for power, number in self.digit_dict_raw.items():
            self.digit_dict_base10.update({power: CHAR_TO_DIGIT_MAP[number]})
        
        # Convert to base 10
        self.number_int = 0
        for power, number in self.digit_dict_base10.items():
            self.number_int += (number * pow(base, power))
        self.integer_int = int(self.number_int)
        self.fraction_int = self.number_int - self.integer_int

    def __str__(self):
        return self.number_str

    def get_fraction_raw(self):
        return self.fraction_str

    def get_integer_raw(self):
        return self.integer_str

    def get_number_raw(self):
        return self.number_str

    def get_fraction(self):
        return self.fraction_int

    def get_integer(self):
        return self.integer_int

    def get_number(self):
            return self.number_int

    def is_fraction_part_present(self):
        if self.get_fraction_raw():
            return True
        else:
            return False

    def _convert_int_part(self, part_int: int, base: int, precision: int = None):
        digits = []
        dividend = part_int
        counter = 0
        while True:
            digits.append(dividend % base) # To save
            dividend = int(dividend / base)
            counter += 1
            # If specified, then we calculate fraction part, otherwise integer part
            if precision:
                if not dividend and counter >= precision:
                    break
            else:
                if not dividend:
                    break
        return digits

    def _convert_fraction_part(self, part_frac: int, base: int, precision: int):
        digits = []
        fractional_part = part_frac
        counter = 0
        
        while counter < precision:
            fractional_part *= base
            digit = int(fractional_part)
            digits.append(digit)
            fractional_part -= digit 
            counter += 1
            
        return digits
        
    def convert_to(self, base: int, precision:int = 2) -> str:
        result_number = ""
        
        if self.sign_provided:
            result_number = self.sign + result_number
        
        if base == self.base:
            result_number += self.get_integer_raw()
            if self.is_fraction_part_present():
                result_number += '.'
                result_number += self.get_fraction_raw()[:precision]
            return result_number

        # Converting integer part of the number
        for digit in list(reversed(self._convert_int_part(self.integer_int, base))):
            result_number += DIGIT_TO_CHAR_MAP[digit]
        
        # Converting fraction part of the number
        if self.is_fraction_part_present():
            result_number += '.'
            for digit in self._convert_fraction_part(self.fraction_int, base, precision):
                result_number += DIGIT_TO_CHAR_MAP[digit]


        return result_number
