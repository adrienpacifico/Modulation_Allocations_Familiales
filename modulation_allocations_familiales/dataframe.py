# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division


import os
import datetime



from openfisca_core import periods, reforms
from openfisca_core.decompositions import get_decomposition_json
import openfisca_france




from modulation_allocations_familiales.reforms import anticipation_modulation_af_2015
from openfisca_france.tests import base




TaxBenefitSystem = openfisca_france.init_country()
tax_benefit_system = TaxBenefitSystem()
#from modulation_allocations_familiales.reforms import anticipation_modulation_af_2015


from openfisca_matplotlib.dataframes import data_frame_from_decomposition_json
#from modulation_allocations_familiales.reforms import anticipation_modulation_af_2015


def create_simulation(year = 2014, bareme = False):
    simulation_period = periods.period('year', year)

    reference_legislation_json = tax_benefit_system.legislation_json

    reform = anticipation_modulation_af_2015.build_reform(base.tax_benefit_system)

    parent1 = dict(
        birth = datetime.date(year - 40, 1, 1),
        salbrut = 35 if bareme is False else None,
        )
    parent2 = dict(
        birth = datetime.date(year - 40, 1, 1),
        salbrut = 0,
        )
    menage = dict(
        loyer = 1000000,
        so = 4,
        )
    axes = [
        dict(
            count = 10,
            name = 'salbrut',
            max = 300000,
            min = 0,
            ),
        ]

    scenario = reform.new_scenario().init_single_entity(
        axes = axes if bareme else None,
#        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        menage = menage,
        period = periods.period('year', year),
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)

    print("final", reform_simulation.calculate("af"))
    print reference_simulation

    return reform_simulation, reference_simulation



def test_remove_null():
    reform_simulation, reference_simulation = create_simulation()
    data_frame = data_frame_from_decomposition_json(
        reform_simulation,
        decomposition_json = None,
        reference_simulation = reference_simulation,
        remove_null = True)
    data_frame.to_excel('IDEP.xlsx', sheet_name='Sheet1',  engine='xlsxwriter')
    print data_frame


if __name__ == '__main__':
 #   test()
    test_remove_null()
