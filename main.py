import streamlit as st
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

st.set_page_config(page_title="Emailizer", page_icon=":email:", layout="centered", initial_sidebar_state="expanded")


template = """
You are a helpful assistant that takes care of the following tasks:
- Translate the email into the correct English type
- Add the correct salutation
- Add the correct closing
- Takes care of the correct formality of the email

An example of formal emails is:
'Subject: [Name] has joined the team

Dear [Name],

I am pleased to introduce you to [Another Name] who is starting today as a Customer Support Representative. She will be providing technical support and assistance to our users, making sure they enjoy the best experience with our products.

Feel free to greet [Another Name] in person and congratulate her with the new role!

Best regards,
[Your name]
[Job title]'

An examples of informal emails is:
'Subject: How are you?
Hi [Name],

How's it going?

Sorry I haven't been in touch for such a long time but I've had exams so I've been studying every free minute. Anyway, I'd love to hear all your news and I'm hoping we can get together soon to catch up. We just moved to a bigger flat so maybe you can come and visit one weekend?

How's the new job?  

Looking forward to hearing from you!

[Your name]'

Some examples of British English vs American English:
French fries/fries (American) vs. chips (British)
cotton candy (American) vs. candyfloss (British)
apartment (American) vs. flat (British)
garbage (American) vs. rubbish (British)
cookie (American) vs. biscuit (British)
green thumb (American) vs. green fingers (British)
parking lot (American) vs. car park (British)
pants (American) vs. trousers (British)
windshield (American) vs. windscreen (British)


Here are the input parameters:
- Formality: {formality}
- English type: {type}
- Email: will be added by the user

Here goes your output:
"""

human_template="{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

prompt=PromptTemplate(
    template=template,
    input_variables=["formality", "type"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])


def load_llm(api_key):
    chat = ChatOpenAI(openai_api_key=api_key, temperature=0.4)
    chain = LLMChain(llm=chat, prompt=chat_prompt)
    return chain

st.title("Hey :wave:")
st.write("This is a simple app that takes an email and translates it into the correct English type, adds the correct salutation and closing, and takes care of the correct formality of the email.")

ai_key = st.text_input(label="AI key", placeholder="Enter your OpenAI api key", type="password")

try:
    chain = load_llm(ai_key)
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
        output = chain.run(formality=formality_type, type=eng_type, text=mail_input)
        st.write(output)
    except Exception as e:
        if "API key" in str(e):
            st.error("Woops, the api key is not valid")
        else:
            st.error("Woops, something went wrong")
