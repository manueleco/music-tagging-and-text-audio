"""Cache identity and row alignment; no model or dataset downloads."""
import hashlib
import json


def cache_digest(settings):
    payload = json.dumps(settings, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]


def source_row_indices(meta, total_rows):
    indices = [item["i"] for item in meta]
    if any(type(i) is not int or not 0 <= i < total_rows for i in indices):
        raise ValueError("Cache metadata contains invalid source row indices.")
    if len(indices) != len(set(indices)):
        raise ValueError("Cache metadata contains duplicate source row indices.")
    return indices
