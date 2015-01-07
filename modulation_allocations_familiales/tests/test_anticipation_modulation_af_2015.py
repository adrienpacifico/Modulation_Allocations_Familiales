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

from modulation_allocations_familiales.reforms import anticipation_modulation_af_2015
from openfisca_france.tests import base


def test_af():
    year = 2010
    period = periods.period("year", year, 10)
    test_year = 2015
    test_period = periods.period("month", "{}-12".format(test_year))

    reform = anticipation_modulation_af_2015.build_reform(base.tax_benefit_system)
    scenario = reform.new_scenario().init_single_entity(
        axes = [
            dict(
                count = 20,
                max = 200000 * 10,
                min = 0,
                name = 'sal'
                ),
            ],
        period = period,
        parent1 = dict(birth = datetime.date(year - 40, 1, 1)),
        parent2 = dict(birth = datetime.date(year - 40, 1, 1)),
        enfants = [
            dict(birth = datetime.date(year - 9, 1, 1)),
            dict(birth = datetime.date(year - 9, 1, 1)),
            ],
        )

    reference_simulation = scenario.new_simulation(debug = True, reference = True)
    reform_simulation = scenario.new_simulation(debug = True)
    assert (reference_simulation.calculate("af", period = test_period)[:8].round(2) == 194.98).all()
    assert (reference_simulation.calculate("af", period = test_period)[-9:].round(2) == 97.49).all()
    assert (reform_simulation.calculate("af", period = test_period).round(2) == 194.98).all()


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_af()
