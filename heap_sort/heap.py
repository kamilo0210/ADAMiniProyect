# heap_sort/heap.py

class MaxHeap:
    def __init__(self):
        self.data = []

    def push(self, item, key):
        """Inserta elemento y reorganiza el heap."""
        self.data.append((key, item))
        self._sift_up(len(self.data) - 1)

    def pop(self):
        """Extrae mayor elemento."""
        if not self.data:
            return None
        top = self.data[0][1]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return top

    def _sift_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.data[idx][0] > self.data[parent][0]:
            self.data[idx], self.data[parent] = self.data[parent], self.data[idx]
            self._sift_up(parent)

    def _sift_down(self, idx):
        left = 2 * idx + 1
        right = 2 * idx + 2
        largest = idx
        for child in (left, right):
            if child < len(self.data) and self.data[child][0] > self.data[largest][0]:
                largest = child
        if largest != idx:
            self.data[idx], self.data[largest] = self.data[largest], self.data[idx]
            self._sift_down(largest)
