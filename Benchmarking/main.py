import CompilersLogic.HybridMapperMQT.HybridMapperRunner as HybridMapper
import CompilersLogic.Enola.EnolaRunner as EnolaRunner
import os

CURRENT_QASM = r"CircuitsQASM/dj_nativegates_rigetti_qiskit_opt3_10.qasm"
if __name__ == '__main__':
     abs_path = os.path.abspath(CURRENT_QASM)


     result = HybridMapper.run(CURRENT_QASM,
                               r"CompilersLogic\HybridMapperMQT\architectures\example.json", # edit this json for additional control
                               {
                                   "lookahead_weight_swaps": 0.1,
                                   "lookahead_weight_moves": 0.1,
                                   "decay": 0.1,
                                   "shuttling_time_weight": 1,
                                   "gate_weight": 0,  # 0 only shuttling
                                   "shuttling_weight": 1, # 0 only swaps
                               })
     print(f"HybridMapper results: {result}")
        #ExampleOutput: HybridMapper results: {'nSwaps': 0.0, 'nMoves': 7.0, 'nMoveGroups': 6.0,
        # 'totalPlannedExecutionTimeOfCircuit': 331.6909090909092, 'totalPlannedIdleTimeOfCircuit': 3299.709090909092,
        # 'totalPlannedGateFidelitiesOfCircuit': 0.9137660866912318, 'totalPlannedFidelitiesOfCircuit': 0.9117281029480642,
        # 'totalnCZsOfCircuit': 9.0, 'CompilationTime': 0.015889883041381836, 'GateCount': 45}




    #takes longer than HybridMapper
     result = EnolaRunner.run(abs_path, {
         "arcitecture" : 8,  # means pohysical 8x8 grid
         "routing_strategy" : "maximalis_sort", # "mis" , "maximalis", "maximalis_sort"
         "trivial_layout": False,  # if true then  logical and physical qubits will be associated 1 to 1
         "returning_to_initial": False,  #after each gate will return qubits to start state
         "window": True,  # if true then set 1000 Verticies max for MIS algorithm
         "full_code" : True, # Full code, also will create animation ALQAYS TRUE
         "hardware_times" : r"C:\Users\khusa\Documents\Bachelorthesis\Bachelor-Thesis-Emil-Khusainov\Benchmarking\CompilersLogic\Enola\architectures\compute_store_arch.json",
         "hardware_fidelities" : r"C:\Users\khusa\Documents\Bachelorthesis\Bachelor-Thesis-Emil-Khusainov\Benchmarking\CompilersLogic\Enola\architectures\compute_store_arch_fidelity.json",
     })
     print(f"Enola results: {result}")
        #Example output: Enola results: {'cir_fidelity': 0.7530460209580623, 'cir_fidelity_1q_gate': 1,
        # 'cir_fidelity_2q_gate': 0.9558895783575597, 'cir_fidelity_2q_gate_for_idle': 0.8350819830107532,
        # 'cir_fidelity_atom_transfer': 0.9665550620990835, 'cir_fidelity_coherence': 0.976018563489321, 'num_movement_stage': 68,
        # 'movement_time_ratio': [0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.8056585227217502, 0.7990504949089619, 0.7925499836042604],
        # 'average_movement': 42.97993063803415, 'list_movement_duration': [26.967994498529684, 83.12094145936335, 33.028912953790815, 26.967994498529684, 46.70993664969137, 63.245553203367585, 19.069251784911845, 26.967994498529684, 26.967994498529684, 63.245553203367585, 33.028912953790815, 26.967994498529684, 46.70993664969137, 83.12094145936335, 19.069251784911845, 26.967994498529684, 26.967994498529684, 76.27700713964738, 33.028912953790815, 26.967994498529684, 46.70993664969137, 89.44271909999159, 19.069251784911845, 26.967994498529684, 26.967994498529684, 89.44271909999159, 33.028912953790815, 26.967994498529684, 46.70993664969137, 76.27700713964738, 19.069251784911845, 26.967994498529684, 26.967994498529684, 89.44271909999159, 33.028912953790815, 26.967994498529684, 46.70993664969137, 76.27700713964738, 19.069251784911845, 26.967994498529684, 26.967994498529684, 89.44271909999159, 33.028912953790815, 26.967994498529684, 46.70993664969137, 83.12094145936335, 19.069251784911845, 26.967994498529684, 26.967994498529684, 83.12094145936335, 33.028912953790815, 26.967994498529684, 46.70993664969137, 89.44271909999159, 19.069251784911845, 26.967994498529684, 26.967994498529684, 76.27700713964738, 33.028912953790815, 26.967994498529684, 46.70993664969137, 89.44271909999159, 19.069251784911845, 26.967994498529684, 26.967994498529684, 97.23448696087954, 33.028912953790815, 26.967994498529684],
        # 'scheduling': 0.0, 'placement': 93.4866361618042, 'routing': 0.002262592315673828, 'codegen': 0.005128622055053711,
        # 'total': 93.49402737617493, 'GateCount': 59}
