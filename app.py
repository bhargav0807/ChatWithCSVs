import streamlit as st
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import os

# Streamlit app UI for uploading multiple CSV files
st.title("Chat with Your CSV Data")
st.write("Upload one or more CSV files and ask questions about the data.")

# File uploader for multiple CSV files
uploaded_files = st.file_uploader("Upload CSV files", type="csv", accept_multiple_files=True)

# Check if any CSV files have been uploaded
if uploaded_files:
    # List to store file paths (not saving to disk, just for memory)
    csv_paths = []
    
    # Load and display the uploaded CSVs
    for file in uploaded_files:
        # Save the uploaded file to a local directory (currently in use, but can be omitted)
        path = os.path.join(os.getcwd(), file.name)
        with open(path, "wb") as f:
            f.write(file.getbuffer())
        csv_paths.append(path)
        
        # Load the CSV into a DataFrame and display the first few rows
        df = pd.read_csv(file)
        st.write(f"**Sample of {file.name}:**")
        st.dataframe(df.head())  # Display the first 5 rows of the dataframe

    # Allow users to ask questions about the data
    question = st.text_input("Ask a question about your CSV data:")

    if question:
        # Create a LangChain agent to interact with the CSVs
        agent = create_csv_agent(
            ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613"),
            csv_paths,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            allow_dangerous_code=True  # Opt-in to allow code execution
        )

        # Run the question through the agent
        try:
            response = agent.run(question)
            st.write("Answer:")
            st.write(response)
        except Exception as e:
            st.write(f"Error: {e}")
