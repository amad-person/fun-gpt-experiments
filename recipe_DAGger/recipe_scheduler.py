import pandas as pd
from pydantic import BaseModel
from datetime import datetime
from recipe_graph import RecipeAdjListGraph


class RecipeSchedule(BaseModel):
    recipe_graph: RecipeAdjListGraph
    max_width: int
    levels: dict[int, list[int]] = {}

    def gantt_df(self):
        time_intervals = pd.interval_range(
            start=datetime.now(), periods=len(self.levels.keys()), freq="15min"
        )

        tasks = []
        for i, level in enumerate(reversed(self.levels.keys())):
            time_interval = time_intervals[i]
            for j, u_id in enumerate(self.levels[level]):
                tasks.append(
                    {
                        "Start Time": time_interval.left,
                        "End Time": time_interval.right,
                        "Chef": f"Chef {j + 1}",
                        "Step": f"Step {u_id + 1}",
                        "Task Description": self.recipe_graph.get_node_by_id(
                            u_id
                        ).instr,
                    }
                )

        return pd.DataFrame(tasks)

    def report(self):
        report = {}
        for time_step, level in enumerate(reversed(self.levels.keys())):
            tasks = []
            for chef_id, u_id in enumerate(self.levels[level]):
                tasks.append(
                    f"\tChef {chef_id}: {self.recipe_graph.get_node_by_id(u_id).instr}"
                )
            report[time_step] = tasks
        return report

    def print_report(self):
        report = self.report()
        for time_step in sorted(report.keys()):
            print(f"Tasks for time step {time_step}:")
            print("\n".join(report[time_step]))


def get_transitive_reduction(graph: RecipeAdjListGraph) -> RecipeAdjListGraph:
    reduced_graph = graph.model_copy(deep=True)

    node_ids = reduced_graph.adjacency_list.keys()
    # check if u -> v is redundant, remove it if true
    for u_id in node_ids:
        u_neighbours = reduced_graph.adjacency_list[u_id]
        for v_id in u_neighbours:
            for m_id in u_neighbours:
                # u -> v is redundant if u -> m -> v exists
                m_neighbours = reduced_graph.adjacency_list[m_id]
                if m_id != v_id and m_id in node_ids and v_id in m_neighbours:
                    u_neighbours.remove(v_id)
                    break

    return reduced_graph


def get_topological_order(graph: RecipeAdjListGraph) -> list[int]:
    # calculate in-degree for each node in graph
    node_id_to_in_degree_map = {node_id: 0 for node_id in graph.adjacency_list.keys()}
    for u in graph.nodes:
        u_neighbours = graph.adjacency_list[u.id]
        for v_id in u_neighbours:
            node_id_to_in_degree_map[v_id] += 1

    # initialize set of nodes with in-degree = 0
    zero_in_degree = []
    for node_id, in_degree in node_id_to_in_degree_map.items():
        if in_degree == 0:
            zero_in_degree.append(node_id)

    # create topological order using Kahn's algorithm
    topological_order = []
    while zero_in_degree:
        u_id = zero_in_degree.pop(0)
        topological_order.append(u_id)

        # update node in-degrees for neighbours
        u_neighbours = graph.adjacency_list[u_id]
        for v_id in u_neighbours:
            node_id_to_in_degree_map[v_id] -= 1

            # add neighbour to zero_in_degree if needed
            if node_id_to_in_degree_map[v_id] == 0:
                zero_in_degree.append(v_id)

    return topological_order


def create_recipe_schedule(graph: RecipeAdjListGraph, max_width: int) -> RecipeSchedule:
    schedule = RecipeSchedule(recipe_graph=graph, max_width=max_width)  # store result

    # run first two steps in Coffman–Graham algorithm
    reduced_graph = get_transitive_reduction(graph)
    topological_order = get_topological_order(reduced_graph)

    # initialize all levels to -1
    node_to_level_map = {}
    for u in reduced_graph.nodes:
        node_to_level_map[u.id] = -1

    # perform the last step in Coffman–Graham algorithm
    for u_id in reversed(topological_order):
        # get maximum level among all of u's neighbours
        max_neighbour_level = -1
        for v_id in reduced_graph.adjacency_list[u_id]:
            max_neighbour_level = max(
                max_neighbour_level, node_to_level_map.get(v_id, -1)
            )

        # find level for u starting from maximum_neighbour_level
        assigned_level = -1
        level = max_neighbour_level + 1
        while assigned_level == -1:
            if level not in schedule.levels:
                schedule.levels[level] = []

            # assign u to level only if there is space for it
            if len(schedule.levels[level]) < max_width:
                assigned_level = level
            else:
                level += 1

        # update schedule with u's assigned level
        node_to_level_map[u_id] = assigned_level
        schedule.levels[assigned_level].append(u_id)

    return schedule
