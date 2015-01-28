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
import pandas as pd

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



def test(nb_enf = 2):

    start_year = 2020
    number_of_years = 30
    salaire_min = 0
    salaire_max = 200000
    fill_year = start_year - 2
    axes = [
        dict(
            count = 55,
            max = salaire_max * (number_of_years + 2),
            min = salaire_min * (number_of_years + 2),
            name = 'salaire_de_base',
            ),
        ]
    parent1 = dict(birth = datetime.date(start_year - 40, 1, 1))
    parent2 = dict(birth = datetime.date(start_year - 40, 1, 1))
    enfants = [dict(birth = datetime.date(start_year - 0, 1, 1))] * nb_enf
    menage = dict(
        loyer = 1000,
        so = 4,
        )
    bareme = True
    period = "{}:{}".format(fill_year, number_of_years + (start_year - fill_year))

    benchmark1 = benchmark_modu_af(
        axes = axes,
        bareme = bareme,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
        )

    benchmark2 = bechmark_plaf_qf(
        axes = axes,
        bareme = bareme,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
        )




    return benchmark1, benchmark2




def dataframe_result(nb_enf = 5):
    import time

    tps1 = time.clock()

    benchmark1, benchmark2 = test(nb_enf = nb_enf)
    life_cycle_impact = pd.DataFrame
    etape1 = tps1 - time.clock()


    print etape1

    tps2 = time.clock()

    key_list = ['revdisp',
    'psoc',  # presations sociales
      'pfam',  # prestations familiales
          'af',  # allocations familiales
            'af_base', 'af_majo', 'af_forf', 'crds_pfam',
        'cf', 'ars', 'paje',  # commentaire là
        'aide_logement',
    'asf', #Allocation de soutien familial
    'mini', 'ppe',
    'impo']

    step = 2 + nb_enf
    dataframe1 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])
    dataframe2 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])

    print(tps1 - time.clock())
    np.set_printoptions(precision=2, suppress=True, linewidth=140)
    writer1 = pd.ExcelWriter('modulation_af_' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer2 = pd.ExcelWriter('plaf_qf_2012_' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer3 = pd.ExcelWriter('impact_modu_vs_qf' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer4 = pd.ExcelWriter('life_cycle_impact' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')

    start = 2020
    end = 2022 + 1

    etape2 = tps2 - time.clock()
    print etape2

    for annee in range(start, end):
        tps_boucle_annee = time.clock()

        for var in key_list:

#            if benchmark1.calculate(var, period = annee).shape > (80,):
#                print('wrong size for: ', var)
            df1 = pd.DataFrame(benchmark1.calculate(var, period = annee), columns = [var])
            dataframe1[var] = df1
            df2 = pd.DataFrame(benchmark2.calculate(var, period = annee), columns = [var])
            dataframe2[var] = df2
        dataframe1.T.to_excel(writer1, sheet_name ='{}'.format(annee))
        dataframe2.T.to_excel(writer2, sheet_name ='{}'.format(annee))

        impact = dataframe1 - dataframe2
        impact['salaire_mensuel_brut'] = pd.DataFrame(data = benchmark2.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel']) / 12
        impact['revdisponible_qf2012'] = pd.DataFrame(data = benchmark2.calculate('revdisp', period = annee), columns = ['revdisponible'])
        if annee == 2020:
            life_cycle_impact = impact * 0
        life_cycle_impact += impact
        impact.T.to_excel(writer3, sheet_name ='impact' + '{}'.format(annee))
        print('temps_boucle_annee', tps_boucle_annee - time.clock())

    print life_cycle_impact.T
    life_cycle_impact['salaire_mensuel_brut'] = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel']) / 12
    life_cycle_impact['salaire_net_mensuel'] = pd.DataFrame(data = benchmark1.calculate('salnet', period = 2020)[::step], columns = ['salaire_net']) / 12
    life_cycle_impact['revdisponible'] = pd.DataFrame(data = benchmark2.calculate('revdisp', period = 2020), columns = ['revdisponible'])
    life_cycle_impact['impact_en_pourcentage'] =  (-1 + (life_cycle_impact['revdisponible_qf2012'] + life_cycle_impact['revdisp'])/life_cycle_impact['revdisponible_qf2012']) * 100
    life_cycle_impact.T.to_excel(writer4, sheet_name ='impact_life_cycl_over_' + "{}".format(start - end) + "_year" )

    writer1.save()
    writer2.save()
    writer3.save()
    writer4.save()
    print 'fini'


if __name__ == '__main__':
    import logging
    import sys
    import matplotlib
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)

    dataframe_result(nb_enf = 4)