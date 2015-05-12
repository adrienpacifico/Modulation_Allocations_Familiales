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


def test(nb_enf = 2):

    start_year = 2020
    number_of_years = 30
    salaire_min = 0
    salaire_max = 250000
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



def print_options(all_p = False, compare = False, nb_enf = 2, print_benchmark1 = True, print_benchmark2 = True ):
    np.set_printoptions(precision=2, suppress=True, linewidth=190)
    benchmark1, benchmark2 =  test(nb_enf = nb_enf)

    if (all_p == True):
        for annee in range(2020, 2050):
        #        b1 = benchmark1.calculate('revdisp', period = str(annee))
        #        b2 = benchmark2.calculate('revdisp', period = str(annee))
        #        a += (b1 - b2)
        #        print(annee)
        #        print('b1', b1 == b2)
        #        print('a', a)
        #        af1 = benchmark1.calculate('af', period = str(annee))
        #        af2 = benchmark2.calculate('af', period = str(annee))
        #        print('af1', af1)
        #        print('af2', af2)
        #        af_majo1 = benchmark1.calculate('af_majo', period = str(annee))
        #        af2_majo2 = benchmark2.calculate('af_majo', period = str(annee))
        #        print('af_majo', af1)
        #        print('af_majo', af2)
        #        marie = benchmark1.calculate('statmarit', period = str(annee))
        #        print('marie', marie)
            if (print_benchmark2 == True):
                print('*****', annee, 'benchmark2','**********')
            #        print('rev_trav', benchmark2.calculate('rev_trav', period = annee))
#                print('pen', benchmark2.calculate('pen', period = annee))
#                print('rev_cap', benchmark2.calculate('rev_cap', period = annee))
#                print('psoc', benchmark2.calculate('psoc', period = annee))

                print('pfam', benchmark2.calculate('pfam', period = annee))
                print('af_base', benchmark2.calculate('af_base', period = annee))
                print('af_majo', benchmark2.calculate('af_majo', period = annee))
                print('af_forf', benchmark2.calculate('af_forf', period = annee))


#                print('cf', benchmark2.calculate('cf', period = annee))
#                print('ars', benchmark2.calculate('ars', period = annee))
#                print('aeeh', benchmark2.calculate('aeeh', period = annee))
#                print('paje', benchmark2.calculate('paje', period = annee))
#                print('asf', benchmark2.calculate('asf', period = annee))
#                print('crds_pfam', benchmark2.calculate('crds_pfam', period = annee))

#                print('mini', benchmark2.calculate('mini', period = annee))
##                print('logt', benchmark2.calculate('logt', period = annee))
#
#
#
#                print('ppe', benchmark2.calculate('ppe', period = annee))
#                print('impo', benchmark2.calculate('impo', period = annee))


            if (print_benchmark1 == True):
                print('*****', annee, 'benchmark1','**********')

            #        print('rev_trav', benchmark1.calculate('rev_trav', period = annee))
#                print('pen', benchmark1.calculate('pen', period = annee))
#                print('rev_cap', benchmark1.calculate('rev_cap', period = annee))
#                print('psoc', benchmark1.calculate('psoc', period = annee))

                print('pfam', benchmark1.calculate('pfam', period = annee))
                print('af_base', benchmark1.calculate('af_base', period = annee))
                print('af_majo', benchmark1.calculate('af_majo', period = annee))
                print('af_forf', benchmark1.calculate('af_forf', period = annee))


                print('cf', benchmark1.calculate('cf', period = annee))
                print('ars', benchmark1.calculate('ars', period = annee))
#                print('aeeh', benchmark1.calculate('aeeh', period = annee))
#                print('paje', benchmark1.calculate('paje', period = annee))
#                print('asf', benchmark1.calculate('asf', period = annee))
#                print('crds_pfam', benchmark1.calculate('crds_pfam', period = annee))
#
#                print('mini', benchmark1.calculate('mini', period = annee))
##                print('logt', benchmark1.calculate('logt', period = annee))
#
#
#
#                print('ppe', benchmark1.calculate('ppe', period = annee))
#                print('impo', benchmark1.calculate('impo', period = annee))







        #        print(('rev_trav', benchmark1.calculate('rev_trav', period = annee) == ('rev_trav', benchmark1.calculate('rev_trav', period = annee))
#            print('pen', benchmark1.calculate('pen', period = annee))
#            print('rev_cap', benchmark1.calculate('rev_cap', period = annee))
#            print('psoc', benchmark1.calculate('psoc', period = annee))

            print('pfam', benchmark1.calculate('pfam', period = annee))
            print('af_base', benchmark1.calculate('af_base', period = annee))
            print('af_majo', benchmark1.calculate('af_majo', period = annee))
            print('af_forf', benchmark1.calculate('af_forf', period = annee))

#
#            print('cf', benchmark1.calculate('cf', period = annee))
#            print('ars', benchmark1.calculate('ars', period = annee))
#            print('aeeh', benchmark1.calculate('aeeh', period = annee))
#            print('paje', benchmark1.calculate('paje', period = annee))
#            print('asf', benchmark1.calculate('asf', period = annee))
#            print('crds_pfam', benchmark1.calculate('crds_pfam', period = annee))
#
#            print('mini', benchmark1.calculate('mini', period = annee))
###            print('logt', benchmark1.calculate('logt', period = annee))
#
#
#
#            print('ppe', benchmark1.calculate('ppe', period = annee))
#            print('impo', benchmark1.calculate('impo', period = annee))





    if (compare == True):
        key_list = ['pen', 'rev_cap',
        'psoc',  # presations sociales
          'pfam',  # prestations familiales
              'af',  # allocations familiales
                'af_base', 'af_majo', 'af_forf',
            'cf', 'ars', 'aeeh', 'paje',  # commentaire là
        'asf', 'crds_pfam',
        'mini', 'ppe',
        'impo',
        'revdisp']
#        for annee in range(2016, 2026):
#            print('*****', annee, 'Compare','**********')
##            print('rev_trav', benchmark2.calculate('rev_trav', period = annee))
#            print('pen', benchmark2.calculate('pen', period = annee) == benchmark1.calculate('pen', period = annee) )
#            print('rev_cap', benchmark2.calculate('rev_cap', period = annee) == benchmark1.calculate('rev_cap', period = annee))
#            print('psoc', benchmark2.calculate('psoc', period = annee) == benchmark1.calculate('psoc', period = annee))
#
#            print('pfam', benchmark2.calculate('pfam', period = annee))
#            print('af_base', benchmark2.calculate('af_base', period = annee))
#            print('af_majo', benchmark2.calculate('af_majo', period = annee))
#            print('af_forf', benchmark2.calculate('af_forf', period = annee))
#
#
#            print('cf', benchmark2.calculate('cf', period = annee))
#            print('ars', benchmark2.calculate('ars', period = annee))
#            print('aeeh', benchmark2.calculate('aeeh', period = annee))
#            print('paje', benchmark2.calculate('paje', period = annee))
#            print('asf', benchmark2.calculate('asf', period = annee))
#            print('crds_pfam', benchmark2.calculate('crds_pfam', period = annee))
#
#            print('mini', benchmark2.calculate('mini', period = annee))
#            print('logt', benchmark2.calculate('logt', period = annee))
#
#
#
#            print('ppe', benchmark2.calculate('ppe', period = annee))
#            print('impo', benchmark2.calculate('impo', period = annee))
        np.set_printoptions(precision=2, suppress=True, linewidth=140)
        for annee in range(2020, 2050):
            for var in key_list:
                if not np.all(benchmark2.calculate(var, period = annee).round(1) == benchmark1.calculate(var, period = annee).round(1)):
                    print(annee, var, np.around((benchmark2.calculate(var, period = annee) - benchmark1.calculate(var, period = annee))))
#                print(annee, 'af_base', np.around((benchmark2.calculate('af_base', period = annee))))
#                print(annee, 'af_majo', np.around((benchmark2.calculate('af_majo', period = annee))))
#                print(annee, 'af_forf', np.around((benchmark2.calculate('af_forf', period = annee))))
#                    print(annee, 'avantage_qf', np.around((benchmark2.calculate('avantage_qf', period = annee) - benchmark1.calculate('avantage_qf', period = annee))))
#                print('revenu disponible1', benchmark1.calculate('revdisp', period = annee))
#                print('revenu disponible2', benchmark2.calculate('revdisp', period = annee))
    return 2


def dataframe_result(nb_enf = 5):

    benchmark1, benchmark2 = test(nb_enf = nb_enf)
    life_cycle_impact = pd.DataFrame


    key_list = [
    'psoc',  # presations sociales
      'pfam',  # prestations familiales
          'af',  # allocations familiales
            'af_base', 'af_majo', 'af_forf', 'crds_pfam',
        'cf', 'ars', 'paje',  # commentaire là
        'aide_logement',
    'asf', #Allocation de soutien familial
    'mini', 'ppe',
    'impo',
    'revdisp']
    step = 2 + nb_enf
    dataframe1 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])
    dataframe2 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])

    np.set_printoptions(precision=2, suppress=True, linewidth=140)
    writer1 = pd.ExcelWriter('modulation_af_' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer2 = pd.ExcelWriter('plaf_qf_2012_' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer3 = pd.ExcelWriter('impact_modu_vs_qf' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer4 = pd.ExcelWriter('life_cycle_impact' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    start = 2020
    end = 2024 + 1
    for annee in range(2020, 2025):
        for var in key_list:
            if benchmark1.calculate(var, period = annee).shape > (80,):
                print('wrong size for: ', var)


            df1 = pd.DataFrame(benchmark1.calculate(var, period = annee), columns = [var])
            dataframe1[var] = df1
            df2 = pd.DataFrame(benchmark2.calculate(var, period = annee), columns = [var])
            dataframe2[var] = df2
        dataframe1.T.to_excel(writer1, sheet_name ='{}'.format(annee))
        dataframe2.T.to_excel(writer2, sheet_name ='{}'.format(annee))

        impact = dataframe1 - dataframe2
        impact['salaire_mensuel_de_base'] = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel']) / 12
        impact['revdisponible'] = pd.DataFrame(data = benchmark1.calculate('revdisp', period = 2020), columns = ['revdisponible'])
        if annee == 2020:
            life_cycle_impact = impact * 0
        life_cycle_impact += impact
        impact.T.to_excel(writer3, sheet_name ='impact' + '{}'.format(annee))

    print life_cycle_impact.T
    life_cycle_impact['salaire_mensuel_de_base'] = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel'])/12
    life_cycle_impact['revdisponible'] = pd.DataFrame(data = benchmark1.calculate('revdisp', period = 2020), columns = ['revdisponible'])
    life_cycle_impact.T.to_excel(writer4, sheet_name ='impact_life_cycl_over_' + start - end + "_year" )

    writer1.save()
    writer2.save()
    writer3.save()
    writer4.save()
#                if not np.all(benchmark2.calculate(var, period = annee).round(1) == benchmark1.calculate(var, period = annee).round(1)):
#                    print(annee, var, np.around((benchmark2.calculate(var, period = annee) - benchmark1.calculate(var, period = annee))))
#                    a = pd.DataFrame(data = benchmark1.calculate(var, period = annee),columns = [var])
#                    print a

#                print(annee, var, np.around((benchmark2.calculate(var, period = annee) - benchmark1.calculate(var, period = annee))))
    print 'fini'


def dataframe_result_year(nb_enf = 5, annee = 0):

    benchmark1, benchmark2 = test(nb_enf = nb_enf)

    key_list = [
    'psoc',  # presations sociales
      'pfam',  # prestations familiales
          'af',  # allocations familiales
            'af_base', 'af_majo', 'af_forf', 'crds_pfam',
        'cf', 'ars', 'paje',  # commentaire là
        'aide_logement',
    'asf', #Allocation de soutien familial
    'mini', 'ppe',
    'impo',
    'revdisp']
    step = 2 + nb_enf
    dataframe1 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])
    dataframe2 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])


    np.set_printoptions(precision=2, suppress=True, linewidth=140)


    for var in key_list:
        if benchmark1.calculate(var, period = annee).shape > (80,):
            print('wrong size for: ', var)

        df1 = pd.DataFrame(benchmark1.calculate(var, period = annee), columns = [var])
        dataframe1[var] = df1
        df2 = pd.DataFrame(benchmark2.calculate(var, period = annee), columns = [var])
        dataframe2[var] = df2


    return dataframe1.T, dataframe2.T

def dataframe_over_year(nb_enf = 5):
        for annee in range(2020, 2022):
            df1, df2 = dataframe_result_year(nb_enf, annee)
            df1.to_excel('plaf_qf_2012_all_year.xlsx', sheet_name ='impact' + {}.format(annee), engine = 'xlsxwriter')




if __name__ == '__main__':
    import logging
    import sys
    import matplotlib
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    df, df2 = test(nb_enf = 0)
#    print_options(True, False, nb_enf = 5)
    dataframe_result()
#    dataframe_over_year()




#
#    step = 2 + nb_enf + 1
#    dataframe1 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])
#    dataframe1.to_excel('plaf_qf_2012.xlsx', sheet_name='del', engine='xlsxwriter')
#    dataframe2 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])
#    dataframe1.to_excel('plaf_qf_2012.xlsx', sheet_name='del', engine='xlsxwriter')
#
#    np.set_printoptions(precision=2, suppress=True, linewidth=140)
#
#    for annee in range(2020, 2021):
#        for var in key_list:
#            if benchmark1.calculate(var, period = annee).shape > (80,):
#                print('wrong size for: ', var)
#
#            df1 = pd.DataFrame(benchmark1.calculate(var, period = annee), columns = [var])
#            dataframe1[var] = b1
#        writer1 = ExcelWriter('plaf_qf_2012.xlsx')
#        dataframe1.to_excel(writer1,"{}".format(year))
#
#        writer2 = ExcelWriter('modu_af.xlsx')
#        df2 = pd.DataFrame(benchmark2.calculate(var, period = annee), columns = [var])
#        df1.to_excel('plaf_qf_2012.xlsx', sheet_name='impact', engine='xlsxwriter')
#        writer1.save()







#>>> writer = ExcelWriter('output.xlsx')
#>>> df1.to_excel(writer,'Sheet1')
#>>> df2.to_excel(writer,'Sheet2')
#>>> writer.save()
#
#    a = pd.DataFrame(np.array([True, True]), columns = {'a'})






#    print benchmark1.calculate('revdisp', period = "2017") - benchmark2.calculate('revdisp', period = "2017")

    # df2.to_excel('IDEP2.xlsx', sheet_name='plafqf2012', engine='xlsxwriter')
#    print benchmark2.calculate('af', period = "2016")
#    a = (benchmark1.calculate('revdisp', period = "2017") - benchmark2.calculate('revdisp', period = "2017")
#    print a
#
#    a = np.zeros(len(benchmark2.calculate('revdisp', period = str(2015))))



#    rev_trav + pen + rev_cap + psoc + ppe + impo
##    a = np.array
#    for annee in range(2016, 2026):
#        b1 = benchmark1.calculate('revdisp', period = str(annee))
#        b2 = benchmark2.calculate('revdisp', period = str(annee))
#        a += (b1 - b2)
#        print(annee)
#        print('b1', b1 == b2)
#        print('a', a)
#        af1 = benchmark1.calculate('af', period = str(annee))
#        af2 = benchmark2.calculate('af', period = str(annee))
#        print('af1', af1)
#        print('af2', af2)
#        af_majo1 = benchmark1.calculate('af_majo', period = str(annee))
#        af2_majo2 = benchmark2.calculate('af_majo', period = str(annee))
#        print('af_majo', af1)
#        print('af_majo', af2)
#        marie = benchmark1.calculate('statmarit', period = str(annee))
#        print('marie', marie)
#
#        print('*****', annee, 'benchmark2','**********')
##        print('rev_trav', benchmark2.calculate('rev_trav', period = annee))
#        print('pen', benchmark2.calculate('pen', period = annee))
#        print('rev_cap', benchmark2.calculate('rev_cap', period = annee))
#        print('psoc', benchmark2.calculate('psoc', period = annee))
#
#        print('pfam', benchmark2.calculate('pfam', period = annee))
#        print('af_base', benchmark2.calculate('af_base', period = annee))
#        print('af_majo', benchmark2.calculate('af_majo', period = annee))
#        print('af_forf', benchmark2.calculate('af_forf', period = annee))
#
#
#        print('cf', benchmark2.calculate('cf', period = annee))
#        print('ars', benchmark2.calculate('ars', period = annee))
#        print('aeeh', benchmark2.calculate('aeeh', period = annee))
#        print('paje', benchmark2.calculate('paje', period = annee))
#        print('asf', benchmark2.calculate('asf', period = annee))
#        print('crds_pfam', benchmark2.calculate('crds_pfam', period = annee))
#
#        print('mini', benchmark2.calculate('mini', period = annee))
#        print('logt', benchmark2.calculate('logt', period = annee))
#
#
#
#        print('ppe', benchmark2.calculate('ppe', period = annee))
#        print('impo', benchmark2.calculate('impo', period = annee))
#
#
#
#        print('*****', annee, 'benchmark1','**********')
#
##        print('rev_trav', benchmark1.calculate('rev_trav', period = annee))
#        print('pen', benchmark1.calculate('pen', period = annee))
#        print('rev_cap', benchmark1.calculate('rev_cap', period = annee))
#        print('psoc', benchmark1.calculate('psoc', period = annee))
#
#        print('pfam', benchmark1.calculate('pfam', period = annee))
#        print('af_base', benchmark1.calculate('af_base', period = annee))
#        print('af_majo', benchmark1.calculate('af_majo', period = annee))
#        print('af_forf', benchmark1.calculate('af_forf', period = annee))
#
#
#        print('cf', benchmark1.calculate('cf', period = annee))
#        print('ars', benchmark1.calculate('ars', period = annee))
#        print('aeeh', benchmark1.calculate('aeeh', period = annee))
#        print('paje', benchmark1.calculate('paje', period = annee))
#        print('asf', benchmark1.calculate('asf', period = annee))
#        print('crds_pfam', benchmark1.calculate('crds_pfam', period = annee))
#
#        print('mini', benchmark1.calculate('mini', period = annee))
#        print('logt', benchmark1.calculate('logt', period = annee))
#
#
#
#        print('ppe', benchmark1.calculate('ppe', period = annee))
#        print('impo', benchmark1.calculate('impo', period = annee))
#
#
#
#
#
#
#
##        print(('rev_trav', benchmark1.calculate('rev_trav', period = annee) == ('rev_trav', benchmark1.calculate('rev_trav', period = annee))
#        print('pen', benchmark1.calculate('pen', period = annee))
#        print('rev_cap', benchmark1.calculate('rev_cap', period = annee))
#        print('psoc', benchmark1.calculate('psoc', period = annee))
#
#        print('pfam', benchmark1.calculate('pfam', period = annee))
#        print('af_base', benchmark1.calculate('af_base', period = annee))
#        print('af_majo', benchmark1.calculate('af_majo', period = annee))
#        print('af_forf', benchmark1.calculate('af_forf', period = annee))
#
#
#        print('cf', benchmark1.calculate('cf', period = annee))
#        print('ars', benchmark1.calculate('ars', period = annee))
#        print('aeeh', benchmark1.calculate('aeeh', period = annee))
#        print('paje', benchmark1.calculate('paje', period = annee))
#        print('asf', benchmark1.calculate('asf', period = annee))
#        print('crds_pfam', benchmark1.calculate('crds_pfam', period = annee))
#
#        print('mini', benchmark1.calculate('mini', period = annee))
#        print('logt', benchmark1.calculate('logt', period = annee))
#
#
#
#        print('ppe', benchmark1.calculate('ppe', period = annee))
#        print('impo', benchmark1.calculate('impo', period = annee))
#
#
#
#
#
#    print('resultat', a)




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
