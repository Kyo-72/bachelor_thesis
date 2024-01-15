from qiskit_my_lib import login_qiskit, convert_array_to_qiskit, convert_copling, convert_qiskit_to_array
from qiskit import IBMQ
from qiskit import IBMQ, QuantumCircuit, QuantumRegister
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import SabreSwap as SW
from qiskit.transpiler import CouplingMap

def insert_swap_by_sabre(circuit, node):
    #ログイン処理
    login_qiskit()
    #circuitとnodeを　qiskit方式に変更
    qc = convert_array_to_qiskit(circuit)
    print(qc)
    cmap = CouplingMap(convert_copling(node))
    pm = PassManager(SW(cmap, "lookahead"))
    new_qc = pm.run(qc)
    print(new_qc)

    circuit = convert_qiskit_to_array(new_qc)

    return circuit
