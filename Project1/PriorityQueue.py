class PQ:
    def __init__(self):
        self.pq = []

    def add(self, value):
        self.pq.append(value)
        self.pq.sort(key=lambda x: x.priority, reverse=True)

    def pop(self):
        return self.pq.pop()

    def front(self):
        return self.pq[0]

    def remove(self, process):
        self.pq.remove(process)

    def __repr__(self):
        repr_str = "PQ("
        for pcb in self.pq:
            repr_str += "," + repr(pcb)
        repr_str += ")"
        return repr_str
