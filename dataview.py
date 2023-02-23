from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QAbstractItemModel
from PySide6.QtWidgets import QTableView, QAbstractItemView, QHeaderView
from typing import Optional, List

class GenericTableModel(QAbstractTableModel):
    def __init__(self, items: Optional[list] = None,
        properties: Optional[List[str]] = None):
        super().__init__()
        self.items = items
        self.properties = properties
        

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)
    
    def columnCount(self, parent= QModelIndex()):
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

class GenericTableView(QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setHorizontalHeader()
    
    def setHorizontalHeader(self):
        header_view = QHeaderView(Qt.Horizontal)
        header_view.setSectionResizeMode(QHeaderView.Stretch)
        super().setHorizontalHeader(header_view)