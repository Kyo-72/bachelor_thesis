from qiskit import IBMQ
from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.qasm import pi
from qiskit.tools.visualization import plot_histogram, circuit_drawer
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import SabreSwap as SW
from qiskit.transpiler import CouplingMap
import const
from mapping import convert_copling 
from qiskit.converters import circuit_to_gate
from qiskit.visualization import dag_drawer
import display

def convert_qiskit_to_array(qc):
    char_array = [[' ' for _ in range(qc.size())] for _ in range(qc.num_qubits)]

    for i,gate in enumerate(qc.data):
        gate_type = gate[0].name
        if(gate_type == 'cx'):
            controll = gate[1][0].index
            target   = gate[1][1].index

            char_array[i][controll] = const.CONTROLL_BIT
            char_array[i][target]   = const.TARGET_BIT
        else:
            index = gate[1][0].index
            if(gate_type == 't'):
                char_array[i][index] = const.T_GATE
            elif(gate_type == 'tdg'):
                char_array[i][index] = const.T_DAGGER_GATE
            elif(gate_type == 'h'):
                char_array[i][index] = const.HADAMARD_GATE

    return char_array

def insert_qiskit_object(qc, gate_type, qubits):
    if(gate_type != 'cx'):
        index = qubits.index(gate_type)
        if(gate_type == const.T_GATE):
            qc.t(index)
        elif(gate_type == const.T_DAGGER_GATE):
            qc.tdg(index)
        elif(gate_type == const.HADAMARD_GATE):
            qc.h(index)
    else:
        controll = qubits.index(const.CONTROLL_BIT)
        target   = qubits.index(const.TARGET_BIT)
        qc.cx(controll, target)

def convert_array_to_qiskit(array):
    qr = QuantumRegister(len(array[0]), "q")
    qc = QuantumCircuit(qr)

    for qubits in array:
        index = -1
        gate_type = ' '
        if(const.CONTROLL_BIT in qubits):
            gate_type = 'cx'
        elif(const.T_GATE in qubits):
            gate_type = const.T_GATE
        elif(const.T_DAGGER_GATE in  qubits):
            gate_type = const.T_DAGGER_GATE
        elif(const.HADAMARD_GATE in qubits):
            gate_type = const.HADAMARD_GATE

        insert_qiskit_object(qc, gate_type, qubits)
        print(qc)

    return qc




api_key = 'bb9b908d83393870f29f842eece93fd95f187dec8f25cfd1b20459f20e03a8b17f973dcc29be3237feb50429d3999b47fd7fae49a151c3cf9b133f6c1734e148'

IBMQ.save_account(api_key)

# 自分のアカウント情報をloadする。（あらかじめ IBMQ.save_account を実行しておく必要がある. 複数のアカウントを使い分ける時はここで行う)
provider = IBMQ.load_account()

# 量子回路を作成
qr = QuantumRegister(10, "q")
qc = QuantumCircuit(qr)
qc.cx(3, 4)  # free
qc.cx(4, 3)  # free
qc.cx(1, 0)  # free
qc.cx(0, 1)
qc.cx(2, 1)  # free
qc.cx(2, 3)
qc.h(1)
qc.h(3)
qc.tdg(3)

print(qc)
circuit = convert_qiskit_to_array(qc)
display.display_circuit(circuit)

# node = [[1, 3], [0, 2, 4, 5], [1, 4, 5], [0, 4, 6, 7], [1, 2, 3, 5, 6, 7], [1, 2, 4, 8, 9], [3, 4, 7], [3, 4, 6, 8], [5, 7, 9], [5, 8]]
# # SabreSwapを使用してスワップゲートを最小化
# cmap = CouplingMap(convert_copling(node))
# pm = PassManager(SW(cmap, "lookahead"))
# new_qc = pm.run(qc)

# print(cmap)

# # 最適化された回路を表示print("Optimized circuit:")
# print(qc)
# print(new_qc)
# dag_circuit = circuit_to_dag(qc)
# d = dag_circuit.gate_nodes()[0].op
# circuit = convert_qiskit_to_array(qc)