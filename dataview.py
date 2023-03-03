from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, Signal, Slot
from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from PySide6 import QtGui
from typing import Optional, List
from state import GuiState
import numpy as np


class GenericTableModel(QAbstractTableModel):
    def __init__(
        self,
        items: Optional[list] = None,
        properties: Optional[List[str]] = None,
        state: GuiState = None,
    ):
        super().__init__()
        self.items = items
        self.properties = properties
        self.show_row_numbers = False
        self._activated_index = None
        self._selected_index = []
        self.state = state

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

        if role == Qt.BackgroundRole and idx != self._activated_index:
            return QtGui.QBrush(Qt.white)
        if role == Qt.BackgroundRole and idx == self._activated_index:
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        if role == Qt.BackgroundRole and idx not in self._selected_index:
            return QtGui.QBrush(Qt.white)
        if role == Qt.BackgroundRole and idx in self._selected_index:
            return QtGui.QBrush(QtGui.QColor(180, 230, 250))

        return None

    def flags(self, index: QModelIndex):
        flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable  # | Qt.ItemIsEditable
        return flags

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

    def get_item_index(self, target):
        # Return row number of the target item
        for i, item in enumerate(self.items):
            if item is target:
                return i
        return None


class CellListTableModel(GenericTableModel):
    def data(self, index, role):
        # Override the GenericTableModel method
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None

        item = self.items[idx]
        activated_item = self.state["focus_cell"]

        if role == Qt.ForegroundRole and key == "Label":
            Label = getattr(item, key)
            return (
                QtGui.QBrush(Qt.darkGreen)
                if Label == "Good"
                else QtGui.QBrush(Qt.darkRed)
            )

        if role == Qt.DisplayRole and key == "Corr":
            try:
                return self.state["Ms"].get_corr_coeff(
                    activated_item.ID, item.ID, "filt"
                )
            except:
                return 0

        if role == Qt.DisplayRole and key == "Dist":
            try:
                return self.state["Ms"].get_dist(activated_item.ID, item.ID)
            except:
                return "Inf"

        if role == Qt.DisplayRole and key == "PixVal":
            try:
                value = np.round(
                    item.FiltTrace[self.state["current_frame"]], decimals=3
                )
                return value.item()
            except:
                return "NA"

        return super().data(index, role)


class GenericTableView(QTableView):
    rowActivated = Signal(int)

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

    def setstate(self, state: GuiState):
        self.state = state

    def activateSelected(self, index):
        # row = index.row()
        # if not self.model()._activated_index:
        #     self.model()._activated_index = index.row()
        # else:
        #     old_index = self.model()._activated_index
        #     self.model()._activated_index = index.row()
        self.model()._activated_index = index.row()
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )
        return True

    def selectionChanged(self, new, old):
        # Not actually doing visible things because selected items are already highlighted by the cursor
        super().selectionChanged(new, old)
        old = self.model()._selected_index
        if old:
            row_min = min(old, key=lambda x: x.row())
            row_max = max(old, key=lambda x: x.row())
            self.model().dataChanged.emit(row_min, row_max)
        self.model()._selected_index = self.selectionModel().selectedRows()

    def update_focus_entry(self, idx: QModelIndex = None):
        # Repaint the whole table
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )
        return True

    def update_activate_entry(self, idx: QModelIndex = None):
        # Called when user activate focus cell by clicking on the contour
        idx = self.model()._activated_index
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )
        self.scrollTo(self.model().index(idx, 0), QAbstractItemView.EnsureVisible)
        return True

    def update_pixval(self):
        try:
            col_idx = self.model().properties.index("PixVal")
            self.model().dataChanged.emit(
                self.model().index(0, col_idx),
                self.model().index(self.model().rowCount(), col_idx),
            )
            return True
        except:
            return False


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

    def set_activated(self):
        focus_cell = self.state["focus_cell"]
        idx = self.model().get_item_index(focus_cell)
        self.model()._activated_index = idx
        super().update_activate_entry()


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
