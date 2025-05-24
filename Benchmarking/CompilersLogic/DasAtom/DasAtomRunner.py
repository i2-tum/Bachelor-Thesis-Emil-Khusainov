import os
import subprocess
import sys

VENV_NAME = "venv_DasAtom"

def run():
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    python = os.path.join(current_dir, VENV_NAME, "Scripts", "python")
    cwd = os.path.join(current_dir, "DasAtom")

    # mapping, codegen andd etc
    command = [python, "DasAtom.py", "dj_nativegates_rigetti_qiskit_opt3_10.qasm",
        r"C:\Users\khusa\Documents\Bachelorthesis\Bachelor-Thesis-Emil-Khusainov\Benchmarking\CircuitsQASM"
               ]
    proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True, check=True, cwd=cwd)
    print(proc.stdout)
    return ""