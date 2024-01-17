from sabreSWAP import insert_swap_by_sabre
from mapping import bit_mapping
from generate_circuit_by_bitset import generate_circuit
from display import display_circuit

import copy
import os
import mapping
import read_file

# dir_name = input()
dir_name = "tekitou"
test_list = os.listdir(path="./input/{}".format(dir_name))

for file_name in test_list:

    #テスト用回路のディレクトリ移動する
    os.chdir('./input/{}'.format(dir_name))

    #ファイルから回路を読み込む
    source_circuit = read_file.read_file(file_name)
    circuit = copy.copy(source_circuit)
    print(circuit)
    #回路からビット数を読み込む
    n = len(circuit[0])

    node = mapping.bit_mapping(n)
    display_circuit(insert_swap_by_sabre(circuit, node))