import rustworkx as rx
import networkx as nx
import numpy as np
import random
import math
import os
import re
import json

from qiskit import qasm2, transpile, QuantumCircuit, QuantumRegister
from qiskit.converters import dag_to_circuit, circuit_to_dag
from qiskit.circuit import library
import copy
from copy import deepcopy

custom = [
    qasm2.CustomInstruction("p",num_params= 1, num_qubits=1 ,constructor=library.PhaseGate, builtin=True),
]

parameters = {}

def CreateCircuitFromQASM(file, path):
    filePath = os.path.join(path,file)
    # print(filePath)
    cir = qasm2.load(filePath, custom_instructions=custom)
    gates_in_circuit = {op[0].name for op in cir.data}
    allowed_basis_gates = {'cz', 'h', 's', 't', 'rx', 'ry', 'rz'}
    # Check if there are any disallowed gates by checking the difference between sets
    if gates_in_circuit - allowed_basis_gates:
        cir = transpile(cir, basis_gates=list(allowed_basis_gates),optimization_level=0)
    return cir


def get_rx_one_mapping(graph_max, G):
    sub_graph = rx.networkx_converter(graph_max)
    big_graph = rx.networkx_converter(G)
    nx_edge_s = list(graph_max.edges())
    rx_edge_s = list(sub_graph.edge_list())
    rx_nx_s = dict()
    for i in range(len(rx_edge_s)):
        if rx_edge_s[i][0] not in rx_nx_s:
            rx_nx_s[rx_edge_s[i][0]] = nx_edge_s[i][0]
        if rx_edge_s[i][1] not in rx_nx_s:
            rx_nx_s[rx_edge_s[i][1]] = nx_edge_s[i][1]
    nx_edge_G = list(G.edges())
    rx_edge_G = list(big_graph.edge_list())
    rx_nx_G = dict()
    for i in range(len(rx_edge_G)):
        if rx_edge_G[i][0] not in rx_nx_G:
            rx_nx_G[rx_edge_G[i][0]] = nx_edge_G[i][0]
        if rx_edge_G[i][1] not in rx_nx_G:
            rx_nx_G[rx_edge_G[i][1]] = nx_edge_G[i][1]
    vf2 = rx.vf2_mapping(big_graph, sub_graph, subgraph=True, induced = False)
    item = next(vf2)
    reverse_mapping = {rx_nx_s[value]: rx_nx_G[key] for  key, value in item.items()}
    return reverse_mapping

def rx_is_subgraph_iso(G, subG):
    Grx = rx.networkx_converter(G)
    subGrx = rx.networkx_converter(subG)
    gm = rx.is_subgraph_isomorphic(Grx, subGrx, induced = False)   
    return gm

def get_layer_gates(dag):
    gate_layer_list = []
    for item in dag.layers():
        gate_layer = []
        graph_one = nx.Graph()
        for gate in item['partition']:
            c0 = gate[0]._index
            c1 = gate[1]._index
            gate_layer.append([c0, c1])
        gate_layer_list.append(gate_layer)
    return gate_layer_list

def partition_from_DAG(dag, coupling_graph):
    gate_layer_list = get_layer_gates(dag)
    num_of_gate = 0
    last_index = 0
    partition_gates = []
    for i in range(len(gate_layer_list)):
        #print(i)
        #print(last_index)
        merge_gates = sum(gate_layer_list[last_index:i+1], [])
        tmp_graph = nx.Graph()
        tmp_graph.add_edges_from(merge_gates)
        connected_components = list(nx.connected_components(tmp_graph))
        isIso = True
        for idx, component in enumerate(connected_components, 1):
            subgraph = tmp_graph.subgraph(component)
            if len(subgraph.edges()) == nx.diameter(subgraph): #path-tolopology, must sub_iso
                continue
            # print(subgraph.edges())
            if not rx_is_subgraph_iso(coupling_graph, subgraph):
                isIso = False
                break
        if isIso:
            if i == len(gate_layer_list) - 1:
                merge_gates = sum(gate_layer_list[last_index: i+1], [])
                partition_gates.append(merge_gates)
            continue
        else:
            merge_gates = sum(gate_layer_list[last_index: i], [])
            partition_gates.append(merge_gates)
            last_index = i
            if i == len(gate_layer_list) - 1:
                merge_gates = sum(gate_layer_list[last_index: i+1], [])
                partition_gates.append(merge_gates)

    return partition_gates

def get_2q_gates_list(circ):
    gate_2q_list = []
    instruction = circ.data
    for ins in instruction:
        if ins.operation.num_qubits == 2:
            gate_2q_list.append((ins.qubits[0]._index, ins.qubits[1]._index))
    return gate_2q_list


def get_qubits_num(gate_2q_list):
    num = max(max(gate) for gate in gate_2q_list)
    num += 1
    return num

def gates_list_to_QC(gate_list):  #default all 2-q gates circuit
    Lqubit = get_qubits_num(gate_list)
    circ = QuantumCircuit(Lqubit)
    # issue: cz
    for two_qubit_gate in gate_list:
        circ.cz(two_qubit_gate[0], two_qubit_gate[1])
    
    dag = circuit_to_dag(circ)
    return circ, dag


def euclidean_distance(node1, node2):
    x1, y1 = node1
    x2, y2 = node2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def generate_grid_with_Rb(n, m, Rb):
    G = nx.grid_2d_graph(n, m)  # 生成n*m的网格图
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2:
                distance = euclidean_distance(node1, node2)
                if distance <= Rb:
                    G.add_edge(node1, node2)

    return G

def extend_graph(coupling_graph, arch_size, Rb):
    coupling_graph = generate_grid_with_Rb(arch_size+1, arch_size+1, Rb)
    return coupling_graph


def map2list(mapping, num_q):
    map_list = [-1] * num_q
    for key, value in mapping.items():
        map_list[key] = value

    return map_list

def complete_mapping(i, embeddings, indices, coupling_graph):
    cur_map = embeddings[i]
    unoccupied = [value for value in coupling_graph.nodes() if value not in cur_map]
    for index in indices:
        flag = False
        if i != 0:  #If pre_map is not empty
            if embeddings[i-1][index] in unoccupied:
                cur_map[index] = embeddings[i-1][index]
                flag = True
                unoccupied.remove(cur_map[index])
        if i != len(embeddings) - 1 and flag == False:
            for j in range(i+1, len(embeddings)):
                if embeddings[j][index] != -1 and embeddings[j][index] in unoccupied:
                    cur_map[index] = embeddings[j][index]
                    unoccupied.remove(cur_map[index])
                    flag = True
                    break
        if flag == False:
            if i != 0:
                source = embeddings[i-1][index]
                node_of_shortest = dict()
                for node in unoccupied:
                    distance = nx.shortest_path_length(coupling_graph, source=source, target=node)
                    node_of_shortest[node] = distance
                min_node = min(node_of_shortest, key=node_of_shortest.get)
                cur_map[index] = min_node
                unoccupied.remove(min_node)
                flag = True
            elif i != len(embeddings) - 1:
                for j in range(i+1, len(embeddings)):
                    if embeddings[j][index] != -1:
                        source = embeddings[j][index]
                        node_of_shortest = dict()
                        for node in unoccupied:
                            distance = nx.shortest_path_length(coupling_graph, source=source, target=node)
                            node_of_shortest[node] = distance
                        min_node = min(node_of_shortest, key=node_of_shortest.get)
                        cur_map[index] = min_node
                        unoccupied.remove(min_node)
                        flag = True
                        break
        if flag == False:
            min_node = random.choice(unoccupied)
            cur_map[index] = min_node
            unoccupied.remove(min_node)
    return cur_map


def loc_to_qasm(n: int, qubit: int, loc: tuple[int, int]) -> str:
    """
    Converts a qubit location to a QASM formatted string.

    Parameters:
    n (int): The number of qubits in the quantum register.
    qubit (int): The specific qubit index.
    loc (tuple[int, int]): The location of the qubit as a tuple of two integers.

    Returns:
    str: The QASM formatted string representing the qubit location.

    Raises:
    ValueError: If the loc tuple does not have exactly two elements.
    """
    if len(loc) != 2:
        raise ValueError("Invalid loc, it must be a tuple of length 2")
    return f"Qubit(QuantumRegister({n}, 'q'), {qubit})\n({loc[0]}, {loc[1]})"

def map_to_qasm(n: int, map: list[tuple[int, int]], filename: str) -> None:
    """
    Converts a list of qubit locations to QASM format and saves it to a file.

    Parameters:
    n (int): The number of qubits in the quantum register.
    map (list[tuple[int, int]]): A list of tuples representing the locations of the qubits.
    filename (str): The name of the file to save the QASM formatted strings.

    Returns:
    None
    """
    with open(filename, 'w') as f:
        for i in range(n):
            f.write(loc_to_qasm(n, i, map[i]) + '\n')

def gate_in_layer(gate_list:list[list[int]])->list[map]:
    res = []
    for i in range(len(gate_list),-1):
        assert len(gate_list[i]) == 2
        res.append({'id':i,'q0':gate_list[i][0],'q1':gate_list[i][1]})
    return res

def check_available(graph, coupling_graph, mapping):

    for eg0, eg1 in graph.edges():
        if (mapping[eg0], mapping[eg1]) not in coupling_graph.edges():
            return False
    return True

def check_intersect(gate1, gate2, coupling_graph, mapping):
    rg1 = 1/2 * (euclidean_distance(mapping[gate1[0]], mapping[gate1[1]]))
    rg2 = 1/2 * (euclidean_distance(mapping[gate2[0]], mapping[gate2[1]]))
    dis = rg1 + rg2
    if euclidean_distance(mapping[gate1[0]], mapping[gate2[0]]) >= dis and \
        euclidean_distance(mapping[gate1[0]], mapping[gate2[1]]) >= dis and \
        euclidean_distance(mapping[gate1[1]], mapping[gate2[0]]) >= dis and \
        euclidean_distance(mapping[gate1[1]], mapping[gate2[1]]) >= dis:
        return True
    else:
        return False

def check_intersect_ver2(gate1, gate2, coupling_graph, mapping, r_re):
    if euclidean_distance(mapping[gate1[0]], mapping[gate2[0]]) > r_re and \
        euclidean_distance(mapping[gate1[0]], mapping[gate2[1]]) > r_re and \
        euclidean_distance(mapping[gate1[1]], mapping[gate2[0]]) > r_re and \
        euclidean_distance(mapping[gate1[1]], mapping[gate2[1]]) > r_re:
        return True
    else:
        return False

def get_parallel_gates(gates, coupling_graph, mapping, r_re):
    gates_list = []
    _, dag = gates_list_to_QC(gates)
    gate_layer_list = get_layer_gates(dag)

    for items in gate_layer_list:
        gates_copy = deepcopy(items)
        while(len(gates_copy) != 0):
            parallel_gates = []
            parallel_gates.append(gates_copy[0])
            for i in range(1, len(gates_copy)):
                flag = True
                for gate in parallel_gates:
                    if check_intersect_ver2(gate, gates_copy[i], coupling_graph, mapping, r_re):
                        continue
                    else:
                        flag = False
                        break
                if flag:
                    parallel_gates.append(gates_copy[i])

            for gate in parallel_gates:
                gates_copy.remove(gate)
            gates_list.append(parallel_gates)
            #print("parl:",parallel_gates)
    return gates_list

'''def set_parameters(default):
    para = {}
    if default:
        para['T_cz'] = 0.2  #us
        para['T_eff'] = 1.5e6 #us
        para['T_trans'] = 20 # us
        para['AOD_width'] = 3 #um
        para['AOD_height'] = 3 #um
        para['Move_speed'] = 0.55 #um/us
        para['F_cz'] = 0.995 

    return para'''

def set_parameters(T_cz = 0.2, T_eff = 1.5e6, T_trans=20, AOD_width=3,AOD_height=3,Move_speed=0.55,F_cz=0.995, F_trans = 1, F_1Q = 1):
    global parameters
    if parameters != {}:
        return parameters
    para = {}
    para['T_cz'] = T_cz  #us
    para['T_eff'] = T_eff #us
    para['T_trans'] = T_trans # us
    para['AOD_width'] = AOD_width #um
    para['AOD_height'] = AOD_height #um
    para['Move_speed'] = Move_speed #um/us
    para['F_cz'] = F_cz
    para['F_trans'] = F_trans
    para['F_1Q'] = F_1Q
    parameters = para
    return para

'''def compute_fidelity(parallel_gates, all_movements, num_q, gate_num):
    para = set_parameters(True)
    t_total = 0
    t_total += (len(parallel_gates) * para['T_cz']) # cz execution time, parallel
    t_move = 0
    for move in all_movements:
        t_total += (4 * para['T_trans']) # pick/drop/pick/drop
        t_move += (4 * para['T_trans'])
        max_dis = 0
        for each_move in move:
            x1, y1 = each_move[1][0],each_move[1][1]
            x2, y2 = each_move[2][0],each_move[2][1]
            dis = (abs(x2-x1)*para['AOD_width'])**2 + (abs(y2-y1)*para['AOD_height'])**2
            if dis > max_dis:
                max_dis = dis
        max_dis = math.sqrt(max_dis)
        t_total += (max_dis/para['Move_speed'])
        t_move += (max_dis/para['Move_speed'])

    t_idle = num_q * t_total - gate_num * para['T_cz']
    Fidelity = math.exp(-t_idle/para['T_eff']) * (para['F_cz']**gate_num)
    move_fidelity = math.exp(-t_move/para['T_eff'])
    return t_idle, Fidelity, move_fidelity'''

def compute_fidelity(parallel_gates, all_movements, num_q, gate_num, para=None, gate_1Q_num = 0):
    if para is None:
        para = set_parameters()
    t_total = 0
    t_total += (len(parallel_gates) * para['T_cz']) # cz execution time, parallel
    t_move = 0
    num_trans = 0
    num_move = 0
    all_move_dis = 0
    for move in all_movements:
        t_total += (4 * para['T_trans']) # pick/drop/pick/drop
        t_move += (4 * para['T_trans'])
        num_trans += 4
        max_dis = 0
        for each_move in move:
            num_move += 1
            x1, y1 = each_move[1][0],each_move[1][1]
            x2, y2 = each_move[2][0],each_move[2][1]
            dis = (abs(x2-x1)*para['AOD_width'])**2 + (abs(y2-y1)*para['AOD_height'])**2
            if dis > max_dis:
                max_dis = dis
        max_dis = math.sqrt(max_dis)
        all_move_dis += max_dis
        t_total += (max_dis/para['Move_speed'])
        t_move += (max_dis/para['Move_speed'])

    t_idle = num_q * t_total - gate_num * para['T_cz']
    Fidelity = math.exp(-t_idle/para['T_eff']) * (para['F_cz']**gate_num) * (para['F_trans'] ** num_trans)
    move_fidelity = math.exp(-t_move/para['T_eff'])
    Fidelity1Q = Fidelity * (para["F_1Q"] ** gate_1Q_num)
    FidelityCoherence = math.exp(-t_idle/para['T_eff'])
    return t_idle, Fidelity, move_fidelity, t_total, num_trans, num_move, all_move_dis, Fidelity1Q, FidelityCoherence

def get_embeddings(partition_gates, coupling_graph, num_q, arch_size, Rb, initial_mapping=None):
    embeddings = []
    begin_index = 0
    extend_position = []
    if initial_mapping:
        embeddings.append(initial_mapping)
        begin_index = 1
    for i in range(begin_index, len(partition_gates)):
        tmp_graph = nx.Graph()
        tmp_graph.add_edges_from(partition_gates[i])
        if not rx_is_subgraph_iso(coupling_graph, tmp_graph):
            coupling_graph = extend_graph(coupling_graph, arch_size, Rb)
            extend_position.append(i)
        next_embedding = get_rx_one_mapping(tmp_graph, coupling_graph)
        next_embedding = map2list(next_embedding,num_q)
        embeddings.append(next_embedding)

    for i in range(begin_index, len(embeddings)):
        indices = [index for index, value in enumerate(embeddings[i]) if value == -1]
        if indices:
            embeddings[i] = complete_mapping(i, embeddings, indices, coupling_graph)

    return embeddings, extend_position

def qasm_to_map(filename):

    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # 确保行数为偶数
    if len(lines) % 2 != 0:
        raise ValueError("文件内容的行数应为偶数，以便正确配对比特和映射位置。")
    qubit_pattern = re.compile(r"Qubit\(QuantumRegister\((\d+), 'q'\), (\d+)\)")
    match = qubit_pattern.search(lines[0].strip())
    num_q = int(match.group(1))
    mapping = [-1]*num_q
    # 遍历每对行
    for i in range(0, len(lines), 2):
        # 读取比特行和映射位置行
        qubit_line = lines[i].strip()
        position_line = lines[i+1].strip()
        
        # 解析比特索引
        match = qubit_pattern.search(qubit_line)
        if match:
            num_q = int(match.group(1))
            bit_index = int(match.group(2))
        else:
            raise ValueError(f"无法从比特行提取索引: {qubit_line}")
        # 解析映射位置
        try:
            position = eval(position_line)
        except Exception as e:
            raise ValueError(f"解析映射位置时出错: {position_line}") from e
        
        # 扩展列表到足够的长度
        mapping[bit_index] = position
    
    return mapping

def compute_fidelity_tetris(cycle_file, qasm_file, path):

    with open(path+cycle_file, 'r') as cyc_file:
        cyc_lines = cyc_file.readlines()

    last_line = cyc_lines[-1].strip()
    last_gate = list(map(int, last_line.split()))

    cnot_count = 0
    swap_count = 0
    circ = CreateCircuitFromQASM(qasm_file, path)
    for instruction, qargs, cargs in circ.data:
        if instruction.name == 'cx':  # CNOT 门
            cnot_count += 1
        elif instruction.name == 'swap':  # SWAP 门
            swap_count += 1

    num_q = len(circ.qubits)
    gate_num = cnot_count + 3*swap_count
    
    para = set_parameters(True)
    gate_cycle = (last_gate[0]+1)/2
    t_total = gate_cycle*para['T_cz']
    t_idle = num_q * t_total - gate_num * para['T_cz']

    Fidelity =math.exp(-t_idle/para['T_eff']) * (para['F_cz']**gate_num)
    # print(Fidelity)
    return Fidelity, swap_count, gate_cycle

def write_data(data, path, file_name):
    with open(os.path.join(path,file_name), 'w') as file:
        for sublist in data:
        # 将每个子列表转换为 JSON 格式的字符串，并写入文件
            file.write(json.dumps(sublist) + '\n')
def write_data_json(data, path, file_name):
    with open(os.path.join(path,file_name), 'w') as file:
        file.write(json.dumps(data) + '\n')

def read_data(path, file_name):
    with open(os.path.join(path,file_name), 'r') as file:
    # 逐行读取文件
        data = [json.loads(line) for line in file]

# 输出读取的数据
    return data

def get_circuit_from_json(num_qubits: int):
    """
    Load a quantum circuit from a JSON file based on the number of qubits.

    Args:
        num_qubits (int): The number of qubits for the desired circuit.

    Returns:
        QuantumCircuit: The loaded quantum circuit.

    Raises:
        ValueError: If no circuit configuration is found for the specified number of qubits.
    """
    # Path to the JSON file containing the circuits
    json_file_path = "./Enola/graphs.json"
    with open(json_file_path, "r") as file:
        data = json.load(file)
    circuit_data = data.get(str(num_qubits))
    from qiskit.qasm2.export import dump
    # Check if the circuit configuration exists
    if circuit_data:
        # Add gates to the circuit based on the data
        index = 1
        for circuits in circuit_data: 
            for gate in circuits:
                quantum_circuit = QuantumCircuit(num_qubits)
                quantum_circuit.cz(gate[0], gate[1])
            dump(quantum_circuit, 'Data/3_regular_cz/circuits/3_regular_{}_{}.qasm'.format(num_qubits, index))
            index += 1
        #return quantum_circuit
    else:
        # Raise an error if no configuration is found
        raise ValueError(f"No circuit configuration for {num_qubits} qubits in graphs.json")