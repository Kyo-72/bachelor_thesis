import os

def count_cnot(circuit):
    res = 0
    for gate in circuit:
        if("c" in gate):
            res += 1

    return res
        
    

def ex_aggregate_result(file_name,circuit,decomposed_circuit,n):
    os.chdir("./output")
    
    with open("ex_{}bit_output.txt".format(n),"a") as output:
        num_gate_before = count_cnot(circuit)
        num_gate_after = count_cnot(decomposed_circuit)

        output.write("{} | {} | {}\n".format(file_name,num_gate_before,num_gate_after))

    os.chdir("../")
        
