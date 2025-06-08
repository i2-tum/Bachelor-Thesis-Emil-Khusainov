from qiskit import QuantumCircuit, qasm2, transpile
from mqt.qmap.pyqmap import NeutralAtomHybridArchitecture, HybridMapperParameters, HybridNAMapper
from mqt.core.plugins.qiskit import qiskit_to_mqt
import re
import os, sys
import time
from pathlib import Path
import json


stats: dict[str, float] = {}
def run(path_circuit, path_architecture, parameters):
    print()
    fileName = Path(path_circuit).stem
    compile_time = 0.0
    time_start = time.time()
    arch = NeutralAtomHybridArchitecture(path_architecture)
    params = HybridMapperParameters(
        lookahead_weight_swaps = parameters["lookahead_weight_swaps"],
        lookahead_weight_moves = parameters["lookahead_weight_moves"],
        decay = parameters["decay"],
        shuttling_time_weight = parameters["shuttling_time_weight"],
        gate_weight = parameters["gate_weight"],  # 0 only shuttling
        shuttling_weight = parameters["shuttling_weight"])  # 0 only swaps
    mapper = HybridNAMapper(arch, params)
    compile_time = compile_time + (time.time() - time_start)

    with open(path_architecture, 'r', encoding='utf-8') as f:
        basisGates = json.load(f)["parameters"]["gateAverageFidelities"].keys()
    qc = QuantumCircuit.from_qasm_file(path_circuit)

    qc = transpile(qc, basis_gates=basisGates)
    #redirection of verbose mapping result (chossing between SWAP and shuttling) to extract statistic that printed from C lib
    r_fd, w_fd = os.pipe()
    orig_stdout_fd = sys.stdout.fileno()
    saved_stdout_fd = os.dup(orig_stdout_fd)
    os.dup2(w_fd, orig_stdout_fd)
    os.close(w_fd)
    try:
        time_start = time.time()
        qc = qiskit_to_mqt(qc)
        mapper.map(qc, verbose= False)
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

    #schedule to get fidelity and time
    result = mapper.get_mapped_qc()
    time_start = time.time()
    schedule = mapper.schedule(verbose=False, create_animation_csv=False)
    compile_time = compile_time + (time.time() - time_start)

    #for debug, maybe usefull later
    # print(result)
    #result = mapper.get_mapped_qc_aod()
    # print(result)
    #result = mapper.get_init_hw_pos()
    # print(result)

    #mapper.save_animation_csv(f"CompilersLogic/HybridMapperMQT/results/{fileName}_animation.csv")
    mapped_qc_path = f"CompilersLogic/HybridMapperMQT/results/{fileName}_mapped_qc"
    mapper.save_mapped_qc(mapped_qc_path)
    #mapper.save_mapped_qc_aod(f"CompilersLogic/HybridMapperMQT/results/{fileName}_mapper_qc_aod")

    #for GateCount
    with open(mapped_qc_path, "r") as f:
        lines = f.readlines()
    filtered = [l for l in lines if not l.strip().startswith("move")]
    with open("filtered.qasm", "w") as f:
        f.writelines(filtered)
    gate_count = sum(qasm2.load("filtered.qasm").count_ops().values())
    os.remove("filtered.qasm")

    stats["totalPlannedExecutionTimeOfCircuit"] = schedule.get("totalExecutionTime")
    stats["totalPlannedIdleTimeOfCircuit"] = schedule.get("totalIdleTime")
    stats["totalPlannedGateFidelitiesOfCircuit"] = schedule.get("totalGateFidelities")
    stats["totalPlannedFidelitiesOfCircuit"] = schedule.get("totalFidelities")
    stats["totalnCZsOfCircuit"] = schedule.get("nCZs")

    stats["CompilationTime"] = compile_time

    stats["GateCount"] = gate_count

    return stats