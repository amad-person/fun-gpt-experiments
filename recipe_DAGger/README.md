# Recipe DAGger

Inputs: 
- Link to any recipe page
- Number of chefs 

Outputs: 
- Sequence of recipe steps for each chef that can be run in parallel   

Method:
- [ ] Parse the recipe webpage for the recipe text
- [x] Use an LLM to convert the recipe text to a DAG 
  - [x] Come up with a prompt for [recipe_nlg_hf_data](https://huggingface.co/datasets/mbien/recipe_nlg) which already has well-formatted recipe text
  - [ ] If needed, manually create a few bootstrapping samples and use DSPY
- [x] Use Coffman–Graham algorithm on the DAG for task scheduling

Current output of `main.py` (formatted for readability):

```
Getting recipe schedule for 2 chefs: No-Bake Nut Cookies
Original recipe text: 
  Get 1 c firmly packed brown sugar. 
  Get 1/2 c evaporated milk. 
  Get 1/2 tsp vanilla. 
  Get 1/2 c broken nuts (pecans). 
  Get 2 Tbsp butter or margarine.
  Get 3 1/2 c bite size shredded rice biscuits. 
  In a heavy 2-quart saucepan, mix brown sugar, nuts, evaporated milk and butter or margarine. 
  Stir over medium heat until mixture bubbles all over top. 
  Boil and stir 5 minutes more. 
  Take off heat. 
  Stir in vanilla and cereal; mix well. 
  Using 2 teaspoons, drop and shape into 30 clusters on wax paper. 
  Let stand until firm, about 30 minutes.

Tasks for time step 1:
	Chef 0: Get 1/2 c evaporated milk.
	Chef 1: Get 1 c firmly packed brown sugar.
Tasks for time step 2:
	Chef 0: Get 2 Tbsp butter or margarine.
	Chef 1: Get 1/2 c broken nuts (pecans).
Tasks for time step 3:
	Chef 0: In a heavy 2-quart saucepan, mix brown sugar, nuts, evaporated milk and butter or margarine.
Tasks for time step 4:
	Chef 0: Stir over medium heat until mixture bubbles all over top.
Tasks for time step 5:
	Chef 0: Boil and stir 5 minutes more.
	Chef 1: Get 1/2 tsp vanilla.
Tasks for time step 6:
	Chef 0: Take off heat.
	Chef 1: Get 3 1/2 c bite size shredded rice biscuits.
Tasks for time step 7:
	Chef 0: Stir in vanilla and cereal; mix well.
Tasks for time step 8:
	Chef 0: Using 2 teaspoons, drop and shape into 30 clusters on wax paper.
Tasks for time step 9:
	Chef 0: Let stand until firm, about 30 minutes.
```