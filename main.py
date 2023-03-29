import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import os

st.set_page_config(page_title="Emailizer", page_icon=":email:", layout="centered", initial_sidebar_state="expanded")

template = """
You are a helpful assistant that takes care of the following tasks:
- Translate the email into the correct English type from Italian
- Add the correct salutation
- Add the correct closing
- Takes care of the correct formality of the email

Some examples of formal emails are:
- Thank you for your email. I will get back to you as soon as possible.
- I am sorry to hear that you are not feeling well. I hope you will feel better soon.
Some examples of informal emails are:
- Thank you for your email. I will get back to you as soon as possible.
- I am sorry to hear that you are not feeling well. I hope you will feel better soon.

American english: Fries, 
British english: Chips, 

Here are the input parameters:
- Formality: {formality}
- English type: {type}
- Email: {mail}

Here goes your output:
"""

prompt = PromptTemplate(
    input_variables=["formality", "type", "mail"],
    template=template
    )

def load_llm(api_key):
    os.environ["OPENAI_API_KEY"] = api_key
    llm = OpenAI(temperature=0.4)
    return llm

st.title("Hello World")
st.write("This is a test")

ai_key = st.text_input(label="AI key", placeholder="Enter your OpenAI api key", type="password")

try:
    llm = load_llm(ai_key)
    st.success("AI key loaded successfully")
except Exception as e:
    st.error("AI key not loaded")

st.header("Enter your email")

col_1, col_2 = st.columns(2)
with col_1:
    formality_type = st.selectbox(
        "Formality", 
        options=["Formal", "Informal"]
        )
with col_2:
    eng_type = st.selectbox(
        "English type", 
        options=["American english", "British english"]
        )

mail_input = st.text_area(label="", placeholder="Enter your email", height=100)

st.header("Email output")

if mail_input:
    try:
        prompt_input = prompt.format(
            formality=formality_type,
            type=eng_type,
            mail=mail_input
        )
        output = llm(prompt_input)
        st.write(output)
    except Exception as e:
        if "API key" in str(e):
            st.error("Woops, the api key is not valid")
        else:
            st.error("Woops, something went wrong")
