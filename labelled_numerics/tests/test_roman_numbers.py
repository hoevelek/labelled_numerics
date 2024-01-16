from labelled_numerics.roman_numbers import RomanNumbers

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


def test_cases_roman2arab():
    for arab, roman in zip(arabs, romans):
        assert RomanNumbers.roman2arab(roman) == arab
        AssertionError(f"Back conversion of {roman} failed.")


def test_conversion():
    for num in range(0, 3999):
        assert num == RomanNumbers.label2num(
            RomanNumbers.num2label(
                num, RomanNumbers.conversion_dict, sep=" ", method="decimal"
            ),
            RomanNumbers.conversion_dict,
        )
        # print(f"{num} passed test and is equal to {RomanNumbers.formate_nice_roman(LabelledNumerics.num2label(num, RomanNumbers.conversion_dict, sep=' ', method='decimal'))}")
        AssertionError(f"Back conversion of {num} failed.")


def test_cases_arab2roman():
    for arab, roman in zip(arabs, romans):
        assert RomanNumbers.arab2roman(arab) == roman
        AssertionError(f"Back conversion of {arab} failed.")


def test_cases_add_to():
    for index in range(len(instans) - 2):
        print(
            f"The sum of {instans[index].nice_label} and {instans[(index + 1)].nice_label} has the value {instans[index].arab + instans[(index + 1)].arab} with representation {RomanNumbers.formate_nice_roman((instans[index].add_to(instans[(index + 1)])))}."
        )
        precision_arabs = max(
            [
                len(str(arab).split(".")[1]) if isinstance(arab, float) else 0
                for arab in arabs[index : index + 2]
            ]
        )  # precision to prevent from numerical errors
        add_to_part = RomanNumbers.formate_nice_roman(
            instans[index].add_to(instans[(index + 1)])
        )
        add_plus_convert_part = RomanNumbers.formate_nice_roman(
            RomanNumbers.arab2roman(
                round(arabs[index] + arabs[(index + 1)], ndigits=precision_arabs)
            )
        )
        print(
            "The sum of both representations {} and {} is {}.".format(
                instans[index].nice_label,
                instans[(index + 1)].nice_label,
                add_plus_convert_part,
            )
        )
        print(add_to_part)
        print(add_plus_convert_part)
        assert add_to_part == add_plus_convert_part
        AssertionError(
            f"Excecution of {instans[index].add_to(instans[(index + 1)])} failed"
        )


if __name__ == "__main__":
    test_cases_add_to()
    print("Everything passed")

    test_conversion()
    print("Everything passed")

    test_cases_roman2arab()
    print("Everything passed")

    test_cases_arab2roman()
    print("Everything passed")
