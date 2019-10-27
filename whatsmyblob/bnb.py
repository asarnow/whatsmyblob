import pybnb
from . import neighbor_tree

class DensitySearch(pybnb.Problem):
    def __init__(self, n, s):
        self.s = s
        self._L = np.empty((n,n))
        self._U = np.empty((n,n))
        self._L1D = None
        self._U1D = None
        self._SLB = None
        self._GW = None
    def sense(self):
        pybnb.minimize
    def objective(self):
        if self._GW is None:
            self._GW = 0.
        return self._GW
    def save_state(self, node):
        node.state = (self._L, self._U)
    def load_state(self, node):
        (self._L, self._U) = node.state
        self._SLB = None
        self._GW = None
        self._L1D = neighbor_tree.get_inv_cdf(self._L, self.s)
        self._U1D = neighbor_tree.get_inv_cdf(self._U, self.s)
    def bound(self):
        if self._SLB is None:
            self._SLB = 0.5 * np.sqrt(np.sum((self._L1D - self._U1D) ** 2))
        return self._SLB
    def branch(self):
        child = pybnb.Node()
        child.state = (self._L, self._M, self._L1D, self._U1D, self._fT)
        yield child
        child = pybnb.Node()
        child.state = (self._M, self._U, self._L1D, self._U1D, self._fT)
        yield child


def bnb_search(upb, lwb):
    pass