# Recipe DAGger

Inputs: 
- Link to any recipe page
- Number of chefs 

Outputs: 
- Sequence of recipe steps for each chef that can be run in parallel   

Method:
- [ ] Use an LLM to convert the recipe text to a DAG
- [x] Use Coffman–Graham algorithm on the DAG for task scheduling