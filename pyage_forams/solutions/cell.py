import logging
from pyage.core.inject import Inject

from pyage.core.address import Addressable


logger = logging.getLogger(__name__)


class Cell(Addressable):
    @Inject("movement_energy", "algae_limit", "cell_capacity")
    def __init__(self, algae=0, cell_size=1):
        super(Cell, self).__init__()
        self.cell_max = self.cell_capacity * cell_size
        self.cell_algae_limit = self.algae_limit * cell_size
        self.cell_movement_energy = self.movement_energy * cell_size
        self._algae = algae
        self.forams = set()
        self._neighbours = []

    def insert_foram(self, foram):
        logger.info("inserting %s into %s" % (foram, self))
        if self.is_full():
            raise ValueError("cannot insert foram to full cell")
        self.forams.add(foram)
        foram.cell = self

    def remove_foram(self, foram):
        self.forams.remove(foram)
        foram.cell = None
        return foram

    def is_empty(self):
        return not self.forams

    def is_full(self):
        return len(self.forams) >= self.cell_max

    def take_algae(self, demand):
        to_let = min(demand, self._algae)
        self._algae -= to_let
        return to_let

    def get_algae(self):
        return self._algae

    def add_algae(self, algae):
        self._algae += algae
        self._algae = min(self._algae, self.cell_algae_limit)

    def available_food(self):
        return self._algae + sum(map(lambda c: c.get_algae(), self._neighbours))

    def add_neighbour(self, cell):
        self._neighbours.append(cell)

    def get_neighbours(self):
        return self._neighbours

    def get_movement_energy(self):
        return self.cell_movement_energy

    def to_shadow(self):
        return self.get_address(), self.available_food(), self._algae, self.is_full(), [cell.get_address() for cell in
                                                                                        self.get_neighbours()]

    def __repr__(self):
        return "(%d, %s, %d)" % (self._algae, self.forams, self.available_food())