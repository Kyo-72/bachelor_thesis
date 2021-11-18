import calc
import logic
import display
import time

while(1):
    
    print("入力ビットの数を入力してください(0でプログラム終了):")
    n = int(input())

    if(n == 0):
        break
    
    print("入力集合：")
    input_list = []
    for i in range(n):
        x = (1<<i)
        
        input_list.append(x)


    print("出力ビットの数を入力してください:")
    m = int(input())

    desired_output_list = []
    print("要求出力集合:")
    for i in range(m):
        x = int(input())
        if(x  <= 0):
           print("変数の値が不当です")
           i -= 1;
           continue
        
        desired_output_list.append(x)

    #開始時間
    start = time.time()
    #NNAを満たすように回路を分解する
    decomposed_circuit = calc.calc(input_list,desired_output_list,n)
    #出力の論理状態を取得
    x = logic.logical_state(input_list,decomposed_circuit)
    #回路を出力する
    display.display_circuit(decomposed_circuit,x)
    process_time = time.time() - start
   
    

    print("input_list=[",end="")
    for i in range(n):
        if(i == n - 1):print("%d]"%(input_list[i]))
        else:print("%d,"%(input_list[i]),end="")

    
    print("desired_output_list=[",end="")
    for i in range(len(desired_output_list)):
        if(i == m - 1):print("%d]"%(desired_output_list[i]))
        else:print("%d,"%(desired_output_list[i]),end="")
    
    
    print("所要時間:%ds"%process_time)
    
    

#目的出力関数を得る

#ゲートを分解し、回路を更新




