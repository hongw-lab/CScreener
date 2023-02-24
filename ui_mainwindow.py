# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main-window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QCheckBox, QComboBox,
    QGraphicsView, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

from widgets import (DiscreteSlider, MsGraphicsView)
from dataview import GenericTableView

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1202, 729)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.actionAdd_Video = QAction(MainWindow)
        self.actionAdd_Video.setObjectName(u"actionAdd_Video")
        self.actionImport_MS = QAction(MainWindow)
        self.actionImport_MS.setObjectName(u"actionImport_MS")
        self.actionExport_MS = QAction(MainWindow)
        self.actionExport_MS.setObjectName(u"actionExport_MS")
        self.actionExport_Binary_List = QAction(MainWindow)
        self.actionExport_Binary_List.setObjectName(u"actionExport_Binary_List")
        self.actionSort_Cell = QAction(MainWindow)
        self.actionSort_Cell.setObjectName(u"actionSort_Cell")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.video_layout = QHBoxLayout()
        self.video_layout.setObjectName(u"video_layout")
        self.vid_frame1 = MsGraphicsView(self.centralwidget)
        self.vid_frame1.setObjectName(u"vid_frame1")
        self.vid_frame1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.video_layout.addWidget(self.vid_frame1)

        self.vid_frame2 = MsGraphicsView(self.centralwidget)
        self.vid_frame2.setObjectName(u"vid_frame2")
        self.vid_frame2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.video_layout.addWidget(self.vid_frame2)

        self.video_layout.setStretch(0, 1)
        self.video_layout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.video_layout)

        self.frame_slider = QSlider(self.centralwidget)
        self.frame_slider.setObjectName(u"frame_slider")
        self.frame_slider.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.frame_slider)

        self.trace_layout = QVBoxLayout()
        self.trace_layout.setObjectName(u"trace_layout")
        self.trace1 = QGraphicsView(self.centralwidget)
        self.trace1.setObjectName(u"trace1")

        self.trace_layout.addWidget(self.trace1)

        self.trace2 = QGraphicsView(self.centralwidget)
        self.trace2.setObjectName(u"trace2")

        self.trace_layout.addWidget(self.trace2)

        self.trace_layout.setStretch(0, 1)
        self.trace_layout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.trace_layout)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 2)

        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cell_list1 = GenericTableView(self.centralwidget)
        self.cell_list1.setObjectName(u"cell_list1")

        self.horizontalLayout_2.addWidget(self.cell_list1)

        self.cell_list2 = GenericTableView(self.centralwidget)
        self.cell_list2.setObjectName(u"cell_list2")

        self.horizontalLayout_2.addWidget(self.cell_list2)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.control_panel = QTabWidget(self.centralwidget)
        self.control_panel.setObjectName(u"control_panel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.control_panel.sizePolicy().hasHeightForWidth())
        self.control_panel.setSizePolicy(sizePolicy1)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_3 = QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.currentframe_label = QLabel(self.tab)
        self.currentframe_label.setObjectName(u"currentframe_label")

        self.horizontalLayout.addWidget(self.currentframe_label)

        self.frame_num_spinbox = QSpinBox(self.tab)
        self.frame_num_spinbox.setObjectName(u"frame_num_spinbox")

        self.horizontalLayout.addWidget(self.frame_num_spinbox)

        self.sort_cell_pushbutton = QPushButton(self.tab)
        self.sort_cell_pushbutton.setObjectName(u"sort_cell_pushbutton")

        self.horizontalLayout.addWidget(self.sort_cell_pushbutton)

        self.sortmethod_comboBox = QComboBox(self.tab)
        self.sortmethod_comboBox.addItem("")
        self.sortmethod_comboBox.addItem("")
        self.sortmethod_comboBox.addItem("")
        self.sortmethod_comboBox.setObjectName(u"sortmethod_comboBox")

        self.horizontalLayout.addWidget(self.sortmethod_comboBox)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.zoom_label = QLabel(self.tab)
        self.zoom_label.setObjectName(u"zoom_label")

        self.gridLayout.addWidget(self.zoom_label, 0, 1, 1, 1)

        self.showgoodcell_checkbox = QCheckBox(self.tab)
        self.showgoodcell_checkbox.setObjectName(u"showgoodcell_checkbox")
        self.showgoodcell_checkbox.setTristate(False)

        self.gridLayout.addWidget(self.showgoodcell_checkbox, 0, 0, 1, 1)

        self.zoom_slider = QSlider(self.tab)
        self.zoom_slider.setObjectName(u"zoom_slider")
        self.zoom_slider.setMinimum(1)
        self.zoom_slider.setMaximum(8)
        self.zoom_slider.setSingleStep(1)
        self.zoom_slider.setSliderPosition(1)
        self.zoom_slider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.zoom_slider, 0, 2, 1, 1)

        self.contour_label = QLabel(self.tab)
        self.contour_label.setObjectName(u"contour_label")

        self.gridLayout.addWidget(self.contour_label, 1, 1, 1, 1)

        self.showbadcell_checkbox = QCheckBox(self.tab)
        self.showbadcell_checkbox.setObjectName(u"showbadcell_checkbox")

        self.gridLayout.addWidget(self.showbadcell_checkbox, 1, 0, 1, 1)

        self.contour_slider = DiscreteSlider(self.tab)
        self.contour_slider.setObjectName(u"contour_slider")
        self.contour_slider.setMinimum(1)
        self.contour_slider.setMaximum(10)
        self.contour_slider.setSingleStep(1)
        self.contour_slider.setPageStep(2)
        self.contour_slider.setValue(7)
        self.contour_slider.setSliderPosition(7)
        self.contour_slider.setTracking(False)
        self.contour_slider.setOrientation(Qt.Horizontal)
        self.contour_slider.setTickPosition(QSlider.TicksAbove)
        self.contour_slider.setTickInterval(1)

        self.gridLayout.addWidget(self.contour_slider, 1, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.image1_label = QLabel(self.tab)
        self.image1_label.setObjectName(u"image1_label")

        self.gridLayout_2.addWidget(self.image1_label, 0, 0, 1, 1)

        self.image2_label = QLabel(self.tab)
        self.image2_label.setObjectName(u"image2_label")

        self.gridLayout_2.addWidget(self.image2_label, 0, 1, 1, 1)

        self.tracemode_label = QLabel(self.tab)
        self.tracemode_label.setObjectName(u"tracemode_label")

        self.gridLayout_2.addWidget(self.tracemode_label, 0, 2, 1, 1)

        self.image1_mode_comboBox = QComboBox(self.tab)
        self.image1_mode_comboBox.addItem("")
        self.image1_mode_comboBox.addItem("")
        self.image1_mode_comboBox.setObjectName(u"image1_mode_comboBox")

        self.gridLayout_2.addWidget(self.image1_mode_comboBox, 1, 0, 1, 1)

        self.image2_mode_comboBox = QComboBox(self.tab)
        self.image2_mode_comboBox.addItem("")
        self.image2_mode_comboBox.addItem("")
        self.image2_mode_comboBox.setObjectName(u"image2_mode_comboBox")

        self.gridLayout_2.addWidget(self.image2_mode_comboBox, 1, 1, 1, 1)

        self.trace_mode_combobox = QComboBox(self.tab)
        self.trace_mode_combobox.addItem("")
        self.trace_mode_combobox.addItem("")
        self.trace_mode_combobox.addItem("")
        self.trace_mode_combobox.setObjectName(u"trace_mode_combobox")

        self.gridLayout_2.addWidget(self.trace_mode_combobox, 1, 2, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.control_panel.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.control_panel.addTab(self.tab_2, "")

        self.verticalLayout_3.addWidget(self.control_panel)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1202, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuAction = QMenu(self.menubar)
        self.menuAction.setObjectName(u"menuAction")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAction.menuAction())
        self.menuFile.addAction(self.actionAdd_Video)
        self.menuFile.addAction(self.actionImport_MS)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_MS)
        self.menuFile.addAction(self.actionExport_Binary_List)
        self.menuAction.addAction(self.actionSort_Cell)

        self.retranslateUi(MainWindow)

        self.control_panel.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CellScreener", None))
        self.actionAdd_Video.setText(QCoreApplication.translate("MainWindow", u"Open Video", None))
        self.actionImport_MS.setText(QCoreApplication.translate("MainWindow", u"Import MS", None))
        self.actionExport_MS.setText(QCoreApplication.translate("MainWindow", u"Export MS", None))
        self.actionExport_Binary_List.setText(QCoreApplication.translate("MainWindow", u"Export Binary List", None))
        self.actionSort_Cell.setText(QCoreApplication.translate("MainWindow", u"Sort Cell", None))
        self.currentframe_label.setText(QCoreApplication.translate("MainWindow", u"Current Frame", None))
        self.sort_cell_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Sort cell by", None))
        self.sortmethod_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Distance", None))
        self.sortmethod_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Correlation", None))
        self.sortmethod_comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"Pix Value", None))

        self.zoom_label.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.showgoodcell_checkbox.setText(QCoreApplication.translate("MainWindow", u"Show good cells", None))
        self.contour_label.setText(QCoreApplication.translate("MainWindow", u"Contour", None))
        self.showbadcell_checkbox.setText(QCoreApplication.translate("MainWindow", u"Show bad cells", None))
        self.image1_label.setText(QCoreApplication.translate("MainWindow", u"Image1", None))
        self.image2_label.setText(QCoreApplication.translate("MainWindow", u"Image2", None))
        self.tracemode_label.setText(QCoreApplication.translate("MainWindow", u"Trace", None))
        self.image1_mode_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Raw Video", None))
        self.image1_mode_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Max Projection", None))

        self.image2_mode_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Raw Video", None))
        self.image2_mode_comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Max Projection", None))

        self.trace_mode_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"Raw Trace", None))
        self.trace_mode_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"Filtered Trace", None))
        self.trace_mode_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"Spikes", None))

        self.control_panel.setTabText(self.control_panel.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Image", None))
        self.control_panel.setTabText(self.control_panel.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tab 2", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuAction.setTitle(QCoreApplication.translate("MainWindow", u"Action", None))
    # retranslateUi

