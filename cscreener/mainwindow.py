from PySide6.QtWidgets import QMainWindow, QFileDialog, QGraphicsRectItem
from PySide6 import QtCore, QtGui
from ui_mainwindow import Ui_MainWindow
from video import MsVideo
import numpy as np
from data import MS, NeuronGroup, ROIcontourItem, Neuron
import cv2
import pyqtgraph as pg
from widgets import AboutDialog, HotkeyDialog

# from plot import ROIcontourItem
from dataview import CellListTableModel
from state import GuiState
from typing import List
import utility as utt


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(":/icon/app_icon"))
        self.state = GuiState()
        # For easy toggle visibility and other collective changes
        self.goodNeuronGroup = NeuronGroup()
        self.badNeuronGroup = NeuronGroup()
        # GrouphicsItemGroup to display selected cell in list2
        self.selectedContourGroup = []
        self.candidateContourGroup = []
        # Contour of the focused cell in vidframe_1
        self.focus_cell_contour = None  # ROIcontourItem()
        self.companion_cell_contour = None
        # Dict to store frame sticks from 2 axis, takes key 1 and 2
        self.frame_sticks = {}
        self.trace_1 = None
        self.trace_2 = None
        self.trace_3 = None
        # Setup initial states
        self.state["Ms"] = MS()
        self.state["video"] = None
        self.state["frame_rate"] = 15
        self.state["contour_level"] = self.contour_slider.value()
        self.state["zoom_level"] = self.zoom_slider.value()
        # Activated cell in cell_list 1
        self.state["focus_cell"] = None
        # Activated cell in cell_list 2
        self.state["companion_cell"] = None
        self.state["show_good_cell"] = self.showgoodcell_checkbox.isChecked()
        self.state["show_bad_cell"] = self.showbadcell_checkbox.isChecked()
        self.state["current_frame"] = None
        self.state["image1_mode"] = self.image1_mode_comboBox.currentText()
        self.state["image2_mode"] = self.image2_mode_comboBox.currentText()
        self.state["trace_mode"] = self.trace_mode_combobox.currentText()
        # Save the pointer (no duplicate) to displayed unfocused companion cells
        self.state["select_cell_1"] = list()
        # Save the pointer to the selected candidate cells (unfocused)
        self.state["select_cell_2"] = list()
        self.state["file_name"] = str()
        self.state["current_frame"] = self.frame_num_spinbox.value()

        # Connect states to callbacks
        self.state.connect("contour_level", self.update_ROI_level)
        self.state.connect("Ms", [self.update_trace_3, self.plot_ROIs])
        self.state.connect(
            "current_frame", [self.go_to_frame, self.update_frame_sticks]
        )
        self.state.connect("frame_rate", lambda: self.update_gui("trace"))
        self.state.connect(
            "frame_rate",
            [self.update_trace_1, self.update_trace_2, self.update_trace_3],
        )
        self.state.connect(
            "trace_mode",
            [
                self.update_trace_1,
                self.update_trace_2,
                self.update_trace_3,
            ],
        )
        self.state.connect("show_good_cell", self.toggle_good_cell)
        self.state.connect("show_bad_cell", self.toggle_bad_cell)
        self.state.connect(
            "focus_cell", [self.activate_focus_cell, self.update_trace_1]
        )
        self.state.connect(
            "companion_cell", [self.activate_companion_cell, self.update_trace_2]
        )
        self.state.connect("select_cell_1", lambda x: self.update_companion_ROIs(x, 1))
        self.state.connect("select_cell_2", lambda x: self.update_companion_ROIs(x, 2))

        self.state.connect("image1_mode", self.update_image1)
        self.state.connect("image2_mode", self.update_image2)
        self.state.connect("zoom_level", self.zoom_image1)

        # self.state.connect("trace_mode")

        # Connect menu bar actions
        self.actionAdd_Video.triggered.connect(self.open_video)
        self.actionImport_MS.triggered.connect(self.import_ms)
        self.actionExport_MS.triggered.connect(self.save_ms)
        self.actionSave_to_MS.triggered.connect(self.save_hdf_ms)
        self.actionSave_Lean_MS.triggered.connect(self.save_ms_lean)
        self.actionExport_Cell_Label_as_CSV.triggered.connect(self.export_label_csv)
        self.actionAbout.triggered.connect(self.show_about_dialog)
        self.actionHotkeys.triggered.connect(self.show_hotkey_dialog)
        # Connect interactable widgets
        self.frame_slider.valueChanged.connect(self.set_current_frame)
        self.frame_slider.sliderReleased.connect(lambda: self.update_gui(["pix_value"]))
        self.frame_num_spinbox.valueChanged.connect(self.set_current_frame)
        self.frame_num_spinbox.valueChanged.connect(
            lambda: self.update_gui(["pix_value"])
            if self.frame_num_spinbox.hasFocus()
            else False
        )
        self.frame_rate_spinbox.valueChanged.connect(self.set_frame_rate)
        self.add_to_display_pushbutton.clicked.connect(self.add_to_display)
        self.clear_display_pushbutton.clicked.connect(self.clear_selected_cell)
        self.image1_mode_comboBox.currentTextChanged.connect(self.set_image1_mode)
        self.image2_mode_comboBox.currentTextChanged.connect(self.set_image2_mode)
        self.trace_mode_combobox.currentTextChanged.connect(self.set_trace_mode)
        self.zoom_slider.valueChanged.connect(self.set_zoom_level)
        self.contour_slider.valueChangedDiscrete.connect(self.set_contour_level)
        self.showgoodcell_checkbox.stateChanged.connect(self.set_show_good_cell)
        self.showbadcell_checkbox.stateChanged.connect(self.set_show_bad_cell)
        self.trace_mode_combobox.currentTextChanged.connect(self.set_trace_mode)
        self.plot_tabs.currentChanged.connect(lambda: self.update_gui(["trace"]))
        self.vid_frame_item_1 = pg.ImageItem(image=np.zeros((500, 500)))
        self.vid_frame1.addItem(self.vid_frame_item_1)
        self.vid_frame_item_2 = pg.ImageItem(iamge=np.zeros((500, 500)))
        self.vid_frame2.addItem(self.vid_frame_item_2)

        self.vid_frame1.show()
        self.vid_frame2.show()

        self.vid_frame1.current_zoom_level = self.state["zoom_level"]
        self.vid_frame1.zoom(self.state["zoom_level"])
        self.zoom_box = QGraphicsRectItem(self.vid_frame1.viewRect())
        self.zoom_box.setPen(QtGui.QPen(QtGui.QColor(200, 255, 200), 2))
        self.zoom_box.setVisible(False)
        self.vid_frame2.addItem(self.zoom_box)

    # State setting functions for the widgets
    def set_contour_level(self, value):
        self.state["contour_level"] = value

    def set_current_frame(self, value):
        # Both slider and spinbox start from 1
        self.state["current_frame"] = int(value - 1)

    def set_frame_rate(self, value):
        self.state["frame_rate"] = value

    def set_image1_mode(self, new_mode):
        self.state["image1_mode"] = new_mode

    def set_image2_mode(self, new_mode):
        self.state["image2_mode"] = new_mode

    def set_trace_mode(self, new_mode):
        self.state["trace_mode"] = new_mode
        try:
            self.cell_list1.model().update_after_activation()
            self.cell_list2.model().update_after_activation()
            self.update_gui(["cell_list"])
        except Exception:
            pass

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
        if event.key() == 71:  # G, toggle focus cell
            try:
                self.toggle_focus_cell()
                return True
            except Exception:
                return False
        if event.key() == 72:  # H, toggle companion cell
            try:
                self.toggle_companion_cell()
                return True
            except:
                return False
        if event.key() == 73:  # I, move up cell 1
            return utt._cell_list_move_(self, 1, "up")
        if event.key() == 79:  # O, move up cell 2
            return utt._cell_list_move_(self, 2, "up")
        if event.key() == 75:  # K, move down cell 1
            return utt._cell_list_move_(self, 1, "down")
        if event.key() == 76:  # L, move down cell 2
            return utt._cell_list_move_(self, 2, "down")
        if event.key() == 65:  # A, sort by column 0(ID)
            return utt._sort_by_column_(self, 0)
        if event.key() == 83:  # S, sort by column 2(Corr)
            return utt._sort_by_column_(self, 2)
        if event.key() == 68:  # D, sort by column 3(Dist)
            return utt._sort_by_column_(self, 3)
        if event.key() == 70:  # F, sort by dFF
            return utt._sort_by_column_(self, 4)
        if event.key() == 66:  # B, jump to max intensity frame of cell 1
            return utt._jump_to_max_(self, 1)
        if event.key() == 78:  # N, jump to max intensity frame of cell 2
            return utt._jump_to_max_(self, 2)
        if event.key() == 16777234:  # Left arrow, move to previous frame
            return utt._arrow_func_(self, "left")
        if event.key() == 16777236:  # Right arrow, move to next frame
            return utt._arrow_func_(self, "right")
        return super().eventFilter(obj, event)

    # Actual worker functions

    def open_video(self):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        video_path, _ = fileDialog.getOpenFileName(
            self,
            caption="Open MS video",
            filter="Video files (*.avi)",
        )
        if not video_path:
            return False
        msvideo = MsVideo(video_path, self)

        self.state["video"] = msvideo
        self.state["current_frame"] = 0

        self.vid_frame1.setRange(self.vid_frame_item_1.boundingRect(), padding=0)
        self.vid_frame2.setRange(self.vid_frame_item_2.boundingRect(), padding=0)

        self.frame_slider.setMaximum(self.state["video"].get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_slider.setMinimum(1)

        self.frame_num_spinbox.setMaximum(
            self.state["video"].get(cv2.CAP_PROP_FRAME_COUNT)
        )
        self.frame_num_spinbox.setMinimum(1)

        # Use a different thread to calculate max intensity projection
        msvideo.threading_get(msvideo.calculate_maxproj_frame, "max_proj")

    def import_ms(self):
        self.statusbar.showMessage("Reading mat file...")
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        ms_path, _ = QFileDialog.getOpenFileName(
            self, caption="Import ms.mat", filter="mat file (*.mat)"
        )
        if not ms_path:
            return False
        self.state["file_name"] = ms_path
        # Loaded raw MS, for easy modify and save
        self.ms_file, file_type, hdf_File = utt.load_ms_file(ms_path)
        self.statusbar.clearMessage()
        if file_type:
            self.statusbar.showMessage("Successfully loaded ms!", 5000)
        else:
            self.statusbar.showMessage("Failed to load ms!", 8000)
            return False
        self.state["Ms"] = MS(self.ms_file, file_type, mainwindow=self)

        if hdf_File is not None:
            hdf_File.close()
        # Enable saving options for different mat file type
        if self.state["Ms"].get_file_type() == 1:
            self.actionExport_MS.setEnabled(True)
            self.actionSave_to_MS.setEnabled(False)
        elif self.state["Ms"].get_file_type() == 2:
            self.actionSave_to_MS.setEnabled(True)
            self.actionExport_MS.setEnabled(False)
        self.actionExport_Cell_Label_as_CSV.setEnabled(True)
        self.actionSave_Lean_MS.setEnabled(True)

        self.vid_frame1.setRange(self.vid_frame1.viewRect(), padding=0)
        self.vid_frame2.setRange(self.vid_frame2.viewRect(), padding=0)
        self.neuron_table_model_1 = CellListTableModel(
            items=self.state["Ms"].NeuronList,
            properties=["ID", "Label", "Corr", "Dist", "dFF"],
            state=self.state,
        )
        self.neuron_table_model_2 = CellListTableModel(
            items=self.state["Ms"].NeuronList,
            properties=["ID", "Label", "Corr", "Dist", "dFF"],
            state=self.state,
        )
        self.cell_list1.setstate(self.state)
        self.cell_list2.setstate(self.state)

        self.cell_list1.setModel(self.neuron_table_model_1)
        self.cell_list2.setModel(self.neuron_table_model_2)
        self.cell_list2.setSortingEnabled(True)
        self.update_gui(["cell_list", "pix_value", "trace"])

    def save_ms(self):
        self.statusbar.showMessage("Saving, wait...", 0)
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save MS", "ms.mat", "mat Files (*.mat)"
        )
        if not filename:
            return False
        # Update cell labels before saving
        self.state["Ms"].update_labels()
        # Save <v7.3 mat file
        self.ms_file.cell_label = self.state["Ms"].get_labels()
        self.ms_file.cell_label = np.reshape(
            self.ms_file.cell_label, (self.ms_file.cell_label.size, 1)
        )
        mat_to_save = {"ms": self.ms_file}
        success = utt.save_ms_file(filename, mat_to_save)

        self.statusbar.clearMessage()
        if success:
            self.statusbar.showMessage("Saving to %s complete!" % filename, 5000)
            return True
        else:
            self.statusbar.showMessage("Saving failed!", 5000)
            return False

    def save_hdf_ms(self):
        self.state["Ms"].update_labels()
        # Save v7.3 HDF file (direct write on original file)
        cell_label = self.state["Ms"].get_labels()
        cell_label = np.reshape(cell_label, (cell_label.size, 1))
        success = utt.write_hdf_field(self.state["file_name"], "cell_label", cell_label)
        self.statusbar.clearMessage()
        if success:
            self.statusbar.showMessage(
                "Saving to original mat file %s complete!" % self.state["file_name"],
                5000,
            )
            return True
        else:
            self.statusbar.showMessage("Saving failed!", 5000)
            return False

    def save_ms_lean(self):
        self.statusbar.showMessage("Saving, wait...", 0)
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save MS", "ms.mat", "mat Files (*.mat)"
        )
        if not filename:
            return False
        # Update cell labels before saving
        self.state["Ms"].update_labels()
        # Save <v7.3 mat file
        ms_file = self.state["Ms"].get_lean_ms()
        mat_to_save = {"ms": ms_file}
        success = utt.save_ms_file(filename, mat_to_save)

        self.statusbar.clearMessage()
        if success:
            self.statusbar.showMessage("Saving to %s complete!" % filename, 5000)
            return True
        else:
            self.statusbar.showMessage("Saving failed!", 5000)
            return False

    def export_label_csv(self):
        self.statusbar.showMessage("Saving, wait...", 0)
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save to csv", "cell_label.csv", "csv Files (*.csv)"
        )
        if not filename:
            return False
        self.state["Ms"].update_labels()
        cell_label = self.state["Ms"].get_labels()
        try:
            np.savetxt(filename, cell_label, fmt="%d", delimiter=",")
            success = True
        except Exception:
            success = False
        if success:
            self.statusbar.showMessage("Exporting to %s complete!" % filename, 5000)
            return True
        else:
            self.statusbar.showMessage("Exporting failed!", 5000)
            return False

    def plot_ROIs(self):
        # Called when Ms is first loaded
        MS = self.state["Ms"]
        MS._threading_(MS.generate_ROIs)

    def go_to_frame(self, frameN):
        video = self.state["video"]
        frame = video.get_frame(frameN)
        if self.state["image1_mode"] == "Raw Video":
            self.vid_frame_item_1.setImage(frame)
            self.vid_frame_item_1.updateImage()
        if self.state["image2_mode"] == "Raw Video":
            self.vid_frame_item_2.setImage(frame)
            self.vid_frame_item_2.updateImage()
        self.update_gui(topic=["frame"])

    def zoom_image1(self, value):
        self.vid_frame1.zoom(zoom_level=value, center=self.focus_cell_contour)
        self.zoom_box.setRect(self.vid_frame1.viewRect())
        if value <= 10:
            self.zoom_box.setVisible(False)
        else:
            self.zoom_box.setVisible(True)

    def toggle_good_cell(self, visible):
        self.goodNeuronGroup.setVisible(visible)

    def toggle_bad_cell(self, visible):
        self.badNeuronGroup.setVisible(visible)

    def update_companion_ROIs(self, selected_cells, group_num):
        if group_num == 1:
            target_group = self.selectedContourGroup
        elif group_num == 2:
            target_group = self.candidateContourGroup
        else:
            return False

        # Display all the selected cells in vid_frame 2
        if not target_group:
            for i, cell in enumerate(selected_cells):
                color_str = "green" if cell.is_good() else "red"
                target_group.append(
                    ROIcontourItem(
                        data=cell.ROI,
                        contour_center=cell.center,
                        level=self.state["contour_level"],
                        pen=color_str,
                    )
                )
                self.vid_frame1.addItem(target_group[i])
            return None
        if len(selected_cells) > len(target_group):
            # More plotting cells than already exist
            for i, item in enumerate(target_group):
                item.setData(selected_cells[i].ROI)
                if selected_cells[i].is_good():
                    item.setPen("green")
                else:
                    item.setPen("red")

            for k in range(i + 1, len(selected_cells)):
                cell = selected_cells[k]
                color_str = "green" if cell.is_good() else "red"
                target_group.append(
                    ROIcontourItem(
                        data=cell.ROI,
                        contour_center=cell.center,
                        level=self.state["contour_level"],
                        pen=color_str,
                    )
                )
                self.vid_frame1.addItem(target_group[k])

        elif selected_cells:
            # More existing than incoming plots when incoming is not empty
            for i, cell in enumerate(selected_cells):
                target_group[i].setData(cell.ROI)
                if cell.is_good():
                    target_group[i].setPen("green")
                else:
                    target_group[i].setPen("red")
            for k in range(len(target_group) - 1, i, -1):
                item_to_rmv = target_group.pop(k)
                item_to_rmv.deleteLater()
        else:
            # Incoming is empty, clear all the contour objects
            for k in range(len(target_group) - 1, -1, -1):
                item_to_rmv = target_group.pop(k)
                item_to_rmv.deleteLater()

        return True

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
        self.cell_list1.update_after_toggle()
        self.cell_list2.update_after_toggle()
        self.update_trace_3(self.state["focus_cell"])
        self.update_gui(["cell_list", "focus_contours", "good_bad_contour"])

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
        self.cell_list1.update_after_toggle()
        self.cell_list2.update_after_toggle()
        self.update_trace_3(self.state["companion_cell"])
        self.update_gui(["cell_list", "focus_contours", "good_bad_contour"])

    def update_frame_sticks(self, cur_frame):
        if len(self.frame_sticks.keys()) < 1:
            # Create stick items
            self.frame_sticks[1] = pg.InfiniteLine(
                pos=np.ones(2) * cur_frame / self.state["frame_rate"], angle=90, pen="y"
            )
            self.frame_sticks[2] = pg.InfiniteLine(
                pos=np.ones(2) * cur_frame / self.state["frame_rate"], angle=90, pen="y"
            )
            self.frame_sticks[3] = pg.InfiniteLine(
                pos=np.ones(2) * cur_frame / self.state["frame_rate"], angle=90, pen="y"
            )
            self.trace_1_axis.addItem(self.frame_sticks[1])
            self.trace_2_axis.addItem(self.frame_sticks[2])
            self.trace_3_axis.addItem(self.frame_sticks[3])
        else:
            for key in self.frame_sticks.keys():
                frame_stick = self.frame_sticks[key]
                frame_stick.setValue(cur_frame / self.state["frame_rate"])

    def update_image1(self, image_mode):
        if image_mode == "Max Projection":
            try:
                self.vid_frame_item_1.setImage(self.state["video"].max_proj)
                return True
            except Exception:
                return False
        else:
            try:
                frameN = self.state["current_frame"]
                frame = self.state["video"].get_frame(frameN)
                self.vid_frame_item_1.setImage(frame)
                self.vid_frame_item_1.updateImage()
                return True
            except Exception:
                return False

    def update_image2(self, image_mode):
        if image_mode == "Max Projection":
            try:
                self.vid_frame_item_2.setImage(self.state["video"].max_proj)
                return True
            except Exception:
                return False
        else:
            try:
                frameN = self.state["current_frame"]
                frame = self.state["video"].get_frame(frameN)
                self.vid_frame_item_2.setImage(frame)
                self.vid_frame_item_2.updateImage()
                return True
            except Exception:
                return False

    def update_gui(self, topic: List[str] = None):
        if "frame" in topic:
            frameN = self.state["current_frame"]
            self.frame_num_spinbox.setValue(frameN + 1)
            self.frame_slider.setValue(frameN + 1)
        if "trace" in topic:
            self.trace_1_axis.setXRange(
                0, 1 / self.state["frame_rate"] * (self.state["Ms"].num_frame() - 1)
            )
            self.trace_2_axis.setXRange(
                0, 1 / self.state["frame_rate"] * (self.state["Ms"].num_frame() - 1)
            )
            self.trace_3_axis.setXRange(
                0, 1 / self.state["frame_rate"] * (self.state["Ms"].num_frame() - 1)
            )
            self.trace_1_axis.enableAutoRange(pg.ViewBox.YAxis)
            self.trace_2_axis.enableAutoRange(pg.ViewBox.YAxis)
            self.trace_3_axis.enableAutoRange(pg.ViewBox.YAxis)
        if "cell_list" in topic:
            try:
                self.cell_list1.repaint_table()
                self.cell_list2.repaint_table()
            except:
                return False
        if "scroll_to_focus" in topic:
            try:
                self.cell_list1.scroll_to_activated()
            except:
                return False

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
        if "pix_value" in topic:
            try:
                self.cell_list1.update_pixval()
                self.cell_list2.update_pixval()
            except:
                return False

        if "good_bad_contour" in topic:
            self.badNeuronGroup.setVisible(self.state["show_bad_cell"])
            self.goodNeuronGroup.setVisible(self.state["show_good_cell"])

    def activate_focus_cell(self, focus_cell):
        # Called after state["focus_cell"] is changed
        # 1. Create focus cell contour in image 1, center onto it
        # 2. Update info displayed in cell_list 1 and 2
        if self.focus_cell_contour is not None:
            self.focus_cell_contour.setData(focus_cell.ROI, self.state["contour_level"])
        else:
            self.focus_cell_contour = ROIcontourItem(
                data=focus_cell.ROI,
                level=self.state["contour_level"],
                contour_center=focus_cell.center,
                neuron=focus_cell,
            )
            self.vid_frame1.addItem(self.focus_cell_contour)

        if focus_cell.is_good():
            self.focus_cell_contour.setPen(color=(180, 240, 180), width=2)
        else:
            self.focus_cell_contour.setPen(color=(240, 180, 180), width=2)
        # Center on focus cell
        self.vid_frame1.set_center(self.focus_cell_contour)
        # Adjust the zoom box
        self.zoom_box.setRect(self.vid_frame1.viewRect())
        # Update info in cell tables
        self.state["focus_cell"].visits += 1
        self.cell_list2.update_after_activation()
        self.cell_list1.update_after_activation()
        self.cell_list2.model().reset_sort_order()
        self.update_gui(["cell_list", "scroll_to_focus"])

    def activate_companion_cell(self, companion_cell):
        if self.companion_cell_contour is not None:
            self.companion_cell_contour.setData(
                companion_cell.ROI, self.state["contour_level"]
            )
        else:
            self.companion_cell_contour = ROIcontourItem(
                data=companion_cell.ROI,
                level=self.state["contour_level"],
                contour_center=companion_cell.center,
                neuron=companion_cell,
            )
            self.vid_frame1.addItem(self.companion_cell_contour)
        self.update_gui(["cell_list"])

        if companion_cell.is_good():
            self.companion_cell_contour.setPen(color=(180, 240, 180), width=2)
        else:
            self.companion_cell_contour.setPen(color=(240, 180, 180), width=2)
        
        self.state["companion_cell"].visits += 1
        self.cell_list2.update_after_activation()
        self.cell_list1.update_after_activation()
        self.update_gui(["cell_list"])

    def update_trace_1(self):
        focus_cell = self.state["focus_cell"]
        trace_mode = self.state["trace_mode"]
        if not focus_cell:
            return False
        if self.trace_1 is None:
            self.trace_1 = pg.PlotDataItem(
                x=np.arange(0, self.state["Ms"].num_frame()) / self.state["frame_rate"],
                y=getattr(focus_cell, trace_mode),
            )
            self.trace_1_axis.addItem(self.trace_1)
        else:
            self.trace_1.setData(
                x=np.arange(0, self.state["Ms"].num_frame()) / self.state["frame_rate"],
                y=getattr(focus_cell, trace_mode),
            )
            return True

    def update_trace_2(self):
        companion_cell = self.state["companion_cell"]
        trace_mode = self.state["trace_mode"]
        if not companion_cell:
            return False
        if self.trace_2 is None:
            self.trace_2 = pg.PlotDataItem(
                x=np.arange(0, self.state["Ms"].num_frame()) / self.state["frame_rate"],
                y=getattr(companion_cell, trace_mode),
            )
            self.trace_2_axis.addItem(self.trace_2)
        else:
            self.trace_2.setData(
                x=np.arange(0, self.state["Ms"].num_frame()) / self.state["frame_rate"],
                y=getattr(companion_cell, trace_mode),
            )

    def update_trace_3(self, toggled_cell: Neuron = None):
        if not isinstance(toggled_cell, Neuron):
            toggled_cell = None
        trace_mode = self.state["trace_mode"]
        if self.trace_3 is None:
            mean_trace = self.state["Ms"].get_mean_trace(trace_mode)
            self.trace_3 = pg.PlotDataItem(
                x=np.arange(0, mean_trace.size) / self.state["frame_rate"], y=mean_trace
            )
            self.trace_3_axis.addItem(self.trace_3)
            self.update_gui(["trace"])
        else:
            self.state["Ms"].update_mean_trace(toggled_cell)
            mean_trace = self.state["Ms"].get_mean_trace(trace_mode)
            self.trace_3.setData(
                x=np.arange(0, mean_trace.size) / self.state["frame_rate"], y=mean_trace
            )

    def update_ROI_level(self, slider_value):
        MS = self.state["Ms"]
        try:
            for neuron in MS.NeuronList:
                neuron.ROI_Item.setLevel(slider_value)
        except Exception:
            pass
        if self.selectedContourGroup:
            for selected_contour in self.selectedContourGroup:
                selected_contour.setLevel(slider_value)
        if self.candidateContourGroup:
            for candidate_contour in self.candidateContourGroup:
                candidate_contour.setLevel(slider_value)
        try:
            self.focus_cell_contour.setLevel(slider_value)
        except Exception:
            pass
        try:
            self.companion_cell_contour.setLevel(slider_value)
        except Exception:
            pass

    def add_to_display(self):
        try:
            # Add pointers in select_cell_2 into select_cell_1 (set)
            self.state["select_cell_1"] = (
                self.state["select_cell_1"] + self.state["select_cell_2"]
            )
            temp_set = set(self.state["select_cell_1"])
            self.state["select_cell_1"] = list(temp_set)
            self.state["select_cell_2"] = list()
            self.cell_list2.selection_added_display()
            return True
        except:
            return False

    def clear_selected_cell(self):
        # Only clear ones already added and not the currently selected candidates
        self.state["select_cell_1"] = list()
        self.cell_list2.display_cleared()

    def stop_threads(self):
        try:
            self.state["video"].stop_worker()
            self.state["video"].clear_threads()
            self.state["Ms"].stop_worker()
            self.state["Ms"].clear_threads()
            return True
        except Exception:
            return False

    def show_about_dialog(self):
        about_dialog = AboutDialog()
        about_dialog.exec()
    
    def show_hotkey_dialog(self):
        hotkey_dialog = HotkeyDialog()
        hotkey_dialog.exec()
