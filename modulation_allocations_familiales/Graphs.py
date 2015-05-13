# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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

from __future__ import division


import datetime
import sys


from openfisca_france.reforms import allocations_familiales_modulation
from openfisca_france.tests import base


from openfisca_matplotlib import graphs





def test_modulations_allocations_familiales():
    year = 2014
    reform = allocations_familiales_modulation.build_reform(base.tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 10,
#                min = 72000, #teste la monotonie sur le premier plafond.
#                max = 73800,
#                min = 96000, #sur le deuxième
#                max = 97000,
                min = 0,
                max = 200000,
#                name = 'br_pf'
                name = 'sali'
                ),
            ],
        period = year,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    print reference_simulation.calculate("af")
    reform_simulation = scenario.new_simulation(debug = True)
    print("final", reform_simulation.calculate("allocations_familiales"))


def rates():
    reform_simulation, reference_simulation = create_simulation(bareme = True)
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    axes = win.mplwidget.axes
    graphs.draw_rates(
        simulation = reform_simulation,
        axes = axes,
        x_axis = 'sali',
        y_axis = 'revdisp',
        reference_simulation = reference_simulation,
        )
    win.resize(1400, 700)
    win.mplwidget.draw()
    win.show()
    sys.exit(app.exec_())

def create_simulation(year = 2014, bareme = False):

    simulation_period = periods.period('year', year)
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = reforms.update_legislation(
        legislation_json = reference_legislation_json,
        path = ('children', 'ir', 'children', 'bareme', 'slices', 0, 'rate'),
        period = simulation_period,
        value = 1,
        )

    reform = reforms.Reform(
        name = u'IR_100_tranche_1',
        label = u"Imposition à 100% dès le premier euro et jusqu'à la fin de la 1ère tranche",
        legislation_json = reform_legislation_json,
        reference = tax_benefit_system
        )
    parent1 = dict(
        birth = datetime.date(year - 40, 1, 1),
        sali = 10000 if bareme is False else None,
        )
#    parent2 = dict(
#        birth = datetime.date(year - 40, 1, 1),
#        sali = 0,
#        )
    # Adding a husband/wife on the same tax sheet (foyer)
    menage = dict(
        loyer = 1000,
        so = 4,
        )
    axes = [
        dict(
            count = 200,
            name = 'sali',
            max = 300000,
            min = 0,
            ),
        ]
    scenario = reform.new_scenario().init_single_entity(
        axes = axes if bareme else None,
#        menage = menage,
        parent1 = parent1,
#        parent2 = parent2,
        period = periods.period('year', year),
        )
    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)

    return reform_simulation, reference_simulation