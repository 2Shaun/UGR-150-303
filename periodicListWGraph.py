import timeit
import networkx as nx
import matplotlib.pyplot as plt

start = timeit.default_timer()
G = nx.DiGraph()

class Node(object):
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def __str__(self):
        return str(self.data)

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next

class LinkedList(object):
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def __iter__(self):
        return self

    def next(self):
        current = self.head
        while current.get_next() != None:
            yield current
            current = current.get_next()

    def insert(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
        if self.tail != None:
            self.tail.next_node = new_node
        
        self.tail = new_node

    def tostring(self):
        current = self.head
        while current:
            print current
            current = current.get_next()

    def printList(self, iterations):
        current = self.head
        i = 0

        while current != None and i <= iterations:
            print "%d" % current.data,
            current = current.get_next()
            i += 1
        print

def iteratePhi(linkedlist, preimage, divisor):
    phi = preimage
    previous = 0
    print "first pre-image: %d divisor: %d" % (preimage, divisor)
    for i in range(((divisor-3)/2)+1):
       phi = phi**2
       phi = long(phi % divisor)
       G.add_node(phi)
       G.add_edge(previous,phi)
       previous = phi
       linkedlist.insert(phi)
    nx.draw_spectral(G)

def findAndPrintPeriodicValues(linkedlist):
    tortoise = linkedlist.head.get_next()
    hare = linkedlist.head.get_next().get_next()
    while tortoise.get_data() != hare.get_data():
        tortoise = tortoise.get_next()
        hare = hare.get_next().get_next()
    preperiodicNodes = 0
    tortoise = linkedlist.head
    while tortoise.get_data() != hare.get_data():
        tortoise = tortoise.get_next()
        hare = hare.get_next()
        preperiodicNodes += 1
    print "first periodic node: %d " % tortoise.get_data(),
    periodicity = 1
    hare = tortoise.get_next()
    while tortoise.get_data() != hare.get_data():
        hare = hare.get_next()
        periodicity += 1
    print "pre-periodic nodes: %d periodicity: %d" % (preperiodicNodes, periodicity)
    linkedlist.printList(periodicity+preperiodicNodes);
    print "pre-periodic nodes: %d periodicity: %d" % (preperiodicNodes, periodicity)

if __name__ == "__main__":
    import sys
    modPhiNodes = LinkedList()
    iteratePhi(modPhiNodes, long(sys.argv[1]), long(sys.argv[2]))
    nx.write_gml(G, 'modP.gml')
    #plt.show()
    #modPhiNodes.printList()
    findAndPrintPeriodicValues(modPhiNodes)

stop = timeit.default_timer()

print "time: %.2f s" % (stop - start )
