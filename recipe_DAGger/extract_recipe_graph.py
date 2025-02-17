import os

import datasets
from dotenv import load_dotenv
from openai import OpenAI

from recipe_graph import RecipeEdgeListGraph

load_dotenv("../.env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

recipe_nlg_dataset = datasets.load_dataset(
    "mbien/recipe_nlg",
    data_dir="/Users/aadyaamaddi/Desktop/Aadyaa/fun-gpt-experiments/recipe_DAGger/recipe_nlg_hf_data",
)


def get_recipe_text_from_nlg_hf(recipe_idx: int = 0):
    # Fetch recipe object from dataset
    recipe_obj = recipe_nlg_dataset["train"][recipe_idx]

    # Add ingredients as instructions
    recipe_text_array = []
    for ingredient in recipe_obj["ingredients"]:
        recipe_text_array.append(
            f"Get {ingredient.replace('.', '')}."
        )  # To avoid being considered as separate sentences

    # Add instructions
    for instr in recipe_obj["directions"]:
        recipe_text_array.append(instr)

    # Return title and text representation of recipe
    return recipe_obj["title"], " ".join(recipe_text_array)


def get_recipe_graph(recipe_text: str):
    # Construct prompt from recipe_text
    prompt = (
        "You are helping create a directed acyclic graph (DAG) representation of a recipe from recipe text.\n"
        "The recipe DAG is made of RecipeNodes, where each node has an integer `id` and a string `instr` containing the node's recipe instruction.\n\n"
        "Follow these instructions closely to create the recipe DAG:\n"
        "1. Split the recipe text into individual sentences. Each sentence is an instruction.\n"
        "2. Each instruction becomes an individual node in the recipe DAG.\n"
        "3. Set the node `id` to be the 0-based indexing position of the instruction in the list, and set `instr` to be the instruction text.\n"
        "4. For each instruction I, extract the set of objects O that the instruction takes as input.\n"
        "5. Connect I and any previous instruction P whose output objects are in O, by adding an edge with P as source node and I as dest node. If there are no such previous instructions, do not add any edges.\n"
        "6. Repeat the process until no more instructions are left.\n\n"
        f"Recipe text: {recipe_text}\n"
    )

    # Call using beta API for structured outputs
    completion = client.beta.chat.completions.parse(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format=RecipeEdgeListGraph,
        model="gpt-4o",
    )

    # Extract the response content
    recipe_edge_list: RecipeEdgeListGraph = completion.choices[0].message.parsed

    # Convert to graph with adjacency list
    recipe_graph = recipe_edge_list.to_recipe_adj_list_graph()

    return recipe_graph
