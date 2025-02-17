from pydantic import BaseModel


class RecipeNode(BaseModel):
    id: int
    instr: str


class RecipeAdjListGraph(BaseModel):
    nodes: list[RecipeNode] = []
    adjacency_list: dict[int, list[int]] = {}

    def get_node_by_id(self, node_id: int):
        for u in self.nodes:
            if u.id == node_id:
                return u

    def add_node(self, node: RecipeNode):
        self.nodes.append(node)
        self.adjacency_list[node.id] = []

    def add_edge(self, source_node_id: int, dest_node_id: int):
        if (
            source_node_id in self.adjacency_list.keys()
            and dest_node_id in self.adjacency_list.keys()
        ):
            self.adjacency_list[source_node_id].append(dest_node_id)
        else:
            if source_node_id not in self.adjacency_list.keys():
                raise ValueError(
                    f"Error: source node {source_node_id} not present in graph."
                )

            if dest_node_id not in self.adjacency_list.keys():
                raise ValueError(
                    f"Error: dest node {dest_node_id} not present in graph."
                )


class Edge(BaseModel):
    source_node_id: int
    dest_node_id: int


class RecipeEdgeListGraph(BaseModel):
    nodes: list[RecipeNode]
    edge_list: list[Edge]

    def to_recipe_adj_list_graph(self) -> RecipeAdjListGraph:
        graph = RecipeAdjListGraph()

        for node in self.nodes:
            graph.add_node(node)

        for edge in self.edge_list:
            graph.add_edge(
                source_node_id=edge.source_node_id, dest_node_id=edge.dest_node_id
            )
        return graph
