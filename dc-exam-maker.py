import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chains import SimpleSequentialChain


page_title = "Article and Question Generator"
st.set_page_config(
    page_title=page_title,
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Demo Page by AdCreativeDEv"
    }
)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


st.title(page_title)


# Set API keys
system_openai_api_key = os.environ.get('OPENAI_API_KEY')
system_openai_api_key = st.text_input(":key: OpenAI Key :", value=system_openai_api_key)
os.environ["OPENAI_API_KEY"] = system_openai_api_key




llm = OpenAI(
          model_name="text-davinci-003", # default model
          temperature=0.9,
          verbose=True) 

st.header(':robot_face: Hi ! I am an Exam & Question Bot')
st.header(':point_right: please provide the :blue[Topic] :')
user_topic = st.text_input("Topic ", value="What is different between Hugging Face and OpenAi ?", max_chars=100)
if st.button("Generate"):
    st.subheader("Chain 1 - Article generator")
   

    template = """You are a teacher, your output is to write a estimated 200 words article of this topic.

    Topic:{topic}
    Teacher: Think creative and write this article."""

    prompt_template = PromptTemplate(input_variables=["topic"], template=template)
    article_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)

    article_output = article_chain.run(user_topic)


    
    st.info(article_chain.prompt)
    



    ############################
    # Chain2 - write a question with sugguested 5 multiple choice answers, and only allow one correct answer
    ############################
    st.subheader("Chain 2 - Questions generator")
    template = """ You are a examiner and read on given article , 
                    then write 5 questions and each question with 3 multiple choice answers, only one answer is corrected. 
                    After completed writing all questions,  
                    list out the correct answer of each question  with brief explanation in new section.
    exam article: {article}
    Write questions with required multiple choice answers based on the article:"""




    prompt_template = PromptTemplate(input_variables=["article"], template=template)
    question_chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    st.info(question_chain.prompt)




    # This is the overall chain where we run these two chains in sequence.
    code = f"""
    overall_chain = SimpleSequentialChain(chains=[article_chain, question_chain], verbose=True)
    question = overall_chain.run('{user_topic}'")

    """
    st.subheader("Execute SimpleSequentialChain of Article and question")
    st.code(code)
            
    overall_chain = SimpleSequentialChain(chains=[article_chain, question_chain], verbose=True)
    question = overall_chain.run(user_topic)

    colArticle, colQuestion = st.columns(2)

    with colArticle:
        st.header("Article")
        st.info(article_output)

    with colQuestion:
        st.header("MC Question")
        st.info(question)
        
        
        
 
 

log = """
> Entering new LLMChain chain...
Prompt after formatting:
You are a teacher, your output is to write a estimated 200 words article of this topic.

    Topic:What is different between Hugging Face and OpenAi ?
    Teacher: Think creative and write this article.

> Finished chain.


> Entering new SimpleSequentialChain chain...


> Entering new LLMChain chain...
Prompt after formatting:
You are a teacher, your output is to write a estimated 200 words article of this topic.

    Topic:What is different between Hugging Face and OpenAi ?
    Teacher: Think creative and write this article.

> Finished chain.


When it comes to Artificial Intelligence (AI) technology, two of the most popular and widely used platforms are Hugging Face and OpenAI. Both platforms have their own strengths and weaknesses and offer distinct solutions for different kinds of AI projects. Understanding the differences between them can be helpful in deciding which platform to use. 

The main difference between Hugging Face and OpenAI is the type of AI technology each platform offers. Hugging Face is an open-source platform for natural language processing (NLP) applications while OpenAI is a research laboratory focused on developing artificial general intelligence (AGI) systems. As such, OpenAI has access to more advanced technologies, such as deep learning, machine learning, and reinforcement learning, that can be used to develop AGI systems. By comparison, Hugging Face focuses mainly on natural language processing technology, such as text classification, sentiment analysis, question answering, and automatic summarization. 

When it comes to the development process, Hugging Face is easier to work with for small projects because it offers a range of ready-made models that can be adapted for use. This makes it a great choice for rapid prototyping and tinkering, and it is particularly useful for natural language processing applications. OpenAI, on


> Entering new LLMChain chain...
Prompt after formatting:
 You are a examiner and read on given article , 
                    then write 5 questions and each question with 3 multiple choice answers, only one answer is corrected. 
                    After completed writing all questions,  
                    list out the correct answer of each question  with brief explanation in new section.
    exam article: 

When it comes to Artificial Intelligence (AI) technology, two of the most popular and widely used platforms are Hugging Face and OpenAI. Both platforms have their own strengths and weaknesses and offer distinct solutions for different kinds of AI projects. Understanding the differences between them can be helpful in deciding which platform to use. 

The main difference between Hugging Face and OpenAI is the type of AI technology each platform offers. Hugging Face is an open-source platform for natural language processing (NLP) applications while OpenAI is a research laboratory focused on developing artificial general intelligence (AGI) systems. As such, OpenAI has access to more advanced technologies, such as deep learning, machine learning, and reinforcement learning, that can be used to develop AGI systems. By comparison, Hugging Face focuses mainly on natural language processing technology, such as text classification, sentiment analysis, question answering, and automatic summarization. 

When it comes to the development process, Hugging Face is easier to work with for small projects because it offers a range of ready-made models that can be adapted for use. This makes it a great choice for rapid prototyping and tinkering, and it is particularly useful for natural language processing applications. OpenAI, on
    Write questions with required multiple choice answers based on the article:

> Finished chain.


Q1. What is the main difference between Hugging Face and OpenAI?
A. OpenAI focuses on natural language processing while Hugging Face focuses on artificial general intelligence
B. OpenAI is an open-source platform while Hugging Face is a research laboratory 
C. Hugging Face offers a range of ready-made models while OpenAI is more difficult to work with
D. Hugging Face focuses on machine learning while OpenAI focuses on deep learning

Answer: A. OpenAI focuses on natural language processing while Hugging Face focuses on artificial general intelligence

Explanation: The article states that OpenAI is a research laboratory focused on developing artificial general intelligence (AGI) systems, while Hugging Face is an open-source platform for natural language processing (NLP) applications. 

Q2. What type of technology does OpenAI have access to?
A. Text classification
B. Question answering
C. Automatic summarization
D. Deep learning, machine learning, and reinforcement learning

Answer: D. Deep learning, machine learning, and reinforcement learning

Explanation: The article states that OpenAI has access to more advanced technologies, such as deep learning, machine learning, and reinforcement

> Finished chain.

"""

st.code(log)
