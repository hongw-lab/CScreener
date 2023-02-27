import cv2

class MsVideo(cv2.VideoCapture):
    def __init__(self, video_path) -> None:
        super().__init__(video_path)
        self.current_frame_index = 0
        self.last_frame_index = int(self.get(cv2.CAP_PROP_FRAME_COUNT)-1)
        self.video_path = video_path
    
    def get_frame(self, frameN):
        self.set(cv2.CAP_PROP_POS_FRAMES, frameN)
        success, frame = self.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
    
    def num_frame(self):
        return self.last_frame_index+1
    
    def get_maxproj_frame(self):
        return
    
    def get_mean_frame(self):
        return
    