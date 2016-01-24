# coding=utf-8

from pyage_forams.pyage.core.address import SequenceAddressProvider
from pyage_forams.pyage.core.stop_condition import StepLimitStopCondition
from pyage_forams.solutions.environment import environment_factory, Environment3d
from pyage_forams.solutions.foram import create_forams, create_agent
from pyage_forams.solutions.genom import GenomFactory
from pyage_forams.solutions.insolation_meter import DynamicInsolation
from pyage_forams.solutions.statistics import SimpleStatistics, PsiStatistics, CsvStatistics, MultipleStatistics


factory = GenomFactory(chambers_limit=5)
genom_factory = lambda: factory.generate
forams = create_forams(8, initial_energy=5)
agents = create_agent
insolation_meter = lambda: DynamicInsolation([(20, 10, 0.2), (10, 20, 0.4)])
size = lambda: (10, 15, 20)
length = lambda: 8

reproduction_minimum = lambda: 10
movement_energy = lambda: 0.5
growth_minimum = lambda: 25
energy_need = lambda: 0.2
algae_limit = lambda: 20
algae_growth_probability = lambda: 0.3
newborn_limit = lambda: 10
reproduction_probability = lambda: 0.8
growth_probability = lambda: 0.9
growth_cost_factor = lambda: 0.05
capacity_factor = lambda: 1.1
initial_algae_probability = lambda: 0.3
cell_capacity = lambda: 2

environment = environment_factory(regeneration_factor=0.1, clazz=Environment3d)

stop_condition = lambda: StepLimitStopCondition(30000)

address_provider = SequenceAddressProvider
stats = lambda: MultipleStatistics([CsvStatistics(), PsiStatistics()])