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

from nose.tools import assert_less

from openfisca_france.reforms import allocations_familiales_modulation
from openfisca_france.tests import base


def test_modulations_allocations_familiales():
    year = 2014
    reform = allocations_familiales_modulation.build_reform(base.tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 20,
                max = 200000,
                min = 0,
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
#    print reference_simulation.calculate("af")
    reform_simulation = scenario.new_simulation(debug = True)
#    print('reforme')
    print("final", reform_simulation.calculate("allocations_familiales"))


#    error_margin = 0.01
#
#    rfr = reference_simulation.calculate('rfr')
#    expected_rfr = [13247, 13338, 13429, 13520, 13611, 13703, 13793, 13884, 13975, 14066]
#    assert_less(max(abs(expected_rfr - rfr)), error_margin)
#
#    impo = reference_simulation.calculate('impo')
#    expected_impo = [-249.11, -268.22, -287.33, -306.44, -325.55, -344.87, -363.77, -382.88, -401.99, -421.1]
#    assert_less(max(abs(expected_impo - impo)), error_margin)
#
#    reform_simulation = scenario.new_simulation(debug = True)
#    reform_reduction_impot_exceptionnelle = reform_simulation.calculate('reduction_impot_exceptionnelle')
#    expected_reform_reduction_impot_exceptionnelle = [350, 350, 350, 350, 350, 350, 350, 261, 170, 79]
#    assert_less(max(abs(expected_reform_reduction_impot_exceptionnelle - reform_reduction_impot_exceptionnelle)),
#        error_margin)
#
#    reform_rfr = reform_simulation.calculate('rfr')
#    assert_less(max(abs(expected_rfr - reform_rfr)), error_margin)  # rfr must be the same than before reform
#
#    reform_impo = reform_simulation.calculate('impo')
#    expected_reform_impo = [0, 0, 0, 0, 0, 0, 0, -121.88, -231.99, -342.1]
#    assert_less(max(abs(expected_reform_impo - reform_impo)), error_margin)


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_modulations_allocations_familiales()
