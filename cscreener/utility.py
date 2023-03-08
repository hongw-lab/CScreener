import numpy as np
from scipy.io import loadmat, savemat


def _cell_list_move_(mw, which_one, direction):
    if which_one == 1:
        focus = "focus_cell"
        clist = mw.cell_list1
    elif which_one == 2:
        focus = "companion_cell"
        clist = mw.cell_list2

    # Get the current activated idx
    activated_idx = clist.model()._activated_index
    if activated_idx is None:
        # When there is no activated neuron. Start from the top or bottom
        if direction == "up":
            activated_idx = clist.model().rowCount()
        if direction == "down":
            activated_idx = -1

    if direction == "up":
        new_idx = max(0, activated_idx - 1)
    elif direction == "down":
        new_idx = min(clist.model().rowCount() - 1, activated_idx + 1)
    else:
        return False

    if new_idx == activated_idx:
        return False
    else:
        try:
            clist.model()._activated_index = new_idx
            mw.state[focus] = clist.model().item_list[new_idx]["item"]
            clist.scroll_to_activated()
            return True
        except Exception:
            return False


def _sort_by_column_(mw, column):
    try:
        mw.cell_list2.model().sort(column)
        mw.cell_list2.on_header_clicked(column)
        return True
    except Exception:
        return False


def _jump_to_max_(mw, which_cell):
    if which_cell == 1:
        focus = mw.state["focus_cell"]
    elif which_cell == 2:
        focus = mw.state["companion_cell"]
    if focus is None:
        return False
    try:
        trace = getattr(focus, mw.state["trace_mode"])
        idx = int(np.argmax(trace)) - 1
        mw.state["current_frame"] = idx
        return True
    except Exception:
        return False


def _arrow_func_(mw, direction):
    if direction == "left":
        try:
            current_frame = mw.state["current_frame"]
            mw.state["current_frame"] = max(0, current_frame - 1)
            return True
        except Exception:
            return False
    elif direction == "right":
        try:
            current_frame = mw.state["current_frame"]
            mw.state["current_frame"] = min(
                current_frame + 1, mw.state["video"].num_frame()
            )
            return True
        except Exception:
            return False
    else:
        return False


def load_ms_file(ms_path):
    try:
        ms_file = loadmat(ms_path, struct_as_record=False)["ms"]
        ms_file = ms_file[0, 0]
        success = True
    except Exception:
        success = False
        ms_file = None
    return (ms_file, success)


def save_ms_file(filename, ms):
    try:
        ms_dict = obj_to_dict(ms)
        savemat(filename, ms_dict)
        return True
    except Exception:
        return False


def obj_to_dict(obj):
    # Helper function to convert a class with multi-level attributes to a dict for save
    if isinstance(obj, dict):
        return {k: obj_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return {k: obj_to_dict(v) for k, v in obj.__dict__.items()}
    elif isinstance(obj, (list, tuple, set)):
        return type(obj)(obj_to_dict(v) for v in obj)
    else:
        return obj
