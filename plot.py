from pyqtgraph import IsocurveItem
from skimage import measure
from PySide6 import QtGui
import numpy as np
from scipy.ndimage import center_of_mass

class ROIcontourItem(IsocurveItem):
    def __init__(self, contour_center:np.ndarray=None,*args, **kwarg):
        # Save a look-up table for the levels
        self.level_dict = {}
        # Save paths from previous generation for faster replot
        self.path_dict = {}
        super().__init__(*args, **kwarg)
        if contour_center is None and self.data is not None:
            self.contour_center = center_of_mass(self.data)
        else:
            self.contour_center = contour_center

    

    def generatePath(self):
        if self.data is None:
            self.path = None
            return
        
        if self.axisOrder == 'row-major':
            data = self.data.T
        else:
            data = self.data
        
        if not self.path_dict.get(self.level):
            self.generate_level_table()
            lines = measure.find_contours(data, self.level_dict[self.level])
            self.path = QtGui.QPainterPath()
            for line in lines:
                self.path.moveTo(*line[0])
                for p in line[1:]:
                    self.path.lineTo(*p)
            self.path_dict[self.level] = self.path
        else:
            self.path = self.path_dict[self.level]
    
    def generate_level_table(self):
        if not self.level_dict.get(self.level):
            data_flat = self.data.flatten()
            data_flat = data_flat[np.nonzero(data_flat)]
            # self.level takes values from the slider, [1,10]
            self.level_dict[self.level] = np.quantile(data_flat, self.level*0.1, method='inverted_cdf')
    
    def toggle_color(self):
        return
    
    def setData(self, data, level=None):
        self.reset()
        super().setData(data, level)
        self.set_contour_center()
    
    def set_contour_center(self):
        if self.data is not None:
            self.contour_center = center_of_mass(self.data)
        else:
            self.contour_center = None

    def reset(self):
        self.level_dict.clear()
        self.path_dict.clear()
        self.data = None
        # self.level = None
        self.contour_center = None
    
    def x(self):
        if self.contour_center is None:
            return None
        else:
            return self.contour_center[0]
    
    def y(self):
        if self.contour_center is None:
            return None
        else:
            return self.contour_center[1]
    
        

        
        
        



    

    