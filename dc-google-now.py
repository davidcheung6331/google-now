import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
import subprocess
import speech_recognition as sr
from PIL import Image
image = Image.open("search2.jpg")



page_title = "Google Search"
st.set_page_config(
    page_title=page_title,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "Demo Page by AdCreativeDEv"
    }
)


st.title(":globe_with_meridians:  " + page_title)



hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



# st.header(':robot_face: Hi ! Gogole now')
system_openai_api_key = os.environ.get('OPENAI_API_KEY')
system_openai_api_key = st.text_input(":key: OpenAI Key :", value=system_openai_api_key)
os.environ["OPENAI_API_KEY"] = system_openai_api_key


system_serpapi_api_key = os.environ.get('SERPAPI_API_KEY')
system_serpapi_api_key="2412a22f7b5670afb53a687e0432d84cad408de0ee6bfc11db9c76be08ffec71"
system_serpapi_api_key = st.text_input(":key: SERPAPI Key :", value=system_serpapi_api_key)
os.environ["SERPAPI_API_KEY"] = system_serpapi_api_key



llm = OpenAI(temperature=0)
conversation = ConversationChain(llm=llm, verbose=True)

tools = load_tools(["serpapi", "llm-math"], llm=llm)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


SearchStr = "what is the today biggest news from 10  years ago ?"
recorded_text = ""

if st.button("Start Recording"):
    r = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            r.adjust_for_ambient_noise(source)
            st.info("Recording started...")

            audio = r.listen(source, phrase_time_limit=10)
            transcript = r.recognize_google(audio)
            st.info(transcript)

            # Update the value of SearchStr with the transcribed text
            recorded_text = transcript
            print(f"1. recorded_text = {recorded_text}")


    except sr.UnknownValueError:
        st.warning("No speech detected.")
    except sr.RequestError as e:
        st.error(f"Error: {e}")

# Update the value of SearchStr with the recorded_text
SearchStr = recorded_text if recorded_text else SearchStr
print(f"1. SearchStr = {SearchStr}")
            


# Display the updated value of SearchStr in the text_input control
recorded_text = st.text_input(":point_right:", value=SearchStr)
print(f"2. recorded_text = {recorded_text}")


# if st.button("conversation Search"):
#     print(f"3. recorded_text = {recorded_text}")
#     SearchResult = conversation.predict(input=recorded_text)
#     st.info(SearchResult)
#     # text to spech the search
#     # espeak(SearchResult)
#     subprocess.call(["say", SearchResult])

if st.button("Search"):
    print(f"3. recorded_text = {recorded_text}")
    SearchResult = agent.run(recorded_text)
    st.info(SearchResult)
    # text to spech the search
    # espeak(SearchResult)
    subprocess.call(["say", SearchResult])


log = """
> Entering new AgentExecutor chain...
 I need to find out what the biggest news was 10 years ago

 Action: Search

 Action Input: biggest news 10 years ago

 Observation: No good search result found

 Thought: I need to narrow down the search

 Action: Search

 Action Input: biggest news 10 years ago USA

 Observation: These were the biggest stories of the decade. ... 2010: The FBI arrests 10 Russian spies caught living deep undercover in the United States.

 Thought: I now know the final answer

 Final Answer: The FBI arrests 10 Russian spies caught living deep undercover in the United States.

> Finished chain.


######

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
SearchResult = agent.run(recorded_text)



"""

with st.expander("explanation"):
    st.code(log)
