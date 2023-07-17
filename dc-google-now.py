import streamlit as st
import os
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from PIL import Image



page_title = "Google Search"
st.set_page_config(
    page_title=page_title,
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

image = Image.open("search2.jpg")
st.image(image, caption='created by MJ')

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


SearchStr = "Please explain what is Machine Learning in detail . and suggest at least 3 website with url to start my learning with sample dataset "

with st.expander("Sample"):
    image = Image.open("google-search-sample.png")
    st.image(image, caption='Sample Search')
    

# Display the updated value of SearchStr in the text_input control
SearchStr = st.text_input(":point_right: Enter your Question :", value=SearchStr)


if st.button("Search"):
    with st.spinner('Generating ...'):
        st.write('✔️ Langchain Start with Google Search Tool by SERPAPI')
        SearchResult = agent.run(SearchStr)
        st.write('✔️ Langchain Action Completed')
        st.subheader('Search Results:')
        st.info(SearchResult)


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

"""

with st.expander("explanation"):
    st.code(log)
