from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal, Slot
from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6 import QtGui
from typing import Optional, List
from state import GuiState


class GenericTableModel(QAbstractTableModel):
    def __init__(
        self, items: Optional[list] = None, properties: Optional[List[str]] = None
    ):
        super().__init__()
        self.items = items
        self.properties = properties
        self.show_row_numbers = False

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent=QModelIndex()):
        return len(self.properties)

    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None

        item = self.items[idx]
        if role == Qt.DisplayRole:
            if isinstance(item, dict) and key in item:
                return item[key]

            if hasattr(item, key):
                return getattr(item, key)
        return None

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable #| Qt.ItemIsEditable
        return flags

    # def setData(self, index: QModelIndex, brush: QtGui.QBrush, role: Qt.BackgroundRole):
    #     super().setData(index, brush, role)

    def headerData(self, idx: int, orientation: Qt.Orientation, role=Qt.DisplayRole):
        """Overrides Qt method, returns column (attribute) names."""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                col_str = str(self.properties[idx])
                # use title case if key is lowercase
                if col_str == col_str.lower():
                    return col_str.title()
                # otherwise leave case as is
                return col_str
            elif orientation == Qt.Vertical:
                # Add 1 to the row index so that we index from 1 instead of 0
                if self.show_row_numbers:
                    return str(idx + 1)
                return None

        return None


class CellListTableModel(GenericTableModel):
    def data(self, index, role):
        # Override the GenericTableModel method
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None

        item = self.items[idx]

        if role == Qt.ForegroundRole and key == "Label":
            Label = getattr(item, key)
            return (
                QtGui.QBrush(Qt.darkGreen)
                if Label == "Good"
                else QtGui.QBrush(Qt.darkRed)
            )


        return super().data(index, role)


class GenericTableView(QTableView):
    rowActivated = Signal(int)

    def __init__(self, state: GuiState = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeader()
        self.state = state
        self._activated_row = None

    def setHorizontalHeader(self):
        header_view = QHeaderView(Qt.Horizontal)
        header_view.setSectionResizeMode(QHeaderView.Stretch)
        super().setHorizontalHeader(header_view)

    def getSelectedRowItem(self):
        idx = self.currentIndex()
        return self.model().items[idx.row()]

    def setstate(self, state: GuiState):
        self.state = state

    # def activateSelected(self):
    #     idx = self.currentIndex()
    #     self.set_style(idx)

    # def set_style(self, index):
    #     self.setStyleSheet("QTableView{ selection-background-color: #a9a9a9 }")

    @Slot(QModelIndex)
    def activateSelected(self, index):
        row = index.row()

        # If the newly activated row is different from the previous row
        if self._activated_row is not None and self._activated_row != row:
            prev_index = self.model().index(self._activated_row, 0)
            self.setRowBackground(prev_index, QtGui.QBrush(Qt.white))
        self._activated_row = row
        self.rowActivated.emit(row)
        self.setRowBackground(index, QtGui.QBrush(QtGui.QColor(200, 200, 255)))

    def setRowBackground(self, index, brush):
        # Temporarily allow edit
        # old_flags = self.model().flags(index)
        # self.model().setFlags(index, old_flags | Qt.ItemIsEditable)
        for i in range(self.model().columnCount()):
            self.model().setData(
                self.model().index(index.row(), i), brush, Qt.BackgroundRole
            )


class CellListTableView1(GenericTableView):
    def __init__(self, *args, **kwargs):
        super(CellListTableView1, self).__init__(*args, **kwargs)
        self.doubleClicked.connect(self.activateSelected)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.is_activatable = True
        self.is_sortable = False

    def activateSelected(self, *args):
        self.state["focus_cell"] = self.getSelectedRowItem()
        super().activateSelected(self.currentIndex())


class CellListTableView2(GenericTableView):
    def __init__(self, *args, **kwargs):
        super(CellListTableView2, self).__init__(*args, **kwargs)
        self.doubleClicked.connect(self.activateSelected)
        self.is_activatable = True
        self.is_sortable = True

    def activateSelected(self, *args):
        self.state["companion_cell"] = self.getSelectedRowItem()
        super().activateSelected(self.currentIndex())

    def selectionChanged(self, new, old):
        super().selectionChanged(new, old)
        items = self.getSelectedRowItems()
        self.state["select_cell_2"] = items

    def getSelectedRowItems(self):
        idxes = self.selectionModel().selectedRows()
        return [self.model().items[idx.row()] for idx in idxes]
