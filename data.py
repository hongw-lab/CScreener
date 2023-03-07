import scipy as scp
from scipy.ndimage import center_of_mass
import numpy as np
import warnings
from typing import List


class MS:
    def __init__(self, ms_file=None):
        self.deftFiltTraces = None
        self.deftRawTraces = None
        self.deftSpikes = None
        self.deftROIs = None
        self.deftLabels = None
        self.deftNumNeurons = 0
        self.NeuronList = []
        self.deftNumFrame = 0
        # If path to ms.mat is fed in the contructor, construct accordingly
        if ms_file:
            self.FiltTraces = ms_file.FiltTraces
            self.RawTraces = ms_file.RawTraces
            self.Spikes = ms_file.S
            # Make sure that all the data fields are time x neuron
            if self.Spikes.shape[0] != self.FiltTraces.shape[0]:
                self.Spikes = np.transpose(self.Spikes)

            self.ROIs = ms_file.SFPs
            self.NumNeurons = np.squeeze(ms_file.numNeurons)
            self.NumFrame = ms_file.FiltTraces.shape[0]
            if hasattr(ms_file, "cell_label"):
                self.Labels = ms_file.cell_label.flatten()
            else:
                self.Labels = np.ones(ms_file.FiltTraces.shape[1])

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
        else:
            self.FiltTraces = self.deftFiltTraces
            self.RawTraces = self.deftFiltTraces
            self.Spikes = self.deftSpikes
            self.ROIs = self.deftROIs
            self.NumNeurons = self.deftNumNeurons
            self.CellLabel = self.deftLabels
            self.NumFrame = self.deftNumFrame

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
        return self.Labels

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

    def mean_trace(self, type: str = "FiltTrace"):
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
        zscored_trace = scp.stats.zscore(traces[:, self.Labels == 1])
        return np.mean(zscored_trace, axis=1)


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
