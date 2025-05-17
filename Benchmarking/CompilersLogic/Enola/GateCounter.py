import sys
import qiskit.qasm2
import qiskit.circuit
from qiskit import transpile, qasm2
#later tranfer when need new statistic from inline to here
with open(sys.argv[1], 'r') as f:
    qc = qasm2.loads(f.read())
print(transpile(qc, basis_gates=['cz','rx','ry','rz','h','t']).count_ops())