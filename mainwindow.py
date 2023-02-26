from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsItemGroup,
)
from PySide6.QtGui import QImage, QPixmap, QBrush
from PySide6 import QtCore
from ui_mainwindow import Ui_MainWindow
from video import MsVideo
import numpy as np
from data import MS
import cv2
import pyqtgraph as pg
from scipy.io import loadmat
from plot import ROIcontourItem
from dataview import CellListTableModel
from state import GuiState
import copy


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.state = GuiState()
        # For easy toggle visibility and other collective changes
        self.goodContourGroup = QGraphicsItemGroup()
        self.badContourGroup = QGraphicsItemGroup()
        self.selectedContourGroup = QGraphicsItemGroup()
        self.focus_cell_contour = ROIcontourItem()

        # Setup initial states
        self.state["Ms"] = MS()
        self.state["video"] = None
        self.state["contour_level"] = self.contour_slider.value()
        self.state["zoom_level"] = self.zoom_slider.value()
        self.state["focus_cell"] = None
        self.state["show_good_cell"] = self.showgoodcell_checkbox.isChecked()
        self.state["show_bad_cell"] = self.showbadcell_checkbox.isChecked()
        self.state["current_frame"] = None
        self.state["image1_mode"] = self.image1_mode_comboBox.currentText
        self.state["image2_mode"] = self.image2_mode_comboBox.currentText
        self.state["trace_mode"] = self.trace_mode_combobox.currentText
        self.state["select_cell_1"] = None
        self.state["select_cell_2"] = None
        self.state["file_name"] = None
        self.state["current_frame"] = self.frame_num_spinbox.value()

        # Connect states to callbacks
        self.state.connect("contour_level", self.update_ROI_level)
        self.state.connect("Ms", self.plot_ROIs)
        self.state.connect("current_frame", self.go_to_frame)
        self.state.connect("show_good_cell", self.toggle_good_cell)
        self.state.connect("show_bad_cell", self.toggle_bad_cell)
        self.state.connect("focus_cell", self.focus_on_cell)
        self.state.connect("select_cell_1", self.update_ROI_image1)
        self.state.connect("select_cell_2", self.update_ROI_image2)
        self.state.connect("image1_mode", self.update_image1)
        self.state.connect("image2_mode", self.update_image2)
        self.state.connect("zoom_level", self.zoom_image1)

        # Connect menu bar actions
        self.actionAdd_Video.triggered.connect(self.open_video)
        self.actionImport_MS.triggered.connect(self.import_ms)
        self.actionSort_Cell.triggered.connect(self.sort_cell)

        # Connect interactable widgets
        self.frame_slider.valueChanged.connect(self.set_current_frame)
        self.frame_num_spinbox.valueChanged.connect(self.set_current_frame)
        self.sort_cell_pushbutton.clicked.connect(self.sort_cell)
        self.image1_mode_comboBox.currentTextChanged.connect(self.set_image1_mode)
        self.image2_mode_comboBox.currentTextChanged.connect(self.set_image2_mode)
        self.trace_mode_combobox.currentTextChanged.connect(self.set_trace_mode)
        self.zoom_slider.valueChanged.connect(self.set_zoom_level)
        self.contour_slider.valueChangedDiscrete.connect(self.set_contour_level)
        self.showgoodcell_checkbox.stateChanged.connect(self.set_show_good_cell)
        self.showbadcell_checkbox.stateChanged.connect(self.set_show_bad_cell)

        self.vid_frame_item_1 = pg.ImageItem(image=np.zeros((800, 800)))
        self.vid_frame1.addItem(self.vid_frame_item_1)
        self.vid_frame_item_2 = pg.ImageItem(iamge=np.zeros((500, 500)))
        self.vid_frame2.addItem(self.vid_frame_item_2)

        self.vid_frame1.addItem(self.focus_cell_contour)

        self.vid_frame1.show()
        self.vid_frame2.show()

        self.vid_frame1.current_zoom_level = self.state["zoom_level"]
        self.vid_frame1.zoom(self.state["zoom_level"])

    # State setting functions
    def set_contour_level(self, value):
        self.state["contour_level"] = value

    def set_current_frame(self, value):
        # Both slider and spinbox start from 1
        self.state["current_frame"] = int(value - 1)

    def set_image1_mode(self, new_mode):
        self.state["image1_mode"] = new_mode

    def set_image2_mode(self, new_mode):
        self.state["image2_mode"] = new_mode

    def set_trace_mode(self, new_mode):
        self.state["trace_mode"] = new_mode

    def set_zoom_level(self, new_level):
        self.state["zoom_level"] = new_level

    def set_show_good_cell(self, new_state):
        self.state["show_good_cell"] = new_state > 0

    def set_show_bad_cell(self, new_state):
        self.state["show_bad_cell"] = new_state > 0

    # Actual worker functions

    def open_video(self):
        selected_fileName = QFileDialog.getOpenFileName(self, caption="open video")
        video_path = selected_fileName[0]
        self.state["video"] = MsVideo(video_path)
        self.go_to_frame(0)
        self.vid_frame1.setRange(self.vid_frame_item_1.boundingRect(), padding=0)
        self.vid_frame2.setRange(self.vid_frame_item_2.boundingRect(), padding=0)

        self.frame_slider.setMaximum(self.state["video"].get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_slider.setMinimum(1)

        self.frame_num_spinbox.setMaximum(
            self.state["video"].get(cv2.CAP_PROP_FRAME_COUNT)
        )
        self.frame_slider.setMinimum(1)

    def import_ms(self):
        selected_fileName = QFileDialog.getOpenFileName(self, caption="open ms.mat")
        ms_path = selected_fileName[0]
        self.state["file_name"] = ms_path
        # Loaded raw MS, for easy modify and save
        self.ms_file = self.load_ms_file(ms_path)
        self.state["Ms"] = MS(self.ms_file)

        self.vid_frame1.setRange(self.vid_frame1.viewRect(), padding=0)
        self.vid_frame2.setRange(self.vid_frame2.viewRect(), padding=0)
        self.neuron_table_model = CellListTableModel(
            items=self.state["Ms"].NeuronList, properties=["ID", "Label"]
        )
        self.cell_list1.setstate(self.state)
        self.cell_list2.setstate(self.state)
        self.cell_list1.setModel(self.neuron_table_model)
        self.cell_list2.setModel(self.neuron_table_model)

    def plot_ROIs(self):
        MS = self.state["Ms"]
        for i in range(MS.NumNeurons):
            neuron = MS.NeuronList[i]
            if neuron.is_good():
                neuron.ROI_Item = ROIcontourItem(
                    data=neuron.ROI,
                    contour_center=neuron.center,
                    level=self.contour_slider.value(),
                    pen="y",
                )
                self.goodContourGroup.addToGroup(neuron.ROI_Item)
            else:
                neuron.ROI_Item = ROIcontourItem(
                    data=neuron.ROI,
                    contour_center=neuron.center,
                    level=self.contour_slider.value(),
                    pen="r",
                )
                self.badContourGroup.addToGroup(neuron.ROI_Item)

            # print(roi_item.pen.color().getRgb())
            # print(roi_item.pen.color().getRgbF())

        self.vid_frame2.addItem(self.goodContourGroup)
        self.vid_frame2.addItem(self.badContourGroup)

    def go_to_frame(self, frameN):
        video = self.state["video"]
        frame = video.get_frame(frameN)
        self.frame_num_spinbox.setValue(frameN + 1)
        self.frame_slider.setValue(frameN + 1)
        self.vid_frame_item_1.setImage(frame)
        self.vid_frame_item_2.setImage(frame)
        self.vid_frame_item_1.update()
        self.vid_frame_item_2.update()

    def zoom_image1(self, value):
        self.vid_frame1.zoom(new_zoom_level=value, center=self.focus_cell_contour)

    # def numpy_to_qimage(self, array):
    #     height, width, _ = array.shape
    #     bytes_per_line = 3 * width
    #     qimage = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
    #     return qimage

    def load_ms_file(self, ms_path):
        ms_file = loadmat(ms_path, struct_as_record=False)["ms"]
        ms_file = ms_file[0, 0]
        return ms_file

    def sort_cell(self):
        return

    def toggle_good_cell(self, visible):
        self.goodContourGroup.setVisible(visible)

    def toggle_bad_cell(self, visible):
        self.badContourGroup.setVisible(visible)

    def update_ROI_image1(self, selected_cells):
        return

    def update_ROI_image2(self, selected_cells):
        return

    def update_image1(self):
        return

    def update_image2(self):
        return

    def focus_on_cell(self, focus_cell):
        # If focus cell not yet created, create by deep copy
        self.focus_cell_contour.setData(focus_cell.ROI, self.state["contour_level"])
        if focus_cell.is_good():
            self.focus_cell_contour.setPen("green")
        else:
            self.focus_cell_contour.setPen("red")
        # Center on focus cell
        self.vid_frame1.scale(1, 1, self.focus_cell_contour)

    def update_ROI_level(self, slider_value):
        MS = self.state["Ms"]
        for neuron in MS.NeuronList:
            neuron.ROI_Item.setLevel(slider_value)
        self.focus_cell_contour.setLevel(slider_value)

    def update_Traces(self):
        return

    def update_ROIs(self):
        return
