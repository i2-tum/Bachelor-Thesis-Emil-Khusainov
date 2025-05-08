from qiskit import QuantumCircuit, qasm2
from mqt.qmap.pyqmap import NeutralAtomHybridArchitecture, HybridMapperParameters, HybridNAMapper
from mqt.core.plugins.qiskit import qiskit_to_mqt
import re
import os, sys
import time

stats: dict[str, float] = {}
def run(path_circuit, path_architecture):
    compile_time = 0.0
    time_start = time.time()
    arch = NeutralAtomHybridArchitecture(path_architecture)
    params = HybridMapperParameters(
        lookahead_weight_swaps=0.1,
        lookahead_weight_moves=0.1,
        decay=0.1,
        shuttling_time_weight=1,
        gate_weight=0,  # 0 only shuttling
        shuttling_weight=1)  # 0 only swaps
    mapper = HybridNAMapper(arch, params)
    compile_time = compile_time + (time.time() - time_start)

    qc = QuantumCircuit.from_qasm_file(path_circuit)

    #redirection of verbose mapping result
    r_fd, w_fd = os.pipe()
    orig_stdout_fd = sys.stdout.fileno()
    saved_stdout_fd = os.dup(orig_stdout_fd)
    os.dup2(w_fd, orig_stdout_fd)
    os.close(w_fd)
    try:
        time_start = time.time()
        qc = qiskit_to_mqt(qc)
        mapper.map(qc, verbose= True)
        compile_time = compile_time + (time.time() - time_start)
    finally:

        os.dup2(saved_stdout_fd, orig_stdout_fd)
        os.close(saved_stdout_fd)

    with os.fdopen(r_fd, 'r') as reader:
        output = reader.read()

        for key in ("nSwaps", "nMoves", "nMoveGroups"):
            pattern = rf"{key}:\s*([0-9]+)"
            match = re.search(pattern, output)
            if match:
                stats[key] = float(match.group(1))
            else:
                stats[key] = 0.0

        #print(output)

    result = mapper.get_mapped_qc()
    time_start = time.time()
    schedule = mapper.schedule(verbose=False, create_animation_csv=True)
    compile_time = compile_time + (time.time() - time_start)

    #for debug
    # print(result)
    #result = mapper.get_mapped_qc_aod()
    # print(result)
    #result = mapper.get_init_hw_pos()
    # print(result)

    mapper.save_animation_csv("animation.csv")
    mapper.save_mapped_qc("mapped_qc")
    mapper.save_mapped_qc_aod("mapper_qc_aod")

    #for GateCount
    with open("mapped_qc", "r") as f:
        lines = f.readlines()
    filtered = [l for l in lines if not l.strip().startswith("move")]
    with open("filtered.qasm", "w") as f:
        f.writelines(filtered)
    gate_count = sum(qasm2.load("filtered.qasm").count_ops().values())
    os.remove("filtered.qasm")


    #dict_keys(['totalExecutionTime', 'totalIdleTime', 'totalGateFidelities', 'totalFidelities', 'nCZs'])
    stats["totalPlannedExecutionTimeOfCircuit"] = schedule.get("totalExecutionTime")
    stats["totalPlannedIdleTimeOfCircuit"] = schedule.get("totalIdleTime")
    stats["totalPlannedGateFidelitiesOfCircuit"] = schedule.get("totalGateFidelities")
    stats["totalPlannedFidelitiesOfCircuit"] = schedule.get("totalFidelities")
    stats["totalnCZsOfCircuit"] = schedule.get("nCZs")

    stats["CompilationTime"] = compile_time

    stats["GateCount"] = gate_count


    return stats