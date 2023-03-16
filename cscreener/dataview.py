from PySide6.QtCore import (
    QAbstractTableModel,
    QModelIndex,
    Qt,
    Slot,
    QItemSelectionModel,
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
        # Key "item" points to the Neuron object
        # Key "visits" keep track of number of past activations
        self.properties = properties + ["item","visits"]
        self.state = state
        self.item_list = self.items_to_dict_list(items)

        self.show_row_numbers = False
        self._activated_index = None
        self._selected_index = []  # Keep track of entries in the selected cell list
        self._current_selection = []  # Keep track of user's current selections
        # Default sorting order (value for reverse in sort) for ID, Label, Corr, Dist, dFF
        self._default_sort_order = [False, None, True, False, True]
        self._good_color_dict = {0:(255,255,255), 1:(230,255,230), 2:(180,255,180), 3:(130,255,130)}
        self._bad_color_dict = {0:(255,255,255), 1:(255,230,230), 2:(255,180,180), 3:(255,130,130)}

    def items_to_dict_list(self, items):
        return [self.item_to_dict(item) for item in items]

    def item_to_dict(self, item):
        item_dict = dict()
        for prop in self.properties:
            if prop == "item":
                item_dict[prop] = item
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
        # Keep track of selection state
        item_dict["selected"] = False
        return item_dict

    def rowCount(self, parent=QModelIndex()):
        return len(self.item_list)

    def columnCount(self, parent=QModelIndex()):
        return len(self.properties) - 2  # remove item & visits column

    def data(self, index, role):
        key = self.properties[index.column()]
        idx = index.row()
        if idx >= self.rowCount():
            return None
        data_item = self.item_list[idx]
        num_visits = data_item["visits"]
        
        if num_visits>6:
            num_visits = 6
        num_visits = (num_visits+1)//2

        # Display content
        if role == Qt.DisplayRole:
            if isinstance(data_item, dict) and key in data_item:
                return data_item[key]
            if hasattr(data_item, key):
                return getattr(data_item, key)
        # Color background based on activation/selection state
        if (
            role == Qt.BackgroundRole
            and idx != self._activated_index
            and not data_item["selected"]
        ):
            # Color the background based on the visits (white = no visit) and label
            return QtGui.QBrush(QtGui.QColor(*self._good_color_dict[num_visits])) if data_item["item"].is_good() else QtGui.QBrush(QtGui.QColor(*self._bad_color_dict[num_visits]))
        if role == Qt.BackgroundRole and idx == self._activated_index:
            # Orange background for activated cell
            return QtGui.QBrush(QtGui.QColor(250, 220, 180))
        if role == Qt.BackgroundRole and data_item["selected"]:
            # Light blue background for selected cell
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

    def sort(self, column, order=None):
        self.layoutAboutToBeChanged.emit()
        prop = self.properties[column]
        # Label column header clicked does no sort but reset visits
        if column == 1:
            for item in self.item_list:
                item["item"].reset_visits()
            return True
        try:
            sort_idx = sorted(
                range(0, len(self.item_list)),
                key=lambda x: self.item_list[x][prop],
                reverse=self._default_sort_order[column],
            )
            self.item_list[:] = [self.item_list[i] for i in sort_idx]
            self._default_sort_order[column] = not self._default_sort_order[column]
        except Exception:
            return False

        # Update the saved activate and selection indx after sorting
        try:
            self._activated_index = sort_idx.index(self._activated_index)
        except Exception:
            pass
        try:
            self._selected_index = [sort_idx.index(i) for i in self._selected_index]
        except Exception:
            pass
        # Reposition the selected rows
        try:
            self._current_selection = [
                sort_idx.index(i) for i in self._current_selection
            ]
        except Exception:
            pass
        return True

    def reset_sort_order(self):
        self._default_sort_order = [False, None, True, False, True]


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
                    activated_ID, item["ID"], self.state["trace_mode"]
                )
                item["visits"] = item["item"].visits
            return True
        except:
            return False


class GenericTableView(QTableView):
    # rowActivated = Signal(int)

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

    def repaint_table(self):
        # Repaint the whole table
        self.model().dataChanged.emit(
            self.model().index(0, 0),
            self.model().index(self.model().rowCount(), self.model().columnCount()),
        )

    def scroll_to_activated(self):
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

    def update_after_toggle(self):
        for item in self.model().item_list:
            item["Label"] = item["item"].Label


class CellListTableView1(GenericTableView):
    def __init__(self, *args, **kwargs):
        super(CellListTableView1, self).__init__(*args, **kwargs)
        self.doubleClicked.connect(self.activateSelected)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.is_activatable = True
        self.is_sortable = False

    def activateSelected(self, *args):
        # Called when user double click selected cell
        self.state["focus_cell"] = self.getSelectedRowItem()
        # Super class update the model _activated_index attribute
        super().activateSelected(self.currentIndex())

    def update_after_activation(self):
        # This runs when user activate cell through double clicking the contour
        focus_cell = self.state["focus_cell"]
        if not self.model()._activated_index:
            idx = idx = self.model().get_item_index(focus_cell, "item")
            self.model()._activated_index = idx
        elif self.model().item_list[self.model()._activated_index]["item"] is not focus_cell:
            idx = self.model().get_item_index(focus_cell, "item")
            self.model()._activated_index = idx

        return self.model().update_after_activation()


class CellListTableView2(GenericTableView):
    def __init__(self, *args, **kwargs):
        super(CellListTableView2, self).__init__(*args, **kwargs)
        self.doubleClicked.connect(self.activateSelected)
        self.is_activatable = True
        self.is_sortable = True
        self.horizontalHeader().sectionClicked.connect(self.on_header_clicked)

    @Slot(int)
    def on_header_clicked(self, logical_index):
        # self.model().sort(logical_index, None)
        # Reposition the current selection

        # Hotfix, call mainwindow update_gui to repaint the two tables if logical_index==1
        if logical_index == 1 : 
            mw = self.parent().parent()
            mw.cell_list1.model().update_after_activation()
            mw.cell_list2.model().update_after_activation()
            mw.update_gui(["cell_list"])
        else:
            idx_list = [
                self.model().index(i, j)
                for i in self.model()._current_selection
                for j in range(0, self.model().columnCount())
            ]
            self.selectionModel().clear()
            for idx in idx_list:
                self.selectionModel().select(idx, QItemSelectionModel.Select)
            self.model().layoutChanged.emit()
        

    def activateSelected(self, *args):
        # Called when user double click selected cell
        # Sets the state for the main app
        self.state["companion_cell"] = self.getSelectedRowItem()
        super().activateSelected(self.currentIndex())

    def selectionChanged(self, new, old):
        super().selectionChanged(new, old)
        items = self.getSelectedRowItems()
        self.state["select_cell_2"] = items
        idxes = self.selectionModel().selectedRows()
        self.model()._current_selection = [i.row() for i in idxes]

    def getSelectedRowItems(self):
        idxes = self.selectionModel().selectedRows()
        return [self.model().item_list[idx.row()]["item"] for idx in idxes]

    def update_after_activation(self):
        return self.model().update_after_activation()

    def selection_added_display(self):
        # Set the item_list entries "selected", update the _selected_index
        selected_idxes = self.selectionModel().selectedRows()
        for i in selected_idxes:
            self.model().item_list[i.row()]["selected"] = True
        self.model()._selected_index = self.model()._selected_index + [
            i.row() for i in selected_idxes
        ]
        tmp_set = set(self.model()._selected_index)
        self.model()._selected_index = list(tmp_set)
        self.selectionModel().clear()

        self.repaint_table()

    def display_cleared(self):
        for i in self.model()._selected_index:
            self.model().item_list[i]["selected"] = False
        self.model()._selected_index.clear()
        self.repaint_table()
