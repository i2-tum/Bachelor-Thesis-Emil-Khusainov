import subprocess
import os
from pathlib import Path
import json


VENV_NAME = "venv_enola"

def run(path_circuit_abs, parameters):
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    enola_py = os.path.join(current_dir,VENV_NAME,"Scripts", "python")
    fileName = Path(path_circuit_abs).stem
    cwd = os.path.join(current_dir, "Enola")
    rel_path = Path(os.path.relpath(path_circuit_abs, start=cwd)).as_posix()

    #mapping, codegen andd etc
    command = [enola_py, "run_qasm.py",
                    rel_path,
                    "--arch", str(parameters["arcitecture"]),
                    "--routing_strategy", parameters["routing_strategy"],
                    ]
    if parameters["trivial_layout"]:
        command.append("--trivial_layout")
    if parameters["returning_to_initial"]:
        command.append("--r2i")
    if parameters["window"]:
        command.append("--window")
    if parameters["full_code"]:
        command.append("--full_code")

    proc = None
    try:
        proc = subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE, check=True, cwd= cwd)
        #output = proc.stdout
    except Exception as e:
        print(proc.stderr)
        return {}

    #getting fidelity by adding hardware architecture
    path = Path(f"results\\code\\{fileName}_code_full.json").as_posix()
    command = [enola_py, "simulator.py",
               "--arch_param", parameters["hardware_times"] ,
               "--fidelity_param", parameters["hardware_fidelities"],
                path
               ]

    proc = None
    try:
        proc = subprocess.run(command, check=True, cwd=cwd)
        #output = proc.stdout
    except Exception as e:
        print(proc.stderr)
        return {}

    #collect statistic
    fidelityJson = os.path.join(cwd, "results", "fidelity", f"{fileName}_code_full_fidelity.json")
    with open( fidelityJson,"r", encoding="utf-8") as f:
        fidelityDict = json.load(f)
    timeJson = os.path.join(cwd, "results", "time", f"{fileName}_time.json")
    with open(timeJson, "r", encoding="utf-8") as f:
        timeDict = json.load(f)

    #calculate number of Gates
    inline_code = r"""import sys
import qiskit.qasm2
import qiskit.circuit
import json
from qiskit import transpile, qasm2
with open(sys.argv[1], 'r') as f:
    qc = qasm2.loads(f.read())
transpiled = transpile(qc, basis_gates=['cz','rx','ry','rz','h','t'])
sumAll = sum(transpiled.count_ops().values())
CZNumber = transpiled.count_ops().get('cz', 0)
dict = {"GateCount" : sumAll,
"Num CZ Gates" : CZNumber}
print(json.dumps(dict))"""
    cmd = [
        enola_py,
        "-c", inline_code,
        path_circuit_abs
    ]

    result = ""
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        #output = proc.stdout
    except Exception as e:
        print(proc.stderr)
        return {}

    cmd = [
        enola_py,
        "animation.py", "-h"
    ]

    result2 = ""
    try:
        result2 = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True, cwd=cwd
        )
        #output = proc.stdout
    except Exception as e:
        print(proc.stderr)
        return {}

    return fidelityDict | timeDict | json.loads(result.stdout.strip())

