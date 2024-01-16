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


def test_cases_arab2roman():
    for arab, roman in zip(arabs, romans):
        assert RomanNumbers.arab2roman(arab) == roman
        AssertionError(f"Back conversion of {arab} failed.")


if __name__ == "__main__":
    test_cases_arab2roman()
    print("Everything passed")
