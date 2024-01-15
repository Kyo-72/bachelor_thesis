from qiskit import IBMQ
from qiskit import IBMQ, QuantumCircuit, QuantumRegister
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import SabreSwap as SW
from qiskit.transpiler import CouplingMap
import const
from mapping import convert_copling
from generate_circuit_by_bitset import generate_circuit
from mapping import bit_mapping, convert_copling
import copy


def login_qiskit():
    IBMQ.save_account(const.QISKIT_API_KEY)
    # 自分のアカウント情報をloadする。（あらかじめ IBMQ.save_account を実行しておく必要がある. 複数のアカウントを使い分ける時はここで行う)
    provider = IBMQ.load_account()

def convert_qiskit_to_array(qc):
    char_array = []

    for i,gate in enumerate(qc.data):
        gate_type = gate[0].name
        g = [const.EMPTY for _ in range(qc.num_qubits)]

        if(gate_type == 'cx'):
            controll = gate[1][0].index
            target   = gate[1][1].index

            g[controll] = const.CONTROLL_BIT
            g[target]   = const.TARGET_BIT
            char_array.append(g)
        elif(gate_type == 'swap'):
            index1 = gate[1][0].index
            index2 = gate[1][1].index

            swap = [const.EMPTY for _ in range(qc.num_qubits)]

            swap[index1] = const.CONTROLL_BIT
            swap[index2] = const.TARGET_BIT
            char_array.append(copy.copy(swap))
            swap[index1] = const.TARGET_BIT
            swap[index2] = const.CONTROLL_BIT
            char_array.append(copy.copy(swap))
            swap[index1] = const.CONTROLL_BIT
            swap[index2] = const.TARGET_BIT
            char_array.append(copy.copy(swap))
        else:
            index = gate[1][0].index
            if(gate_type == 't'):
                g[index] = const.T_GATE
            elif(gate_type == 'tdg'):
                g[index] = const.T_DAGGER_GATE
            elif(gate_type == 'h'):
                g[index] = const.HADAMARD_GATE

            char_array.append(g)

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

    return qc


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