def merge_sort(arr, key_fn):
    """Merge Sort genérico: ordena arr descendente según key_fn."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_fn)
    right = merge_sort(arr[mid:], key_fn)
    return _merge(left, right, key_fn)

def _merge(left, right, key_fn):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_fn(left[i]) > key_fn(right[j]):
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
