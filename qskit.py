from qiskit import IBMQ
from qiskit import IBMQ, QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.qasm import pi
from qiskit.tools.visualization import plot_histogram, circuit_drawer
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import SabreSwap as SW
from qiskit.transpiler import CouplingMap
import inspect
from mapping import convert_copling 

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

node = [[1, 3], [0, 2, 4, 5], [1, 4, 5], [0, 4, 6, 7], [1, 2, 3, 5, 6, 7], [1, 2, 4, 8, 9], [3, 4, 7], [3, 4, 6, 8], [5, 7, 9], [5, 8]]
# SabreSwapを使用してスワップゲートを最小化
cmap = CouplingMap(convert_copling(node))
pm = PassManager(SW(cmap, "lookahead"))
new_qc = pm.run(qc)

print(cmap)

# 最適化された回路を表示print("Optimized circuit:")
print(qc)
print(new_qc)