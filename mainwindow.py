from PySide6.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QGraphicsPixmapItem,
    QGraphicsItem,
    QGraphicsItemGroup,
    QGraphicsScene,
)
from PySide6.QtGui import QImage, QPixmap, QBrush
from PySide6 import QtCore
from ui_mainwindow import Ui_MainWindow
from video import MsVideo
import numpy as np
from data import MS, NeuronGroup
import cv2
import pyqtgraph as pg
from scipy.io import loadmat
from plot import ROIcontourItem
from dataview import CellListTableModel
from state import GuiState
from typing import List
from copy import copy


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.state = GuiState()
        # For easy toggle visibility and other collective changes
        self.goodNeuronGroup = NeuronGroup()
        self.badNeuronGroup = NeuronGroup()
        # GrouphicsItemGroup to display selected cell in list2
        self.selectedContourGroup = []
        # Contour of the focused cell in vidframe_1
        self.focus_cell_contour = None  # ROIcontourItem()
        self.companion_cell_contour = None
        # Dict to store frame sticks from 2 axis, takes key 1 and 2
        self.frame_sticks = {}
        self.trace_1 = None
        self.trace_2 = None

        # Setup initial states
        self.state["Ms"] = MS()
        self.state["video"] = None
        self.state["contour_level"] = self.contour_slider.value()
        self.state["zoom_level"] = self.zoom_slider.value()
        # Activated cell in cell_list 1
        self.state["focus_cell"] = None
        # Activated cell in cell_list 2
        self.state["companion_cell"] = None
        self.state["show_good_cell"] = self.showgoodcell_checkbox.isChecked()
        self.state["show_bad_cell"] = self.showbadcell_checkbox.isChecked()
        self.state["current_frame"] = None
        self.state["image1_mode"] = self.image1_mode_comboBox.currentText
        self.state["image2_mode"] = self.image2_mode_comboBox.currentText
        self.state["trace_mode"] = self.trace_mode_combobox.currentText
        # self.state["select_cell_1"] = None
        self.state["select_cell_2"] = None
        self.state["file_name"] = None
        self.state["current_frame"] = self.frame_num_spinbox.value()

        # Connect states to callbacks
        self.state.connect("contour_level", self.update_ROI_level)
        self.state.connect("Ms", self.plot_ROIs)
        self.state.connect(
            "current_frame", [self.go_to_frame, self.update_frame_sticks]
        )
        self.state.connect("show_good_cell", self.toggle_good_cell)
        self.state.connect("show_bad_cell", self.toggle_bad_cell)
        self.state.connect("focus_cell", [self.focus_on_cell, self.update_trace_1])
        self.state.connect("companion_cell", [self.companion_cell, self.update_trace_2])
        # self.state.connect("select_cell_1", self.update_ROI_image1)
        self.state.connect("select_cell_2", self.update_companion_ROIs)
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
        self.vid_frame2.scene().selectionChanged.connect(self.select_cell)
        self.vid_frame1.show()
        self.vid_frame2.show()

        self.vid_frame1.current_zoom_level = self.state["zoom_level"]
        self.vid_frame1.zoom(self.state["zoom_level"])

    # State setting functions for the widgets
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

    # Event filter for keypress function
    def eventFilter(self, obj, event):
        if event.type() != QtCore.QEvent.KeyPress:
            return super().eventFilter(obj, event)
        # Key functions
        if event.key() == 71:  # G,g pressed, toggle focus cell
            self.toggle_focus_cell()
            return True
        if event.key() == 72:  # H,h pressed, toggle companion cell
            self.toggle_companion_cell()
            return True
        return super().eventFilter(obj, event)

    # Actual worker functions

    def open_video(self):
        selected_fileName = QFileDialog.getOpenFileName(
            self, caption="Open MS video", filter="Video files (*.avi)"
        )
        video_path = selected_fileName[0]
        self.state["video"] = MsVideo(video_path)
        self.update_gui(["trace"])
        self.state["current_frame"] = 0

        self.vid_frame1.setRange(self.vid_frame_item_1.boundingRect(), padding=0)
        self.vid_frame2.setRange(self.vid_frame_item_2.boundingRect(), padding=0)

        self.frame_slider.setMaximum(self.state["video"].get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_slider.setMinimum(1)

        self.frame_num_spinbox.setMaximum(
            self.state["video"].get(cv2.CAP_PROP_FRAME_COUNT)
        )
        self.frame_slider.setMinimum(1)

    def import_ms(self):
        selected_fileName = QFileDialog.getOpenFileName(
            self, caption="Import ms.mat", filter="mat file (*.mat)"
        )
        ms_path = selected_fileName[0]
        self.state["file_name"] = ms_path
        # Loaded raw MS, for easy modify and save
        self.ms_file = self.load_ms_file(ms_path)
        self.state["Ms"] = MS(self.ms_file)

        self.vid_frame1.setRange(self.vid_frame1.viewRect(), padding=0)
        self.vid_frame2.setRange(self.vid_frame2.viewRect(), padding=0)
        self.neuron_table_model_1 = CellListTableModel(
            items=self.state["Ms"].NeuronList, properties=["ID", "Label"]
        )
        self.neuron_table_model_2 = CellListTableModel(
            items=self.state["Ms"].NeuronList, properties=["ID", "Label"]
        )
        self.cell_list1.setstate(self.state)
        self.cell_list2.setstate(self.state)
        self.cell_list1.setModel(self.neuron_table_model_1)
        self.cell_list2.setModel(self.neuron_table_model_2)

    def plot_ROIs(self):
        MS = self.state["Ms"]
        for i in range(MS.NumNeurons):
            neuron = MS.NeuronList[i]
            if neuron.is_good():
                neuron.ROI_Item = ROIcontourItem(
                    data=neuron.ROI,
                    contour_center=neuron.center,
                    level=self.state["contour_level"],
                    pen="y",
                    activatable=True,
                    neuron=neuron,
                    state=self.state,
                )
                self.goodNeuronGroup.add_neuron(neuron)
            else:
                neuron.ROI_Item = ROIcontourItem(
                    data=neuron.ROI,
                    contour_center=neuron.center,
                    level=self.state["contour_level"],
                    pen="r",
                    activatable=True,
                    neuron=neuron,
                    state=self.state,
                )
                self.badNeuronGroup.add_neuron(neuron)
            # Make all individual contours in vid_frame2 selectable
            neuron.ROI_Item.setFlag(QGraphicsItem.ItemIsSelectable)
            self.vid_frame2.addItem(neuron.ROI_Item)
            # print(roi_item.pen.color().getRgb())
            # print(roi_item.pen.color().getRgbF())

    def go_to_frame(self, frameN):
        video = self.state["video"]
        frame = video.get_frame(frameN)
        self.vid_frame_item_1.setImage(frame)
        self.vid_frame_item_2.setImage(frame)
        self.vid_frame_item_1.update()
        self.vid_frame_item_2.update()
        self.update_gui(topic=["frame"])

    def zoom_image1(self, value):
        self.vid_frame1.zoom(zoom_level=value, center=self.focus_cell_contour)

    def load_ms_file(self, ms_path):
        ms_file = loadmat(ms_path, struct_as_record=False)["ms"]
        ms_file = ms_file[0, 0]
        return ms_file

    def sort_cell(self):
        return

    def toggle_good_cell(self, visible):
        self.goodNeuronGroup.setVisible(visible)

    def toggle_bad_cell(self, visible):
        self.badNeuronGroup.setVisible(visible)

    def update_companion_ROIs(self, selected_cells):
        # Display all the selected cells in vid_frame 2
        if not self.selectedContourGroup:
            for i, cell in enumerate(selected_cells):
                color_str = "green" if cell.is_good() else "red"
                self.selectedContourGroup.append(
                    ROIcontourItem(
                        data=cell.ROI,
                        contour_center=cell.center,
                        level=self.state["contour_level"],
                        pen=color_str,
                    )
                )
                self.vid_frame1.addItem(self.selectedContourGroup[i])
            return None
        if len(selected_cells) > len(self.selectedContourGroup):
            # More plotting cells than already exist
            for i, item in enumerate(self.selectedContourGroup):
                item.setData(selected_cells[i].ROI)
                if selected_cells[i].is_good():
                    item.setPen("green")
                else:
                    item.setPen("red")

            for k in range(i + 1, len(selected_cells)):
                cell = selected_cells[k]
                color_str = "green" if cell.is_good() else "red"
                self.selectedContourGroup.append(
                    ROIcontourItem(
                        data=cell.ROI,
                        contour_center=cell.center,
                        level=self.state["contour_level"],
                        pen=color_str,
                    )
                )
                self.vid_frame1.addItem(self.selectedContourGroup[k])

        else:
            # More existing than incoming plots
            for i, cell in enumerate(selected_cells):
                self.selectedContourGroup[i].setData(cell.ROI)
                if cell.is_good():
                    self.selectedContourGroup[i].setPen("green")
                else:
                    self.selectedContourGroup[i].setPen("red")
            for k in range(len(self.selectedContourGroup) - 1, i, -1):
                item_to_rmv = self.selectedContourGroup.pop(k)
                item_to_rmv.deleteLater()

        return None

    def toggle_focus_cell(self):
        if self.state["focus_cell"].Label == "Good":
            self.state["focus_cell"].Label = 0
            # Move from good cell group to bad cell group
            self.badNeuronGroup.add_neuron(
                self.goodNeuronGroup.pop_neuron(self.state["focus_cell"])
            )

        else:
            self.state["focus_cell"].Label = 1
            self.goodNeuronGroup.add_neuron(
                self.badNeuronGroup.pop_neuron(self.state["focus_cell"])
            )

        self.update_gui(["cell_list", "focus_contours"])

    def toggle_companion_cell(self):
        if self.state["companion_cell"].Label == "Good":
            self.state["companion_cell"].Label = 0
            self.badNeuronGroup.add_neuron(
                self.goodNeuronGroup.pop_neuron(self.state["companion_cell"])
            )
        else:
            self.state["companion_cell"].Label = 1
            self.goodNeuronGroup.add_neuron(
                self.badNeuronGroup.pop_neuron(self.state["companion_cell"])
            )
        self.update_gui(["cell_list", "focus_contours"])

    def update_frame_sticks(self, cur_frame):
        if len(self.frame_sticks.keys()) < 1:
            # Create stick items
            self.frame_sticks[1] = pg.InfiniteLine(
                pos=np.ones(2) * cur_frame / 15, angle=90, pen="y"
            )
            self.frame_sticks[2] = pg.InfiniteLine(
                pos=np.ones(2) * cur_frame / 15, angle=90, pen="y"
            )
            self.trace_1_axis.addItem(self.frame_sticks[1])
            self.trace_2_axis.addItem(self.frame_sticks[2])
        else:
            for key in self.frame_sticks.keys():
                frame_stick = self.frame_sticks[key]
                frame_stick.setValue(cur_frame / 15)

    def update_image1(self):
        return

    def update_image2(self):
        return

    def update_gui(self, topic: List[str] = None):
        if "frame" in topic:
            frameN = self.state["current_frame"]
            self.frame_num_spinbox.setValue(frameN + 1)
            self.frame_slider.setValue(frameN + 1)
        if "trace" in topic:
            self.trace_1_axis.setXRange(
                0, 1 / 15 * (self.state["video"].num_frame() - 1)
            )
            self.trace_2_axis.setXRange(
                0, 1 / 15 * (self.state["video"].num_frame() - 1)
            )
            self.trace_1_axis.enableAutoRange(pg.ViewBox.YAxis)
            self.trace_2_axis.enableAutoRange(pg.ViewBox.YAxis)
        if "cell_list" in topic:
            self.cell_list1.update_focus_entry()
            self.cell_list1.update_focus_entry(
                self.cell_list1.model().get_item_index(self.state["companion_cell"])
            )
            self.cell_list2.update_focus_entry()
            self.cell_list2.update_focus_entry(
                self.cell_list2.model().get_item_index(self.state["focus_cell"])
            )
        if "focus_contours" in topic:
            focus_cell = self.state["focus_cell"]
            if focus_cell:
                self.focus_cell_contour.setData(
                    focus_cell.ROI, self.state["contour_level"]
                )
                self.focus_cell_contour.setPen(
                    color=(180, 240, 180), width=2
                ) if focus_cell._Label else self.focus_cell_contour.setPen(
                    color=(240, 180, 180), width=2
                )
                focus_cell.ROI_Item.setPen(
                    "yellow"
                ) if focus_cell._Label else focus_cell.ROI_Item.setPen("red")

            companion_cell = self.state["companion_cell"]
            if companion_cell:
                self.companion_cell_contour.setData(
                    companion_cell.ROI, self.state["contour_level"]
                )
                self.companion_cell_contour.setPen(
                    color=(180, 240, 180), width=2
                ) if companion_cell._Label else self.companion_cell_contour.setPen(
                    (240, 180, 180), width=2
                )
                companion_cell.ROI_Item.setPen(
                    "yellow"
                ) if companion_cell._Label else companion_cell.ROI_Item.setPen("red")

    def focus_on_cell(self, focus_cell):
        # If focus cell not yet created, create by deep copy
        if self.focus_cell_contour is not None:
            self.focus_cell_contour.setData(focus_cell.ROI, self.state["contour_level"])
        else:
            self.focus_cell_contour = ROIcontourItem(
                data=focus_cell.ROI,
                level=self.state["contour_level"],
                contour_center=focus_cell.center,
            )
            self.vid_frame1.addItem(self.focus_cell_contour)

        if focus_cell.is_good():
            self.focus_cell_contour.setPen(color=(180, 240, 180), width=2)
        else:
            self.focus_cell_contour.setPen(color=(240, 180, 180), width=2)
        # Center on focus cell
        self.vid_frame1.set_center(self.focus_cell_contour)

    def companion_cell(self, companion_cell):
        if self.companion_cell_contour is not None:
            self.companion_cell_contour.setData(
                companion_cell.ROI, self.state["contour_level"]
            )
        else:
            self.companion_cell_contour = ROIcontourItem(
                data=companion_cell.ROI,
                level=self.state["contour_level"],
                contour_center=companion_cell.center,
            )
            self.vid_frame1.addItem(self.companion_cell_contour)

        if companion_cell.is_good():
            self.companion_cell_contour.setPen(color=(180, 240, 180), width=2)
        else:
            self.companion_cell_contour.setPen(color=(240, 180, 180), width=2)

    def update_trace_1(self, focus_cell):
        if self.trace_1 is None:
            self.trace_1 = pg.PlotDataItem(
                x=np.arange(0, focus_cell.FiltTrace.size) / 15,
                y=focus_cell.FiltTrace,
            )
            self.trace_1_axis.addItem(self.trace_1)
        else:
            self.trace_1.setData(
                x=np.arange(0, focus_cell.FiltTrace.size) / 15,
                y=focus_cell.FiltTrace,
            )

    def update_trace_2(self, companion_cell):
        if self.trace_2 is None:
            self.trace_2 = pg.PlotDataItem(
                x=np.arange(0, companion_cell.FiltTrace.size) / 15,
                y=companion_cell.FiltTrace,
            )
            self.trace_2_axis.addItem(self.trace_2)
        else:
            self.trace_2.setData(
                x=np.arange(0, companion_cell.FiltTrace.size) / 15,
                y=companion_cell.FiltTrace,
            )

    def update_ROI_level(self, slider_value):
        MS = self.state["Ms"]
        for neuron in MS.NeuronList:
            neuron.ROI_Item.setLevel(slider_value)
        for selected_contour in self.selectedContourGroup:
            selected_contour.setLevel(slider_value)

        self.update_gui(["focus_contours"])

    def update_Traces(self):
        return

    def update_ROIs(self):
        return
