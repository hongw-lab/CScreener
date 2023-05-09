# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main-window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractScrollArea,
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QStatusBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from .dataview import CellListTableView1, CellListTableView2
from .widgets import DiscreteSlider, MsGraphicsView, TraceAxis
import cscreener.icons_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1366, 768)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QSize(0, 0))
        MainWindow.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.actionAdd_Video = QAction(MainWindow)
        self.actionAdd_Video.setObjectName("actionAdd_Video")
        self.actionImport_MS = QAction(MainWindow)
        self.actionImport_MS.setObjectName("actionImport_MS")
        self.actionExport_MS = QAction(MainWindow)
        self.actionExport_MS.setObjectName("actionExport_MS")
        self.actionExport_MS.setEnabled(False)
        self.actionSave_to_MS = QAction(MainWindow)
        self.actionSave_to_MS.setObjectName("actionSave_to_MS")
        self.actionSave_to_MS.setEnabled(False)
        self.actionSave_Lean_MS = QAction(MainWindow)
        self.actionSave_Lean_MS.setObjectName("actionSave_Lean_MS")
        self.actionSave_Lean_MS.setEnabled(False)
        self.actionExport_Cell_Label_as_CSV = QAction(MainWindow)
        self.actionExport_Cell_Label_as_CSV.setObjectName(
            "actionExport_Cell_Label_as_CSV"
        )
        self.actionExport_Cell_Label_as_CSV.setEnabled(False)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHotkeys = QAction(MainWindow)
        self.actionHotkeys.setObjectName("actionHotkeys")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.video_layout = QHBoxLayout()
        self.video_layout.setObjectName("video_layout")
        self.vid_frame1 = MsGraphicsView(self.centralwidget)
        self.vid_frame1.setObjectName("vid_frame1")
        self.vid_frame1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame1.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame1.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.video_layout.addWidget(self.vid_frame1)

        self.vid_frame2 = MsGraphicsView(self.centralwidget)
        self.vid_frame2.setObjectName("vid_frame2")
        self.vid_frame2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.vid_frame2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.video_layout.addWidget(self.vid_frame2)

        self.video_layout.setStretch(0, 1)
        self.video_layout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.video_layout)

        self.frame_slider = QSlider(self.centralwidget)
        self.frame_slider.setObjectName("frame_slider")
        self.frame_slider.setOrientation(Qt.Horizontal)

        self.verticalLayout.addWidget(self.frame_slider)

        self.trace_layout = QVBoxLayout()
        self.trace_layout.setObjectName("trace_layout")
        self.plot_tabs = QTabWidget(self.centralwidget)
        self.plot_tabs.setObjectName("plot_tabs")
        self.plot_tabs.setTabPosition(QTabWidget.West)
        self.cell_trace_tab = QWidget()
        self.cell_trace_tab.setObjectName("cell_trace_tab")
        self.verticalLayout_4 = QVBoxLayout(self.cell_trace_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.trace_1_axis = TraceAxis(self.cell_trace_tab)
        self.trace_1_axis.setObjectName("trace_1_axis")

        self.verticalLayout_4.addWidget(self.trace_1_axis)

        self.trace_2_axis = TraceAxis(self.cell_trace_tab)
        self.trace_2_axis.setObjectName("trace_2_axis")

        self.verticalLayout_4.addWidget(self.trace_2_axis)

        self.plot_tabs.addTab(self.cell_trace_tab, "")
        self.plot_tab = QWidget()
        self.plot_tab.setObjectName("plot_tab")
        self.verticalLayout_5 = QVBoxLayout(self.plot_tab)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.trace_3_axis = TraceAxis(self.plot_tab)
        self.trace_3_axis.setObjectName("trace_3_axis")

        self.verticalLayout_5.addWidget(self.trace_3_axis)

        self.pc_trace_ = TraceAxis(self.plot_tab)
        self.pc_trace_.setObjectName("pc_trace_")

        self.verticalLayout_5.addWidget(self.pc_trace_)

        self.plot_tabs.addTab(self.plot_tab, "")

        self.trace_layout.addWidget(self.plot_tabs)

        self.verticalLayout.addLayout(self.trace_layout)

        self.verticalLayout.setStretch(0, 4)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 2)

        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cell_list1 = CellListTableView1(self.centralwidget)
        self.cell_list1.setObjectName("cell_list1")

        self.horizontalLayout_2.addWidget(self.cell_list1)

        self.cell_list2 = CellListTableView2(self.centralwidget)
        self.cell_list2.setObjectName("cell_list2")

        self.horizontalLayout_2.addWidget(self.cell_list2)

        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.control_panel = QTabWidget(self.centralwidget)
        self.control_panel.setObjectName("control_panel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.control_panel.sizePolicy().hasHeightForWidth()
        )
        self.control_panel.setSizePolicy(sizePolicy1)
        self.control_panel.setTabPosition(QTabWidget.North)
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.currentframe_label = QLabel(self.tab)
        self.currentframe_label.setObjectName("currentframe_label")

        self.horizontalLayout.addWidget(self.currentframe_label)

        self.frame_num_spinbox = QSpinBox(self.tab)
        self.frame_num_spinbox.setObjectName("frame_num_spinbox")
        self.frame_num_spinbox.setMinimum(1)

        self.horizontalLayout.addWidget(self.frame_num_spinbox)

        self.label = QLabel(self.tab)
        self.label.setObjectName("label")

        self.horizontalLayout.addWidget(self.label)

        self.frame_rate_spinbox = QSpinBox(self.tab)
        self.frame_rate_spinbox.setObjectName("frame_rate_spinbox")
        self.frame_rate_spinbox.setMinimum(1)
        self.frame_rate_spinbox.setValue(15)

        self.horizontalLayout.addWidget(self.frame_rate_spinbox)

        self.add_to_display_pushbutton = QPushButton(self.tab)
        self.add_to_display_pushbutton.setObjectName("add_to_display_pushbutton")

        self.horizontalLayout.addWidget(self.add_to_display_pushbutton)

        self.clear_display_pushbutton = QPushButton(self.tab)
        self.clear_display_pushbutton.setObjectName("clear_display_pushbutton")

        self.horizontalLayout.addWidget(self.clear_display_pushbutton)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.contour_label = QLabel(self.tab)
        self.contour_label.setObjectName("contour_label")

        self.gridLayout.addWidget(self.contour_label, 1, 1, 1, 1)

        self.showgoodcell_checkbox = QCheckBox(self.tab)
        self.showgoodcell_checkbox.setObjectName("showgoodcell_checkbox")
        self.showgoodcell_checkbox.setChecked(True)
        self.showgoodcell_checkbox.setTristate(False)

        self.gridLayout.addWidget(self.showgoodcell_checkbox, 0, 0, 1, 1)

        self.zoom_slider = QSlider(self.tab)
        self.zoom_slider.setObjectName("zoom_slider")
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(80)
        self.zoom_slider.setSingleStep(2)
        self.zoom_slider.setSliderPosition(10)
        self.zoom_slider.setOrientation(Qt.Horizontal)

        self.gridLayout.addWidget(self.zoom_slider, 0, 2, 1, 1)

        self.contour_slider = DiscreteSlider(self.tab)
        self.contour_slider.setObjectName("contour_slider")
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
        self.zoom_label.setObjectName("zoom_label")

        self.gridLayout.addWidget(self.zoom_label, 0, 1, 1, 1)

        self.showbadcell_checkbox = QCheckBox(self.tab)
        self.showbadcell_checkbox.setObjectName("showbadcell_checkbox")
        self.showbadcell_checkbox.setChecked(True)

        self.gridLayout.addWidget(self.showbadcell_checkbox, 1, 0, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.image1_label = QLabel(self.tab)
        self.image1_label.setObjectName("image1_label")

        self.gridLayout_2.addWidget(self.image1_label, 0, 0, 1, 1)

        self.image2_label = QLabel(self.tab)
        self.image2_label.setObjectName("image2_label")

        self.gridLayout_2.addWidget(self.image2_label, 0, 1, 1, 1)

        self.tracemode_label = QLabel(self.tab)
        self.tracemode_label.setObjectName("tracemode_label")

        self.gridLayout_2.addWidget(self.tracemode_label, 0, 2, 1, 1)

        self.image1_mode_comboBox = QComboBox(self.tab)
        self.image1_mode_comboBox.addItem("")
        self.image1_mode_comboBox.setObjectName("image1_mode_comboBox")

        self.gridLayout_2.addWidget(self.image1_mode_comboBox, 1, 0, 1, 1)

        self.image2_mode_comboBox = QComboBox(self.tab)
        self.image2_mode_comboBox.addItem("")
        self.image2_mode_comboBox.setObjectName("image2_mode_comboBox")

        self.gridLayout_2.addWidget(self.image2_mode_comboBox, 1, 1, 1, 1)

        self.trace_mode_combobox = QComboBox(self.tab)
        self.trace_mode_combobox.addItem("")
        self.trace_mode_combobox.addItem("")
        self.trace_mode_combobox.addItem("")
        self.trace_mode_combobox.setObjectName("trace_mode_combobox")

        self.gridLayout_2.addWidget(self.trace_mode_combobox, 1, 2, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_2)

        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.control_panel.addTab(self.tab, "")
        self.Video = QWidget()
        self.Video.setObjectName("Video")
        self.gridLayout_3 = QGridLayout(self.Video)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QLabel(self.Video)
        self.label_2.setObjectName("label_2")

        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)

        self.contrast_spinbox = QDoubleSpinBox(self.Video)
        self.contrast_spinbox.setObjectName("contrast_spinbox")
        self.contrast_spinbox.setMaximum(10.000000000000000)
        self.contrast_spinbox.setSingleStep(0.100000000000000)
        self.contrast_spinbox.setValue(1.000000000000000)

        self.gridLayout_3.addWidget(self.contrast_spinbox, 0, 1, 1, 1)

        self.label_3 = QLabel(self.Video)
        self.label_3.setObjectName("label_3")

        self.gridLayout_3.addWidget(self.label_3, 0, 2, 1, 1)

        self.brightness_spinbox = QSpinBox(self.Video)
        self.brightness_spinbox.setObjectName("brightness_spinbox")
        self.brightness_spinbox.setMinimum(-255)
        self.brightness_spinbox.setMaximum(255)

        self.gridLayout_3.addWidget(self.brightness_spinbox, 0, 3, 1, 1)

        self.label_4 = QLabel(self.Video)
        self.label_4.setObjectName("label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)

        self.maxproj_contrast_spinbox = QDoubleSpinBox(self.Video)
        self.maxproj_contrast_spinbox.setObjectName("maxproj_contrast_spinbox")
        self.maxproj_contrast_spinbox.setMinimum(1.000000000000000)
        self.maxproj_contrast_spinbox.setMaximum(10.000000000000000)
        self.maxproj_contrast_spinbox.setSingleStep(0.100000000000000)

        self.gridLayout_3.addWidget(self.maxproj_contrast_spinbox, 1, 1, 1, 1)

        self.label_5 = QLabel(self.Video)
        self.label_5.setObjectName("label_5")

        self.gridLayout_3.addWidget(self.label_5, 1, 2, 1, 1)

        self.maxproj_brightness_spinbox = QSpinBox(self.Video)
        self.maxproj_brightness_spinbox.setObjectName("maxproj_brightness_spinbox")
        self.maxproj_brightness_spinbox.setMinimum(-255)
        self.maxproj_brightness_spinbox.setMaximum(255)

        self.gridLayout_3.addWidget(self.maxproj_brightness_spinbox, 1, 3, 1, 1)

        self.control_panel.addTab(self.Video, "")

        self.verticalLayout_3.addWidget(self.control_panel)

        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout_4.setStretch(0, 2)
        self.horizontalLayout_4.setStretch(1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1366, 22))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHep = QMenu(self.menubar)
        self.menuHep.setObjectName("menuHep")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
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
        self.control_panel.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "CellScreener", None)
        )
        self.actionAdd_Video.setText(
            QCoreApplication.translate("MainWindow", "Open Video", None)
        )
        self.actionImport_MS.setText(
            QCoreApplication.translate("MainWindow", "Import MS", None)
        )
        self.actionExport_MS.setText(
            QCoreApplication.translate("MainWindow", "Export MS", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionExport_MS.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Save as an full ms file with modified cell label", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSave_to_MS.setText(
            QCoreApplication.translate("MainWindow", "Save to MS", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSave_to_MS.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Save modified cell labels to the original ms file", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionSave_Lean_MS.setText(
            QCoreApplication.translate("MainWindow", "Save Lean MS", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSave_Lean_MS.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "Save the MS with only the essential fields", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.actionExport_Cell_Label_as_CSV.setText(
            QCoreApplication.translate("MainWindow", "Export Label as CSV", None)
        )
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.actionHotkeys.setText(
            QCoreApplication.translate("MainWindow", "Hotkeys", None)
        )
        # if QT_CONFIG(tooltip)
        self.trace_1_axis.setToolTip(
            QCoreApplication.translate("MainWindow", "cell 1 trace", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.trace_2_axis.setToolTip(
            QCoreApplication.translate("MainWindow", "cell 2 trace", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.plot_tabs.setTabText(
            self.plot_tabs.indexOf(self.cell_trace_tab),
            QCoreApplication.translate("MainWindow", "Cell Traces", None),
        )
        # if QT_CONFIG(tooltip)
        self.trace_3_axis.setToolTip(
            QCoreApplication.translate(
                "MainWindow", "mean trace of all good cells", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.plot_tabs.setTabText(
            self.plot_tabs.indexOf(self.plot_tab),
            QCoreApplication.translate("MainWindow", "Mean Trace", None),
        )
        self.currentframe_label.setText(
            QCoreApplication.translate("MainWindow", "Frame #", None)
        )
        self.label.setText(QCoreApplication.translate("MainWindow", "FrameRate", None))
        self.add_to_display_pushbutton.setText(
            QCoreApplication.translate("MainWindow", "Add to display", None)
        )
        self.clear_display_pushbutton.setText(
            QCoreApplication.translate("MainWindow", "Clear display", None)
        )
        self.contour_label.setText(
            QCoreApplication.translate("MainWindow", "Contour", None)
        )
        self.showgoodcell_checkbox.setText(
            QCoreApplication.translate("MainWindow", "Show good cells", None)
        )
        self.zoom_label.setText(QCoreApplication.translate("MainWindow", "Zoom", None))
        self.showbadcell_checkbox.setText(
            QCoreApplication.translate("MainWindow", "Show bad cells", None)
        )
        self.image1_label.setText(
            QCoreApplication.translate("MainWindow", "Image1", None)
        )
        self.image2_label.setText(
            QCoreApplication.translate("MainWindow", "Image2", None)
        )
        self.tracemode_label.setText(
            QCoreApplication.translate("MainWindow", "Trace", None)
        )
        self.image1_mode_comboBox.setItemText(
            0, QCoreApplication.translate("MainWindow", "Raw Video", None)
        )

        self.image2_mode_comboBox.setItemText(
            0, QCoreApplication.translate("MainWindow", "Raw Video", None)
        )

        self.trace_mode_combobox.setItemText(
            0, QCoreApplication.translate("MainWindow", "FiltTrace", None)
        )
        self.trace_mode_combobox.setItemText(
            1, QCoreApplication.translate("MainWindow", "RawTrace", None)
        )
        self.trace_mode_combobox.setItemText(
            2, QCoreApplication.translate("MainWindow", "Spike", None)
        )

        self.control_panel.setTabText(
            self.control_panel.indexOf(self.tab),
            QCoreApplication.translate("MainWindow", "Display", None),
        )
        self.label_2.setText(
            QCoreApplication.translate("MainWindow", "Video Contrast", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("MainWindow", "Video Brightness", None)
        )
        self.label_4.setText(
            QCoreApplication.translate("MainWindow", "MaxProj contrast", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("MainWindow", "MaxProj brightness", None)
        )
        self.control_panel.setTabText(
            self.control_panel.indexOf(self.Video),
            QCoreApplication.translate("MainWindow", "Video", None),
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuHep.setTitle(QCoreApplication.translate("MainWindow", "Help", None))

    # retranslateUi
