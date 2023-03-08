import cv2
from PySide6.QtCore import QRunnable, QThreadPool, Slot, Signal, QObject
import traceback
import sys
import numpy as np


class MsVideo(cv2.VideoCapture):
    def __init__(self, video_path, mwindow) -> None:
        super().__init__(video_path)
        self.mwindow = mwindow
        self.current_frame_index = 0
        self.last_frame_index = int(self.get(cv2.CAP_PROP_FRAME_COUNT) - 1)
        self.video_path = video_path
        self.threadpool = QThreadPool()
        self.max_proj = None
        self.min_proj = None
        self.mean_frame = None
        self.worker = None
        self._stop = False

    def get_frame(self, frameN):
        self.set(cv2.CAP_PROP_POS_FRAMES, frameN)
        success, frame = self.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def num_frame(self):
        return self.last_frame_index + 1

    def calculate_maxproj_frame(self, progress_callback):
        mip = np.zeros(
            (
                int(self.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                int(self.get(cv2.CAP_PROP_FRAME_WIDTH)),
            ),
            dtype=np.float32,
        )
        tmp_vid = cv2.VideoCapture(self.video_path)
        for i in range(0, self.num_frame(), int(np.ceil(self.num_frame() / 1000))):
            if self._stop:
                break
            tmp_vid.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = tmp_vid.read()
            if not ret:
                break
            frame_max = np.maximum.reduce(frame.astype(np.float32), axis=2)
            np.maximum(mip, frame_max, out=mip)
            progress_callback.emit(i / self.num_frame())
        cv2.normalize(mip, mip, 0, 255, cv2.NORM_MINMAX)
        mip = cv2.convertScaleAbs(mip)
        return mip

    def get_frame_func(self, result, attr_n):
        setattr(self, attr_n, result)

    def threading_get(self, workfunc, attr_n):
        # Use an independent thread to compute maximum frame
        self.worker = Worker(workfunc)
        self.worker.signals.finished.connect(self.finish_message)
        self.worker.signals.progress.connect(self.progress_fn)
        self.worker.signals.result.connect(lambda x: self.get_frame_func(x, attr_n))
        self.threadpool.start(self.worker)

    def progress_fn(self, n):
        self.mwindow.statusbar.clearMessage()
        self.mwindow.statusbar.showMessage(
            "Computing maximum projection image in background... %.2f%%" % (n * 100)
        )

    def finish_message(self):
        if self.mwindow.image1_mode_comboBox.findText("Max Projection") == -1:
            self.mwindow.image1_mode_comboBox.addItem("Max Projection")
            self.mwindow.image2_mode_comboBox.addItem("Max Projection")

        self.mwindow.statusbar.clearMessage()
        self.mwindow.statusbar.showMessage(
            "Finished! New image mode Max Projection now available.", timeout=5000
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


class WorkerSignals(QObject):
    # Defines the signals available from a running worker thread
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(float)


class Worker(QRunnable):
    # Worker thread

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.kwargs["progress_callback"] = self.signals.progress

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
