import os
import const

def count_cnot(circuit):
    res = 0
    for gate in circuit:
        if(const.CONTROLL_BIT in gate):
            res += 1

    return res
        
    

def aggregate_result(file_name,circuit,decomposed_circuit,process_time):
    os.chdir("/Users/DELL/ソースコード/output")
    
    with open("my_{}.txt".format(file_name),"a") as output:
        num_gate_before = count_cnot(circuit)
        num_gate_after = count_cnot(decomposed_circuit)
        print("分解前ゲート数:{}".format(num_gate_before))
        print("分解後ゲート数:{}".format(num_gate_after))

        output.write("{} | {} | {} | {}\n".format(file_name,num_gate_before,num_gate_after,process_time))

        
        
