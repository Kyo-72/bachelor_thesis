from z3 import *
import const
MAX_NUM_GATE = 50

def nearest_neighbor(c_vec,t_vec,n,s):
    
    for i in range(n):
        if(i == 0):
            P = t_vec[1]
        elif(i == n - 1):
            P = t_vec[n - 2]
        else:
            P = Xor(t_vec[i - 1],t_vec[i + 1])
            
        s.add(Implies(c_vec[i],P))
        

def one_bit_per_gate(vec,n,s):

    P_vec = [Bool("P_vec%d" % i) for i in range(n)]
    

    for i in range(n):
        P_vec[i] = vec[i]
        for j in range(n):
            if(i != j):
                P_vec[i] = And(P_vec[i],Not(vec[j]))
            
    #全ての制約をorで追加したい
    P = P_vec[0]
    for i in range(1,n):
       P = Or(P,P_vec[i])

    s.add(P)
    
            

def generate_output(f_vec,c_vec,t_vec,d,n):
    
    for d in range(d):
        for i in range(n):
            f_vec[d + 1][i] = f_vec[d][i]
            for j in range(n):

                #コントロールビットとターゲットビットが隣接していれば制約を追加
                if( abs(i - j) < 2 and i != j):
                    f_vec[d + 1][i] = If(And(t_vec[d][i],c_vec[d][j]),f_vec[d + 1][i]^f_vec[d][j],f_vec[d + 1][i])

        
            

def equal_desired_output(f_vec,output_list,n,d,s):
    
    i = 0
    for output in output_list:
        
        P = False
        
        for i in range(n):
        
            P = Or(P,(f_vec[d][i] == output) )
            
        s.add(P)

def ex_equal_desired_output(f_vec,output_list,n,d,s):
    #負の数の処理
    for i in range(len(output_list)):
        output_list[i] = abs(output_list[i])
        
    for output in output_list:
        
        #要求出力と出力が正しいかを判定
        s.add(f_vec[d][output_list.index(output)] == output)


def display_bool(c_vec,t_vec,m,d,n):

    for i in range(d):
        for j in range(n):
                    
            print("%d個目、%dライン"%(i+1,j))
            print("%s"%is_true( m[ c_vec[i][j] ] ))
            print("%s"%is_true( m[ t_vec[i][j] ] ))
        print()

def convert_output(m,d,n,c_vec,t_vec):
    output = [[" " for j in range(n)] for i in range(d)]
    
    for i in range(d):
        output
        for j in range(n):
            if(m[c_vec[i][j]] == True):
                output[i][j] = "c"

            if(m[t_vec[i][j]] == True):
                output[i][j] = "t"
                
    return output
    
                                             
                        
            

def calc(input_list,output_list,n,num_of_var,gate_type):

    d = 0;
    #ゲート数200まで探索

    #論理状態を表現する変数
    
    
    
        
    
    while(d < MAX_NUM_GATE):
        gate = {}

        #d*n CNOTゲート群を表す変数
        c_vec = [[Bool("c_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d)]
        t_vec = [[Bool("t_vec[%d,%d]" % (i,j)) for j in range(n)] for i in range(d)]
        #論理状態を表す変数
        f_vec = [[BitVec("f_vec[%d,%d]" % (i,j),num_of_var) for j in range(n)] for i in range(d + 1)]
        for i in range(n):
        
            f_vec[0][i] =  BitVecVal(input_list[i],num_of_var)
        #z3-solver インスタンスの作成
        s = Solver()

        
        #ゲートごとに制約を追加
        for i in range(d):

            
            #NNA制約式の追加(使わなくていいかも)
            #nearest_neighbor(c_vec[i],t_vec[i],n,s)
            #同一ゲートはコントロールビットが一つしかない制約
            one_bit_per_gate(c_vec[i],n,s)
            one_bit_per_gate(t_vec[i],n,s)

        
        #出力を生成
        generate_output(f_vec,c_vec,t_vec,d,n)
        #出力と要求出力の一致
        
        
        ex_equal_desired_output(f_vec,output_list,n,d,s)
        
        #for i in range(n):
            #print("%dline f_vec P :%s"%(i + 1,f_vec[d][i]) )
            
        print("d=%d"%d)
        if(s.check() == sat):
            m = s.model()
            #display_gates(c_vec,t_vec,m,d,n)
            
            return convert_output(m,d,n,c_vec,t_vec)
        d += 1

    
#input = [1,2,4,8,16]
#output = [17]
#n = len(input) 
#calc(input,output,n)
