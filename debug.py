from sabreSWAP import insert_swap_by_sabre
from mapping import bit_mapping
from generate_circuit_by_bitset import generate_circuit
from display import display_circuit

bit_set = [0, 2, 3, 5, 7 , 8 , 9]
circuit = generate_circuit(bit_set, 10)

nodes = bit_mapping(10)

display_circuit(insert_swap_by_sabre(circuit, nodes))