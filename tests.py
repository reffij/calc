import unittest

from calculator import (
    is_float,
    BinaryOperator,
    tokenize,
    calculate_rpn,
    infix_to_postfix,
    parse_tree,
    calculate,
)


class TestUtils(unittest.TestCase):

    def test_is_float_true(self) -> None:
        self.assertTrue(is_float("3.14"))
        self.assertTrue(is_float("10"))
        self.assertTrue(is_float("0.0"))

    def test_is_float_false(self) -> None:
        self.assertFalse(is_float("abc"))
        self.assertFalse(is_float("+"))
        self.assertFalse(is_float(""))

class TestBinaryOperator(unittest.TestCase):

    def test_from_char(self) -> None:
        self.assertEqual(BinaryOperator.from_char("+"), BinaryOperator.ADD)
        self.assertEqual(BinaryOperator.from_char("-"), BinaryOperator.SUB)
        self.assertEqual(BinaryOperator.from_char("*"), BinaryOperator.MUL)
        self.assertEqual(BinaryOperator.from_char("/"), BinaryOperator.DIV)
        self.assertEqual(BinaryOperator.from_char("^"), BinaryOperator.EXP)

    def test_operation(self) -> None:
        self.assertEqual(BinaryOperator.ADD(2, 3), 5)
        self.assertEqual(BinaryOperator.SUB(5, 2), 3)
        self.assertEqual(BinaryOperator.MUL(3, 4), 12)
        self.assertEqual(BinaryOperator.DIV(10, 2), 5)
        self.assertEqual(BinaryOperator.EXP(2, 3), 8)

    def test_all_chars_contains_basic(self) -> None:
        chars = BinaryOperator.all_chars()
        for c in ["+", "-", "*", "/", "^"]:
            self.assertIn(c, chars)


class TestTokenizer(unittest.TestCase):

    def test_simple_expression(self) -> None:
        self.assertEqual(
            tokenize("2+2"),
            ["2", "+", "2"]
        )

    def test_complex_expression(self) -> None:
        self.assertEqual(
            tokenize("3+(4*5)"),
            ["3", "+", "(", "4", "*", "5", ")"]
        )

    def test_spaces(self) -> None:
        self.assertEqual(tokenize(" 2 + 2 "), ["2", "+", "2"])

    def test_decimal_numbers(self) -> None:
        self.assertEqual(tokenize("3.5+2.1"), ["3.5", "+", "2.1"])

    def test_multi_digit_numbers(self) -> None:
        self.assertEqual(tokenize("123+456"), ["123", "+", "456"])


class TestRPN(unittest.TestCase):

    def test_basic_rpn(self) -> None:
        self.assertEqual(
            calculate_rpn(["2", "3", "+"]),
            5
        )

    def test_rpn_mixed_ops(self) -> None:
        self.assertEqual(
            calculate_rpn(["2", "3", "4", "*", "+"]),
            14
        )

    def test_rpn_unary_minus(self) -> None:
        self.assertEqual(
            calculate_rpn(["5", "-u"]),
            -5
        )

    def test_rpn_invalid_stack(self) -> None:
        with self.assertRaises(ValueError):
            calculate_rpn(["+"])

    def test_rpn_unknown_token(self) -> None:
        with self.assertRaises(ValueError):
            calculate_rpn(["2", "?", "+"])

    
    def test_1(self) -> None:
        val = [
            "2", "2", "+"
        ]
        res: float = 4
        self.assertEqual(calculate_rpn(val), res)

    def test_2(self) -> None:
        val = [
            "10", "4", "-"
        ]
        res: float = 6
        self.assertEqual(calculate_rpn(val), res)

    def test_3(self) -> None:
        val = [
            "5", "6", "*"
        ]
        res: float = 30
        self.assertEqual(calculate_rpn(val), res)

    def test_4(self) -> None:
        val = [
            "12", "4", "/"
        ]
        res: float = 3
        self.assertEqual(calculate_rpn(val), res)

    def test_5(self) -> None:
        val = [
            "3", "4", "+", "5", "*"
        ]
        res: float = 35
        self.assertEqual(calculate_rpn(val), res)        

    def test_6(self) -> None:
        val = [
            "3", "4", "5", "*", "+"
        ]
        res: float = 23
        self.assertEqual(calculate_rpn(val), res)        

    def test_7(self) -> None:
        val = [
            "5", "1", "2", "+", "4", "*", "+", "3", "-"
        ]
        res: float = 14
        self.assertEqual(calculate_rpn(val), res)        
   
    def test_8(self) -> None:
        val = [
            "100", "200", "+"
        ]
        res: float = 300
        self.assertEqual(calculate_rpn(val), res)        

    def test_9(self) -> None:
        val = [
            "3", "7", "-"
        ]
        res: float = -4
        self.assertEqual(calculate_rpn(val), res)        

    def test_10(self) -> None:
        val = [
            "-5", "-3", "+"
        ]
        res: float = -8
        self.assertEqual(calculate_rpn(val), res)        

    def test_11(self) -> None:
        val = [
            "3.5", "2", "*"
        ]
        res: float = 7
        self.assertEqual(calculate_rpn(val), res)        

    def test_12(self) -> None:
        val = [
            "42"
        ]
        res: float = 42
        self.assertEqual(calculate_rpn(val), res)        
    def test_div_by_0(self) -> None:
        val = [
            "5", "0", "/"
        ]
        self.assertRaises(ZeroDivisionError, calculate_rpn, val)

    def test_13(self) -> None:
        val = [
            "3", "4", "+", "*"
        ]
        self.assertRaises(ValueError, calculate_rpn, val)

    def test_14(self) -> None:
        val = [
            "3", "4", "5", "+"
        ]
        self.assertRaises(ValueError, calculate_rpn, val)

    def test_15(self) -> None:
        val = [
            "3", "4", "+", "*"
        ]
        self.assertRaises(ValueError, calculate_rpn, val)

    def test_16(self) -> None:
        val = [
            "3", "abc", "+"
        ]
        self.assertRaises(ValueError, calculate_rpn, val)


class TestParserAndPostfix(unittest.TestCase):

    def test_postfix_simple(self) -> None:
        tokens = ["2", "+", "3"]
        self.assertEqual(infix_to_postfix(tokens), ["2", "3", "+"])

    def test_postfix_precedence(self) -> None:
        tokens = ["2", "+", "3", "*", "4"]
        self.assertEqual(
            infix_to_postfix(tokens),
            ["2", "3", "4", "*", "+"]
        )
    
    def test_single_operand(self) -> None:
        self.assertEqual(
            infix_to_postfix(["42"]),
            ["42"]
        )

    def test_simple_addition(self) -> None:
        self.assertEqual(
            infix_to_postfix(["2", "+", "3"]),
            ["2", "3", "+"]
        )

    def test_simple_subtraction(self) -> None:
        self.assertEqual(
            infix_to_postfix(["5", "-", "2"]),
            ["5", "2", "-"]
        )

    def test_multiplication_precedence(self) -> None:
        self.assertEqual(
            infix_to_postfix(["2", "+", "3", "*", "4"]),
            ["2", "3", "4", "*", "+"]
        )

    def test_division_precedence(self) -> None:
        self.assertEqual(
            infix_to_postfix(["10", "-", "6", "/", "2"]),
            ["10", "6", "2", "/", "-"]
        )

    def test_parentheses_override_precedence(self) -> None:
        self.assertEqual(
            infix_to_postfix(["(", "2", "+", "3", ")", "*", "4"]),
            ["2", "3", "+", "4", "*"]
        )

    def test_nested_parentheses(self) -> None:
        self.assertEqual(
            infix_to_postfix(
                ["(", "2", "+", "(", "3", "*", "4", ")", ")"]
            ),
            ["2", "3", "4", "*", "+"]
        )

    def test_exponent_precedence(self) -> None:
        self.assertEqual(
            infix_to_postfix(["2", "+", "3", "^", "4"]),
            ["2", "3", "4", "^", "+"]
        )

    def test_decimal_operands(self) -> None:
        self.assertEqual(
            infix_to_postfix(["3.5", "*", "2.1"]),
            ["3.5", "2.1", "*"]
        )

    def test_negative_number_operand(self) -> None:
        self.assertEqual(
            infix_to_postfix(["-3.5", "+", "2"]),
            ["-3.5", "2", "+"]
        )

    def test_complex_expression(self) -> None:
        self.assertEqual(
            infix_to_postfix(
                ["3", "+", "4", "*", "2", "/", "(", "1", "-", "5", ")"]
            ),
            ["3", "4", "2", "*", "1", "5", "-", "/", "+"]
        )
    
    def test_invalid_operand_raises(self) -> None:
        with self.assertRaises(SyntaxError):
            infix_to_postfix(["2", "+", "abc"])

    def test_unmatched_left_parenthesis_raises(self) -> None:
        with self.assertRaises(SyntaxError):
            infix_to_postfix(["(", "2", "+", "3"])

    def test_unmatched_right_parenthesis_raises(self) -> None:
        with self.assertRaises(SyntaxError):
            infix_to_postfix(["2", "+", "3", ")"])
    
    def test_empty_input(self) -> None:
        res: list[str] = []
        self.assertEqual(
            infix_to_postfix([]),
            res
        )


class TestFullCalculator(unittest.TestCase):

    def test_basic(self) -> None:
        self.assertEqual(calculate("2+2"), 4)

    def test_precedence(self) -> None:
        self.assertEqual(calculate("2+3*4"), 14)

    def test_parentheses(self) -> None:
        self.assertEqual(calculate("(2+3)*4"), 20)

    def test_power_right_associative(self) -> None:
        self.assertEqual(calculate("2^3^2"), 512)

    def test_power_left_side_grouping(self) -> None:
        self.assertEqual(calculate("(2^3)^2"), 64)

    def test_unary_minus(self) -> None:
        self.assertEqual(calculate("-2+3"), 1)

    def test_complex_expression(self) -> None:
        self.assertEqual(calculate("3+(4*5)-2^3"), 15)

    def test_unary_minus_only(self) -> None:
        self.assertEqual(calculate("-5"), -5)

    def test_double_negative(self) -> None:
        self.assertEqual(calculate("--5+2"), 7)

    def test_unary_in_expression(self) -> None:
        self.assertEqual(calculate("2*-3"), -6)

if __name__ == "__main__":
    unittest.main()
