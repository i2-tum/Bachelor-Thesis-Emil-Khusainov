import math
from networkx import maximal_independent_set, Graph


def compatible_2D(a: list[int], b: list[int]) -> bool:
    """
    Checks if two 2D points are compatible based on specified rules.

    Parameters:
    a (list[int]): A list of four integers representing the first point. The elements are ordered as [x_loc_before, y_loc_before, x_loc_after, y_loc_after].
    b (list[int]): A list of four integers representing the second point. The elements are ordered as [x_loc_before, y_loc_before, x_loc_after, y_loc_after].

    Returns:
    bool: True if the points are compatible, False otherwise.
    """
    assert len(a) == 4 and len(b) == 4, "Both arguments must be lists with exactly four elements."

    # Check compatibility for the first two elements of each point
    if a[0] == b[0] and a[2] != b[2]:
        return False
    if a[2] == b[2] and a[0] != b[0]:
        return False
    if a[0] < b[0] and a[2] >= b[2]:
        return False
    if a[0] > b[0] and a[2] <= b[2]:
        return False

    # Check compatibility for the last two elements of each point
    if a[1] == b[1] and a[3] != b[3]:
        return False
    if a[3] == b[3] and a[1] != b[1]:
        return False
    if a[1] < b[1] and a[3] >= b[3]:
        return False
    if a[1] > b[1] and a[3] <= b[3]:
        return False

    return True

def maximalis_solve_sort(n: int, edges: list[tuple[int]], nodes: set[int]) -> list[int]:
    """
    Finds a maximal independent set from the given graph nodes using a sorted approach.

    Parameters:
    n (int): Number of nodes in the graph. The nodes were expressed by integers from 0 to n-1.
    edges (list[tuple[int]]): list of edges in the graph, where each edge is a tuple of two nodes.
    nodes (set[int]): Set of nodes to consider for the maximal independent set.

    Returns:
    list[int]: list of nodes in the maximal independent set.
    """
    # Initialize conflict status for each node
    is_node_conflict = [False for _ in range(n)]
    
    # Create a dictionary to store neighbors of each node
    node_neighbors = {i: [] for i in range(n)}
    
    # Populate the neighbors dictionary
    for edge in edges:
        node_neighbors[edge[0]].append(edge[1])
        node_neighbors[edge[1]].append(edge[0])
    
    result = []
    for i in nodes:
        if is_node_conflict[i]:
            continue
        else:
            result.append(i)
            for j in node_neighbors[i]:
                is_node_conflict[j] = True
    return result

def maximalis_solve(nodes:list[int], edges:list[tuple[int]])-> list[int]:
    """
    Wrapper function to find a maximal independent set using the Graph class.

    Parameters:
    n (int): Number of nodes in the graph. The nodes were expressed by integers from 0 to n-1.
    edges (list[tuple[int]]): list of edges in the graph.

    Returns:
    list[int]: list of nodes in the maximal independent set.
    """
    G = Graph()
    for i in nodes:
        G.add_node(i)
    for edge in edges:
        G.add_edge(edge[0], edge[1])
    
    # Use a library function to find the maximal independent set
    result = maximal_independent_set(G, seed=0) 
    return result

def get_movements(current_map: list, next_map: list, window_size=None) -> map:
    """
    Determines the movements of qubits between two maps.

    Parameters:
    current_map (list): list of current positions of qubits.
    next_map (list): list of next positions of qubits.
    window_size (optional): Size of the window for movement calculations.

    Returns:
    map: A dictionary with qubit movements.
    """
    movements = {}
    # Determine movements of qubits
    for qubit, current_position in enumerate(current_map):
        next_position = next_map[qubit]
        if current_position != next_position:
            move_details = current_position + next_position
            movements[qubit] = move_details
    return movements

class QuantumRouter:
    def __init__(self, num_qubits: int, embeddings: list[list[list[int]]], gate_list: list[list[int]], arch_size: list[int], routing_strategy: str = "maximalis") -> None:
        """
        Initialize the QuantumRouter object with the given parameters.
        
        Parameters:
        num_qubits (int): Number of qubits.
        embeddings (list[list[list[int]]]): Embeddings for the qubits.
        gate_list (list[list[int]]): list of two-qubit gates.
        arch_size (list[int]): Architecture size as [x, y].
        routing_strategy (str): Strategy used for routing.
        """
        self.num_qubits = num_qubits
        self.validate_embeddings(embeddings)
        self.embeddings = embeddings
        
        assert len(embeddings) == len(gate_list), "The number of embeddings should match the number of two-qubit gates in gate_list."
        self.gate_list = gate_list
        
        self.validate_architecture_size(arch_size)
        self.arch_size = arch_size
        self.routing_strategy = routing_strategy
        self.movement_list = []

    def validate_embeddings(self, embeddings: list[list[list[int]]]) -> None:
        """
        Validate the embeddings to ensure they contain locations for all qubits.
        
        Parameters:
        embeddings (list[list[list[int]]]): Embeddings for the qubits.
        """
        for embedding in embeddings:
            assert len(embedding) == self.num_qubits, f"Each embedding must contain locations for all {self.num_qubits} qubits."
            for loc in embedding:
                assert len(loc) == 2, "Each location must be a list containing exactly two coordinates: [x, y]."

    def validate_architecture_size(self, arch_size: list[int]) -> None:
        """
        Validate the architecture size to ensure it can accommodate all qubits.
        
        Parameters:
        arch_size (list[int]): Architecture size as [x, y].
        """
        assert len(arch_size) == 2, "Architecture size should be specified as a list with two elements: [x, y]."
        assert arch_size[0] * arch_size[1] >= self.num_qubits, (
            f"The product of the architecture dimensions x and y must be at least {self.num_qubits} to accommodate all qubits; "
            f"currently, it is {arch_size[0] * arch_size[1]}."
        )

    def process_all_embeddings(self) -> None:
        """
        Process all embeddings to resolve movements and update the program.
        """
        for current_pos in range(len(self.embeddings) - 1):
            movements = self.resolve_movements(current_pos)
            assert len(movements) > 0, "there should be some movements between embeddings"
            self.movement_list.append(movements)

    def solve_violations(self, movements, violations, sorted_keys):
        """
        Resolves violations in qubit movements based on the routing strategy.

        Parameters:
        movements (dict): Dictionary of qubit movements.
        violations (list): list of violations to be resolved.
        sorted_keys (list): list of qubit keys sorted based on priority.

        Returns:
        tuple: remaining movements, unresolved violations and movement sequence to finish movement this time
        """
        if self.routing_strategy == "maximalis":
            resolution_order = maximalis_solve(sorted_keys, violations)
        else:
            resolution_order = maximalis_solve_sort(self.num_q, violations, sorted_keys)
        # print(f'Resolution Order: {resolution_order}')
        move_sequence =[]
        for qubit in resolution_order:
            sorted_keys.remove(qubit)

            move = movements[qubit]
            # print(self.momvents)
            move_sequence.append([qubit,(move[0],move[1]),(move[2],move[3])])
            # print(f'Move qubit {qubit} from ({move[0]}, {move[1]}) to ({move[2]}, {move[3]})')
            # Remove resolved violations
            violations = [v for v in violations if qubit not in v]
            del movements[qubit]
        
        return movements, violations, move_sequence

    def resolve_movements(self, current_pos: int) -> list[int, tuple[int, int], tuple[int, int]]:
        """
        Resolve movements between the current and next embeddings.
        
        Parameters:
        current_pos (int): The current position in the embeddings list.
        
        Returns:
        str: The program for the resolved movements.
        """
        next_pos = current_pos + 1
        movements = get_movements(self.embeddings[current_pos], self.embeddings[next_pos])
        sorted_movements = sorted(movements.keys(), key=lambda k: math.dist(movements[k][:2], movements[k][2:]))
        violations = self.check_violations(sorted_movements, movements)
        move_sequences = self.handle_violations(violations, movements, sorted_movements, current_pos)
        return move_sequences

    def handle_violations(self, violations: list[tuple[int, int]], remained_mov_map: dict[int, tuple[int, int, int, int]], sorted_movements: list[int], current_pos: int) -> list[int, tuple[int, int], tuple[int, int]]:
        """
        Handle violations and return the movement sequence accordingly.
        
        Parameters:
        violations (list[tuple[int, int]]): list of violations.
        movements (dict[int, tuple[int, int, int, int]]): Movements between embeddings.
        sorted_movements (list[int]): Sorted list of movements.
        current_pos (int): The current position in the embeddings list.
        
        Returns:
        list[int, tuple[int, int], tuple[int, int]]: movement sequences.
        """
        movement_sequence =[]
        while remained_mov_map:
            remained_mov_map, violations, movement = self.solve_violations(remained_mov_map, violations, sorted_movements)
            movement_sequence.append(movement)

        return movement_sequence

    def check_violations(self, sorted_movements: list[int], remained_mov_map: dict[int, tuple[int, int, int, int]]) -> list[tuple[int, int]]:
        """
        Check for violations between movements.
        
        Parameters:
        sorted_movements (list[int]): Sorted list of movements.
        movements (dict[int, tuple[int, int, int, int]]): Movements between embeddings.
        
        Returns:
        list[tuple[int, int]]: list of violations.
        """
        violations = []
        for i in range(len(sorted_movements)):
            for j in range(i + 1, len(sorted_movements)):
                if not compatible_2D(remained_mov_map[sorted_movements[i]], remained_mov_map[sorted_movements[j]]):
                    violations.append((sorted_movements[i], sorted_movements[j]))
        return violations

    def run(self) -> None:
        """
        Run the QuantumRouter to initialize, process embeddings.
        """
        self.movement_list = []
        self.process_all_embeddings()