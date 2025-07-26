# heap_sort/heap_sort.py
from heap_sort.heap import MaxHeap

def heap_sort(arr, key_fn):
    """Ordena arr descendente usando un MaxHeap."""
    heap = MaxHeap()
    for item in arr:
        heap.push(item, key_fn(item))
    sorted_list = []
    while True:
        top = heap.pop()
        if top is None:
            break
        sorted_list.append(top)
    return sorted_list
