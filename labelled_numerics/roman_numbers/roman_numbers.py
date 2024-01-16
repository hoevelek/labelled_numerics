from __future__ import annotations  # to allow self-reference in type hints

from labelled_numerics import setup_logger
from labelled_numerics.utils import labelled_numerics as ln

logger = setup_logger.logger


class RomanNumbers(ln.LabelledNumerics):
    """Class for Roman numbers. Inherits from abstract class LabelledNumerics meaning that each 'sillabus' of the roman number is a label with a corresponding value.
    Combinations of this labels correspond to a total number which is the sum of its labels.
    """

    conversion_dict = {
        "zero": 0,
        "I": 1,
        "IV": 4,
        "V": 5,
        "IX": 9,
        "X": 10,
        "XL": 40,
        "L": 50,
        "XC": 90,
        "C": 100,
        "CD": 400,
        "D": 500,
        "CM": 900,
        "M": 1000,
    }

    _max_value = 3999

    def __init__(self, label):
        # string preprocessing/chunking if e.g. formate is MMMCMXCIX instead of M M M CM XC IX
        # can not work for floats, because of the ambiguity after the dot, e.g. .3 -> .III and .111 -> .I I I
        if "." not in label:
            label = ln.LabelledNumerics.formate_chunky(
                label, RomanNumbers.conversion_dict, sep=" "
            )
        super().__init__(label, RomanNumbers.conversion_dict)
        if (
            "." in self.name
        ):  # whatever comes after the dot is not converted and estimated to be a chunked properly, e.g. .3 -> .III and .1 -> .I I I (ambiguous otherwise)
            part_int = RomanNumbers.formate_chunky(
                self.name.split(".")[0].strip(), RomanNumbers.conversion_dict, sep=" "
            )
            part_past_comma = self.name.split(".")[1].strip()
            self.label = part_int + " . " + part_past_comma
            self.nice_label = (
                RomanNumbers.formate_nice_roman(part_int) + " . " + part_past_comma
            )
        else:
            self.label = self.name
            self.nice_label = RomanNumbers.formate_nice_roman(self.name)
        self.arab = RomanNumbers.roman2arab(self.name)

    def add_to(self, other: RomanNumbers):
        """Adds two Roman numerals.
        :param other: other Roman numeral
        :type other: RomanNumbers
        :return: sum of two Roman numerals as Roman numeral string
        :rtype: str
        """
        # get values

        if not isinstance(other, RomanNumbers):
            raise TypeError(
                f"Other {other} is not a valid Roman number instance (RomanNumbers)."
            )
        else:
            result = self.arab + other.arab
            # round to precision of the larger number  #this expects that the other number can be determined with same precision to make sense!
            digits = max(
                [
                    len(str(num).split(".")[1]) if isinstance(num, float) else 0
                    for num in [self.arab, other.arab]
                ]
            )
            result = round(result, ndigits=digits)
            if isinstance(result, int):
                return RomanNumbers.formate_nice_roman(
                    RomanNumbers.formate_chunky(
                        RomanNumbers.arab2roman(result), RomanNumbers.conversion_dict
                    )
                )
            elif isinstance(result, float):
                return RomanNumbers.arab2roman(result)

    @staticmethod
    def arab2roman(number):
        """
        Converts a number to Roman numerals. Use num2label from abstract class LabelledNumerics.
        :param number: number to be converted
        :type number: int, float
        :return: Roman numeral
        :rtype: str
        """
        if number < 0 or number > RomanNumbers._max_value:
            raise ValueError(f"Number {number} is not in valid range (1-3999).")

        if "0" in str(number):
            # warning message
            logger.warning(msg='Number {number} contains zero, replacement "zero"')

        if isinstance(number, int):
            return RomanNumbers.num2label(
                number, RomanNumbers.conversion_dict, sep=" ", method="decimal"
            )
        elif isinstance(number, float):
            return RomanNumbers.num2label(
                number, RomanNumbers.conversion_dict, sep=" ", method="decimal_float"
            )
        else:
            raise TypeError(f"Number {number} is not a valid number (int, float).")

    @staticmethod
    def roman2arab(number):
        """Converts Roman numerals to a arabian number.
        :param number: Roman numeral
        :type number: str
        :return: arabian number
        :rtype: int
        """
        if isinstance(number, str):
            if "." in number:
                # if float, split at dot
                digits = 0  # to round properly to prevent float errors
                result = RomanNumbers.label2num(
                    number.split(".")[0].strip(), RomanNumbers.conversion_dict, sep=" "
                )
                for exponent, word in enumerate(number.split(".")[1].strip().split()):
                    digits += 1
                    result += RomanNumbers.label2num(
                        RomanNumbers.formate_chunky(word, RomanNumbers.conversion_dict),
                        RomanNumbers.conversion_dict,
                        sep=" ",
                    ) / 10 ** (exponent + 1)
                return round(result, ndigits=digits)
            else:
                return RomanNumbers.label2num(
                    number, RomanNumbers.conversion_dict, sep=" "
                )
        else:
            raise TypeError(f"Number {number} is not a valid number (str).")

    @staticmethod
    def formate_nice_roman(roman_number: str) -> str:
        """Format roman number to be used in conversion_dict
        :param roman_no: roman number
        :type roman_no: str
        :return: formatted roman number
        :rtype: str
        """
        # group as long as follwoing char is equal to current char, e.g. C C C -> CCC
        rom_no_out = ""
        mem = "?"
        for char in roman_number.split():
            if char != " ":
                if char == mem:
                    rom_no_out += char
                else:
                    rom_no_out += " " + char
                mem = char
            if (
                char == "."
            ):  # do not format after dot . III : .3 and .I I I: .111 are different and expected to be typed in correctly
                rom_no_out += roman_number.split(".")[1]
                break
        return rom_no_out.strip()

    @staticmethod
    def replace_all_arabs(text: str) -> str:
        """Replace all arabic numbers in text by roman numbers.
        :param text: text to be scanned
        :type text: str
        :return: text with replaced arabic numbers
        :rtype: str
        """
        # replace all arabic numbers in text by roman numbers
        text_out = ""
        for word in text.split():
            if word.isdigit():
                if "." in word:
                    text_out += RomanNumbers.arab2roman(word) + " "
                else:
                    text_out += (
                        RomanNumbers.formate_nice_roman(
                            RomanNumbers.arab2roman(int(word))
                        )
                        + " "
                    )
            else:
                text_out += word + " "
        return text_out.strip()


if __name__ == "__main__":
    # special test cases
    arabs = [1050, 1999, 1, 0, 3, 5.67893, 3999]
    romans = [
        "M L",
        "M CM XC IX",
        "I",
        "zero",
        "I I I",
        "V . VI VII VIII IX III",
        "M M M CM XC IX",
    ]
    instans = [RomanNumbers(roman) for roman in romans]
    RomanNumbers(
        RomanNumbers.formate_chunky("MMCMXCIX", RomanNumbers.conversion_dict)
    ).nice_label

    # list all methods of instans[0]
    # print(dir(instans[0]))

    print("SOME EXAMPLES:")
    # implemented for integers only (relying class was made for molecule formula string and does not support floats)
    print(f"The conversion dictionary of an instance is {instans[1].conversion}.")
    print(
        "You can do mathematical operations using the arab property, e.g. instans[0].arab * instans[5].arab"
    )
    print(
        f"E. g.: The obtained number for {instans[4].nice_label} times {instans[5].nice_label} is {instans[4].arab * instans[5].arab}."
    )
    print(
        "You can convert the obtained number back to a roman number using RomanNumbers.arab2roman(instans[0].arab * instans[5].arab)"
    )
    print(
        f"E. g.: The obtained number for {instans[4].nice_label} time {instans[5].nice_label} is {RomanNumbers.formate_nice_roman(RomanNumbers.arab2roman(instans[4].arab * instans[5].arab))}."
    )
    print(f"The name of the roman number is {instans[1].name}.")
    print(
        "The nicely formatted roman number of e.g. M MM L V I II is {}.".format(
            RomanNumbers("M MM L V I II").nice_label
        )
    )
    print(
        f"The sum of all chunks (integer only) (I, X, ...) is {instans[1].sum_values}."
    )
    print(f"It should be equal to .arab property: {instans[1].arab}")
    print(
        f"Some implemented operations: If you add two roman numbers with add_to this also works for floats: {instans[0].add_to(instans[1])} with value {instans[0].arab + instans[1].arab}."
    )
    print(
        f"Only in the integer case this will be equal to the sum of the instances: {instans[0] + instans[1]}"
    )
    print(
        'To replace all arabic numbers in "bla 34 bla 56 bla" by roman numbers use RomanNumbers.replace_all_arabs("bla 34 bla 56 bla")'
    )
    print("E. g.: {}".format(RomanNumbers.replace_all_arabs("bla 34 bla 56 bla")))
