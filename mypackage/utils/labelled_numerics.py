from typing import Tuple

import numpy as np

from mypackage import setup_logger

# get logger from setup_logger.py
logger = setup_logger.logger


class LabelledNumerics:
    """A class representing labelled numerics:
    A labelled numeric is a string of labels, e.g. "H H O".
    Each label has a corresponding numeric value, e.g. H: 1, O: 16.
    The numeric value of a labelled numeric is the sum of the numeric values of the labels, e.g. "H2O" -> 1 + 1 + 16 = 18.
    Fucionalities:
    - convert a string to a labelled numeric
    - convert a labelled numeric to a string
    - calculate all combinations of labels that sum to a given number (e. g. all molecules that have a mass of 18)
    - calculate the combination with least number of labels (e.g. H20 instaed of H18)
    - calculate the mean of two labelled numerics
    - append two labelled numerics (e. g. clustering molecules)
    - calculate the sum of two labelled numerics (e. g. mass of cluster)
    - convert a chunked string to a chemical formula (e.g. H H H O O O -> H3O3)
    """

    def __init__(self, label_str: str, conversion_dict: dict[str, int], sep: str = " "):
        self.conversion = conversion_dict
        self.name = label_str
        self.sep = sep
        # error if dict values are not unique
        if len(set(self.conversion.values())) != len(self.conversion.values()):
            raise ValueError()  # "values not unique"
        # error if values are smaller than zero
        if any(value < 0 for value in self.conversion.values()):
            raise ValueError()  # "value < 0"

    def get_dictionary(self):
        return self.conversion

    def get_name(self):
        return self.name

    def set_name(self, name: str):
        self.name = name

    def set_dictionary(self, conversion_dict: dict[str, int]):
        self.conversion = conversion_dict

    def __repr__(self):
        return f"{self.name} object"

    def __str__(self):
        return f"{self.name} object"

    def __add__(self, other):
        return self.sum_values + other.sum_values

    def __sub__(self, other):
        return self.sum_values - other.sum_values

    def __mul__(self, other):
        return self.sum_values * other.sum_values

    def __truediv__(self, other):
        return self.sum_values / other.sum_values

    def __floordiv__(self, other):
        return self.sum_values // other.sum_values

    def __mod__(self, other):
        return self.sum_values % other.sum_values

    def _tolist(self) -> list:
        return self.name.split(self.sep)

    def _convert(self):
        num_list = [self.conversion[word] for word in self._tolist()]
        return num_list

    def append(self, other, sort: bool = False):
        if sort:
            # sort by value
            new_name = self.sep.join(
                sorted(
                    self._tolist() + other._tolist(), key=lambda x: self.conversion[x]
                )
            )
        else:
            new_name = self.sep.join(self._tolist() + other._tolist())
        return LabelledNumerics(new_name, self.conversion)

    @property
    def condensed_name(self):  # will give H3O2 instead of HHHOO
        # count occurences of each label
        labels = self._tolist()
        label_count = {label: labels.count(label) for label in labels}
        # condensed name
        condensed_name = ""
        for label in label_count.keys():
            if label_count[label] > 1:
                condensed_name += label + str(label_count[label])
            else:
                condensed_name += label
        return condensed_name

    @property
    def values(self):
        return self._convert()

    @property
    def sum_values(self):
        return sum(self._convert())

    @property
    def mean(self):
        return np.mean(self._convert())

    @staticmethod
    def _to_chunks(
        number: int | float, conversion_dict: dict[str, int]
    ) -> Tuple[list, list, str]:
        """Split a number into chunks of a given size, starting with the largest chunk and working down to the smallest
        :num: number to split
        :type num: int
        :return: list of chunks
        :rtype: list
        """
        # test type
        if not isinstance(number, int):
            raise TypeError(f"num must be int, not {type(number)}")

        # initialize lists
        values = []
        labels = []
        result_string = ""

        # special zero case relevant for single digit numbers
        # check if num is zero
        if str(number).startswith("0"):
            values.append(0)
            # corresponding key
            if 0 in conversion_dict.values():
                labels.append(
                    [key for key, value in conversion_dict.items() if value == 0][0]
                )
            else:
                labels.append("0")

        # remove zeros from conversion_dict as algorithm does not work with zeros
        if 0 in conversion_dict.values():
            conversion_dict = {
                key: value for key, value in conversion_dict.items() if value != 0
            }

        for chunklabel, chunksize in sorted(
            conversion_dict.items(), reverse=True, key=lambda item: item[1]
        ):
            # print(chunklabel, chunksize, number)
            while number >= chunksize and chunksize > 0:
                # if number is greater than chunksize, add chunk to outputlist
                values.append(chunksize)
                labels.append(chunklabel)
                result_string += chunklabel + " "
                number -= chunksize
        return values, labels, result_string.strip()

    @staticmethod
    def _combinations_sum(target, candidates):
        """Given a set of candidate numbers (candidates) (without duplicates) and a target number (target),
        find all unique combinations in candidates where the candidate numbers sum to target.
        The same repeated number may be chosen from candidates unlimited number of times.
        Note:
        All numbers (including target) will be positive integers.
        The solution set must not contain duplicate combinations.
        Parameters:
        :target: target number
        candidates: list of candidate numbers
        :Returns:
        :result: list of lists of the unique combinations, where each inner list is a combination that sums to target
        """

        def backtrack(start, target, path):
            if target == 0:
                result.append(path)
                return
            for i in range(start, len(candidates)):
                if candidates[i] > target:
                    break
                backtrack(i, target - candidates[i], path + [candidates[i]])

        result = []
        candidates.sort()
        backtrack(0, target, [])
        return result

    @staticmethod
    def get_combinations(
        target_number: int, conversion_dict, selected_keys: list[str] = None
    ) -> list:
        """Get all combinations of a target number
        :param target_number: target number
        :type target_number: int
        :param selected_keys: selected keys, defaults to None
        :type selected_keys: list[str], optional
        :return: list of combinations
        :rtype: list
        """
        # test type
        if not isinstance(target_number, int):
            raise TypeError(f"target_number must be int, not {type(target_number)}")
        if selected_keys is not None:
            if not isinstance(selected_keys, list):
                raise TypeError(
                    f"selected_keys must be list, not {type(selected_keys)}"
                )
            if not all(isinstance(key, str) for key in selected_keys):
                raise TypeError(
                    f"selected_keys must be list[str], not {type(selected_keys)}"
                )
        # get combinations
        if selected_keys is None:
            return LabelledNumerics._combinations_sum(
                target_number, list(conversion_dict.values())
            )
        else:
            return LabelledNumerics._combinations_sum(
                target_number,
                [
                    conversion_dict[key]
                    for key in selected_keys
                    if key in conversion_dict
                ],
            )

    @staticmethod
    def convert_formula(formula: str) -> str:
        """Replaces chemical formula or equivalent string to labelled numerics compatible format, e.g. H20 to HHO or C6H12O6 to CCCCCCOOOOOOHHHHHHHHHHHH"""
        # test type
        if not isinstance(formula, str):
            raise TypeError(f"formula must be str, not {type(formula)}")
        # initialize output
        output = ""
        # loop over formula
        # break into parts at each capital letter
        list_of_parts = []
        for char in formula:
            if char.isupper():
                list_of_parts.append(char)
            else:
                list_of_parts[-1] += char

        for part in list_of_parts:
            # split into letters and numbers if number is present
            # multiply letters by number
            if any(char.isdigit() for char in part):
                # split into letters and numbers
                letters = ""
                numbers = ""
                for char in part:
                    if char.isalpha():
                        letters += char
                    else:
                        numbers += char
                # multiply letters by numbers
                output += (letters + " ") * int(numbers)
            else:
                output += part + " "
        return output.strip()

    @staticmethod
    def formate_chunky(
        string_repr: str, conversion_dict: dict, sep: str = " ", sorted_inv: bool = True
    ) -> str:
        """Breaks a string to chunks. If sorted_inv it starts with the largest chunk (largest value for key) and working down to the smallest.
            If sorted_inv is False, it will start with the longest chunk (largest length of key) and working down to the smallest. In this case the return value will be unsorted.
        :param string_repr: string to break into chunks
        :type string_repr: str
        :param conversion_dict: dictionary to convert
        :type conversion_dict: dict[str, int]
        :param sep: separator, defaults to " "
        :type sep: str, optional
        :param sorted_inv: if True, string will be sorted by chunk size (e.g. for numbers), else return string might be permutation of input string (e.g. for chemical formulas)
        :type sorted_inv: bin
        :return: string
        """
        if not isinstance(string_repr, str):
            raise TypeError(
                f"string representation must be str, not {type(string_repr)}"
            )

        if (
            "." in string_repr
        ):  # chunk will end at dot, relevant for number representations
            logger.warning(msg="formate chunky ignores everything after dot")
            string_repr = string_repr.split(".")[0]

        result_string = ""

        if sorted_inv:
            for chunklabel, _ in sorted(
                conversion_dict.items(), reverse=True, key=lambda item: item[1]
            ):
                while len(string_repr) > 0:
                    # if number is greater than chunksize, add chunk to outputlist
                    if string_repr.strip().startswith(chunklabel):
                        result_string += chunklabel + sep
                        string_repr = string_repr.strip()[len(chunklabel) :]
                    else:
                        break
            return result_string.strip(sep)
        else:
            # sort dictionary by longest key first (otherwise substrings maybe will be replaced first)
            # conversion_dict_sorted = {
            #     k: v
            #     for k, v in sorted(
            #         conversion_dict.items(), key=lambda item: len(item[0]), reverse=True
            #     )
            # }
            conversion_dict_sorted = dict(
                sorted(
                    conversion_dict.items(), key=lambda item: len(item[0]), reverse=True
                )
            )

            for chunklabel, _ in conversion_dict_sorted.items():
                while len(string_repr) > 0:
                    # if number is somewhere in word, remove word from string and add chunk to outputlist
                    if chunklabel in string_repr:
                        result_string += chunklabel + sep
                        string_repr = string_repr.replace(chunklabel, "", 1)
                    else:
                        break
            return result_string.strip(sep)

    @staticmethod
    def _convert_to_str_digitwise(
        num: int, conversion_dict: dict[str, int], sep: str = " "
    ) -> str:
        """Convert a number to a string digitwise
        :param num: number to convert
        :type num: int
        :param conversion_dict: dictionary to convert
        :type conversion_dict: dict[str, int]
        :return: string
        :rtype: str
        """
        # test type
        if not isinstance(num, int):
            raise TypeError(f"num must be int, not {type(num)}")
        # test type of conversion_dict
        if not isinstance(conversion_dict, dict):
            raise TypeError(
                f"conversion_dict must be dict[str, int], not {type(conversion_dict)}"
            )
        # convert each digit of chunk to label
        labels = []
        for digit in str(num):
            _, label, _ = LabelledNumerics._to_chunks(int(digit), conversion_dict)
            labels.append("".join(label))
        return sep.join(labels)

    @staticmethod
    def _convert_to_str_decimal(
        num: int, conversion_dict: dict[str, int], sep: str = " "
    ) -> str:
        """Convert a number to a string decimal
        :param num: number to convert
        :type num: int
        :param conversion_dict: dictionary to convert
        :type conversion_dict: dict[str, int]
        :return: string
        :rtype: str
        """
        if not isinstance(num, int):
            raise TypeError(f"num must be int, not {type(num)}")
        if not isinstance(conversion_dict, dict):
            raise TypeError(
                f"conversion_dict must be dict[str, int], not {type(conversion_dict)}"
            )

        _, labels, _ = LabelledNumerics._to_chunks(num, conversion_dict)
        return sep.join(labels)

    @staticmethod
    def _convert_to_str_decimal_float(
        num: float, conversion_dict: dict[str, int], sep: str = " "
    ) -> str:
        """Convert a number to a string decimal
        :param num: number to convert
        :type num: int
        :param conversion_dict: dictionary to convert
        :type conversion_dict: dict[str, int]
        :return: string
        :rtype: str
        """
        if not isinstance(num, float):
            raise TypeError(f"num must be float, not {type(num)}")
        if not isinstance(conversion_dict, dict):
            raise TypeError(
                f"conversion_dict must be dict[str, int], not {type(conversion_dict)}"
            )

        _, labels, _ = LabelledNumerics._to_chunks(int(num), conversion_dict)
        return (
            sep.join(labels)
            + " . "
            + LabelledNumerics._convert_to_str_digitwise(
                int(str(num).split(".")[1]), conversion_dict, sep=sep
            )
        )

    @staticmethod
    def num2label(
        num: int | float,
        conversion_dict: dict[str, int],
        sep: str = "",
        method: str = "decimal",
    ) -> str:
        """Convert a number to a string
        :param num: number to convert
        :type num: int
        :param conversion_dict: dictionary to convert
        :type conversion_dict: dict[str, int]
        :return: string
        :rtype: str
        """
        # test input
        if not isinstance(num, (int, float)):
            raise TypeError(f"num must be int or float, not {type(num)}")
        if not isinstance(conversion_dict, dict):
            raise TypeError(
                f"conversion_dict must be dict[str, int], not {type(conversion_dict)}"
            )
        if not isinstance(sep, str):
            raise TypeError(f"sep must be str, not {type(sep)}")
        if not isinstance(method, str):
            raise TypeError(
                f"method must be str and 'decimal', 'digitwise' or 'decimal_float', not {type(method)}"
            )
        if method not in ["decimal", "digitwise", "decimal_float"]:
            raise ValueError(
                f"method must be 'decimal', 'digitwise' or 'decimal_float', not {method}"
            )

        # convert num to string
        if method == "decimal":
            return LabelledNumerics._convert_to_str_decimal(
                int(num), conversion_dict, sep=sep
            )
        elif method == "digitwise":
            return LabelledNumerics._convert_to_str_digitwise(
                int(num), conversion_dict, sep=sep
            )
        elif method == "decimal_float":
            return LabelledNumerics._convert_to_str_decimal_float(
                num, conversion_dict, sep=sep
            )
        else:
            raise ValueError(f"method {method} not implemented")

    @staticmethod
    def label2num(label: str, conversion_dict: dict[str, int], sep: str = " ") -> int:
        """Convert a string to a number
        :param label: string to convert
        :type label: str
        :param conversion_dict: dictionary to convert
        :type conversion_dict: dict[str, int]
        :return: number
        :rtype: int
        """
        # test type
        if not isinstance(label, str):
            raise TypeError(f"label must be str, not {type(label)}")
        if not isinstance(conversion_dict, dict):
            raise TypeError(
                f"conversion_dict must be dict[str, int], not {type(conversion_dict)}"
            )
        if not isinstance(sep, str):
            raise TypeError(f"sep must be str, not {type(sep)}")

        # convert each chunk of label to number
        num_list = []
        for chunk in label.split(sep):
            num_list.append(conversion_dict[chunk])
        return sum(num_list)


if __name__ == "__main__":
    # EXAMPLES: chemical formulas, spoken numbers, roman numbers

    # This example is for working with chemical formulas
    organic_atoms = {
        "H": 1,
        "C": 12,
        "N": 14,
        "O": 16,
        "F": 19,
        "P": 31,
        "S": 32,
        "Cl": 35,
        "Br": 80,
        "I": 127,
    }

    water = LabelledNumerics(
        LabelledNumerics.convert_formula("H2O"), conversion_dict=organic_atoms
    )
    oxygen = LabelledNumerics(
        LabelledNumerics.convert_formula("O2"), conversion_dict=organic_atoms
    )
    print(
        f"For numerical representations of {water.condensed_name} use {water.name} with masses {water.values}."
    )
    mass_water_oxygen_complex = water + oxygen
    water_oxygen_complex = water.append(oxygen, sort=True)
    expected_loss_mass = water_oxygen_complex.sum_values - water.sum_values
    mean_atomic_mass = water_oxygen_complex.mean
    print(f"The mean atomic mass of {water_oxygen_complex.name} is {mean_atomic_mass}.")
    print(
        f"The expected mass after the loss of water from {water_oxygen_complex.condensed_name} is {expected_loss_mass}."
    )
    water_oxygen_complex.name
    print(
        f"The mass of the two constitutens {water.condensed_name} and {oxygen.condensed_name} is {water + oxygen}."
    )

    selected_keys = ["O", "H"]
    dict_selection = {
        key: organic_atoms[key] for key in selected_keys if key in organic_atoms
    }
    # careful, use all combinations (fct combinations_sum)! Will only give you largest number of molecules, likely valid for most small hydrocarbons
    combi_with_lowest_number_of_atoms = LabelledNumerics(
        LabelledNumerics.num2label(
            mass_water_oxygen_complex, dict_selection, sep=" ", method="decimal"
        ),
        organic_atoms,
    )
    print(
        f"Simple chunk method to find the combination for mass {mass_water_oxygen_complex} with lowest number of atoms: {combi_with_lowest_number_of_atoms.condensed_name}"
    )

    # all combinations
    all_combis = LabelledNumerics.get_combinations(
        mass_water_oxygen_complex, organic_atoms, selected_keys=selected_keys
    )
    # convert to chemical formula
    print(
        f"all combinations for the mass {mass_water_oxygen_complex} with allowed elements {selected_keys}:"
    )  # costly for large molecules
    for solution in all_combis:
        converted = [
            LabelledNumerics.num2label(int(elem), organic_atoms) for elem in solution
        ]
        # convert to chemical formula
        print(LabelledNumerics(" ".join(converted), organic_atoms).condensed_name)

    # convert vector of masses (output of backtrack algorithm) to chemical formula
    mass_vec = [12, 1, 1, 1, 1, 1, 16]  # output of find_combinations
    testobject5 = [
        LabelledNumerics.num2label(int(mass_vec_entry), organic_atoms)
        for mass_vec_entry in mass_vec
    ]
    print(
        "It is also possible to hand over a vector of masses ({}) to calculate the chemical formula {}:".format(
            mass_vec,
            LabelledNumerics(" ".join(testobject5), organic_atoms).condensed_name,
        )
    )
    mass_of_unformated = LabelledNumerics.label2num(
        LabelledNumerics.formate_chunky(
            "ClCC C H HH", conversion_dict=organic_atoms, sep=",", sorted_inv=False
        ),
        conversion_dict=organic_atoms,
        sep=",",
    )
    print(
        "The mass of the unformated string {} is {}.".format(
            "ClCC C H HH", mass_of_unformated
        )
    )
    print(
        "The unformated string {} can be converted to the chemical formula {}.".format(
            "HClCC C H HH",
            LabelledNumerics(
                LabelledNumerics.formate_chunky(
                    "HClCC C H HH", organic_atoms, sorted_inv=False
                ),
                conversion_dict=organic_atoms,
            ).condensed_name,
        )
    )

    ############################################################################################################

    # This example is for working with spoken numbers
    # define conversion dictionary
    conversion_dict = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15,
        "sixteen": 16,
        "seventeen": 17,
        "eighteen": 18,
        "nineteen": 19,
        "twenty": 20,
        "thirty": 30,
        "forty": 40,
        "fifty": 50,
        "sixty": 60,
        "seventy": 70,
        "eighty": 80,
        "ninety": 90,
        # "hundred": 100,
        "one hundred": 100,  # for "one hundred four
        "two hundred": 200,
        "three hundred": 300,
        "four hundred": 400,
        "five hundred": 500,
        "six hundred": 600,
        "seven hundred": 700,
        "eight hundred": 800,
        "nine hundred": 900,
        "one thousand": 1000,
    }
    # initialize object (if whitespaces are in keys, use another separator, e.g. ",")
    testobject1 = LabelledNumerics(
        LabelledNumerics.formate_chunky("one hundred four", conversion_dict, sep=","),
        conversion_dict,
        sep=",",
    )
    testobject2 = LabelledNumerics(
        LabelledNumerics.formate_chunky("seventy one", conversion_dict, sep=","),
        conversion_dict,
        sep=",",
    )

    # print object and properties
    print(testobject1)
    print(f"The chunk values are: {testobject1.values}")
    print(
        f"The arabian number representation of the object is: {testobject1.sum_values}"
    )
    print(
        "The sum of the two numbers {} and {} is {}.".format(
            testobject1.name.replace(",", " "),
            testobject2.name.replace(",", " "),
            testobject1 + testobject2,
        )
    )
    print(
        f"The total, chunked constitution of two numbers can be found by appending the two numbers:\n {testobject1.append(testobject2, sort=True).name}."
    )
    print(
        'The mean of the two numbers "{}" and "{}" is {}.'.format(
            testobject1.name.replace(",", " "),
            testobject2.name.replace(",", " "),
            (testobject1 + testobject2) / 2,
        )
    )
    print(
        "The spoken representation of the decimal number {} is:\n {}".format(
            testobject1.sum_values,
            testobject1.num2label(
                testobject1.sum_values, conversion_dict, sep=" ", method="decimal"
            ),
        )
    )
    print(
        "The spoken representation of the series {} is:\n {}".format(
            "1 2 3 4 5 6 7 8 9 1 0",
            testobject1.num2label(
                12345678910, conversion_dict, sep=", ", method="digitwise"
            ),
        )
    )
    print(
        "The spoken representation of the float {} is:\n {}".format(
            "1034.567890",
            testobject1.num2label(
                1034.567890, conversion_dict, sep=" ", method="decimal_float"
            ),
        )
    )

    ##################################################################################################

    # Example roman numbers
    roman_numbers = {
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

    def formate_nice_roman(roman_no: str) -> str:
        """Format roman number to be used in conversion_dict
        :param roman_no: roman number
        :type roman_no: str
        :return: formatted roman number
        :rtype: str
        """
        # group as long as follwoing char is equal to current char, e.g. C C C -> CCC
        rom_no_out = ""
        mem = "?"
        for char in roman_no.split():
            if char != " ":
                if char == mem:
                    rom_no_out += char
                else:
                    rom_no_out += " " + char
                mem = char
            if (
                char == "."
            ):  # do not format after dot . III : .3 and .I I I: .111 are different and expected to be typed in correctly
                rom_no_out += roman_no.split(".")[1]
                break
        return rom_no_out.strip()

    conversion_dict = roman_numbers

    print(
        "The unformatted roman number {} can be broken into chunks {}.".format(
            "MMMCMXCVIII",
            LabelledNumerics.formate_chunky("MMMCMXCVIII", conversion_dict, sep=" "),
        )
    )
    print(
        "The unformatted roman number {} can be formatted nicely {}.".format(
            "M MMCMXCVI II",
            formate_nice_roman(
                LabelledNumerics.formate_chunky(
                    "M MMCMXCVI II", conversion_dict, sep=" "
                )
            ),
        )
    )
    arab = LabelledNumerics.label2num(
        LabelledNumerics.formate_chunky(
            "MMMCMXCVIII", conversion_dict=roman_numbers, sep=","
        ),
        conversion_dict=roman_numbers,
        sep=",",
    )
    print(
        "The arabian number representation of the roman number {} is {}.".format(
            "MMM CM XC V III", arab
        )
    )
    back_converted = LabelledNumerics.num2label(
        arab, conversion_dict=roman_numbers, sep=" ", method="decimal"
    )
    print(
        f"Back_conversion: The roman number representation of the arabian number {arab} is {formate_nice_roman(back_converted)}."
    )
    # convert a float to roman number
    print(
        "The roman number representation of the float {} is {}.".format(
            3.1415,
            LabelledNumerics.num2label(
                3.123456789,
                conversion_dict=roman_numbers,
                sep=" ",
                method="decimal_float",
            ),
        )
    )

    # initialize object
    testobject3 = LabelledNumerics("M CM XC IV", roman_numbers)
    testobject4 = LabelledNumerics("M CM XC I I", roman_numbers)

    # print object
    print(f"The name of the object is {testobject3.name}.")
    # print values
    print(f"The values of the object are {testobject3.values}.")
    # print sum
    print(f"The sum of the object is {testobject3.sum_values}.")
    # numeric to labelled
    print(
        "The sum of {} and {} has the value {} with representation {}.".format(
            formate_nice_roman(testobject3.name),
            formate_nice_roman(testobject4.name),
            testobject3 + testobject4,
            formate_nice_roman(
                LabelledNumerics.num2label(
                    testobject3 + testobject4, roman_numbers, sep=" ", method="decimal"
                )
            ),
        )
    )
    print(
        " A conversion of the series {} to roman numbers is {}.".format(
            "1 2 3 4 5 6 7 8 9 1 0",
            LabelledNumerics.num2label(
                12345678910, roman_numbers, sep=", ", method="digitwise"
            ),
        )
    )

    # test case: back conversion and original should be equal for all numbers in range 1-3999

    def test_conversion():
        for num in range(0, 3999):
            assert num == LabelledNumerics.label2num(
                LabelledNumerics.num2label(
                    num, roman_numbers, sep=" ", method="decimal"
                ),
                roman_numbers,
                sep=" ",
            )
            # print(f"{num} passed test and is equal to {formate_nice_roman(LabelledNumerics.num2label(num, roman_numbers, sep=' ', method='decimal'))}")
            AssertionError(f"Back conversion of {num} failed.")
        return True

    print(
        f"The conversion arab -> roman follow by roman -> arab gave the same result for all numbers in range 0 to 3999: {test_conversion()}"
    )
    print(
        "All numbers in range 1-3999 can be converted to roman numbers and back without loss of information."
    )
