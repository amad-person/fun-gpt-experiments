from pydantic import BaseModel


class RecipeNode(BaseModel):
    id: int
    instr: str


class RecipeGraph(BaseModel):
    nodes: list[RecipeNode] = []
    adjacency_list: dict[int, list[int]] = {}

    def get_node_by_id(self, id):
        for u in self.nodes:
            if u.id == id:
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
            raise ValueError(
                f"Error: either source node {source_node_id} or dest node {dest_node_id} not present in graph."
            )
