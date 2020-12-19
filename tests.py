import expression
import unittest

class SimplifyTest(unittest.TestCase):

    def test_integers(self):
        expression1 = "1 + 2 - 3 * 4"
        expression2 = "-9"
        self.assertEqual(expression.auto_simplify(expression1), expression2)
    
    def test_zeros(self):
        expression1 = "0 + 0 - 0 * 0"
        expression2 = "0"
        self.assertEqual(expression.auto_simplify(expression1), expression2)
    
    def test_empty(self):
        expression1 = ""
        expression2 = "0"
        self.assertEqual(expression.auto_simplify(expression1), expression2)
    
    def test_zero_result(self):
        expression1 = "2x^2 * 2x^-2 - 5 + 3x^3 // 3x^3"
        expression2 = "0"
        self.assertEqual(expression.auto_simplify(expression1), expression2)
    
    def test_no_simplification(self):
        expression1 = "5x^4-4x^3+3x^2-2x+1"
        self.assertEqual(expression.auto_simplify(expression1), expression1)
    
    def test_main_cases(self):
        expression1 = "3x^2 * 2x^3 * 3x // 9x^3 + 6 - x"
        expression2 = "2x^3-x+6"
        self.assertEqual(expression.auto_simplify(expression1), expression2)

        expression1 = "3 - x^2 - x - x + 1 - 2 + x^2 * x^3 // x^5"
        expression2 = "-x^2-2x+3"
        self.assertEqual(expression.auto_simplify(expression1), expression2)

        expression1 = "p^444//p^222*p^-222 + 1"
        expression2 = "2"
        self.assertEqual(expression.auto_simplify(expression1), expression2)

        expression1 = "2p^36 // p^18 * 625p // 5p^12 + 1000"
        expression2 = "250p^7+1000"
        self.assertEqual(expression.auto_simplify(expression1), expression2)

        expression1 = "2p^36 // p^18 * 5 * 5 * 5 * 5 * p // 5p^12 - 250 + 750 + 500 + 1 + 0 + 1000000p^-100000 * 0"
        expression2 = "250p^7+1001"
        self.assertEqual(expression.auto_simplify(expression1), expression2)
    
    def test_mult_div(self):
        expression1 = "3821 * -111 * -15895 * 1028 // 20"
        expression2 = "346516299393"
        self.assertEqual(expression.auto_simplify(expression1), expression2)
    
    def test_other(self):
        expression1 = "a + 2a + 3a + 4a + 5a + 100a^2 // 5a - 25a^2 // 5a"
        expression2 = "30a"
        self.assertEqual(expression.auto_simplify(expression1), expression2)

        expression1 = "1 + 1 * 1 - 1"
        expression2 = "1"
        self.assertEqual(expression.auto_simplify(expression1), expression2)

        expression1 = "a^-21 // -a^-4 * -6a^7 * a"
        expression2 = "6a^-9"
        self.assertEqual(expression.auto_simplify(expression1), expression2)




if __name__ == "__main__":
    unittest.main()