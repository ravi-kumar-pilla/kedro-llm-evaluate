import os
import json
import pandas as pd
import numpy as np


def serialize_value(val):
    if isinstance(val, pd.DataFrame):
        return {
            "__type__": "DataFrame",
            "shape": val.shape,
            "columns": val.columns.tolist(),
            "sample": val.head(1).to_dict(orient="records")
        }
    elif isinstance(val, np.ndarray):
        return {
            "__type__": "ndarray",
            "shape": val.shape,
            "dtype": str(val.dtype),
            "sample": val[:1].tolist()
        }
    elif isinstance(val, (str, int, float, bool, type(None), list, dict)):
        return val
    else:
        return {
            "__type__": str(type(val)),
            "repr": repr(val)
        }

def safe_serialize(data: dict):
    return {k: serialize_value(v) for k, v in data.items()}


def log_trace(inputs, outputs, node_name, config):
    if not config.get("log_outputs", False):
        return

    trace_dir = config.get("trace_dir", "data/99_traces")
    os.makedirs(trace_dir, exist_ok=True)
    trace_path = os.path.join(trace_dir, f"{node_name}_trace.json")

    try:
        inputs_serialized = safe_serialize(inputs)
        outputs_serialized = safe_serialize(outputs)
        
        trace = {
            "node": node_name,
            "inputs": inputs_serialized,
            "outputs": outputs_serialized,
        }

        with open(trace_path, "w") as f:
            json.dump(trace, f, indent=2)

    except Exception as e:
        print(f"[log_trace] Serialization failed: {e}")