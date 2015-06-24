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
from openfisca_core import periods, web_tools

from modulation_allocations_familiales.reforms import prolongement_legislation_af_plaf_qf_2011
from openfisca_france.tests import base


def test_prolongement_legislation_af_plaf_qf_2011():
    error_margin = 0.01
    year = 2018
    period = periods.period("year", year)
    reform = prolongement_legislation_af_plaf_qf_2011.build_reform(base.tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 40,
                min = 2000*12,
                max = 15000*12,
                name = 'salaire_de_base',
                ),
            ],
        period = period,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 1, 1, 1)),
 #           dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        menage = dict(statut_occupation = 4,
                  loyer = 1000,)
        )
 #   code.interact(local=locals())
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)

    print "le plafonde qf est de {} en {}".format(reform_simulation.legislation_at(periods.instant( year)).ir.plafond_qf.marpac,
                                                    year)
#    web_tools.open_trace_tool(scenario, ["rsa"])
 
    assert (reference_simulation.calculate("avantage_qf", period = year) <= reform_simulation.calculate("avantage_qf", period = year)).all
    assert (reference_simulation.calculate("avantage_qf", period = year)[-5::] < reform_simulation.calculate("avantage_qf", period = year)[-5::]).all



if __name__ == '__main__':
    import code
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_prolongement_legislation_af_plaf_qf_2011()
#TODO : demander a manu pourquoi webtools marche bien mais les prints des calculate ne renvoient pas les bons résultats ?

