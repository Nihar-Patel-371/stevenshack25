from openai import OpenAI
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
import time


load_dotenv()

# Retrieve the API key
api_key = os.getenv("OPENAI_API_KEY_STEVENS")

# Initialize OpenAI client with API key
client = OpenAI(api_key=api_key)


def query_gpt(prompt):
    print(prompt)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a assistant"},
            {
                "role": "user",
                # "content": prompt[-1]["content"]
                "content":f'''

You are a helpfull assistant, specialised in finanical consulting and furture growth. Your aim to help the user by providing the correct and senseble futher guidence depending on the user's query.

And depending on the user's input, return a json formated object, having 2 items as follows:
{{
	text: "",
	figure: "",
    graph : "graph_data = {{
    "type": "line",
    "title": "My Graph Title",
    "x_label": "X Axis Label",
    "y_label": "Y Axis Label",
    "data": [
       data for graph
    ],
    "style": {{
        "line_style": "-",
        "line_color": "blue",
        "marker": "o"
    }},
    "legend": True,
    "grid": True
}}"
}}
the value of the 'text' key will be the formated answer in english responding to the user.
and the value of the 'figure' key will be to show relevent matplotlib figure code as string, based on the inference done by the LLM and also based on the following data:
'Nihar - 150000 - 2025', 'Rahul - 100000 - 2026', 'Vaibhav - 500000 - 2023', 'Krutin - 120000 - 2022', 'Rohan - 80000 - 2015', 'Dev - 450000 - 2014'

Following is the user's query:
{prompt[-1]["content"]}
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
def generate_simulation_graphs(current_role, target_role, years, out):
    years_range, salary_current, salary_target, skills_current, skills_target, job_market_current, job_market_target, opportunities_current, opportunities_target = generate_career_simulation_data(current_role, target_role, years)
    
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

    return out['figure']