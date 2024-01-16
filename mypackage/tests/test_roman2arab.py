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


def test_cases_roman2arab():
    for arab, roman in zip(arabs, romans):
        assert RomanNumbers.roman2arab(roman) == arab
        AssertionError(f"Back conversion of {roman} failed.")


if __name__ == "__main__":
    test_cases_roman2arab()
    print("Everything passed")
