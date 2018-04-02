def detect_type(workload):
    if workload is None:
        return 'cur-dir'
    else:
        workload = workload.strip()
        workload_lower = workload.lower()
        if workload_lower.startswith('http://') or workload_lower.startswith('https://'):
            if workload_lower.endswith('.zip') or '.zip#' in workload_lower:
                return 'zip-url'
        raise NotImplementedError("could not detect workload type")
