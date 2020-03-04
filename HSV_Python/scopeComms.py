import pyvisa
import time

if __name__ == "__main__":
    rm = pyvisa.ResourceManager()
    rm.list_resources()
    scope = rm.open_resource("USB0::0xF4ED::0xEE3A::SDS1EDED3R6607::INSTR")
    #print(scope.query("TDIV?"))
    #scope.write("*RCL 1")
    #time.sleep(2)
    #scope.timeout = None
    scope.write("GET_CSV? DD,MAX,SAVE,ON")
    # filename = "D:\SCDP.bmp"
    # scope.write("SCDP")
    # result = scope.read_raw()
    # f = open(filename, 'wb')
    # f.write(result)
    # f.flush()
    # f.close()
    scope.write("WFSU SP,0,NP,0,FP,0")
    c1Vdiv = float(scope.query("C1:VDIV?").split()[-1][:-1])
    c1OffSet = float(scope.query("C1:OFST?").split()[-1][:-1])
    c2Vdiv = float(scope.query("C2:VDIV?").split()[-1][:-1])
    c2OffSet = float(scope.query("C2:OFST?").split()[-1][:-1])
    print(c1Vdiv)
    print(c2Vdiv)
    print(c1OffSet)
    print(c2OffSet)

    ch1Data = []
    ch2Data = []
    scope.write("C1:WF? DAT2")
    result = str(scope.read_raw()).split('\\x')[1:]
    #print(result)
    for byte in result:
        ch1Data.append(int(byte[:2], 16))
    scope.write("C2:WF? DAT2")
    result2 = str(scope.read_raw()).split('\\x')[1:]
    #print(result2)
    for byte in result2:
        ch2Data.append(int(byte[:2], 16))
    #print(ch2Data)

    ch1Values = []
    ch2Values = []
    for data in ch1Data:
        if data > 127:
            codeVal = data - 255
        else:
            codeVal = data
        ch1Values.append(codeVal * (c1Vdiv/25)-c1OffSet)

    for data in ch2Data:
        if data > 127:
            codeVal = data - 255
        else:
            codeVal = data
        ch2Values.append(codeVal * (c2Vdiv/25)-c2OffSet)

    chMath = []
    for i in range(min(len(ch1Values), len(ch2Values))):
        chMath.append(ch1Values[i]-ch2Values[i])

    for i in range(len(chMath)):
        print("{}. {}:{} = {}".format(i, ch1Values[i], ch2Values[i], chMath[i]))

    print("Min: {}\nMax: {}".format(min(chMath), max(chMath)))
    #print(scope.query("WaveForm_SetUp?"))
    #while True:
    #    print(scope.read_bytes(1))