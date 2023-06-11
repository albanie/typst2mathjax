# Import necessary module
import streamlit as st
from converter import typst2mathjax
from streamlit_utils import use_latex_delimiters


# Title of the webpage
st.title('Typst to MathJax')

# Textbox where user can paste or type text
user_input = st.text_area('Enter/Paste your text here', height=200)

# Convert button
if st.button('Convert to MathJax'):
    mathjax_text = typst2mathjax(user_input)

    # Display the converted text
    st.text_area('Converted Text (MathJax)', value=mathjax_text, height=200)
    
    st.title('Rendered MathJax')

    # Render the text as MathJax
    st.markdown(use_latex_delimiters(mathjax_text))
