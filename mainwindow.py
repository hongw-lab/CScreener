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
from Video import MsVideo
import numpy as np
from Ms import MS
import cv2
import pyqtgraph as pg
from scipy.io import loadmat
from Plot import ROIcontourItem
from dataview import GenericTableModel

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Connect menu bar actions
        self.actionAdd_Video.triggered.connect(self.open_video)
        self.actionImport_MS.triggered.connect(self.import_ms)
        self.actionSort_Cell.triggered.connect(self.sort_cell)
        # Connect interactable widgets
        self.frame_slider.valueChanged.connect(self.go_to_frame)
        self.sort_cell_pushbutton.clicked.connect(self.sort_cell)
        self.image1_mode_comboBox.currentTextChanged.connect(self.update_Image1)
        self.image2_mode_comboBox.currentTextChanged.connect(self.update_Image2)
        self.trace_mode_combobox.currentTextChanged.connect(self.update_Traces)
        self.zoom_slider.valueChanged.connect(self.update_Image1)
        self.contour_slider.valueChangedDiscrete.connect(self.update_ROI_level)

        self.showgoodcell_checkbox.stateChanged.connect(self.update_ROIs)
        self.showbadcell_checkbox.stateChanged.connect(self.update_ROIs)

        # self.scene_1 = QGraphicsScene()
        self.vid_frame_item_1 = pg.ImageItem(image=np.zeros((800,800)))
        self.vid_frame1.addItem(self.vid_frame_item_1)
        self.vid_frame_item_2 = pg.ImageItem(iamge=np.zeros((500,500)))
        self.vid_frame2.addItem(self.vid_frame_item_2)

        self.vid_frame1.show()
        self.vid_frame2.show()

        self.contour_range = np.arange(10,110,10)

    def open_video(self):
        selected_fileName = QFileDialog.getOpenFileName(self, caption="open video")
        video_path = selected_fileName[0]
        self.video = MsVideo(video_path)
        self.go_to_frame(0)
        self.vid_frame1.setRange(self.vid_frame_item_1.boundingRect(),padding=0)
        self.vid_frame2.setRange(self.vid_frame_item_2.boundingRect(),padding=0)
        
        self.frame_slider.setMaximum(self.video.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
        self.frame_slider.setMinimum(0)

    def import_ms(self):
        selected_fileName = QFileDialog.getOpenFileName(self, caption="open ms.mat")
        self.ms_path = selected_fileName[0]
        self.ms_file = self.load_ms_file(self.ms_path)
        self.MS = MS(self.ms_file)
        self.goodContourGroup = QGraphicsItemGroup()
        self.badContourGroup = QGraphicsItemGroup()
        # self.plot_ROIs()
        self.vid_frame1.setRange(self.vid_frame1.viewRect(),padding=0)
        self.vid_frame2.setRange(self.vid_frame2.viewRect(),padding=0)
        self.neuron_table_model = GenericTableModel(items=self.MS.NeuronList, properties=["ID","Label"])
        self.cell_list1.setModel(self.neuron_table_model)
        self.cell_list1.setHorizontalHeader()
        self.cell_list2.setModel(self.neuron_table_model)
        self.cell_list2.setHorizontalHeader()

    def go_to_frame(self, frameN):
        frame = self.video.get_frame(frameN)
        self.vid_frame_item_1.setImage(frame)
        self.vid_frame_item_2.setImage(frame)
        self.vid_frame_item_1.update()
        self.vid_frame_item_2.update()

    def numpy_to_qimage(self, array):
        height, width, _ = array.shape
        bytes_per_line = 3 * width
        qimage = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return qimage

    def load_ms_file(self, ms_path):
        ms_file = loadmat(ms_path,struct_as_record=False)["ms"]
        ms_file = ms_file[0,0]
        return ms_file

    def sort_cell(self):
        return
    
    def update_Image1(self):
        return

    def update_Image2(self):
        return
    
    def update_ROI_level(self, slider_value):
        for neuron in self.MS.NeuronList:
            neuron.ROI_Item.setLevel(slider_value)

    
    def update_Traces(self):
        return
    
    def plot_ROIs(self):
        for i in range(self.MS.NumNeurons):
            neuron = self.MS.NeuronList[i]
            if neuron.is_good():
                roi_item = ROIcontourItem(neuron.ROI, level=self.contour_slider.value(),pen='y')
                self.goodContourGroup.addToGroup(roi_item)
            else:
                roi_item = ROIcontourItem(neuron.ROI, level=self.contour_slider.value(),pen='r')
                self.badContourGroup.addToGroup(roi_item)
            neuron.ROI_Item = roi_item
            
            # print(roi_item.pen.color().getRgb())
            # print(roi_item.pen.color().getRgbF())

            self.vid_frame2.addItem(roi_item)

    def update_ROIs(self):
        return

        
        


        

