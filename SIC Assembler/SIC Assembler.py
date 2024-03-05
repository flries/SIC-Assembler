
"""
第一階段組譯－先寫入，後運算
"""

# 開啟組合語言檔
inp = open("input.txt","r")
# 輸出含有位址的中間檔
loc = open("loc.txt","w")

# 創建符號表（Dictionary）
sym = {}
# 指令表
op = {
        "ADD":"18",
        "ADDF":"58",
        "ADDR":"90",
        "AND":"40",
        "CLEAR":"B4",
        "COMP":"28",
        "COMPF":"88",
        "COMPR":"A0",
        "DIV":"24",
        "DIVF":"64",
        "DIVR":"9C",
        "FIX":"C4",
        "FLOAT":"C0",
        "HIO":"F4",
        "J":"3C",
        "JEQ":"30",
        "JGT":"34",
        "JLT":"38",
        "JSUB":"48",
        "LDA":"00",
        "LDB":"68",
        "LDCH":"50",
        "LDF":"70",
        "LDL":"08",
        "LDS":"6C",
        "LDT":"74",
        "LDX":"04",
        "LPS":"E0",
        "MUL":"20",
        "MULF":"60",
        "MULR":"98",
        "NORM":"C8",
        "OR":"44",
        "RD":"D8",
        "RMO":"AC",
        "RSUB":"4C",
        "SHIFTL":"A4",
        "SHIFTR":"A8",
        "SIO":"F0",
        "SSK":"EC",
        "STA":"0C",
        "STB":"78",
        "STCH":"54",
        "STF":"80",
        "STI":"D4",
        "STL":"14",
        "STS":"7C",
        "STSW":"E8",
        "STT":"84",
        "STX":"10",
        "SUB":"1C",
        "SUBF":"5C",
        "SUBR":"94",
        "SVC":"B0",
        "TD":"E0",
        "TIO":"F8",
        "TIX":"2C",
        "TIXR":"B8",
        "WD":"DC"
}

# 讀取第一行程式碼
first = inp.readline()
# 切割第一行程式碼的 address, opcode, operands
data = first.split('\t')

# 如果第一行程式碼的 opcode（第二欄） 為 START
if data[1] == "START":
    # 把第一行的 operands（第三欄） 儲存為16進位的數字（first[2] = 1000 / LOCCTR = 4096）
    LOCCTR = int(data[2],16)
    # 把LOCCTR(4096)轉為16進位(0x1000)，並刪除前兩個字符(0x)，若有英文轉換為大寫，以tab分隔first。
    loc.write(str.upper(hex(LOCCTR)[2:]) +"\t"+ first)

while True:

    # 讀取下一行程式碼
    line = inp.readline()
    data = line.split('\t')
    # 加上位址寫入loc檔案，並以tab分隔。
    loc.write(str.upper(hex(LOCCTR)[2:]) +"\t"+ line)
    
    # 如果該行為註解則忽略此行，繼續下一輪迴圈
    if data[0] == "." or data[0] == ".\n":
        continue

    # 取得標記（data[0]）並於符號表中尋找該標記
    if data[0] in sym:
        # 如果找到該標記則報告錯誤，標記重複定義
        print(data[0] + "duplicate symbol\n")
        # 如果此標記名稱不為NULL
    elif data[0] != '':
        # 否則將標記及位址放入符號表中
        sym[data[0]] = LOCCTR

    if data[1].strip() in op :
        LOCCTR += 3
    elif data[1] == "WORD":
        LOCCTR += 3
    elif data[1] == "RESW":
        LOCCTR = LOCCTR + 3*int(data[2])
    elif data[1] == "RESB":
        LOCCTR = LOCCTR + int(data[2])
    elif data[1] == "BYTE":
        # 以「'」將運算符號切割為list['C','EOF','']
        OPERAND = data[2].split('\'')
        if 'C' in data[2]:
            LOCCTR += len(OPERAND[1])
        elif 'X' in data[2]:
            LOCCTR += int(len(OPERAND[1])/2)
        
    # 若讀取到 END 或檔案讀寫完畢則跳出迴圈
    if data[1]=="END" or not line:
        break
    
# 關閉檔案
inp.close()
loc.close()

"""
第二階段組譯－先運算，後寫入
"""

# 開啟含有位址的中間檔
loc = open("loc.txt","r")
# 輸出含有目的碼的列表檔
out = open("output.txt","w")

# 讀取第一行程式碼
first = loc.readline()
# 切割第一行程式碼的 locctr, address, opcode, operands
data = first.split("\t")

# 如果第一行程式碼的 opcode（第三欄） 為 START
if data[2] == "START":
    # 直接寫入output檔
    out.write(first)

while True:

    # 讀取下一行程式碼
    line = loc.readline()
    # 切割程式碼的 locctr, address, opcode, operands
    data = line.split("\t")
    # 去除該行程式碼(list)最後一個元素中的換行符號(\n)
    data = [i.strip() for i in data]

    # 判斷該行是否為註解，若為註解
    if data[1] == "." or data[1] == ".\n":
        # 把註解的第一個元素(locctr)換成NULL
        data[0] = ''
        # 以tab分隔印出至output檔
        out.write("\t".join(data) + "\n")
        continue


    # 在OPTABLE裡面找尋運算碼
    if data[2] in op:

        # 若有運算符號（SYMBOL），則data長度為4（含有4個元素）
        if len(data) == 4:
            # 以「,」將運算符號切割為list['BUFFER','X']
            OPERAND = data[3].split(',')
            
            # 如果data的第三個元素中含有X（index addressing），則輸出加上8000(16進位)
            if "X" in OPERAND:
                LOCCTR = sym[OPERAND[0]] + 32768
            # 如果data的第三個元素中只有OPERAND，則輸出的目的碼為sym表內的值
            else:
                LOCCTR = sym[data[3]]
                
            # 加上目的碼（opcode + sym內的locctr）寫入output檔案，並以tab分隔。
            out.write("\t".join(data) +"\t"+ op[data[2]] + str.upper(hex(LOCCTR)[2:]) + "\n")

        # 若沒有運算符號（RSUB），則輸出目的碼（opcode + 0000）。
        else:
            out.write("\t".join(data) +"\t\t"+ op[data[2]] + "0000\n")


    # 若運算碼為"BYTE"
    elif data[2] == "BYTE":
        # 以「'」將運算符號切割為list['C','EOF','']
        OPERAND = data[3].split('\'')
        # 若為'C'開頭的（C'EOF'）
        if OPERAND[0] == 'C':
            ASCII = []
            for i in OPERAND[1]:
                # 將'EOF'裡面的各個字元印出ascii數字（ord()結果為非字串，所以再轉換一次）
                code = str(ord(i))
                # 轉成16進位並將（0x）去掉
                code = hex(int(code))[2:]
                ASCII.append(str.upper(code))
            out.write("\t".join(data) +"\t"+ ''.join(ASCII) + "\n")
        # 若為'X'則直接印出''之間的值（X'F1'印出F1）
        elif OPERAND[0] == 'X':
            out.write("\t".join(data) +"\t"+ str(OPERAND[1]) + "\n")
        
    # 若運算碼為"WORD"
    elif data[2] == "WORD":
        # 不需印出opcode，目的碼為data[3]的值，並補0到6位數
        LOCCTR = int(data[3])
        out.write("\t".join(data) +"\t"+ str.upper(hex(LOCCTR)[2:]).zfill(6) + "\n")
        
    # 若運算碼為"END"，去除掉LOCCTR的值，並輸出程式碼
    elif data[2] =="END":
        data[0] = ''
        out.write("\t".join(data))
    # 若運算碼為其他（"RESW"或"RESB"），則不輸出目的碼，直接輸出此行程式碼
    else :
        out.write(line)
        
    # 若讀取到 END 或檔案讀寫完畢則跳出迴圈
    if "END" in data or not line :
        break

# 關閉檔案
loc.close()
out.close()

"""
第三階段組譯－編譯為objectcode檔
"""

# 開啟loc檔案來計算檔案大小
loc = open("loc.txt","r")
# 開啟含有目的碼的output檔案來輸出目的碼
out = open("output.txt","r")
# 輸出目的碼檔
obj = open("objectcode.txt","w")

# 讀進第一行（START）
first = loc.readline()
data = first.split("\t")

# 取出程式名稱['1000', 'COPY', 'START', '1000\n']
NAME = data[1].ljust(6,' ')

# 取出程式起始位置（"START"的locctr）並設定為16進位值
START = int(data[0],16)

while True:
    # 讀取下一行並以"\t"分割
    line = loc.readline()
    data = line.split("\t")
    # 直到讀取完畢（讀到"END"）
    if "END" in data or not line:
        # 計算程式總長度（"END"的locctr 減去 START）
        LENGTH = int(data[0],16) - START
        break
    
#寫出表頭紀錄（H + 程式名稱 + 程式起始位置 + 程式總長度）
obj.write("H" + NAME + str.upper(hex(START))[2:].zfill(6) + str.upper(hex(LENGTH))[2:].zfill(6) + "\n")

# 本文紀錄第一欄的起始位置預設為程式起始位置
head = START
# 此紀錄目的碼的長度預設為0
LENGTH = 0
# 此紀錄中的目的碼list
CODE = []

while True:

    # 讀取下一行並分割
    line = out.readline()
    data = line.split("\t")

    # 若為註解則跳過此次迴圈
    if "." in data[0] or ".\n" in data[0]:
        continue

    if "START" in data:
        continue

    # 如果此行含有目的碼（項目有5個：locctr, address, opcode, operands, object code）
    if len(data) == 5:
        # 若上一行的object code為空（RESW），則重新開始計算
        if head == 0:
            head = int(data[0],16)

        '''一欄本文紀錄最多紀錄長度為69，除去開頭的 'T' + 開始位置 '001000' + 紀錄長度'00'，剩下 60'''
        
        # 如果長度超過 60 則印出
        if (LENGTH + len(data[4])) > 60:
            
            # 紀錄的長度為目的碼的長度再除以2，以16進位儲存
            LENGTH = hex(int(LENGTH / 2))
            # 寫出此欄的本文紀錄（T + 起始位置 + 此紀錄長度）
            obj.write("T" + str.upper(hex(head))[2:].zfill(6) + str.upper(LENGTH)[2:].zfill(2))
            # 接續寫下此欄之目的碼
            obj.write("".join(CODE) + "\n")
            
            # 設定下一欄的起始位置為此欄最後一筆的下一筆的LOCCTR
            head = int(data[0],16)
            # 重設紀錄長度
            LENGTH = 0
            # 清空目的碼list
            CODE = []
            
        # 取出目的碼並切割（去除\n）
        data[4] = data[4].strip()
        # 長度為目的碼的長度
        LENGTH += len(data[4])
        # 增加此行目的碼至目的碼list
        CODE.append(data[4])

    elif "RESW" in data or 'RESB' in data:
        # 如果長度大於 0 ，則直接印出目前所儲存的CODE
        if LENGTH > 0:
            # 紀錄的長度為目的碼的長度再除以2，以16進位儲存
            LENGTH = hex(int(LENGTH / 2))
            # 寫出此欄的本文紀錄（T + 起始位置 + 此紀錄長度）
            obj.write("T" + str.upper(hex(head))[2:].zfill(6) + str.upper(LENGTH)[2:].zfill(2))
            # 接續寫下此欄之目的碼
            obj.write("".join(CODE) + "\n")

            # 設定下一欄的起始位置為此欄最後一筆的下一筆的LOCCTR
            head = int(data[0],16)
            # 重設紀錄長度
            LENGTH = 0
            # 清空目的碼list
            CODE = []

    # 如果讀到"END"（程式結束）
    if "END" in data or not line:
        # 如果長度大於 0 
        if LENGTH > 0:
            # 紀錄的長度為目的碼的長度再除以2，以16進位儲存
            LENGTH = hex(int(LENGTH / 2))
            # 寫出此欄的本文紀錄（T + 起始位置 + 此紀錄長度）
            obj.write("T" + str.upper(hex(head))[2:].zfill(6) + str.upper(LENGTH)[2:].zfill(2))
            # 接續寫下此欄之目的碼
            obj.write("".join(CODE) + "\n")
            
        # 因為已程式結束，印出結束紀錄（E + 程式中第一個可執行指令的位址）
        obj.write("E" + str.upper(hex(START))[2:].zfill(6))
        break


# 關閉檔案
loc.close()
out.close()
obj.close()
