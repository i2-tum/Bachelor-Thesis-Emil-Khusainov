from qiskit import QuantumCircuit, transpile

import CompilersLogic.HybridMapperMQT.HybridMapperRunner as HybridMapper
import CompilersLogic.Enola.EnolaRunner as EnolaRunner
import CompilersLogic.DasAtom.DasAtomRunner as DasAtomRunner
import CompilersLogic.Atomique.AtomiqueRunner as AtomiqueRunner
import os
import qiskit

#CURRENT_QASM = r"CircuitsQASM/dj_nativegates_rigetti_qiskit_opt3_10.qasm"
#CURRENT_QASM = r"CircuitsQASM/3_17_13.qasm"
#CURRENT_QASM = r"CircuitsQASM/rd53_130.qasm"
#CURRENT_QASM = r"CircuitsQASM/QFT/qft2.qasm"


if __name__ == '__main__':
     hybridMapper = True
     enola = False
     dasAtom = False
     atomique = False

     for i in range(9,131):
         CURRENT_QASM = f"CircuitsQASM/QFT/qft_indep_qiskit_{i}.qasm"
         abs_path = os.path.abspath(CURRENT_QASM)
         try:
             with open(abs_path, 'r') as f:
                 qasm_str = f.read()
                 circuit = qiskit.qasm2.loads(qasm_str)
         except Exception as e:
             print("FAILURE")
         print(i)
         if hybridMapper:
            try:
                Architecture1 = r"CompilersLogic\HybridMapperMQT\architectures\Architecture1.json"
                params1 = {
                    "lookahead_weight_swaps": 0.0,
                    "lookahead_weight_moves": 0.0,
                    "decay": 0.0,
                    "shuttling_time_weight": 1,
                    "gate_weight": 0,  # 0 only shuttling
                    "shuttling_weight": 1,  # 0 only swaps
                }
                params2 = {
                    "lookahead_weight_swaps": 1.0,
                    "lookahead_weight_moves": 1.0,
                    "decay": 0.99,
                    "shuttling_time_weight": 1,
                    "gate_weight": 0.5,  # 0 only shuttling
                    "shuttling_weight": 0.5,  # 0 only swaps
                }
                params3 = {
                    "lookahead_weight_swaps": 0.0,
                    "lookahead_weight_moves": 0.0,
                    "decay": 0.0,
                    "shuttling_time_weight": 1,
                    "gate_weight": 1,  # 0 only shuttling
                    "shuttling_weight": 0,  # 0 only swaps
                }
                arch = Architecture1
                params = params1

                result = HybridMapper.run(CURRENT_QASM,
                                       arch, # edit this json for additional control
                                       params
                                       )
                print(f"HybridMapper results: {result}")
                with open("RESULTS/HybridMapperResultsParameter1.txt", "a") as f:
                    f.write("------------------------------------------------------------\n")
                    f.write("Architecture: " + os.path.basename(arch) + "\n")
                    f.write("Circuit: " + os.path.basename(CURRENT_QASM) + "\n")
                    f.write(str(result) + "\n")
                    f.write("Fidelity: " + str(result["totalPlannedFidelitiesOfCircuit"]) + "\n")
                    f.write("TotalTime: " + str(result["CompilationTime"]) + "\n")
                    f.write("AllGateCount: " + str(result["GateCount"]) + "\n")
                    f.write("CZGateCount: " + str(result["totalnCZsOfCircuit"]) + "\n")
                    f.write("------------------------------------------------------------\n\n")
            except Exception as e:
                print(e)
                with open("RESULTS/HybridMapperResultsParameter1.txt", "a") as f:
                    f.write(CURRENT_QASM + "FAILURE\n")

            params = params2

            try:
                result = HybridMapper.run(CURRENT_QASM,
                                          arch,  # edit this json for additional control
                                          params
                                          )
                print(f"HybridMapper results: {result}")
                with open("RESULTS/HybridMapperResultsParameter2.txt", "a") as f:
                    f.write("------------------------------------------------------------\n")
                    f.write("Architecture: " + os.path.basename(arch) + "\n")
                    f.write("Circuit: " + os.path.basename(CURRENT_QASM) + "\n")
                    f.write(str(result) + "\n")
                    f.write("Fidelity: " + str(result["totalPlannedFidelitiesOfCircuit"]) + "\n")
                    f.write("TotalTime: " + str(result["CompilationTime"]) + "\n")
                    f.write("AllGateCount: " + str(result["GateCount"]) + "\n")
                    f.write("CZGateCount: " + str(result["totalnCZsOfCircuit"]) + "\n")
                    f.write("------------------------------------------------------------\n\n")
            except Exception as e:
                print(e)
                with open("RESULTS/HybridMapperResultsParameter2.txt", "a") as f:
                    f.write(CURRENT_QASM + "FAILURE\n")

            params = params3

            try:
                result = HybridMapper.run(CURRENT_QASM,
                                          arch,  # edit this json for additional control
                                          params
                                          )
                print(f"HybridMapper results: {result}")
                with open("RESULTS/HybridMapperResultsParameter3.txt", "a") as f:
                    f.write("------------------------------------------------------------\n")
                    f.write("Architecture: " + os.path.basename(arch) + "\n")
                    f.write("Circuit: " + os.path.basename(CURRENT_QASM) + "\n")
                    f.write(str(result) + "\n")
                    f.write("Fidelity: " + str(result["totalPlannedFidelitiesOfCircuit"]) + "\n")
                    f.write("TotalTime: " + str(result["CompilationTime"]) + "\n")
                    f.write("AllGateCount: " + str(result["GateCount"]) + "\n")
                    f.write("CZGateCount: " + str(result["totalnCZsOfCircuit"]) + "\n")
                    f.write("------------------------------------------------------------\n\n")
                #ExampleOutput: HybridMapper results: {'nSwaps': 0.0, 'nMoves': 7.0, 'nMoveGroups': 6.0,
                # 'totalPlannedExecutionTimeOfCircuit': 331.6909090909092, 'totalPlannedIdleTimeOfCircuit': 3299.709090909092,
                # 'totalPlannedGateFidelitiesOfCircuit': 0.9137660866912318, 'totalPlannedFidelitiesOfCircuit': 0.9117281029480642,
                # 'totalnCZsOfCircuit': 9.0, 'CompilationTime': 0.015889883041381836, 'GateCount': 45}
            except Exception as e:
                print(e)
                with open("RESULTS/HybridMapperResultsParameter3.txt", "a") as f:
                    f.write(CURRENT_QASM + "FAILURE\n")


         if enola:
                #takes much longer than HybridMapper
            try:
                hardware_times = r"C:\Users\khusa\Documents\Bachelorthesis\Bachelor-Thesis-Emil-Khusainov\Benchmarking\CompilersLogic\Enola\architectures\Architecture1.json"
                hardware_fidelities = r"C:\Users\khusa\Documents\Bachelorthesis\Bachelor-Thesis-Emil-Khusainov\Benchmarking\CompilersLogic\Enola\architectures\Architecture1_fidelity.json"
                result = EnolaRunner.run(abs_path, {
                 "arcitecture" : 15,  # means physical 8x8 grid
                 "routing_strategy" : "maximalis_sort", # "mis" , "maximalis", "maximalis_sort"
                 "trivial_layout": False,  # if true then  logical and physical qubits will be associated 1 to 1
                 "returning_to_initial": False,  #after each gate will return qubits to start state
                 "window": True,  # if true then set 1000 Verticies max for MIS algorithm
                 "full_code" : True, # Full code, also will create animation ALQAYS TRUE
                 "hardware_times" : hardware_times,
                 "hardware_fidelities" : hardware_fidelities,
                    })
                print(f"Enola results: {result}")

                with open("RESULTS/EnolaResults.txt", "a") as f:
                    f.write("------------------------------------------------------------\n")
                    f.write("HardwareTimes: " + os.path.basename(hardware_times) + "\n")
                    f.write("HardwareFidelities: " + os.path.basename(hardware_fidelities) + "\n")
                    f.write("Circuit: " + os.path.basename(CURRENT_QASM) + "\n")
                    f.write(str(result) + "\n")
                    f.write("Fidelity: " + str(result['cir_fidelity']) + "\n")
                    f.write("TotalTime: " + str(result["total"]) + "\n")
                    f.write("AllGateCount: " + str(result["GateCount"]) + "\n")
                    f.write("CZGateCount: " + str(result["Num CZ Gates"]) + "\n")
                    f.write("------------------------------------------------------------\n\n")
            except Exception as e:
                with open("RESULTS/EnolaResults.txt", "a") as f:
                    f.write("------------------------------------------------------------\n")
                    f.write(CURRENT_QASM + "FAILURE\n")
                    f.write("------------------------------------------------------------\n\n")
            #Example output: Enola results: {'cir_fidelity': 0.7530460209580623, 'cir_fidelity_1q_gate': 1,
            # 'cir_fidelity_2q_gate': 0.9558895783575597, 'cir_fidelity_2q_gate_for_idle': 0.8350819830107532,
            # 'cir_fidelity_atom_transfer': 0.9665550620990835, 'cir_fidelity_coherence': 0.976018563489321, 'num_movement_stage': 68,
            # 'movement_time_ratio': [0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.7990504949089619, 0.7925499836042604],
            # 'average_movement': 42.97993063803415, 'list_movement_duration': [26.967994498529684, 83.12094145936335, 33.028912953790815, 26.967994498529684, 46.70993664969137, 63.245553203367585, 19.069251784911845, 26.967994498529684, 26.967994498529684, 63.245553203367585, 33.028912953790815, 26.967994498529684, 46.70993664969137, 83.12094145936335, 19.069251784911845, 26.967994498529684, 26.967994498529684, 76.27700713964738, 33.028912953790815, 26.967994498529684, 46.70993664969137, 89.44271909999159, 19.069251784911845, 26.967994498529684, 26.967994498529684, 89.44271909999159, 33.028912953790815, 26.967994498529684, 46.70993664969137, 76.27700713964738, 19.069251784911845, 26.967994498529684, 26.967994498529684, 89.44271909999159, 33.028912953790815, 26.967994498529684, 46.70993664969137, 76.27700713964738, 19.069251784911845, 26.967994498529684, 26.967994498529684, 89.44271909999159, 33.028912953790815, 26.967994498529684, 46.70993664969137, 83.12094145936335, 19.069251784911845, 26.967994498529684, 26.967994498529684, 83.12094145936335, 33.028912953790815, 26.967994498529684, 46.70993664969137, 89.44271909999159, 19.069251784911845, 26.967994498529684, 26.967994498529684, 76.27700713964738, 33.028912953790815, 26.967994498529684, 46.70993664969137, 89.44271909999159, 19.069251784911845, 26.967994498529684, 26.967994498529684, 97.23448696087954, 33.028912953790815, 26.967994498529684],
            # 'scheduling': 0.0, 'placement': 93.4866361618042, 'routing': 0.002262592315673828, 'codegen': 0.005128622055053711,
            # 'total': 93.49402737617493, 'GateCount': 18, 'Num CZ Gates': 5}

         if dasAtom:
             params = {
                "interaction_radius": "2",
                "T_cz": "0.36",
                "T_eff": "1.5e6",
                "T_trans": "0.55",
                "AOD_width": "15",
                "AOD_height": "15",
                "Move_speed": "0.55",
                "F_cz": "0.9999",
                "F_trans": "0.9999",
                "F_1Q": "0.9999"
                }
             try:
                 result = DasAtomRunner.run(abs_path, params)
                 print(f"DasAtom results: {result}")
                 with open("RESULTS/DasAtomResults.txt", "a") as f:
                     f.write("------------------------------------------------------------\n")
                     f.write("Params: " + str(params) + "\n")
                     f.write("Circuit: " + os.path.basename(CURRENT_QASM) + "\n")
                     f.write(str(result) + "\n")
                     f.write("Fidelity: " + str(result["Fidelity"]) + "\n")
                     f.write("TotalTime: " + str(result["CompileTime"]) + "\n")
                     f.write("AllGateCount: " + str(result["GateCount"]) + "\n")
                     f.write("CZGateCount: " + str(result["Num CZ Gates"]) + "\n")
                     f.write("------------------------------------------------------------\n\n\n")
                 #Example output: DasAtom results: {'QASM File': 'dj_nativegates_rigetti_qiskit_opt3_10.qasm', 'Num Qubits': 10,
                 # 'Num CZ Gates': 9, 'Circuit Depth': 9, 'Fidelity': 0.36846800226594456, 'Movement Fidelity': 1.0,
                 # 'Num Movement Ops': 0, 'Num Transferred Qubits': 0, 'Num Moves': 0, 'Total Move Distance': 0, 'Num Gate Cycles': 9,
                 # 'Num Partitions': 1, 'Elapsed Time (s)': 0.03343391418457031, 'Total_T (from fidelity calc)': 2.6999999999999997,
                 # 'Idle Time': 24.299999999999997, 'FidelityWith1Q': 0.9977010915392792, 'GateCount': 23, 'CompileTime': 1.3780298233032227}
             except Exception as e:
                with open("RESULTS/DasAtomResults.txt", "a") as f:
                    f.write("------------------------------------------------------------\n")
                    f.write(CURRENT_QASM + "FAILURE\n")
                    f.write("------------------------------------------------------------\n\n")
         if atomique:
            result = AtomiqueRunner.run()
            print(f"Atomique results: {result}")