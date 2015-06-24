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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE,  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program,  If not, see <http://www.gnu.org/licenses/>.


import datetime

from openfisca_core.tools import assert_near
from openfisca_core import periods

from modulation_allocations_familiales.reforms import af_modulation2
from openfisca_france.tests import base


def test_non_plaf_qf():
    error_margin = 0.01
    year = 2020
    period = periods.period("month", str(year) + '-01')
    reform = af_modulation2.build_reform(base.tax_benefit_system)
    count = 100
    salaire_imposable_maximal = 100000
    variable_for_axes = 'salaire_imposable'
    scenario = reform.new_scenario().init_single_entity(
        axes = [[
            dict(
                count = count,
                min = 0,
                max = salaire_imposable_maximal,
                name = 'salaire_imposable',
                period = year-2,
                ),
            dict(
                count = count,
                min = 0,
                max = salaire_imposable_maximal,
                name = 'salaire_imposable',
                period = year-1,
                ),
            dict(
                count = count,
                min = 0,
                max = salaire_imposable_maximal,
                name = 'salaire_imposable',
                period = year,
                ),
            ]],
        period = period,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    


##    web_tools.open_trace_tool(scenario, ["salaire_net_a_payer"], 'http://api-test.openfisca.fr')
#    print reform_simulation.calculate("salaire_net_a_payer", period = "{}-01".format(year))*12
##    print reference_simulation.calculate_add("af", period = year)
#    print reform_simulation.calculate_add("af", period = year)
    import numpy as np
    np.set_printoptions( precision = 2, suppress =True) 
    assert (reference_simulation.calculate_add("af", period = year)+0.1 >= reform_simulation.calculate_add("af", period = year)).all
    assert ((reference_simulation.calculate_add("af", period = year)[-10:] > reform_simulation.calculate_add("af", period = year)[-10:]+100)).all
if __name__ == '__main__':
    import code
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_non_plaf_qf()
#    code.interact(local=locals())
