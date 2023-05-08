import cv2
from PySide6.QtCore import QRunnable, QThreadPool, Slot, Signal, QObject, QThread, QTimer
import traceback
import sys
import numpy as np


class MsVideo(QObject):
    request_frame = Signal(int)
    progress_signal = Signal(object)
    finish_signal =Signal(object)
    run_control = Signal(bool)
    emit_frame = Signal(object)
    emit_permission = Signal()
    
    def __init__(self, video_path) -> None:
        super().__init__()
        _video = cv2.VideoCapture(video_path)
        self._frame_number = int(_video.get(cv2.CAP_PROP_FRAME_COUNT))
        self._video_path = video_path
        _video.release()
        
        self._threadpool = QThreadPool()
        self._frame_fetcher = FrameFetcher(self._video_path)
        self.request_frame.connect(self._frame_fetcher.receive_frame_number)
        self.run_control.connect(self._frame_fetcher.receive_run_state)
        self._frame_fetcher._signals.result.connect(lambda x: self.emit_frame.emit(x))
        self.emit_permission.connect(self._frame_fetcher.receive_emit_permission)
        self.frame_timer = QTimer(self)
        self.frame_timer.timeout.connect(lambda: self.emit_permission.emit())
        self.frame_timer.start(33)
        self._threadpool.start(self._frame_fetcher)
        
        # Save max, min and average frames
        self.special_frames = dict()
        self.worker = None
        self._run = True

    def get_frame(self, frame):
        self.request_frame.emit(frame)

    def num_frame(self):
        return self._frame_number

    def calculate_maxproj_frame(self, progress_callback):
        tmp_vid = cv2.VideoCapture(self._video_path)
        mip = np.zeros(
            (
                int(tmp_vid.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                int(tmp_vid.get(cv2.CAP_PROP_FRAME_WIDTH)),
            ),
            dtype=np.float32,
        )
        for i in range(0, self.num_frame(), int(np.ceil(self.num_frame() / 1000))):
            if not self._run:
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

    def calculate_special_frame(self, workfunc, attr_n):
        # Use an independent thread to compute maximum frame
        # attr_n is the name of the attributes you want to set to the returned value
        self.worker = Worker(workfunc)
        self.worker.signals.finished.connect(lambda: self.finish_signal.emit(attr_n))
        self.worker.signals.progress.connect(self.progress_fn)
        self.worker.signals.result.connect(lambda x: self.special_frames.update({attr_n:x}))
        self._threadpool.start(self.worker)

    def progress_fn(self, n):
        self.progress_signal.emit(n)

    def stop_worker(self):
        self.frame_timer.stop()
        self._run = False
        self.run_control.emit(False)
        self._threadpool.waitForDone()
        self._threadpool.clear()





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

class FrameFetcher(QRunnable):
    @Slot()
    def receive_frame_number(self, frame:int):
        self._frame = frame
    @Slot()
    def receive_run_state(self,run:bool):
        self._run = run
    @Slot()
    def receive_emit_permission(self):
        self._emit_permission = True
    
    def __init__(self, video_path):
        super().__init__()
        self._frame = None
        self._run = True
        self._path = video_path
        self._signals = WorkerSignals()
        self._emit_permission = True
    
    @Slot()
    def run(self):
        cap = cv2.VideoCapture(self._path)
        if not cap.isOpened():
            print("Error opening video file")
            return False
        while self._run:
            if self._frame is not None:
                cap.set(cv2.CAP_PROP_POS_FRAMES, self._frame)
                success, frame = cap.read()
                if success and self._emit_permission:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self._signals.result.emit(frame)
                    self._emit_permission = False
                else:
                    QThread.msleep(20)
            else:
                QThread.msleep(20)
        
        
        