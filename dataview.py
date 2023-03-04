from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Signal,
    QSortFilterProxyModel,
)
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
        self.properties = properties + ["item"]
        self.state = state
        self.item_list = self.items_to_dict_list(items)

        self.show_row_numbers = False
        self._activated_index = None
        self._selected_index = []
        self._last_sort_column = None
        self._last_sort_order = None

    def items_to_dict_list(self, items):
        return [self.item_to_dict(item) for item in items]

    def item_to_dict(self, item):
        item_dict = dict()
        for prop in self.properties:
            if prop == "item":
                item_dict["item"] = item
            elif prop == "dFF":
                value = np.round(
                    item.FiltTrace[self.state["current_frame"]], decimals=2
                )
                item_dict["dFF"] = value.item()
            else:
                try:
                    item_dict[prop] = getattr(item, prop)
                except:
                    item_dict[prop] = None
        return item_dict

    def rowCount(self, parent=QModelIndex()):
        return len(self.item_list)

    def columnCount(self, parent=QModelIndex()):
        return len(self.properties) - 1  # remove item column

    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None

        data_item = self.item_list[idx]
        if role == Qt.DisplayRole:
            if isinstance(data_item, dict) and key in data_item:
                return data_item[key]
            if hasattr(data_item, key):
                return getattr(data_item, key)

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

    def get_item_index(self, target, prop):
        # Return row number of the target item
        for i, item in enumerate(self.item_list):
            if item[prop] is target:
                return i
        return None

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        if column != self._last_sort_column:
            if column == 0:  # Sort by ID, low to high
                self.item_list.sort(reverse=False, key=lambda x: x["ID"])
                self._last_sort_order = False
                self._last_sort_column = column
            if column == 2:  # Sort by Corr, high to low
                try:
                    self.item_list.sort(reverse=True, key=lambda x: x["Corr"])
                    self._last_sort_order = True
                    self._last_sort_column = column
                except:
                    return False
            if column == 3:  # Sort by Dist, low to high
                try:
                    self.item_list.sort(reverse=False, key=lambda x: x["Dist"])
                    self._last_sort_order = True
                    self._last_sort_column = column
                except:
                    return False
            if column == 4:  # Sort by dFF, high to low
                try:
                    self.item_list.sort(reverse=True, key=lambda x: x["dFF"])
                    self._last_sort_order = True
                    self._last_sort_column = column
                except:
                    return False
        else:
            prop = self.properties[column]
            try:
                self.item_list.sort(
                    reverse=not self._last_sort_order, key=lambda x: x[prop]
                )
                self._last_sort_column = column
                self._last_sort_order = not self._last_sort_order
            except:
                return False

        self.layoutChanged.emit()
        return True


class CellListTableModel(GenericTableModel):
    def data(self, index, role):
        # Override the GenericTableModel method
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None

        data_item = self.item_list[idx]

        if role == Qt.ForegroundRole and key == "Label":
            Label = data_item["Label"]
            return (
                QtGui.QBrush(Qt.darkGreen)
                if Label == "Good"
                else QtGui.QBrush(Qt.darkRed)
            )

        return super().data(index, role)

    def update_after_activation(self):
        # Update Dist, Corr after activating a cell
        try:
            activated_ID = self.state["focus_cell"].ID
            for item in self.item_list:
                item["Dist"] = self.state["Ms"].get_dist(activated_ID, item["ID"])
                item["Corr"] = self.state["Ms"].get_corr_coeff(
                    activated_ID, item["ID"], "filt"
                )
        except:
            return False


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
        header_view.setSectionsClickable(True)
        super().setHorizontalHeader(header_view)

    def getSelectedRowItem(self):
        idx = self.currentIndex()
        return self.model().item_list[idx.row()]["item"]

    def setstate(self, state: GuiState):
        self.state = state

    def activateSelected(self, index):
        self.model()._activated_index = index.row()

        # Update model item_list
        self.model().update_after_activation()

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

    def repaint_table(self):
        # Repaint the whole table
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )
        idx = self.model()._activated_index
        if idx:
            self.scrollTo(self.model().index(idx, 0), QAbstractItemView.EnsureVisible)
        return True

    def update_pixval(self):
        # First save the current dFF value into item_list

        for item in self.model().item_list:
            value = np.round(
                item["item"].FiltTrace[self.state["current_frame"]], decimals=2
            )
            item["dFF"] = value.item()

        col_idx = self.model().properties.index("dFF")
        self.model().dataChanged.emit(
            self.model().index(0, col_idx),
            self.model().index(self.model().rowCount(), col_idx),
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
        return [self.model().item_list[idx.row()]["item"] for idx in idxes]

    def update_after_activation(self):
        self.model().update_after_activation()
