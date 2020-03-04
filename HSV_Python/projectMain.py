import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import *
import pyvisa
import csv
import random
import time
from datetime import datetime

ARDUINO_BAUDRATE = 9600

# Setup the user interface
def guiSetup():
    app = QApplication([])
    window = QWidget()

    pTextLabel = QLabel("Plaintext 16B:")
    pTextInput = QLineEdit()
    pTextInput.setPlaceholderText("Space between bytes")
    keyLabel= QLabel("Private Key 16B:")
    keyInput = QLineEdit()
    keyInput.setPlaceholderText("Space between bytes")
    comLabel = QLabel("COM Port:")

    comInput = QComboBox()
    populateCOM(comInput)
    comRefreshButton = QPushButton("R")
    comRefreshButton.setMaximumWidth(20)
    comRefreshButton.clicked.connect(lambda: populateCOM(comInput))
    comRefreshLayout = QHBoxLayout()
    comRefreshLayout.addWidget(comInput)
    comRefreshLayout.addWidget(comRefreshButton)
    comRefreshLayout.setContentsMargins(0, 0, 0, 0)
    comInputRefresh = QWidget()
    comInputRefresh.setLayout(comRefreshLayout)

    encButton = QPushButton("Encrypt")
    encButton.setEnabled(False)
    resetButton = QPushButton("Reset")
    resetButton.clicked.connect(lambda: resetFunc(app))
    formLayoutLeft = QFormLayout()
    formLayoutLeft.addRow(pTextLabel, pTextInput)
    formLayoutLeft.addRow(keyLabel, keyInput)
    formLayoutLeft.addRow(comLabel, comInputRefresh)
    formLayoutLeft.addRow(resetButton, encButton)
    formLayoutLeft.setContentsMargins(0, 0, 0, 0)

    leftWidg = QWidget()
    leftWidg.setLayout(formLayoutLeft)

    traceLabel = QLabel("# of Traces")
    traceInput = QLineEdit()
    traceInput.setText("1")
    numEncrLabel = QLabel("# of Encrypts")
    numEncrInput = QLineEdit()
    settingsLabel = QLabel("Settings File")

    settingsInput = QComboBox()
    populateSettings(settingsInput)
    settingsRefreshButton = QPushButton("R")
    settingsRefreshButton.setMaximumWidth(20)
    settingsRefreshButton.clicked.connect(lambda: populateSettings(settingsInput))
    settingsRefreshLayout = QHBoxLayout()
    settingsRefreshLayout.addWidget(settingsInput)
    settingsRefreshLayout.addWidget(settingsRefreshButton)
    settingsRefreshLayout.setContentsMargins(0, 0, 0, 0)
    settingsInputRefresh = QWidget()
    settingsInputRefresh.setLayout(settingsRefreshLayout)


    setupLabel = QLabel("Scope Setup:")
    setupButton = QPushButton("SETUP")
    setupButton.clicked.connect(lambda: setupScope(encButton, setupButton, app))
    formLayoutRight = QFormLayout()
    formLayoutRight.addRow(traceLabel, traceInput)
    formLayoutRight.addRow(numEncrLabel, numEncrInput)
    formLayoutRight.addRow(settingsLabel, settingsInputRefresh)
    formLayoutRight.addRow(setupLabel, setupButton)
    formLayoutRight.setContentsMargins(0, 0, 0, 0)

    rightWidg = QWidget()
    rightWidg.setLayout(formLayoutRight)


    leftRightLayout = QHBoxLayout()
    leftRightLayout.addWidget(leftWidg)
    leftRightLayout.addWidget(rightWidg)
    leftRightLayout.setContentsMargins(0, 0, 0, 0)
    topWidget = QWidget()
    topWidget.setLayout(leftRightLayout)

    saveLabel = QLabel("Save Location")
    saveinput = QLineEdit()
    saveinput.setPlaceholderText("Enter Folder Name")
    saveLayout = QFormLayout()
    saveLayout.addRow(saveLabel, saveinput)
    saveLayout.setContentsMargins(0, 0, 0, 0)
    saveWidget = QWidget()
    saveWidget.setLayout(saveLayout)
    progressBar = QProgressBar()
    encButton.clicked.connect(lambda: encryptController(encButton, comInput.currentText(), keyInput.text().split(),
                                                        pTextInput.text(), int(traceInput.text()), progressBar))
    botLayout = QVBoxLayout()
    botLayout.addWidget(saveWidget)
    botLayout.addWidget(progressBar)
    botLayout.setContentsMargins(0, 0, 0, 0)
    botWidget = QWidget()
    botWidget.setLayout(botLayout)

    combinedLayout = QVBoxLayout()

    combinedLayout.addWidget(topWidget)
    combinedLayout.addWidget(botWidget)

    window.setLayout(combinedLayout)
    window.show()
    app.exec()

# Populates comList with the COM ports of the PC
# And prints them all too
# Returns comList
def populateCOM(comboBox):
    for i in range(comboBox.count()):
        comboBox.removeItem(i)
    for com in serial.tools.list_ports.comports():
        comboBox.addItem(com.device)

def populateSettings(settingsBox):
    # TODO populate combo box with text files in this dir
    pass

def setupScope(encButton, setupButton, appAlert):
    setupButton.setEnabled(False)
    try:
        resourceManager = pyvisa.ResourceManager()
        scope = resourceManager.open_resource("USB0::0xF4ED::0xEE3A::SDS1EDED3R6607::INSTR")
        print("Recalling...")
        scope.write("*RCL 1")
        for i in range(7):
            print("Recalling: {}".format(i))
            time.sleep(1)
        print("Setup")
        scope.write("WFSU SP,0,NP,0,FP,0")
        scope.close()
        encButton.setEnabled(True)
    except:
        warningAlert("Scope Failure", "Failed to Connect to Scope")
    finally:
        setupButton.setEnabled(True)

def randomPT():
    rand = random.Random()
    hexString = "%016x" % rand.randrange(16**16)
    hexArray = []
    i = 0
    while i < len(hexString):
        hexArray.append(hexString[i:i+2])
        i += 2
    return hexArray

def warningAlert(title, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

def encryptController(encButton, comPort, key, plaintext, numTraces, progressBar):
    if numTraces > 0:
        if "COM" in comPort:
            progressBar.setValue(0)
            complete = 0
            resourceManager = pyvisa.ResourceManager()
            scope = resourceManager.open_resource("USB0::0xF4ED::0xEE3A::SDS1EDED3R6607::INSTR")
            C1VDIV = float(scope.query("C1:VDIV?").split()[-1][:-1])
            print(C1VDIV)
            C1OFFSET = float(scope.query("C1:OFST?").split()[-1][:-1])
            print(C1OFFSET)
            C2VDIV = float(scope.query("C2:VDIV?").split()[-1][:-1])
            print(C2VDIV)
            C2OFFSET = float(scope.query("C2:OFST?").split()[-1][:-1])
            print(C2OFFSET)
            for i in range(numTraces):
                encryptFunc(encButton, comPort, key, "test", "KNOWN", scope, C1VDIV, C1OFFSET, C2VDIV, C2OFFSET)
                #encryptFunc(encButton, comPort, key, randomPT(), "RANDOM", scope)
                complete += 1/numTraces * 100
                progressBar.setValue(complete)
            progressBar.setValue(100)
        else:
            warningAlert("COM Failure", "No COM port selected")
    else:
        warningAlert("Trace  Failure", "Number of traces can't be <= 0")


def encryptFunc(encButton, comPort, keySend, textSend, tag, scope, C1VDIV, C1OFFSET, C2VDIV, C2OFFSET):
    encButton.setEnabled(False)
    # Minimum length of 4: ex.'COM1'
    print("serial")
    ser = serial.Serial("COM18", ARDUINO_BAUDRATE)
    print("done")
    time.sleep(2)
    ser.write('encrypt\n'.encode())
    # Change the flow once key sending is implemented
    # if False:
    #     # TODO send key given in the line edit
    #     ser.write('{0}\n{1}\n'.format(keySend, textSend))
    print(ser.readline())
    ser.close()

    ch1Data = []
    ch2Data = []
    scope.write("C1:WF? DAT2")
    ch1Raw = str(scope.read_raw()).split('\\x')[1:]
    scope.write("C2:WF? DAT2")
    ch2Raw = str(scope.read_raw()).split('\\x')[1:]
    print("Got Raw")
    # print(ch1Raw)
    for byte in ch1Raw:
        ch1Data.append(int(byte[:2], 16))
    # print(ch2Raw)
    for byte in ch2Raw:
        ch2Data.append(int(byte[:2], 16))
    # print(ch2Data)
    print("Got Bytes")
    ch1Values = []
    ch2Values = []
    for data in ch1Data:
        if data > 127:
            codeVal = data - 255
        else:
            codeVal = data
        ch1Values.append(codeVal * (C1VDIV / 25) - C1OFFSET)

    for data in ch2Data:
        if data > 127:
            codeVal = data - 255
        else:
            codeVal = data
        ch2Values.append(codeVal * (C2VDIV / 25) - C2OFFSET)
    print("Got Voltages")
    chMath = []
    for i in range(min(len(ch1Values), len(ch2Values))):
        chMath.append(ch1Values[i] - ch2Values[i])
    print("Got Math")
    filename = 'Traces/{}/{}_{}.csv'.format(tag, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"), textSend)
    with open(filename, 'w+', newline='') as csvfile:
        csvWriter = csv.writer(csvfile)
        for voltage in chMath:
            csvWriter.writerow(['{0:.4f}'.format(voltage)])
    print("Made CSV")
    encButton.setEnabled(True)
    # argChoices = ['0', '1', '2']
    # args = []
    # args[0] = input("Key choice (0, 1, 2): ") + '\n'
    # while args[0] not in argChoices:
    #     args[0] = input("Choose a key (0, 1, 2): ") + '\n'
    #
    # args[1] = input("Plaintext choice (0, 1, 2): ") + '\n'
    # while args[1] not in argChoices:
    #     args[1] = input("Choose a plaintext (0, 1, 2): ") + '\n'
    # for arg in args:
    #     ser.write(arg)

def resetFunc(app):
    for widget in app.allWidgets():
        if isinstance(widget, QLineEdit):
            if not widget.isReadOnly():
                widget.setText("")

if __name__ == "__main__":
    guiSetup()
    # comList = listComs()
    # ser = chooseCom(comList)
    # if ser is not None:
    #     serSending = True
    #     while serSending:
    #         serialCommand = input("Enter a Command:").lower()
    #         if checkCommand(serialCommand):
    #             ser.write(serialCommand + '\n')
    #             SERIAL_COMMANDS[serialCommand]()
