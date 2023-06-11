import unittest

from converter import (convert_math, found_typst_op_match,
                       process_math_inline_text, process_unary_math_op,
                       typst2mathjax)


class Tests(unittest.TestCase):

    def test_process_math_inline_text(self):
        sample = '"Var"[X] + "Var"[Y]'
        expected_output = "\\mathrm{Var}[X] + \\mathrm{Var}[Y]"
        actual_output = process_math_inline_text(sample)
        self.assertEqual(expected_output, actual_output)

    def test_convert_math_symbols(self):
        sample = "x in RR arrow CC"
        expected_output = "x \\in \\mathbb{R} \\to \\mathbb{C}"
        actual_output = convert_math(sample)
        self.assertEqual(expected_output, actual_output)

    def test_convert_math_no_args_times(self):
        sample = "x times y"
        expected_output = "x \\times y"
        actual_output = convert_math(sample)
        self.assertEqual(expected_output, actual_output)

    def test_convert_math_no_args_dot(self):
        sample = "x dot y"
        expected_output = "x \\cdot y"
        actual_output = convert_math(sample)
        self.assertEqual(expected_output, actual_output)

    def test_found_typst_op_match_positive_starts_string(self):
        sample = "bold(V) = U + W"
        typst_op = "bold"
        expected_output = True
        actual_output = found_typst_op_match(sample, typst_op=typst_op)
        self.assertEqual(expected_output, actual_output)

    def test_found_typst_op_match_positive_interior(self):
        sample = "x + bold(V)"
        typst_op = "bold"
        expected_output = True
        actual_output = found_typst_op_match(sample, typst_op=typst_op)
        self.assertEqual(expected_output, actual_output)

    def test_found_typst_op_match_negative(self):
        sample = "verybold(V) = U + W"
        typst_op = "bold"
        expected_output = False
        actual_output = found_typst_op_match(sample, typst_op=typst_op)
        self.assertEqual(expected_output, actual_output)

    def test_process_unary_op(self):
        sample = "bold(V) = U + W"
        expected_output = "\mathbf{V} = U + W"
        typst_op = "bold"
        matjax_op = "\\mathbf"
        actual_output = process_unary_math_op(sample, typst_op=typst_op, mathjax_op=matjax_op)
        self.assertEqual(expected_output, actual_output)

    def test_typst2mathjax_no_args(self):
        sample = "A real-valued vector space $(V, +, dot)$ is a set $V$"
        expected_output = "A real-valued vector space \((V, +, \cdot)\) is a set \(V\)"
        actual_output = typst2mathjax(sample)
        self.assertEqual(expected_output, actual_output)

    def test_typst2mathjax_no_args_trailing_text(self):
        sample = "A real-valued vector space $(V, +, dot)$ is a set $V$ and so forth"
        expected_output = "A real-valued vector space \((V, +, \cdot)\) is a set \(V\) and so forth"
        actual_output = typst2mathjax(sample)
        self.assertEqual(expected_output, actual_output)

    def test_typst2math2jax_unary_op(self):
        sample = "A real-valued vector space $bold(V) = U + W$"
        expected_output = "A real-valued vector space \(\mathbf{V} = U + W\)"
        actual_output = typst2mathjax(sample)
        self.assertEqual(expected_output, actual_output)

if __name__ == "__main__":
    unittest.main()
