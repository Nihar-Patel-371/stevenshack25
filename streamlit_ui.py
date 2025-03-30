import streamlit as st
import pandas as pd
from utils import query_gpt, generate_graph, generate_career_simulation_data, chatbot_prompt,simulation_prompt
from PyPDF2 import PdfReader
import plotly.graph_objects as go


ms = st.session_state
if "themes" not in ms: 
  ms.themes = {"current_theme": "light",
                    "refreshed": True,
                    
                    "dark": {"theme.base": "white",
                              "theme.backgroundColor": "white",
                              "theme.primaryColor": "#FF4B4B",
                              "theme.secondaryBackgroundColor": "#F0F2F6",
                              "theme.textColor": "#31333F",
                              "button_face": "🌞"},

                    "light":  {"theme.base": "black",
                              "theme.backgroundColor": "#000000",
                              "theme.primaryColor": "#FF4B4B",
                              "theme.secondaryBackgroundColor": "#1a1a1a",
                              "theme.textColor": "#F0F2F6",
                              "button_face": "🌜"},

            
                    }


  

def ChangeTheme():
  previous_theme = ms.themes["current_theme"]
  tdict = ms.themes["light"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]
  for vkey, vval in tdict.items(): 
    if vkey.startswith("theme"): st._config.set_option(vkey, vval)

  ms.themes["refreshed"] = False
  if previous_theme == "dark": ms.themes["current_theme"] = "light"
  elif previous_theme == "light": ms.themes["current_theme"] = "dark"


btn_face = ms.themes["light"]["button_face"] if ms.themes["current_theme"] == "light" else ms.themes["dark"]["button_face"]
st.button(btn_face, on_click=ChangeTheme)

if ms.themes["refreshed"] == False:
  ms.themes["refreshed"] = True
  st.rerun()
st.markdown("""
    <style>
    section[data-testid="stSidebar"] img {
        margin-top: -80px;
    }
    </style>
""", unsafe_allow_html=True)
with st.sidebar:
    st.image("logo_t.png", width=180)

# Main Application
st.title("CareerIQ")

# Tabs for Chatbot and Visualizations
tab1, tab2 = st.tabs(["Chatbot", "What If Simulation"])

# Chatbot Tab
with tab1:
    st.header("Take your next career step with us...")
    
    # Initialize chat history if it doesn't exist in session state
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    # User input
    user_input = st.chat_input("Type your message")
    if user_input:
        # Append user message to history
        st.session_state["messages"].append({"role": "user", "content": user_input})
        
        # Show loading spinner while getting AI response
        with st.spinner("Generating response..."):
            # Get AI response
            ai_response, fig = chatbot_prompt(st.session_state["messages"])
            st.plotly_chart(fig, use_container_width=True)
        
        # Append AI response to history
        st.session_state["messages"].append({"role": "assistant", "content": ai_response['text']})
        
        # Display the entire conversation as a list in reverse order (latest on top)
        for message in reversed(st.session_state["messages"]):
            with st.chat_message(message["role"]):
                st.write(message['content'])

# Visualization Tab
with tab2:
    st.header("Simulate Your Career Growth")

    # Sidebar User Input
    st.sidebar.header("Career Growth Simulation Parameters")
    current_role = st.sidebar.text_input("Enter your current role ", "")
    target_role = st.sidebar.text_input("Enter your target role", "")
    years = st.sidebar.number_input("How many years ahead would you like to simulate?", min_value=1, max_value=10, value=3)

    # File Upload Inputs for PDF and CSV
    uploaded_pdf = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
    uploaded_csv = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

    pdf_text = None
    if uploaded_pdf:
        # Handle PDF file upload
        with st.spinner("Reading PDF..."):
            pdf_reader = PdfReader(uploaded_pdf)
            pdf_text = "".join([page.extract_text() for page in pdf_reader.pages])
            st.text_area("PDF Content", pdf_text, height=300)

    if uploaded_csv:
        # Handle CSV file upload
        with st.spinner("Reading CSV..."):
            df = pd.read_csv(uploaded_csv)
            st.write("CSV Data Preview", df.head())

    # Generate and display the simulation graphs
    # fig = generate_graph(current_role, target_role, years) if pdf_text else go.Figure()
    # st.plotly_chart(fig)

    # Button to analyze career growth using GPT
    if st.button("Ask AI"):
        prompt = f"""
        This is a simulation of career growth comparing {current_role} and {target_role} over {years} years:
        - Salary, skill growth, job market demand, and opportunities. {pdf_text}
        """
        
        with st.spinner("Analyzing career growth..."):
            analysis =simulation_prompt(prompt)
        
        # st.write("GPT Analysis:", analysis)

        if analysis:
            st.subheader("Year-wise Career Growth Projection")
            analysis_dict = analysis.content  # Extract JSON content

            # Remove markdown code block format if present
            if analysis_dict.startswith("```json"):
                analysis_dict = analysis_dict[7:-3]  # Strip code block markers
            
            import json
            analysis_data = json.loads(analysis_dict)  # Convert to Python dictionary
            
            for idx,(year, details) in enumerate( analysis_data.items()):
                with st.expander(f"📅 {year}", expanded=(idx == 0)):
                    st.write(details)
