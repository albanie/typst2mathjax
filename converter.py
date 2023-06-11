"""A minimalist converter from typst to MathJax.

Notes:
Currently only supports simple Typst usage (e.g. inline $...$ math mode).
"""
import re

def get_dollar_offsets(line):
    """Get the offsets of all $'s in a line (used to parse math expresssions
    from Typst text)
    
    Args:
        line (str): A line of text
        
    Returns:
        list: A list of offsets of all $'s in the line (0-indexed)
    """
    dollar_offsets = []
    for idx, char in enumerate(line):
        if char == '$' and line[max(idx - 1, 0)] != "\\":
            dollar_offsets.append(idx)
    assert len(dollar_offsets) % 2 == 0, "Number of $'s is not even"
    return dollar_offsets

def process_unary_math_op(x, typst_op, mathjax_op):
    """Convert a unary math operator from Typst to MathJax.

    Args:
        x (str): A string containing a unary math operator
        typst_op (str): The unary math operator in Typst
        mathjax_op (str): The unary math operator in MathJax

    Returns:
        str: The string with the unary math operator converted to MathJax
    """
    assert typst_op in x, f"Operator {typst_op} not found in {x}"
    stack = []
    # split into tokens by delimiters
    delimiters = [f"{typst_op}(", "(", ")"]
    # find groups
    regex_pattern = '(' + '|'.join(map(re.escape, delimiters)) + ')'
    chunks = re.split(regex_pattern, x)
    processed = ""
    curr = ""
    for chunk in chunks:
        if chunk == f"{typst_op}(":
            stack.append(chunk)
        elif chunk == "(":
            curr += chunk
            stack.append(chunk)
        elif chunk == ")":
            matched = stack.pop()
            if matched == f"{typst_op}(":
                processed += f"{mathjax_op}{{{curr}}}"
                curr = ""
            else:
                curr += chunk
        else:
            curr += chunk
    processed += curr
    return processed

    
def found_typst_op_match(x, typst_op):
    """Check if a unary operator is present in a string.

    There are two cases to consider:
    (i) The operator starts the string
    (ii) The operator occurs later in the string, but is prefixed by a space
    """
    return x.startswith(typst_op) or f" {typst_op}" in x


def convert_math(raw_str):
    processed_str = raw_str
    # simple operators that do not require arguments
    operator_map = {
        "dot": "\\cdot",
        "times": "\\times",
        "in": "\\in",
        "arrow": "\\to",
        "lambda": "\\lambda",
        "mu": "\\mu",
    }

    symbol_map = {
        "RR": "\\mathbb{R}",
        "CC": "\\mathbb{C}",
    }

    unary_operator_map = {
        "bold": "\\mathbf",
    }

    for typst_op, mathjax_op in operator_map.items():
        processed_str = processed_str.replace(typst_op, mathjax_op)

    for typst_symbol, mathjax_symbol in symbol_map.items():
        processed_str = processed_str.replace(typst_symbol, mathjax_symbol)
    
    for typst_op, mathjax_op in unary_operator_map.items():
        if found_typst_op_match(processed_str, typst_op):
            processed_str = process_unary_math_op(
                x=processed_str,
                typst_op=typst_op,
                mathjax_op=mathjax_op,
            )
            # add argument
    return processed_str

def typst2mathjax(text):
    """Convert typst text to MathJax text
    
    Parameters
    ----------
    text : str
        Text to be converted
    
    Returns
    -------
    str
        Converted text
    """
    processed_text = []
    for line in text.split("\n"):
        dollar_offsets = get_dollar_offsets(line)
        text_strs, math_strs = [], []

        # add boundaries
        dollar_offsets = [-1] + dollar_offsets + [len(line) + 1]

        for offset_idx, dollar_offset in enumerate(dollar_offsets[:-1]):
            if offset_idx % 2 == 0:
                # text string
                text_strs.append(line[dollar_offset + 1:dollar_offsets[offset_idx + 1]])
            else:
                # math string
                raw_math_str = line[dollar_offset + 1:dollar_offsets[offset_idx + 1]]
                math_strs.append(convert_math(raw_math_str))
        # join text and math strings
        processed_line = []
        for text_str, math_str in zip(text_strs, math_strs):
            processed_line.append(text_str)
            processed_line.append(r"\(" + math_str + r"\)")
        # handle trailing text (if any)
        if len(text_strs) > len(math_strs):
            processed_line.append(text_strs[-1])

        processed_text.append("".join(processed_line))
    return "\n".join(processed_text)


if __name__ == "__main__":
    test_str = "A real-valued vector space $bold(V) = (V, +, dot)$ is a set $V$ with two operations:"
    out = typst2mathjax(test_str)
    print(out)