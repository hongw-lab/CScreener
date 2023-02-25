from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
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
    def __init__(self, state: GuiState = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeader()
        self.state = state

    def setHorizontalHeader(self):
        header_view = QHeaderView(Qt.Horizontal)
        header_view.setSectionResizeMode(QHeaderView.Stretch)
        super().setHorizontalHeader(header_view)

    def getSelectedRowItem(self):
        idx = self.currentIndex()
        return self.model().items[idx.row()]
    
    def setstate(self, state:GuiState):
        self.state = state


class CellListTableView1(GenericTableView):
    def __init__(self, *args, **kwargs):
        super(CellListTableView1,self).__init__(*args, **kwargs)
        self.doubleClicked.connect(self.activateSelected)
        self.is_activatable = True
        self.is_sortable = False

    def activateSelected(self, *args):
        self.state["focus_cell"] = self.getSelectedRowItem()

    def selectionChanged(self, new, old):
        super().selectionChanged(new, old)
        item = self.getSelectedRowItem()
        self.state["select_cell_1"] = item
