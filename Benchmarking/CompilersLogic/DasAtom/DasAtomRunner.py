import os
import subprocess
import sys
import json
import shutil
import time

VENV_NAME = "venv_DasAtom"

def run(abs_path, params):
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    python = os.path.join(current_dir, VENV_NAME, "Scripts", "python")
    cwd = os.path.join(current_dir, "DasAtom")

    temp_dir = os.path.join(cwd, "tempDir")
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    if not os.path.isdir(temp_dir):
        os.makedirs(temp_dir)

    dst_file = os.path.join(temp_dir, os.path.basename(abs_path))
    shutil.copy2(abs_path, dst_file)
    command = [python, "DasAtom.py", "BENCH",
        "tempDir",
        "--interaction_radius", params["interaction_radius"],
        "--tcz", params["T_cz"],
        "--teff", params["T_eff"],
        "--ttrans", params["T_trans"],
        "--t1q", params["T_1Q"],
        "--aodwidth", params["AOD_width"],
        "--aodheight", params["AOD_height"],
        "--movespeed", params["Move_speed"],
        "--fcz", params["F_cz"],
        "--ftrans", params["F_trans"],
        "--f1q", params["F_1Q"]
               ]
    result = "Error"
    time_start = time.time()
    proc = None
    try:
        time_start = time.time()
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True, cwd=cwd)
        output = proc.stdout.strip()
        result = json.loads(output)
    except Exception as e:
        print(proc.stderr)
    return result | {"CompileTime" : (time.time() - time_start)}