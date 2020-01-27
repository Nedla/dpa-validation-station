import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import *

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
    encButton.clicked.connect(lambda: encryptFunc(encButton, comInput.currentText(), keyInput.text(), pTextInput.text()))
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


    countLabel = QLabel("Traces Collected:")
    traceCount = QLineEdit()
    traceCount.setReadOnly(True)
    traceCount.setText("0")
    formLayoutRight = QFormLayout()
    formLayoutRight.addRow(traceLabel, traceInput)
    formLayoutRight.addRow(numEncrLabel, numEncrInput)
    formLayoutRight.addRow(settingsLabel, settingsInputRefresh)
    formLayoutRight.addRow(countLabel, traceCount)
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

def encryptFunc(encButton, comPort, keySend, textSend):
    encButton.setEnabled(False)
    # Minimum length of 4: ex.'COM1'
    if len(comPort) > 4:
        ser = serial.Serial(comPort, ARDUINO_BAUDRATE)
        ser.write('encrypt\n'.encode())
        # Change the flow once key sending is implemented
        # if False:
        #     # TODO send key given in the line edit
        #     ser.write('{0}\n{1}\n'.format(keySend, textSend))
        test = ser.read_until('\n')
        print(test)
        ser.close()
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
