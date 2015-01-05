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


from modulation_allocations_familiales.reforms import allocations_familiales_modulation
from openfisca_france.tests import base


def test_modulations_allocations_familiales_2gosses(age_parents = 40, age_enf1 = 9, age_enf2 = 9):
    reform = allocations_familiales_modulation.build_reform(base.tax_benefit_system)
    impact = 0
    first_year = 2014
    child_birth_year = 2014
    for year in range(first_year, 2019):
        scenario = reform.new_scenario().init_single_entity(
            axes = [
                dict(
    #                count = 10,
    #                min = 72000,
    #                max = 74000,
                    count = 10,
    #                min = 72000, #teste la monotonie sur le premier plafond.
    #                max = 73800,
    #                min = 96000,
    #                max = 97000,
                    min = 0,
                    max = 200000,
    #                name = 'br_pf'
                    name = 'sal'
                    ),
                ],
            period = year,
            parent1 = dict(birth = datetime.date(first_year - age_parents , 1, 1)),
            parent2 = dict(birth = datetime.date(first_year - age_parents , 1, 1)),
            enfants = [
                dict(birth = datetime.date(child_birth_year - age_enf1, 1, 1)),
                dict(birth = datetime.date(child_birth_year - age_enf2, 1, 1)),
                ],
            )
        print("impact", impact)
        reference_simulation = scenario.new_simulation(debug = True, reference = True)
        print reference_simulation.calculate("af")
        reform_simulation = scenario.new_simulation(debug = True)
        print reform_simulation.calculate("af")

        impact += reform_simulation.calculate("allocations_familiales") - reference_simulation.calculate("af")
        #    print('reforme')
        print("final", reform_simulation.calculate("allocations_familiales"))


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    test_modulations_allocations_familiales_2gosses(40, 16, 16)
