from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
import panel as pn
import os

panels = [] # collect display 

pn.extension('texteditor', template="bootstrap", sizing_mode='stretch_width')
pn.state.template.param.update(
    main_max_width="690px",
    header_background="green",
    title='Conversational Chatbot Application'
)

#Widgets
openaikey = pn.widgets.PasswordInput(
    value="", placeholder="Enter your OpenAI API Key here...", width=300, 
)
inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…', toolbar=False, height=50, width=500)
button_conversation = pn.widgets.Button(name="Chat!", button_type='primary')

spacer = pn.Spacer(width=100)

#LLM Model
def chat_bot(input):
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template("The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])

    llm = ChatOpenAI(temperature=0)
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
    response = conversation.predict(input=input)
    
    return response

#Message function
def collect_messages(_):
    os.environ["OPENAI_API_KEY"] = openaikey.value
    prompt = inp.value_input
    inp.value = ''
    if prompt:
        response = chat_bot(input= inp.value_input)
        panels.append(
            pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
        panels.append(
            pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
    
        return pn.Column(*panels)

#layout
interactive_conversation = pn.bind(collect_messages, button_conversation)
pn.Column( 
    pn.pane.Markdown("""
    ## \U0001F60A! A friendly Conversational AI Chatbot
    1) Enter OpenAI API key. This costs $. Set up billing at [OpenAI](https://platform.openai.com/account).
    """
    ),
    pn.Row(inp,spacer,openaikey),
    pn.Row(button_conversation, width=200, margin=(5,150)),
    pn.panel(interactive_conversation, loading_indicator=True, height=200),
).servable()


