from mypackage.roman_numbers import RomanNumbers

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


if __name__ == "__main__":
    test_conversion()
    print("Everything passed")
