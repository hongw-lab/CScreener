import PySide6.QtWidgets
from PySide6.QtCore import Qt, Signal
from pyqtgraph import GraphicsView
import numpy as np


class MsGraphicsView(GraphicsView):
    def __init__(self, zoom: float = 1, *args, **kwargs):
        super().__init__(useOpenGL=True, *args, **kwargs)
        # To track the zoom level of the view
        self.current_zoom_level = zoom
        
        # self.setOptimizationFlags(self.optimizationFlags())

    # def resizeEvent(self, event) -> None:
    #     self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
    #     super().resizeEvent(event)
    
    def zoom(self, new_zoom_level: float, center=None):
        self.scale(new_zoom_level/self.current_zoom_level, new_zoom_level/self.current_zoom_level)
        self.current_zoom_level = new_zoom_level
        self.centerOn(center)



class DiscreteSlider(PySide6.QtWidgets.QSlider):
    valueChangedDiscrete = Signal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valueChanged.connect(self.emit_discrete_value)

    def emit_discrete_value(self, value):
        min_value = self.minimum()
        max_value = self.maximum()
        value_step = self.singleStep()
        valid_value_list = np.arange(min_value, max_value + value_step, value_step)
        val_select = valid_value_list[np.argmin(np.abs(valid_value_list - value))]
        self.setValue(min(val_select, max_value))
        self.valueChangedDiscrete.emit(min(val_select, max_value))
