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


from openfisca_matplotlib.dataframes import data_frame_from_decomposition_json

from openfisca_core import periods


from modulation_allocations_familiales.reforms import af_modulation
from modulation_allocations_familiales.reforms import prolongement_legislation_af_plaf_qf_2011
from openfisca_france.tests import base


def benchmark_modu_af(axes = None, bareme = False, menage = None, parent1 = None, parent2 = None, enfants = None,
                      period = None):
    reform_modu_af = af_modulation.build_reform(base.tax_benefit_system)
    scenario = reform_modu_af.new_scenario().init_single_entity(
        axes = axes if bareme else None,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
        )
    return scenario.new_simulation(debug = True)


def bechmark_plaf_qf(axes = None, bareme = False, menage = None, parent1 = None, parent2 = None, enfants = None,
                     period = None):
    reform_plaf_qf = prolongement_legislation_af_plaf_qf_2011.build_reform(base.tax_benefit_system)
    scenario = reform_plaf_qf.new_scenario().init_single_entity(
        axes = axes if bareme else None,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
        )
    return scenario.new_simulation(debug = True)

def test():
    year = 2014
    axes = [
        dict(
            count = 20,
            max = 200000,
            min = 0,
            name = 'salaire_de_base'
            ),
        ]
    parent1 = dict(birth = datetime.date(year - 40, 1, 1))
    parent2 = dict(birth = datetime.date(year - 40, 1, 1))
    enfants = [
        dict(birth = datetime.date(year - 9, 1, 1)),
        dict(birth = datetime.date(year - 9, 1, 1)),
        ]
    menage = dict(
        loyer = 1000,
        so = 4,
        )
    bareme = True
    period = "2013:5"  # periods.period('year', year - 2, 3),

    benchmark1 = benchmark_modu_af(
        axes = axes,
        bareme = bareme,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
        )

    df = data_frame_from_decomposition_json(
        benchmark1,
        decomposition_json = None,
        remove_null = True)

    print benchmark1.calculate('af', period = "2016")
    print benchmark1.calculate('psoc', period = "2016")
    print df
    # df.to_excel('IDEP.xlsx', sheet_name='modulation_af', engine='xlsxwriter')

    benchmark2 = bechmark_plaf_qf(
        axes = axes,
        bareme = bareme,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
        )
    df2 = data_frame_from_decomposition_json(
        benchmark2,
        decomposition_json = None,
        remove_null = True)

    # df2.to_excel('IDEP2.xlsx', sheet_name='plafqf2012', engine='xlsxwriter')
    print benchmark2.calculate('af', period = "2016")
    return df, df2


if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    df, df2 = test()

















#
#def benchmark_perte_af_plafqf(age_parents = 40, age_enf1 = 9, age_enf2 = 9):
#    reform1 = anticipation_modulation_af_2015.build_reform(base.tax_benefit_system)
#    reform2 = prolongement_legislation_af_plaf_qf_2011.build_reform(base.tax_benefit_system)
#    impact = 0
#    first_year = 2014
#    child_birth_year = 2014
#
#
#    count = 5
#    min = 0
#    max = 100000
#
#
#
#    for year in range(first_year, 2019):
#        scenario1 = reform1.new_scenario().init_single_entity(
#            axes = [
#                dict(
#                    count = count,
#                    min = min,
#                    max = max,
#                    name = 'sal'
#                    ),
#                ],
#            period = year,
#            parent1 = dict(birth = datetime.date(first_year - age_parents , 1, 1)),
#            parent2 = dict(birth = datetime.date(first_year - age_parents , 1, 1)),
#            enfants = [
#                dict(birth = datetime.date(child_birth_year - age_enf1, 1, 1)),
#                dict(birth = datetime.date(child_birth_year - age_enf2, 1, 1)),
#                ],
#            )
#        scenario2 = reform2.new_scenario().init_single_entity(
#            axes = [
#                dict(
#                    count = count,
#                    min = min,
#                    max = max,
#                    name = 'sal'
#                    ),
#                ],
#            period = year,
#            parent1 = dict(birth = datetime.date(first_year - age_parents , 1, 1)),
#            parent2 = dict(birth = datetime.date(first_year - age_parents , 1, 1)),
#            enfants = [
#                dict(birth = datetime.date(child_birth_year - age_enf1, 1, 1)),
#                dict(birth = datetime.date(child_birth_year - age_enf2, 1, 1)),
#                ],
#            )
#
#        reference_simulation = scenario1.new_simulation(debug = True, reference = True)
#        print reference_simulation.calculate("af")
#        reform_simulation = scenario2.new_simulation(debug = True)
#        print reform_simulation.calculate("af")
#
#        impact += reform_simulation.calculate("af") - reference_simulation.calculate("af")
#        #    print('reforme')
#    print("final", impact)
