import streamlit as st
from utils import query_gpt, generate_graph,generate_career_simulation_data,generate_simulation_graphs

# Title of the app
st.title("AI Application")

# Tabs for Chatbot and Visualizations
tab1, tab2 = st.tabs(["Chatbot", "Visualizations"])

# Chatbot Tab
with tab1:
    st.header("Chat with AI")
    
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
            ai_response = query_gpt(st.session_state["messages"])
        
        # Append AI response to history
        st.session_state["messages"].append({"role": "assistant", "content": ai_response.content})
        
        # Display the entire conversation as a list in reverse order (latest on top)
        for message in reversed(st.session_state["messages"]):
            with st.chat_message(message["role"]):
                st.write(message["content"])

# Visualization Tab
with tab2:
    st.header("Simulate Your Career Growth")

    # Sidebar User Input
    st.sidebar.header("Career Growth Simulation Parameters")
    current_role = st.sidebar.text_input("Enter your current role (e.g., Software Developer):", "Software Developer")
    target_role = st.sidebar.text_input("Enter your target role (e.g., Data Scientist):", "Data Scientist")
    years = st.sidebar.number_input("How many years ahead would you like to simulate?", min_value=1, max_value=10, value=5)

    # Generate and display the simulation graphs
    fig = generate_simulation_graphs(current_role, target_role, years)
    st.pyplot(fig)

    # Send the graph details to GPT for analysis
    if st.sidebar.button("Analyze Career Growth"):
        graph_info = f"""
        This is a simulation of career growth comparing {current_role} and {target_role} over {years} years:
        - Salary, skill growth, job market demand, and opportunities have been plotted for both roles.
        """
        
        # Show loading spinner while GPT is processing
        with st.spinner("Analyzing career growth..."):
            analysis = query_gpt([{"role": "system", "content": "Analyze the career growth simulation."},
                                  {"role": "user", "content": graph_info}])
        
        st.write("GPT Analysis:", analysis)
