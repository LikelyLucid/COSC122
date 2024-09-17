class Fraction:
    """Defines a Fraction type that has an integer numerator and a non-zero integer denominator"""

    def __init__(self, num=0, denom=1):
        """Creates a new Fraction with numerator num and denominator denom"""
        if isinstance(num, int) and isinstance(denom, int):
            self.numerator = num
            if denom != 0:
                self.denominator = denom
            else:
                raise ZeroDivisionError
        else:
            raise ValueError("Numerator and denominator must be ints")

    def __add__(self, other):
        """ ADD THEM """
        numerator = (self.numerator * other.denominator ) + (other.numerator * self.denominator)
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __mul__(self, other):
        """ MULTIPLY THEM """
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        return Fraction(numerator, denominator)

    def __eq__(self, other):
        """ DOC STRING """
        return self.numerator * other.denominator == self.denominator * other.numerator

    def __str__(self):
        """ DOC STRING """
        return str(self.numerator) + "/" + str(self.denominator)

    def __repr__(self):
        """ DOC STRING """
        return "Fraction(" + str(self.numerator) + ", " + str(self.denominator) + ")"


class ReducedFraction(Fraction):  # is a sub-class of the Fraction class
    """ DOC STRING """
    def __init__(self, numerator, denominator=1):
        """ DOC STIRNG """
        super().__init__(numerator, denominator)  # use Fraction.__init__
        self._reduce()  # next, reduce the numerator/denominator

    def _reduce(self):
        """ REDUCE REUSE RECYCLE """
        self.gcd = find_gcd(self.numerator, self.denominator)
        self.numerator = self.numerator // self.gcd
        self.denominator = self.denominator // self.gcd

    def __repr__(self):
        """ DOC STRING """
        return "ReducedFraction(" + str(self.numerator) + ", " + str(self.denominator) + ")"

    def __add__(self, other):
        """ DOC STRING """
        result = super().__add__(other)
        return ReducedFraction(result.numerator, result.denominator)

    def __mul__(self, other):
        """ DOC STRING """
        result = super().__mul__(other)
        return ReducedFraction(result.numerator, result.denominator)


def find_gcd(num1, num2):
    """
    Returns the Greatest Common Divisor (GCD) of num1 and num2.
    Assumes num1 and num2 are positive integers.
    """
    smaller = min(num1, num2)
    for i in range(smaller, 1, -1):
        if num1 % i == 0 and num2 % i == 0:
            return i
    return 1


class MixedNumber:
    """ MIXY MIXY CHOCOLATEY """
    def __init__(self, interger, fraction):
        """ INIT BRUV """
        if isinstance(fraction, Fraction)
            fraction = ReducedFraction(fraction.numerator, fraction.denominator)
        if fraction.numerator > fraction.denominator:
            difference = fraction.numerator // fraction.denominator

            interger += difference
            fraction.numerator -= difference * fraction.denominator

        self.interger = interger
        self.fraction = fraction

    def __add__(self, other):
        """ ADD """
        new_int = self.interger + other.interger
        new_frac = self.fraction + other.fraction
        return MixedNumber(new_int, new_frac)

    def __str__(self):
        """ STRRR """
        return f"{self.interger} and {self.fraction}"

    def __repr__(self):
        """ REPRR """
        return f"MixedNumber({self.interger}, {repr(self.fraction)})"


mixed_num = MixedNumber(3, Fraction(4, 6))
print(mixed_num)
mixed_num = MixedNumber(4, Fraction(7, 3))
print(mixed_num)

fraction_1 = Fraction(3, 4)
fraction_2 = Fraction(4, 6)
mixed_num_1 = MixedNumber(2, fraction_1)
mixed_num_2 = MixedNumber(1, fraction_2)
print(mixed_num_1 + mixed_num_2)
