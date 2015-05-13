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
import numpy as np

from openfisca_matplotlib.dataframes import data_frame_from_decomposition_json


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




def impact_over_year(year, age_enf = 3, start_year = 2014, nb_enf = 0):


    number_of_years = 30
    salaire_min = 0
    salaire_max = 250000
    fill_year = start_year - 2
    axes = [
        dict(
            count = 70,
            max = salaire_max * (number_of_years + 2),
            min = salaire_min * (number_of_years + 2),
            name = 'salaire_de_base',
            ),
        ]
    parent1 = dict(birth = datetime.date(start_year - 40, 1, 1))
    parent2 = dict(birth = datetime.date(start_year - 40, 1, 1))
    menage = dict(
        loyer = 1000,
        so = 4,
        )
    bareme = True
    period = "{}:{}".format(fill_year, number_of_years + 2)
    enfants = [dict(birth = datetime.date(start_year - age_enf + (start_year - year), 1, 1))] * nb_enf

    benchmark1 = benchmark_modu_af(
        axes = axes,
        bareme = bareme,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = [dict(birth = datetime.date(start_year - age_enf + (start_year - year), 1, 1))] * nb_enf,
        period = period,
        )

    benchmark2 = bechmark_plaf_qf(
        axes = axes,
        bareme = bareme,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = [dict(birth = datetime.date(start_year - age_enf + (start_year - year), 1, 1))] * nb_enf,
        period = period,
        )

    return benchmark1, benchmark2, (start_year - age_enf - year)


def result(nb_enf = 3 , age_enf = 3, start_year = 2014):
    np.set_printoptions(precision=2, suppress=True, linewidth=140)

    fill_year = start_year - 2

    #juste pour avoir un vecteur nul de la bonne taille.
    benchmark1, benchmark2, age_enf_in_simul = impact_over_year(2016, age_enf, start_year, nb_enf)
    agregate_impact = np.zeros(len(benchmark2.calculate('revdisp', period = str(2015))))


    compare = False
    for year in range(2016, 2025):
        if (compare == True):
            key_list = ['pen', 'rev_cap',
            'psoc',  # presations sociales
              'pfam',  # prestations familiales
                  'af',  # allocations familiales
                    'af_base', 'af_majo', 'af_forf',
                'cf', 'ars', 'aeeh', 'paje',  # commentaire là
            'asf', 'crds_pfam',
            'mini', 'logt', 'ppe',
            'impo',
            'revdisp']



                benchmark1, benchmark2, age_enf_in_simul = impact_over_year(year, age_enf, start_year, nb_enf)
                for var in key_list:
                    if not np.all(benchmark2.calculate(var, 2018).round(1) == benchmark1.calculate(var, period = 2018).round(1)):
                        print('age_enf_in_simul', age_enf_in_simul, var, np.around((benchmark2.calculate(var, period = 2018) - benchmark1.calculate(var, period = 2018))))
                agregate_impact += np.around((benchmark2.calculate('revdisp', period = 2018) - benchmark1.calculate('revdisp', period = 2018))) #TODO : regarder si années différentes changements !
        print((year, 'af_majo', benchmark2.calculate('af_majo', period = 2018), 'age_enf_in_simul', age_enf_in_simul))


        print(year, 'agregate_impact', agregate_impact)





if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
    result(nb_enf = 3 , age_enf = 3, start_year = 2014)

