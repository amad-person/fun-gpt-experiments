from extract_recipe_graph import get_recipe_graph, get_recipe_text_from_nlg_hf
from recipe_scheduler import create_recipe_schedule


def main():
    n_chefs = 2

    recipe_title, recipe_text = get_recipe_text_from_nlg_hf(recipe_idx=0)
    print(f"Getting recipe schedule for {n_chefs} chefs: {recipe_title}")
    print(f"Original recipe text: {recipe_text}")

    recipe_graph = get_recipe_graph(recipe_text=recipe_text)
    recipe_schedule = create_recipe_schedule(recipe_graph, max_width=n_chefs)
    recipe_schedule.print_report()


if __name__ == "__main__":
    main()
