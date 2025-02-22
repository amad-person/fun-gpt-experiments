import re
import string
from dotenv import load_dotenv
import streamlit as st
from extract_recipe_graph import get_recipe_graph, get_recipe_text_from_nlg_hf
from recipe_scheduler import create_recipe_schedule
import plotly.express as px

# PAGE CONFIG
st.set_page_config(page_title="Recipe DAGger", layout="wide")

# SIDEBAR
st.sidebar.title("Menu")

env_path = st.sidebar.text_input("Enter path to .env file:", value=".env")
load_dotenv(env_path)


def prettify_recipe_title(s: str):
    s = string.capwords(s)
    s = re.sub(pattern=r"(\S)\(", repl=r"\1 (", string=s)
    s = re.sub(
        pattern=r"([(\[{])([a-z])",
        repl=lambda match: match.group(1) + match.group(2).upper(),
        string=s,
    )
    return s


default_recipe_titles, default_recipe_title_to_text_map = [], {}
for recipe_id in range(15):
    recipe_title, recipe_text = get_recipe_text_from_nlg_hf(recipe_id)

    # make recipe titles pretty
    recipe_title = prettify_recipe_title(recipe_title)
    default_recipe_titles.append(recipe_title)
    default_recipe_title_to_text_map[recipe_title] = recipe_text

selected_recipe_title = st.sidebar.radio(
    label="Choose a default recipe from the Recipe NLG dataset:",
    options=default_recipe_titles,
    index=None,
)

# MAIN
st.title("Recipe DAGger")

recipe_text = st.text_area(
    label="Enter recipe text (or choose one of the default recipes):",
    value=default_recipe_title_to_text_map.get(selected_recipe_title, None),
    height=200,
)

n_chefs = st.number_input(label="Enter number of chefs:", min_value=2)

is_invalid_input = True
if recipe_text and n_chefs:
    is_invalid_input = False

if st.button("Get recipe schedule!", disabled=is_invalid_input):
    with st.spinner("Running Recipe DAGger...", show_time=True):
        recipe_graph = get_recipe_graph(recipe_text=recipe_text)
        recipe_schedule = create_recipe_schedule(recipe_graph, max_width=n_chefs)

    col1, col2 = st.columns([4, 2])

    # COLUMN 1
    gantt_df = recipe_schedule.gantt_df()
    plotly_fig = px.timeline(
        gantt_df,
        x_start="Start Time",
        x_end="End Time",
        y="Chef",
        color="Chef",
        text="Step",
        hover_data=["Task Description", "Start Time", "End Time"],
    )
    plotly_fig.update_traces(marker_line_color="black", marker_line_width=1, opacity=1)
    # plotly_fig.update_yaxes(
    #     type='category',
    #     tickvals=list(range(n_chefs)),
    #     ticktext=[f"Chef {i + 1}" for i in range(n_chefs)]
    # )
    col1.plotly_chart(plotly_fig)

    # COLUMN 2
    steps_text = []
    for node in sorted(recipe_graph.nodes, key=lambda x: x.id):
        steps_text.append(f"Step {node.id + 1}: {node.instr}")
    col2.write("  \n".join(steps_text))
