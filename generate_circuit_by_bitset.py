import const
import display

def generate_circuit(bit_set, n):
    circuit = [[' ' for _ in range(n)] for _ in range(len(bit_set) - 1)]
    target = bit_set[0]
    for i,bit in enumerate(bit_set[1:]):
        controll = bit
        circuit[i][controll] = const.CONTROLL_BIT
        circuit[i][target]   = const.TARGET_BIT

    return circuit

bit_set = [0, 3, 5, 7]
circuit = generate_circuit(bit_set, 10)
display.display_circuit(circuit)