# Form implementation generated from reading ui file 'qtUI/machineWidget.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MachineWidget(object):
    def setupUi(self, MachineWidget: QtWidgets.QWidget):
        MachineWidget.setObjectName("MachineWidget")
        MachineWidget.resize(250, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(MachineWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.selectMachineLabel = QtWidgets.QLabel(parent=MachineWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectMachineLabel.sizePolicy().hasHeightForWidth())
        self.selectMachineLabel.setSizePolicy(sizePolicy)
        self.selectMachineLabel.setObjectName("selectMachineLabel")
        self.verticalLayout.addWidget(self.selectMachineLabel)
        self.selectMachine = QtWidgets.QComboBox(parent=MachineWidget)
        self.selectMachine.setObjectName("selectMachine")
        self.selectMachine.addItem("")
        self.selectMachine.addItem("")
        self.verticalLayout.addWidget(self.selectMachine)
        self.selectModuleLabel = QtWidgets.QLabel(parent=MachineWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectModuleLabel.sizePolicy().hasHeightForWidth())
        self.selectModuleLabel.setSizePolicy(sizePolicy)
        self.selectModuleLabel.setObjectName("selectModuleLabel")
        self.verticalLayout.addWidget(self.selectModuleLabel)
        self.selectModule = QtWidgets.QComboBox(parent=MachineWidget)
        self.selectModule.setObjectName("selectModule")
        self.verticalLayout.addWidget(self.selectModule)
        self.numberOfModulesLabel = QtWidgets.QLabel(parent=MachineWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberOfModulesLabel.sizePolicy().hasHeightForWidth())
        self.numberOfModulesLabel.setSizePolicy(sizePolicy)
        self.numberOfModulesLabel.setObjectName("numberOfModulesLabel")
        self.verticalLayout.addWidget(self.numberOfModulesLabel)
        self.numberOfModulesSpinBox = QtWidgets.QSpinBox(parent=MachineWidget)
        self.numberOfModulesSpinBox.setObjectName("numberOfModulesSpinBox")
        self.verticalLayout.addWidget(self.numberOfModulesSpinBox)
        self.numberOfBeaconsLabel = QtWidgets.QLabel(parent=MachineWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numberOfBeaconsLabel.sizePolicy().hasHeightForWidth())
        self.numberOfBeaconsLabel.setSizePolicy(sizePolicy)
        self.numberOfBeaconsLabel.setObjectName("numberOfBeaconsLabel")
        self.verticalLayout.addWidget(self.numberOfBeaconsLabel)
        self.numberOfBeaconsSpinBox = QtWidgets.QSpinBox(parent=MachineWidget)
        self.numberOfBeaconsSpinBox.setObjectName("numberOfBeaconsSpinBox")
        self.verticalLayout.addWidget(self.numberOfBeaconsSpinBox)
        self.calculateButton = QtWidgets.QPushButton(parent=MachineWidget)
        self.calculateButton.setObjectName("calculateButton")
        self.verticalLayout.addWidget(self.calculateButton)

        self.retranslateUi(MachineWidget)
        QtCore.QMetaObject.connectSlotsByName(MachineWidget)

    def retranslateUi(self, MachineWidget: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        MachineWidget.setWindowTitle(_translate("MachineWidget", "Form"))
        self.selectMachineLabel.setText(_translate("MachineWidget", "Machine:"))
        self.selectMachine.setItemText(0, _translate("MachineWidget", "item 1"))
        self.selectMachine.setItemText(1, _translate("MachineWidget", "item 2"))
        self.selectModuleLabel.setText(_translate("MachineWidget", "Module:"))
        self.numberOfModulesLabel.setText(_translate("MachineWidget", "Number of Modules:"))
        self.numberOfBeaconsLabel.setText(_translate("MachineWidget", "Number of Beacons"))
        self.calculateButton.setText(_translate("MachineWidget", "Calculate"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MachineWidget = QtWidgets.QWidget()
    ui = Ui_MachineWidget()
    ui.setupUi(MachineWidget)
    MachineWidget.show()
    sys.exit(app.exec())
