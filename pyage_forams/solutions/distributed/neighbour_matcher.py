from collections import defaultdict
import logging

import Pyro4

from pyage.core.agent.agent import AGENT
from pyage.core.inject import Inject
from pyage_forams.solutions.agent.shadow_cell import ShadowCell
from pyage_forams.solutions.distributed.requests.match import Match2dRequest, Match3dRequest


logger = logging.getLogger(__name__)


class NeighbourMatcher(object):
    @Inject("request_dispatcher", "size", "neighbours", 'ns_hostname')
    def __init__(self):
        super(NeighbourMatcher, self).__init__()
        self._located_agents = defaultdict(self._locate_agent)

    def match_neighbours(self, agent):
        for (side, address) in self.neighbours.iteritems():
            neighbour = self._locate_agent(address)
            if neighbour:
                self._join(neighbour, agent, side)

    def _locate_neighbour(self, address):
        try:
            self._locate_agent(address)
        except:
            logger.warning("could not locate %s" % address)

    def _join(self, neighbour, agent, side):
        raise NotImplementedError()

    def _locate_agent(self, remote_address):
        ns = Pyro4.locateNS(self.ns_hostname)
        agent = Pyro4.Proxy(ns.lookup(remote_address))
        return agent


class Neighbour2dMatcher(NeighbourMatcher):
    def _join(self, remote_agent, agent, side):
        try:
            remote_address = AGENT + "." + remote_agent.get_address()
            logger.info("%s matching with: %s" % (side, remote_address))
            cells = remote_agent.get_cells(opposite(side))
            logger.info("received cells: %s" % cells)
            shadow_cells = [ShadowCell(cell.get_address(), cell.available_food(), cell.get_algae(), remote_address) for
                            cell in cells]
            agent.join(remote_address, shadow_cells, side, remote_agent.get_steps())
            self.request_dispatcher.submit_request(
                Match2dRequest(remote_address, agent.environment.get_border_cells(side),
                               AGENT + "." + agent.get_address(), opposite(side), agent.get_steps()))
        except Exception, e:
            logger.exception("could not join: %s", e.message)

    def update(self, remote_address, side, mapping):
        logger.info("updating shadow cels from: %s" % remote_address)
        agent = self._locate_agent(remote_address)
        cells = agent.get_cells(opposite(side))
        for cell in cells:
            if cell.get_address() in mapping:
                mapping[cell.get_address()].update(cell)
            else:
                logger.info("unsuccessful attempt to update cell with address %s", cell.get_address())
        return agent.get_steps()


class Neighbour3dMatcher(NeighbourMatcher):
    def _join(self, remote_agent, agent, side):
        try:
            remote_address = AGENT + "." + remote_agent.get_address()
            logger.info("%s matching with: %s" % (side, remote_address))
            rows = remote_agent.get_cells(opposite(side))
            logger.info("received rows: %s" % rows)
            shadow_cells = [[ShadowCell(cell.get_address(), cell.available_food(), cell.get_algae(), remote_address) for
                             cell in cells] for cells in rows]
            agent.join(remote_address, shadow_cells, side, remote_agent.get_steps())
            self.request_dispatcher.submit_request(
                Match3dRequest(remote_address, agent.environment.get_border_cells(side),
                               AGENT + "." + agent.get_address(), opposite(side), agent.get_steps()))
        except Exception, e:
            logger.exception("could not join: %s", e.message)


    def update(self, remote_address, side, mapping):
        logger.info("updating shadow cels from: %s" % remote_address)
        agent = self._locate_agent(remote_address)
        cells = agent.get_cells(opposite(side))
        for row in cells:
            for cell in row:
                if cell.get_address() in mapping:
                    mapping[cell.get_address()].update(cell)
                else:
                    logger.info("unsuccessful attempt to update cell with address %s", cell.get_address())
        return agent.get_steps()


def opposite(side):
    if side == "left":
        return "right"
    elif side == "right":
        return "left"
    elif side == "upper":
        return "lower"
    elif side == "lower":
        return "upper"
    elif side == "front":
        return "back"
    elif side == "back":
        return "front"
    else:
        raise ValueError("unrecognized side: " + side)
