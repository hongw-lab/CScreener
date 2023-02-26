import PySide6.QtWidgets
from PySide6.QtCore import Qt, Signal, QRectF
from pyqtgraph import GraphicsView
import numpy as np


class MsGraphicsView(GraphicsView):
    def __init__(self, zoom: float = 1, *args, **kwargs):
        super().__init__(useOpenGL=True, *args, **kwargs)
        # To track the zoom level of the view
        self.current_zoom_level = zoom

        # self.setOptimizationFlags(self.optimizationFlags())

    def zoom(self, zoom_level: float, center=None):
        # self.scale(
        #     sx=new_zoom_level / self.current_zoom_level,
        #     sy=new_zoom_level / self.current_zoom_level,
        #     center=center,
        # )
        # self.current_zoom_level = new_zoom_level
        zoom_level = zoom_level / 10
        if center is None:
            center_x = 1 / 2 * self.width()
            center_y = 1 / 2 * self.height()
        else:
            center_x = center.x()
            center_y = center.y()
        w = self.width() / zoom_level
        h = self.height() / zoom_level
        left_margin = min(max(center_x - 1 / 2 * w, 0), self.width() - w)
        top_margin = min(max(center_y - 1 / 2 * h, 0), self.height() - h)
        self.setRange(
            QRectF(
                left_margin,
                top_margin,
                w,
                h,
            ),
            padding=0,
        )

    def set_center(self, center):
        if center is None:
            return None
        w = self.range.width()
        h = self.range.height()
        left_margin = min(max(center.x() - 1 / 2 * w, 0), self.width() - w)
        top_margin = min(max(center.y() - 1 / 2 * h, 0), self.height() - h)
        self.setRange(
            QRectF(
                left_margin,
                top_margin,
                w,
                h,
            ),
            padding=0,
        )


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
