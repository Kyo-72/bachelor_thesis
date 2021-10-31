from z3 import *
MAX_NUM_GATE = 10

def nearest_neighbor(c_vec,t_vec,n,s):
    
    for i in range(1,n):
        P = Xor(t_vec[i - 1],t_vec[i + 1])
        s.add(Implies(c_vec[i],P))

def one_bit_per_gate(vec,n,s):
    
    P = vec[1]
    for i in range(1,n):
        P = Xor(P,vec[i])
    s.add(P)

def generate_output(f_vec,c_vec,t_vec,d,n):
    
    for d in range(d):
        c_bit = BitVec("c_bit",n + 1)
        
        for i in range(1,n + 1):
            c_bit = If(c_vec[d][i],(c_bit^i),c_bit)
        for i in range(1,n + 1):
            f_vec[i] = If(t_vec[d][i],c_bit^f_vec[i],f_vec[i])

def equal_desired_output(f_vec,output_list,n,s):
    

    for output in output_list:
        
        P = False
        for j in range(1,n + 1):
            P = Or(P,f_vec[j] == output)

    s.add(P)

    

        
        

def calc(input_list,output_list,n):

    d = 1;
    #ゲート数200まで探索

    #論理状態を表現する変数
    
    f_vec = [BitVec("f_vec%d" % i, n) for i in range(n + 1)]
    for i in range(1,n + 1):
        
        f_vec[i] = 0 | input_list[i] 
    
    while(d < MAX_NUM_GATE):
        gate = {}

        #d*n CNOTゲート群を表す変数
        c_vec = [[Bool("c_vec[%d,%d]" % (i,j)) for j in range(n + 1)] for i in range(d)]
        t_vec = [[Bool("t_vec[%d,%d]" % (i,j)) for j in range(n + 1)] for i in range(d)]

        #z3-solver インスタンスの作成
        s = Solver()

        
        #ゲートごとに制約を追加
        for i in range(d):

            
            #NNA制約式の追加
            nearest_neighbor(c_vec[i],t_vec[i],n,s)
            #同一ゲートはコントロールビットが一つしかない制約
            one_bit_per_gate(c_vec[i],n,s)
            one_bit_per_gate(t_vec[i],n,s)


        #出力を生成
        generate_output(f_vec,c_vec,t_vec,d,n)
        #出力と要求出力の一致
        equal_desired_output(f_vec,output_list,n,s)
        
        if(s.check() == sat):
            print(d)
            m = s.model()
            for i in range(d):
                for j in range(1,n + 1):
                    print("contoroll bit = %s " %is_true( m[c_vec[i][j]]) )
                    print("target bit = %s " %is_true( m[t_vec[i][j]]) )
            
            
            break
        else:
            d += 1
            

        


    

input = [0,1,2,4,8]
output = [1,2,6,8]
n = 4

calc(input,output,n)
