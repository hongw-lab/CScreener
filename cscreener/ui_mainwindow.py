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
    QDoubleSpinBox, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QSpinBox,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

from .dataview import (CellListTableView1, CellListTableView2)
from .widgets import (DiscreteSlider, MsGraphicsView, TraceAxis)
import cscreener.icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1366, 768)
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
        self.actionExport_MS.setEnabled(False)
        self.actionSave_to_MS = QAction(MainWindow)
        self.actionSave_to_MS.setObjectName(u"actionSave_to_MS")
        self.actionSave_to_MS.setEnabled(False)
        self.actionSave_Lean_MS = QAction(MainWindow)
        self.actionSave_Lean_MS.setObjectName(u"actionSave_Lean_MS")
        self.actionSave_Lean_MS.setEnabled(False)
        self.actionExport_Cell_Label_as_CSV = QAction(MainWindow)
        self.actionExport_Cell_Label_as_CSV.setObjectName(u"actionExport_Cell_Label_as_CSV")
        self.actionExport_Cell_Label_as_CSV.setEnabled(False)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionHotkeys = QAction(MainWindow)
        self.actionHotkeys.setObjectName(u"actionHotkeys")
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
        self.plot_tabs = QTabWidget(self.centralwidget)
        self.plot_tabs.setObjectName(u"plot_tabs")
        self.plot_tabs.setTabPosition(QTabWidget.West)
        self.cell_trace_tab = QWidget()
        self.cell_trace_tab.setObjectName(u"cell_trace_tab")
        self.verticalLayout_4 = QVBoxLayout(self.cell_trace_tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.trace_1_axis = TraceAxis(self.cell_trace_tab)
        self.trace_1_axis.setObjectName(u"trace_1_axis")

        self.verticalLayout_4.addWidget(self.trace_1_axis)

        self.trace_2_axis = TraceAxis(self.cell_trace_tab)
        self.trace_2_axis.setObjectName(u"trace_2_axis")

        self.verticalLayout_4.addWidget(self.trace_2_axis)

        self.plot_tabs.addTab(self.cell_trace_tab, "")
        self.plot_tab = QWidget()
        self.plot_tab.setObjectName(u"plot_tab")
        self.verticalLayout_5 = QVBoxLayout(self.plot_tab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.trace_3_axis = TraceAxis(self.plot_tab)
        self.trace_3_axis.setObjectName(u"trace_3_axis")

        self.verticalLayout_5.addWidget(self.trace_3_axis)

        self.pc_trace_ = TraceAxis(self.plot_tab)
        self.pc_trace_.setObjectName(u"pc_trace_")

        self.verticalLayout_5.addWidget(self.pc_trace_)

        self.plot_tabs.addTab(self.plot_tab, "")

        self.trace_layout.addWidget(self.plot_tabs)


        self.verticalLayout.addLayout(self.trace_layout)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 2)

        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.cell_list1 = CellListTableView1(self.centralwidget)
        self.cell_list1.setObjectName(u"cell_list1")

        self.horizontalLayout_2.addWidget(self.cell_list1)

        self.cell_list2 = CellListTableView2(self.centralwidget)
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
        self.control_panel.setTabPosition(QTabWidget.North)
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
        self.frame_num_spinbox.setMinimum(1)

        self.horizontalLayout.addWidget(self.frame_num_spinbox)

        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.frame_rate_spinbox = QSpinBox(self.tab)
        self.frame_rate_spinbox.setObjectName(u"frame_rate_spinbox")
        self.frame_rate_spinbox.setMinimum(1)
        self.frame_rate_spinbox.setValue(15)

        self.horizontalLayout.addWidget(self.frame_rate_spinbox)

        self.add_to_display_pushbutton = QPushButton(self.tab)
        self.add_to_display_pushbutton.setObjectName(u"add_to_display_pushbutton")

        self.horizontalLayout.addWidget(self.add_to_display_pushbutton)

        self.clear_display_pushbutton = QPushButton(self.tab)
        self.clear_display_pushbutton.setObjectName(u"clear_display_pushbutton")

        self.horizontalLayout.addWidget(self.clear_display_pushbutton)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.contour_label = QLabel(self.tab)
        self.contour_label.setObjectName(u"contour_label")

        self.gridLayout.addWidget(self.contour_label, 1, 1, 1, 1)

        self.showgoodcell_checkbox = QCheckBox(self.tab)
        self.showgoodcell_checkbox.setObjectName(u"showgoodcell_checkbox")
        self.showgoodcell_checkbox.setChecked(True)
        self.showgoodcell_checkbox.setTristate(False)

        self.gridLayout.addWidget(self.showgoodcell_checkbox, 0, 0, 1, 1)

        self.zoom_slider = QSlider(self.tab)
        self.zoom_slider.setObjectName(u"zoom_slider")
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(80)
        self.zoom_slider.setSingleStep(2)
        self.zoom_slider.setSliderPosition(10)
        self.zoom_slider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.zoom_slider, 0, 2, 1, 1)

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

        self.zoom_label = QLabel(self.tab)
        self.zoom_label.setObjectName(u"zoom_label")

        self.gridLayout.addWidget(self.zoom_label, 0, 1, 1, 1)

        self.showbadcell_checkbox = QCheckBox(self.tab)
        self.showbadcell_checkbox.setObjectName(u"showbadcell_checkbox")
        self.showbadcell_checkbox.setChecked(True)

        self.gridLayout.addWidget(self.showbadcell_checkbox, 1, 0, 1, 1)


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
        self.image1_mode_comboBox.setObjectName(u"image1_mode_comboBox")

        self.gridLayout_2.addWidget(self.image1_mode_comboBox, 1, 0, 1, 1)

        self.image2_mode_comboBox = QComboBox(self.tab)
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
        self.Video = QWidget()
        self.Video.setObjectName(u"Video")
        self.gridLayout_3 = QGridLayout(self.Video)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_2 = QLabel(self.Video)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.contrast_spinbox = QDoubleSpinBox(self.Video)
        self.contrast_spinbox.setObjectName(u"contrast_spinbox")
        self.contrast_spinbox.setMaximum(3.000000000000000)
        self.contrast_spinbox.setSingleStep(0.010000000000000)
        self.contrast_spinbox.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.contrast_spinbox, 0, 1, 1, 1)

        self.label_3 = QLabel(self.Video)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout_3.addWidget(self.label_3, 1, 0, 1, 1)

        self.brightness_spinbox = QSpinBox(self.Video)
        self.brightness_spinbox.setObjectName(u"brightness_spinbox")
        self.brightness_spinbox.setMinimum(-255)
        self.brightness_spinbox.setMaximum(255)

        self.gridLayout_3.addWidget(self.brightness_spinbox, 1, 1, 1, 1)

        self.control_panel.addTab(self.Video, "")

        self.verticalLayout_3.addWidget(self.control_panel)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuHep = QMenu(self.menubar)
        self.menuHep.setObjectName(u"menuHep")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHep.menuAction())
        self.menuFile.addAction(self.actionAdd_Video)
        self.menuFile.addAction(self.actionImport_MS)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_MS)
        self.menuFile.addAction(self.actionSave_to_MS)
        self.menuFile.addAction(self.actionSave_Lean_MS)
        self.menuFile.addAction(self.actionExport_Cell_Label_as_CSV)
        self.menuHep.addAction(self.actionAbout)
        self.menuHep.addAction(self.actionHotkeys)

        self.retranslateUi(MainWindow)
        self.frame_slider.valueChanged.connect(self.frame_num_spinbox.setValue)
        self.frame_num_spinbox.valueChanged.connect(self.frame_slider.setValue)

        self.plot_tabs.setCurrentIndex(0)
        self.control_panel.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CellScreener", None))
        self.actionAdd_Video.setText(QCoreApplication.translate("MainWindow", u"Open Video", None))
        self.actionImport_MS.setText(QCoreApplication.translate("MainWindow", u"Import MS", None))
        self.actionExport_MS.setText(QCoreApplication.translate("MainWindow", u"Export MS", None))
#if QT_CONFIG(tooltip)
        self.actionExport_MS.setToolTip(QCoreApplication.translate("MainWindow", u"Save as an full ms file with modified cell label", None))
#endif // QT_CONFIG(tooltip)
        self.actionSave_to_MS.setText(QCoreApplication.translate("MainWindow", u"Save to MS", None))
#if QT_CONFIG(tooltip)
        self.actionSave_to_MS.setToolTip(QCoreApplication.translate("MainWindow", u"Save modified cell labels to the original ms file", None))
#endif // QT_CONFIG(tooltip)
        self.actionSave_Lean_MS.setText(QCoreApplication.translate("MainWindow", u"Save Lean MS", None))
#if QT_CONFIG(tooltip)
        self.actionSave_Lean_MS.setToolTip(QCoreApplication.translate("MainWindow", u"Save the MS with only the essential fields", None))
#endif // QT_CONFIG(tooltip)
        self.actionExport_Cell_Label_as_CSV.setText(QCoreApplication.translate("MainWindow", u"Export Label as CSV", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionHotkeys.setText(QCoreApplication.translate("MainWindow", u"Hotkeys", None))
#if QT_CONFIG(tooltip)
        self.trace_1_axis.setToolTip(QCoreApplication.translate("MainWindow", u"cell 1 trace", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.trace_2_axis.setToolTip(QCoreApplication.translate("MainWindow", u"cell 2 trace", None))
#endif // QT_CONFIG(tooltip)
        self.plot_tabs.setTabText(self.plot_tabs.indexOf(self.cell_trace_tab), QCoreApplication.translate("MainWindow", u"Cell Traces", None))
#if QT_CONFIG(tooltip)
        self.trace_3_axis.setToolTip(QCoreApplication.translate("MainWindow", u"mean trace of all good cells", None))
#endif // QT_CONFIG(tooltip)
        self.plot_tabs.setTabText(self.plot_tabs.indexOf(self.plot_tab), QCoreApplication.translate("MainWindow", u"Mean Trace", None))
        self.currentframe_label.setText(QCoreApplication.translate("MainWindow", u"Frame #", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"FrameRate", None))
        self.add_to_display_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Add to display", None))
        self.clear_display_pushbutton.setText(QCoreApplication.translate("MainWindow", u"Clear display", None))
        self.contour_label.setText(QCoreApplication.translate("MainWindow", u"Contour", None))
        self.showgoodcell_checkbox.setText(QCoreApplication.translate("MainWindow", u"Show good cells", None))
        self.zoom_label.setText(QCoreApplication.translate("MainWindow", u"Zoom", None))
        self.showbadcell_checkbox.setText(QCoreApplication.translate("MainWindow", u"Show bad cells", None))
        self.image1_label.setText(QCoreApplication.translate("MainWindow", u"Image1", None))
        self.image2_label.setText(QCoreApplication.translate("MainWindow", u"Image2", None))
        self.tracemode_label.setText(QCoreApplication.translate("MainWindow", u"Trace", None))
        self.image1_mode_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Raw Video", None))

        self.image2_mode_comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Raw Video", None))

        self.trace_mode_combobox.setItemText(0, QCoreApplication.translate("MainWindow", u"FiltTrace", None))
        self.trace_mode_combobox.setItemText(1, QCoreApplication.translate("MainWindow", u"RawTrace", None))
        self.trace_mode_combobox.setItemText(2, QCoreApplication.translate("MainWindow", u"Spike", None))

        self.control_panel.setTabText(self.control_panel.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Display", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Contrast", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Brightness", None))
        self.control_panel.setTabText(self.control_panel.indexOf(self.Video), QCoreApplication.translate("MainWindow", u"Video", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuHep.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

