import scipy as scp
from scipy.ndimage import center_of_mass

# from plot import ROIcontourItem
import numpy as np
import warnings
from typing import List
import utility as utt
from video import Worker
from PySide6.QtCore import QThreadPool
from PySide6.QtWidgets import QGraphicsItem
from PySide6 import QtGui
from pyqtgraph import IsocurveItem
from skimage import measure
from scipy.ndimage import center_of_mass
from state import GuiState


class MS:
    def __init__(self, ms_file=None, file_type: int = 1, mainwindow=None):
        # If path to ms.mat is fed in the contructor, construct accordingly
        self.NeuronList = []
        self.file_type = file_type
        self.threadpool = QThreadPool()
        self.worker = None
        self._stop = False
        self.mw = mainwindow
        self.mean_trace = dict()
        if ms_file and file_type == 1:
            # Case 1: scipy readable file
            self.scipy_load(ms_file)
        elif ms_file and file_type == 2:
            self.hdf5load(ms_file)
        else:
            self.FiltTraces = None
            self.RawTraces = None
            self.Spikes = None
            self.ROIs = None
            self.NumNeurons = 0
            self.CellLabel = None
            self.NumFrame = 0
        if self.FiltTraces is not None:
            # Construct list of Neuron objects
            for i in range(self.NumNeurons):
                FiltTrace = self.FiltTraces[:, i]
                RawTrace = self.RawTraces[:, i]
                Spike = self.Spikes[:, i]
                ROI = self.ROIs[:, :, i]
                Label = self.Labels[i]
                # Construct Neuron, ID starting from 1
                self.NeuronList.append(
                    Neuron(FiltTrace, RawTrace, Spike, ROI, Label, i + 1)
                )

            self.dist_map = self.distance_map()
            self.raw_correlation_map = self.correlation_map("RawTrace")
            self.filt_correlation_map = self.correlation_map("FiltTrace")
            self.spike_correlation_map = self.correlation_map("Spike")
            # Precomputing the mean traces
            for tracetype in ["RawTrace", "FiltTrace", "Spike"]:
                self.compute_mean_trace(tracetype)

    def hasNeuron(self):
        if self.NumNeurons > 0:
            return True
        else:
            return False

    def num_frame(self):
        return self.NumFrame

    def distance_map(self):
        dist_map = np.zeros((self.NumNeurons, self.NumNeurons))
        for i in range(self.NumNeurons):
            for j in range(i, self.NumNeurons):
                neuron_i_center = self.NeuronList[i].get_center()
                neuron_j_center = self.NeuronList[j].get_center()
                dist_map[i, j] = np.linalg.norm(neuron_i_center - neuron_j_center)
                dist_map[j, i] = dist_map[i, j]
        return dist_map.round(decimals=2)

    def get_labels(self):
        return self.Labels > 0

    def num_good_cell(self):
        self.update_labels()
        return np.sum(self.get_labels())

    def correlation_map(self, trace_type: str = None):
        if trace_type == "RawTrace":
            return np.corrcoef(self.RawTraces, rowvar=False).round(decimals=2)
        elif trace_type == "FiltTrace":
            return np.corrcoef(self.FiltTraces, rowvar=False).round(decimals=2)
        elif trace_type == "Spike":
            return np.corrcoef(self.Spikes, rowvar=False).round(decimals=2)
        else:
            return None

    def get_corr_coeff(self, ID1, ID2, trace_type: str = None):
        # Take neuron ID as input, -1 for index
        if trace_type == "RawTrace":
            value = self.raw_correlation_map[ID1 - 1, ID2 - 1]
            return value.item()
        elif trace_type == "FiltTrace":
            value = self.filt_correlation_map[ID1 - 1, ID2 - 1]
            return value.item()
        elif trace_type == "Spike":
            value = self.spike_correlation_map[ID1 - 1, ID2 - 1]
            return value.item()
        else:
            return None

    def get_dist(self, ID1, ID2):
        value = self.dist_map[ID1 - 1, ID2 - 1]
        return value.item()

    def update_labels(self):
        for i, neuron in enumerate(self.NeuronList):
            self.Labels[i] = neuron.get_ms_Label()

    def compute_mean_trace(self, type: str = "FiltTrace"):
        # Make sure the labels are up to date
        self.update_labels()
        if type == "FiltTrace":
            traces = self.FiltTraces
        elif type == "RawTrace":
            traces = self.RawTraces
        elif type == "Spike":
            traces = self.Spikes
        else:
            return None
        if not self.mean_trace.get(type):
            zscored_trace = scp.stats.zscore(traces[:, self.Labels == 1])
            self.mean_trace[type] = np.mean(zscored_trace, axis=1)

        return True

    def update_mean_trace(self, toggled_cell=None):
        # Minimize the computation when mean trace already exists
        if toggled_cell is None:
            # No change to the mean trace
            return False
        for tracetype in ["RawTrace", "FiltTrace", "Spike"]:
            original_trace = self.mean_trace[tracetype]
            toggled_trace = scp.stats.zscore(getattr(toggled_cell, tracetype))
            if toggled_cell.is_good():
                # Toggled from bad to good, add to mean trace
                new_trace = np.average(
                    np.column_stack((original_trace, toggled_trace)),
                    weights=(self.num_good_cell() - 1, 1),
                    axis=1,
                )

            elif not toggled_cell.is_good():
                # Toggled from good to bad, remove from mean trace
                new_trace = np.average(
                    np.column_stack((original_trace, toggled_trace)),
                    weights=(self.num_good_cell() + 1, -1),
                    axis=1,
                )
            self.mean_trace[tracetype] = new_trace

    def get_mean_trace(self, trace_type):
        if trace_type not in ["RawTrace", "FiltTrace", "Spike"]:
            return None
        return self.mean_trace[trace_type]

    def scipy_load(self, ms_file):
        self.FiltTraces = ms_file.FiltTraces
        self.RawTraces = ms_file.RawTraces
        self.Spikes = ms_file.S
        # Make sure that all the data fields are time x neuron
        self.ROIs = ms_file.SFPs
        self.NumNeurons = int(ms_file.numNeurons)
        if self.FiltTraces.shape[1] != self.NumNeurons:
            self.FiltTraces = self.FiltTraces.T
        if self.RawTraces.shape[1] != self.NumNeurons:
            self.RawTraces = self.RawTraces.T
        if self.Spikes.shape[1] != self.NumNeurons:
            self.Spikes = self.Spikes.T
        self.NumFrame = ms_file.FiltTraces.shape[0]
        if hasattr(ms_file, "cell_label"):
            self.Labels = ms_file.cell_label.flatten()
        else:
            self.Labels = np.ones(ms_file.FiltTraces.shape[1])

    def hdf5load(self, ms_file):
        self.FiltTraces = utt.hdf_np_convert(ms_file, "FiltTraces")
        self.RawTraces = utt.hdf_np_convert(ms_file, "RawTraces")
        self.Spikes = utt.hdf_np_convert(ms_file, "S")
        self.NumNeurons = int(utt.hdf_np_convert(ms_file, "numNeurons"))
        self.ROIs = utt.hdf_np_convert(ms_file, "SFPs")
        if self.FiltTraces.shape[1] != self.NumNeurons:
            self.FiltTraces = self.FiltTraces.T
        if self.RawTraces.shape[1] != self.NumNeurons:
            self.RawTraces = self.RawTraces.T
        if self.Spikes.shape[1] != self.NumNeurons:
            self.Spikes = self.Spikes.T
        if self.ROIs.shape[2] != self.NumNeurons:
            self.ROIs = self.ROIs.T
        self.NumFrame = self.FiltTraces.shape[0]
        if "cell_label" in ms_file.keys():
            self.Labels = utt.hdf_np_convert(ms_file, "cell_label").flatten()
        else:
            self.Labels = np.ones(self.NumNeurons)

    def get_file_type(self):
        return self.file_type

    def get_lean_ms(self):
        # Returns a dictionary with only the very essential fields
        ms_file = {
            "FiltTraces": self.FiltTraces,
            "RawTraces": self.RawTraces,
            "S": self.Spikes,
            "SFPs": self.ROIs,
            "numNeurons": self.NumNeurons,
            "cell_label": self.Labels.astype(bool),
        }
        return ms_file

    def generate_ROIs(self, progress_callback):
        for i, neuron in enumerate(self.NeuronList):
            if self._stop:
                break
            if neuron.is_good():
                neuron.ROI_Item = ROIcontourItem(
                    data=neuron.ROI,
                    contour_center=neuron.center,
                    level=self.mw.state["contour_level"],
                    pen="y",
                    activatable=True,
                    neuron=neuron,
                    state=self.mw.state,
                )
                self.mw.goodNeuronGroup.add_neuron(neuron)
            else:
                neuron.ROI_Item = ROIcontourItem(
                    data=neuron.ROI,
                    contour_center=neuron.center,
                    level=self.mw.state["contour_level"],
                    pen="r",
                    activatable=True,
                    neuron=neuron,
                    state=self.mw.state,
                )
                self.mw.badNeuronGroup.add_neuron(neuron)
            # Make all individual contours in vid_frame2 selectable
            neuron.ROI_Item.setFlag(QGraphicsItem.ItemIsSelectable)
            progress_callback.emit(i)

        return False if self._stop else True

    def _threading_(self, workfunc):
        self.worker = Worker(workfunc)
        self.worker.signals.finished.connect(self.finish_message)
        self.worker.signals.progress.connect(self.progress_message)
        self.threadpool.start(self.worker)

    def finish_message(self):
        self.mw.statusbar.clearMessage()
        self.mw.statusbar.showMessage(
            "ROI plotting finished! Ms loading complete.", timeout=5000
        )
        # Add generated items to the image frame in mainwindow
        for neuron in self.NeuronList:
            self.mw.vid_frame2.addItem(neuron.ROI_Item)
        return True

    def progress_message(self, n):
        self.mw.statusbar.clearMessage()
        self.mw.statusbar.showMessage(
            "Generating ROI contour for neuron %d/%d..." % (n, self.NumNeurons)
        )

    def stop_worker(self):
        try:
            self._stop = True
        except Exception:
            pass

    def clear_threads(self):
        try:
            self.threadpool.clear()
        except Exception:
            pass


class Neuron:
    def __init__(
        self,
        FiltTrace: np.ndarray = None,
        RawTrace: np.ndarray = None,
        Spike: np.ndarray = None,
        ROI: np.ndarray = None,
        Label: int = None,
        ID: int = None,
    ):
        self.FiltTrace = FiltTrace
        self.RawTrace = RawTrace
        self.Spike = Spike
        self.ROI = ROI
        self._Label = Label > 0
        self.ID = ID  # starts from 1
        self.Visible = True
        self.center = np.array(center_of_mass(self.ROI))

    @property
    def Label(self):
        return "Good" if self._Label else "Bad"

    @Label.setter
    def Label(self, value):
        self._Label = value > 0

    def is_good(self):
        return self._Label

    def get_max_filt_frame(self):
        return np.argmax(self.FiltTrace)

    def get_max_raw_frame(self):
        return np.argmax(self.RawTrace)

    def set_good(self):
        self._Label = True

    def set_bad(self):
        self._Label = False

    def toggle_label(self):
        if self.Label == 0:
            self.Label = 1
        else:
            self.Label = 0

    def get_center(self):
        return self.center

    def get_ROI(self):
        return self.ROI

    def get_FiltTrace(self):
        return self.FiltTrace

    def get_RawTrace(self):
        return self.RawTrace

    def get_ID(self):
        return self.ID

    def get_ms_Label(self):
        # Return ms ready label (1 for good, 0 for bad, int)
        return 1 if self._Label else 0


class NeuronGroup(object):
    def __init__(self, neuron_list: List = []) -> None:
        # Use neuron.ID as key and return pointer to the neuron
        self.neuron_dict = dict()
        self.generate_neuron_dict(neuron_list)

    def generate_neuron_dict(self, neuron_list):
        for neuron in neuron_list:
            self.add_neuron(neuron)

    def add_neuron(self, neuron):
        if not neuron:
            return False
        if not self.neuron_dict.get(neuron.ID):
            self.neuron_dict[neuron.ID] = neuron
        else:
            warnings.warn("Neuron ID already exists")

    def pop_neuron(self, neuron):
        return self.neuron_dict.pop(neuron.ID, None)

    def contour_items(self):
        contour_items = []
        for key in self.neuron_dict.keys():
            contour_items.append(self.neuron_dict[key].ROI_Item)

    def setVisible(self, visible: bool = True):
        for key in self.neuron_dict.keys():
            self.neuron_dict[key].ROI_Item.setVisible(visible)

    def is_in(self, neuron):
        if self.neuron_dict.get(neuron.ID):
            return True
        else:
            return False


class ROIcontourItem(IsocurveItem):
    def __init__(
        self,
        contour_center: np.ndarray = None,
        activatable: bool = False,
        state: GuiState = None,
        neuron: Neuron = None,
        *args,
        **kwarg
    ):
        # Save a look-up table for the levels
        self.level_dict = {}
        # Save paths from previous generation for faster replot
        self.path_dict = {}
        self.activatable = activatable
        self.state = state
        self.neuron = neuron
        super().__init__(*args, **kwarg)

        if contour_center is None and self.data is not None:
            self.contour_center = center_of_mass(self.data)
        else:
            self.contour_center = contour_center

    def boundingRect(self):
        if self.path:
            return self.path.controlPointRect()
        else:
            return super().boundingRect()

    def generatePath(self):
        if self.data is None:
            self.path = None
            return

        if self.axisOrder == "row-major":
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
            self.level_dict[self.level] = np.quantile(
                data_flat, self.level * 0.1, method="inverted_cdf"
            )

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

    def mouseDoubleClickEvent(self, event):
        if self.is_activatable():
            self.state["focus_cell"] = self.neuron

        super().mouseDoubleClickEvent(event)

    def is_activatable(self):
        return self.activatable
