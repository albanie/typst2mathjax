"""Functions to help streamlit with rendering.
"""

def use_latex_delimiters(text: str) -> str:
    """Convert text with inline mathjax to use Latex delimiters (streamlit seems
    to struggle with inline mathjax).
    """
    replacements = {
        "\\(": "$",
        "\\)": "$",
        "\\[": "$$",
        "\\]": "$$",
    }
    for key, val in replacements.items():
        text = text.replace(key, val)
    return text

