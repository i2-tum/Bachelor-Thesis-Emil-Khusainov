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
    subprocess.run(command,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE, check=True, cwd= cwd)

    #getting fidelity by adding hardware architecture
    path = Path(f"results\\code\\{fileName}_code_full.json").as_posix()
    command = [enola_py, "simulator.py",
               "--arch_param", parameters["hardware_times"] ,
               "--fidelity_param", parameters["hardware_fidelities"],
                path
               ]
    subprocess.run(command, check=True, cwd=cwd)

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
from qiskit import transpile, qasm2
with open(sys.argv[1], 'r') as f:
    qc = qasm2.loads(f.read())
print(sum(transpile(qc, basis_gates=['cz','rx','ry','rz','h','t']).count_ops().values()))"""
    cmd = [
        enola_py,
        "-c", inline_code,
        path_circuit_abs
    ]
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True
    )

    cmd = [
        enola_py,
        "animation.py", "-h"
    ]
    result2 = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True, cwd=cwd
    )

    return fidelityDict | timeDict | {"GateCount" : int(result.stdout.strip())}

