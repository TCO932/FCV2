# Form implementation generated from reading ui file 'qtUI/machineWidget.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from dataclasses import dataclass
from PyQt6 import QtCore, QtGui, QtWidgets
from classes import EffectedMachine, ItemMeta, Machine, Module

from data import MACHINES, MODULES
from widgets.DraggableModuleWidget import DraggableModule, ModuleDropSlot


class MachineWidget(QtWidgets.QWidget):
    machineSetted = QtCore.pyqtSignal(EffectedMachine)

    def __init__(self):
        super().__init__()
        self.setupUi()

        for machine in MACHINES.values():
            self.selectMachine.addItem(machine.getFormattedName(), machine) 

        self.selectMachine.currentIndexChanged.connect(self.on_machine_changed)
        
        self.setMachineButton.pressed.connect(self.on_set_machine_button)

        self.modules = MODULES['prod'] | MODULES['speed']
        for module in self.modules.values():
            draggableModule = DraggableModule(module)
            self.modulesLayout.addWidget(draggableModule)

        self.modulesSlots = []
        for i in range(4):
            slot = ModuleDropSlot()
            self.modulesSlots.append(slot)
            self.modulesSlotsLayout.addWidget(slot)


    def setModel(self, itemMeta: ItemMeta):
        self.effectedMachine = itemMeta.effectedMachine

        for i in range(3):
            if itemMeta.no_prod:
                self.modulesLayout.itemAt(i).widget().hide()
            else:
                self.modulesLayout.itemAt(i).widget().show()

        self.selectedModules = []
        if self.effectedMachine.modules:
            self.selectedModules = self.effectedMachine.modules

        for i in range(4):
            self.modulesSlotsLayout.itemAt(i).widget().clear()

        for i, module in enumerate(self.selectedModules):
            self.modulesSlotsLayout.itemAt(i).widget().setData(module)

        self.beaconsNumberSlider.setValue(self.effectedMachine.beaconsNumber)
        self.select_machine(self.effectedMachine)


    # TODO use in future: add module by left click
    def addToSlots(self, module: Module):
        for slot in self.modulesSlots:
            if slot.module is None:
                slot.setData(module)


    def select_machine(self, machine: Machine):
        for index in range(self.selectMachine.count()):
            if self.selectMachine.itemData(index).name == machine.name:
                self.selectMachine.setCurrentIndex(index)
                return

    def on_machine_changed(self, index):
        machine: Machine = self.selectMachine.itemData(index)
        self.beaconsNumberSlider.setRange(0, machine.maxBeacons)

        for i, slot in enumerate(self.modulesSlots):
            if i+1 > machine.slots:
                slot.hide()


        # while len of shown slots less than machine slots
        while len(list(filter(lambda slot: not slot.isHidden(), self.modulesSlots))) < machine.slots:
            hiddenSlots = list(filter(lambda slot: slot.isHidden(), self.modulesSlots))
            if hiddenSlots:
                hiddenSlots[0].show()
            else:
                slot = ModuleDropSlot()
                self.modulesSlotsLayout.addWidget(slot)


        print(f"Выбранная машина: {machine}")

    def on_set_machine_button(self):
        modules = []
        for slot in self.modulesSlots:
            if slot.module is not None and not slot.isHidden():
                modules.append(slot.module)

        effectedMachine = EffectedMachine.fromMachine(
            self.selectMachine.currentData(),
            modules=modules,
            beaconsNumber=self.beaconsNumberSlider.value()
        )
        self.machineSetted.emit(effectedMachine)

    def setupUi(self):
        self.setObjectName("MachineWidget")
        self.resize(250, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.selectMachineLabel = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectMachineLabel.sizePolicy().hasHeightForWidth())
        self.selectMachineLabel.setSizePolicy(sizePolicy)
        self.selectMachineLabel.setObjectName("selectMachineLabel")
        self.verticalLayout.addWidget(self.selectMachineLabel)
        self.selectMachine = QtWidgets.QComboBox(parent=self)
        self.selectMachine.setObjectName("selectMachine")
        self.verticalLayout.addWidget(self.selectMachine)

        # Module layout
        self.modulesLabel = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modulesLabel.sizePolicy().hasHeightForWidth())
        self.modulesLabel.setSizePolicy(sizePolicy)
        self.modulesLabel.setObjectName("selectModuleLabel")
        self.verticalLayout.addWidget(self.modulesLabel)

        self.modulesLayout = QtWidgets.QHBoxLayout()
        self.modulesLayout.setObjectName("selectModule")
        self.modulesLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout.addLayout(self.modulesLayout)

        self.modulesSlotsLabel = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.modulesLabel.sizePolicy().hasHeightForWidth())
        self.modulesSlotsLabel.setSizePolicy(sizePolicy)
        self.modulesSlotsLabel.setObjectName("modulesSlotsLabel")
        self.verticalLayout.addWidget(self.modulesSlotsLabel)

        self.modulesSlotsLayout = QtWidgets.QHBoxLayout()
        self.modulesSlotsLayout.setObjectName("modulesSlots")
        self.modulesSlotsLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout.addLayout(self.modulesSlotsLayout)

        # end Module layout

        # Beacons number
        self.beaconsNumberLabelLayout = QtWidgets.QHBoxLayout()
        self.beaconsNumberLabelLayout.setObjectName("beaconsNumberLabelLayout")
        self.beaconsNumberLabelLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.verticalLayout.addLayout(self.beaconsNumberLabelLayout)

        self.beaconsNumberLabel = QtWidgets.QLabel(parent=self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.beaconsNumberLabel.sizePolicy().hasHeightForWidth())
        self.beaconsNumberLabel.setSizePolicy(sizePolicy)
        self.beaconsNumberLabel.setObjectName("numberOfBeaconsLabel")
        self.beaconsNumberLabelLayout.addWidget(self.beaconsNumberLabel)

        self.beaconsNumberValue = QtWidgets.QLabel(parent=self)
        self.beaconsNumberLabelLayout.addWidget(self.beaconsNumberValue)


        self.beaconsNumberSlider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.beaconsNumberSlider.setObjectName("numberOfBeaconsSpinBox")
        self.beaconsNumberSlider.setTickInterval(1)
        self.beaconsNumberSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.beaconsNumberSlider.valueChanged.connect(lambda value: self.beaconsNumberValue.setText(str(value)))
        self.verticalLayout.addWidget(self.beaconsNumberSlider)

        # end Beacons number
        
        self.setMachineButton = QtWidgets.QPushButton(parent=self)
        self.setMachineButton.setObjectName("calculateButton")
        self.verticalLayout.addWidget(self.setMachineButton)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MachineWidget: QtWidgets.QWidget):
        _translate = QtCore.QCoreApplication.translate
        MachineWidget.setWindowTitle(_translate("MachineWidget", "Form"))
        self.selectMachineLabel.setText(_translate("MachineWidget", "Machine:"))
        self.modulesLabel.setText(_translate("MachineWidget", "Modules:"))
        self.modulesLabel.setToolTip(_translate("MachineWidget", "Drag module and drop into slot."))
        self.modulesSlotsLabel.setText(_translate("MachineWidget", "Machine slots:"))
        self.modulesSlotsLabel.setToolTip(_translate("MachineWidget", "Drop module into slot. Right click to remove module."))
        self.beaconsNumberLabel.setText(_translate("MachineWidget", "Number of Beacons:"))
        self.setMachineButton.setText(_translate("MachineWidget", "Set Machine"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    machineWidget = MachineWidget()
    machineWidget.show()
    sys.exit(app.exec())
