from openai import OpenAI
import os
from dotenv import load_dotenv
from personal_info_hidder import secure_data
import matplotlib.pyplot as plt
import numpy as np
import time
import json
import pandas as pd
from PyPDF2 import PdfReader

load_dotenv()

from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma

import chromadb
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_chroma import Chroma

# Retrieve the API key
api_key = os.getenv("OPENAI_API_KEY_STEVENS")

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)

def chatbot_prompt(prompt):
    secured_content = secure_data(prompt[-1]['content'])
    rag_data = rag_layer(prompt[-1]['content'])
    prompt[-1]['content'] = secured_content
    gpt_resp = query_gpt(prompt,rag_data)
    json_content = gpt_resp.content.strip("```json").strip("```")
    parsed_json = json.loads(json_content)
    print("JSON ",parsed_json['graph'])
    fig = make_graph(parsed_json['graph'])
    return parsed_json,fig

def simulation_prompt(prompt):
    print(prompt)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpfull assistant, specialised in career growth you will give simulations based on career options"},
            {
                "role": "user", # "content": prompt[-1]["content"]
                "content":f''' {prompt}
give output based on years, it should be in the json format, with each year as key and its text as value, give only json it is an utomated system and your output is directly used as input for other function
        '''
            }
        ]
    )
    
    print(completion.choices[0].message)
    return completion.choices[0].message
    

# def make_graph(fig_data):
#     fig, ax = plt.subplots(figsize=(8, 5))
#     print("RDD ",fig_data,type(fig_data))
#     ax.barh(range(len(fig_data["data"])), fig_data["data"], color=fig_data["style"]["line_color"])
    
#     ax.set_xlabel(fig_data["x_label"])
#     ax.set_ylabel(fig_data["y_label"])
#     ax.set_title(fig_data["title"])
    

import plotly.express as px

def make_graph(fig_data):
    print("RDD ", fig_data, type(fig_data))

    values = fig_data["data"]
    graph_type = fig_data["type"].lower()

    # Check if the data is a dictionary with 'x' and 'y' keys
    if isinstance(values, dict) and 'x' in values and 'y' in values:
        x_labels = values["x"]
        y_values = values["y"]
    else:
        x_labels = list(range(len(values)))
        y_values = values
    
    fig = None
    
    if graph_type == "line":
        fig = px.line(x=x_labels, y=y_values, markers=True, 
                      line_shape='linear', color_discrete_sequence=[fig_data["style"]["line_color"]])
    elif graph_type == "box":
        fig = px.box(y=y_values, color_discrete_sequence=[fig_data["style"]["line_color"]])

    elif graph_type == "pie":
        fig = px.pie(values=y_values, names=[f"Label {i}" for i in range(len(y_values))],
                     color_discrete_sequence=[fig_data["style"]["line_color"]])
    elif graph_type == "scatter":
        fig = px.scatter(x=x_labels, y=y_values, color_discrete_sequence=[fig_data["style"]["line_color"]])
        fig = px.line(x=x_labels, y=y_values, markers=True, 
                      line_shape='linear', color_discrete_sequence=[fig_data["style"]["line_color"]])
    else:
        fig = px.bar(y=x_labels, x=y_values, orientation='h', color_discrete_sequence=[fig_data["style"]["line_color"]])

    if fig is not None:
        fig.update_layout(
            title=fig_data["title"],
            xaxis_title=fig_data["x_label"],
            yaxis_title=fig_data["y_label"],
            template="plotly_white",
        )
    
    if fig_data["grid"]:
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
    
    return fig

def query_gpt(prompt,rag_data, resume_data=None):
    print(prompt)
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpfull assistant, specialised in career growth and as the ability to think careful and plot graphs which makes impact. Your aim is to help the user by providing the correct and senseble further guidence depending on the user's query and provide proper visualiztion according to the query."},
            {
                "role": "user", # "content": prompt[-1]["content"]
                "content":f''' IMPORTANT: You MUST return output in a valid JSON fomrated object

        And depending on the user's input, return a json formated object, having 3 items as follows:

        {{
            text: "",
            figure: "",
            graph : "{{
            "type": plot_types = [
            "scatter",    # Scatter Plot
            "barh",       # Horizontal Bar Plot
            "hist",       # Histogram
            "pie",        # Pie Chart
            "boxplot",    # Box Plot
            "heatmap",    # Heatmap
            "violin",     # Violin Plot
            "errorbar",   # Error Bar Plot
            "stacked_bar",# Stacked Bar Plot
        ], # it should be any one of these types
            "title": "My Graph Title",
            "x_label": "X Axis Label",
            "y_label": "Y Axis Label",
            "data": [
            IMPORTANT: Identify the x and y axis from the prompt and the asnwer which will be provided by the LLM, and depending on the data try to be creative when visualiztion by ploting complex graphs (not simple ones like bar), and if there are missing data then try to impute it.
                If it is single value then just give list if it is 2 values give x and y as keys for json
                like this x:[1,2,3,4], y:[1,2,3,4] if both x and y are not of same size then generate relevent dummy data, it is mandatory and it canot be empty.
            ],
            "style": {{
                "line_style": "-",
                "line_color": "orange",
                "marker": "o",
                size="10",
            }},
            "legend": True,
            "grid": True
        }}"
        }}


        the value of the 'text' key will be the formated answer in english responding to the user.
        based on the inference done by the LLM and also based on the following data:
        graph should be alid to make a graph in matplotlib, this data will be fed directly to the system to generate graphs
        {rag_data}


        Following is the user's query:
        {prompt[-1]["content"]}

        And the resume data of the user looks like the following:
        {resume_data}
        '''
            }
        ]
    )
    
    print(completion.choices[0].message)
    return completion.choices[0].message


def generate_graph():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y, label="Sine Wave")
    ax.set_title("Sample Graph")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.legend()

    return fig



def generate_career_simulation_data(current_role, target_role, years):
    # Mock Data: Normally, you would fetch data or use an algorithm to generate these
    years_range = np.arange(0, years + 1)
    
    # Mock projections for the current role (software developer) and target role (data scientist)
    salary_current = 60000 * (1.05) ** years_range  # 5% yearly salary growth
    salary_target = 70000 * (1.07) ** years_range  # 7% yearly salary growth
    
    skills_current = np.minimum(100, 80 + 2 * years_range)  # Increasing skill levels
    skills_target = np.minimum(100, 70 + 3 * years_range)  # Faster skill growth
    
    job_market_current = np.minimum(100, 75 + 1.5 * years_range)  # Slower growth in job market
    job_market_target = np.minimum(100, 60 + 2.5 * years_range)  # Faster growth in job market
    
    opportunities_current = np.minimum(100, 50 + 2 * years_range)  # Growing opportunities
    opportunities_target = np.minimum(100, 40 + 3 * years_range)  # Faster growth in opportunities
    
    return years_range, salary_current, salary_target, skills_current, skills_target, job_market_current, job_market_target, opportunities_current, opportunities_target

# Function to generate the simulation graphs
# def generate_simulation_graphs(out):
    # years_range, salary_current, salary_target, skills_current, skills_target, job_market_current, job_market_target, opportunities_current, opportunities_target = generate_career_simulation_data(current_role, target_role, years)
    
    # fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    
    # # Salary Comparison Graph
    # axs[0, 0].plot(years_range, salary_current, label=f"{current_role} Salary", color='blue')
    # axs[0, 0].plot(years_range, salary_target, label=f"{target_role} Salary", color='green')
    # axs[0, 0].set_title("Salary Comparison Over Time")
    # axs[0, 0].set_xlabel("Years")
    # axs[0, 0].set_ylabel("Salary ($)")
    # axs[0, 0].legend()
    
    # # Skill Growth Comparison Graph
    # axs[0, 1].plot(years_range, skills_current, label=f"{current_role} Skills", color='blue')
    # axs[0, 1].plot(years_range, skills_target, label=f"{target_role} Skills", color='green')
    # axs[0, 1].set_title("Skill Growth Comparison Over Time")
    # axs[0, 1].set_xlabel("Years")
    # axs[0, 1].set_ylabel("Skill Level (0-100)")
    # axs[0, 1].legend()
    
    # # Job Market Growth Comparison Graph
    # axs[1, 0].plot(years_range, job_market_current, label=f"{current_role} Job Market", color='blue')
    # axs[1, 0].plot(years_range, job_market_target, label=f"{target_role} Job Market", color='green')
    # axs[1, 0].set_title("Job Market Growth Comparison Over Time")
    # axs[1, 0].set_xlabel("Years")
    # axs[1, 0].set_ylabel("Job Market Demand (0-100)")
    # axs[1, 0].legend()
    
    # # Opportunities Comparison Graph
    # axs[1, 1].plot(years_range, opportunities_current, label=f"{current_role} Opportunities", color='blue')
    # axs[1, 1].plot(years_range, opportunities_target, label=f"{target_role} Opportunities", color='green')
    # axs[1, 1].set_title("Opportunities Comparison Over Time")
    # axs[1, 1].set_xlabel("Years")
    # axs[1, 1].set_ylabel("Opportunities (0-100)")
    # axs[1, 1].legend()

    # plt.tight_layout()
    # return fig

    # return out['figure']



def load_csv(csv_file):
    return pd.read_csv(csv_file)


def rag_layer(query):
    df = load_csv("small_employee_dataset.csv")


    # Initialize ChromaDB (Runs in-memory, no API needed)
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    # Use a local embedding model (e.g., all-MiniLM-L6-v2)
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = Chroma(collection_name="user_data", client=chroma_client, embedding_function=embedding_model)

    # Insert data into ChromaDB
    for _, row in df.iterrows():
        vector_store.add_texts(texts=[str(row)], metadatas=[row.to_dict()])

    # Query function
    def query_rag(user_query):
        docs = vector_store.similarity_search(user_query, k=3)
        retrieved_data = [doc.page_content for doc in docs]
        print("Retrieved Data:", retrieved_data)
        return retrieved_data

    # Example query
    # query = "Only giver me details of Rahul"
    retrieved_docs = query_rag(query)
    print("Retrieved Documents:", retrieved_docs)
    return ','.join(retrieved_docs)


