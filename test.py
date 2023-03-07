from scipy.io import loadmat, savemat
import numpy as np

def obj_to_dict(obj):
    if isinstance(obj, dict):
        return {k: obj_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, '__dict__'):
        return {k: obj_to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, (list, tuple, set)):
        return type(obj)(obj_to_dict(v) for v in obj)
    else:
        return obj


ms_file = loadmat("ms.mat", struct_as_record=False)["ms"]
ms_file = ms_file[0, 0]
ms_dict = {"ms": ms_file}
# ms_file = {"a": np.ones((100, 20)), "b": {"c": np.zeros(10)}}
ms_save = obj_to_dict(ms_dict)

savemat("ms_file_saved.mat", ms_save)
