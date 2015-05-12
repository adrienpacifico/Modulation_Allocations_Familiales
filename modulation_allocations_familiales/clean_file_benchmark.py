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


from modulation_allocations_familiales.reforms import af_modulation_sur_salnet

from modulation_allocations_familiales.reforms import af_modulation2
from modulation_allocations_familiales.reforms import prolongement_legislation_af_plaf_qf_2011
from modulation_allocations_familiales.reforms import modu_af_juillet
from openfisca_france.tests import base





def benchmark_modu_af(axes = None, bareme = False, menage = None, parent1 = None, parent2 = None, enfants = None,
                      period = None):
    reform_modu_af = af_modulation_sur_salnet.build_reform(base.tax_benefit_system)
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

def simul_modu_juillet(axes = None, bareme = False, menage = None, parent1 = None, parent2 = None, enfants = None,
                     period = None):
    reform_plaf_qf = modu_af_juillet.build_reform(base.tax_benefit_system)
    scenario = reform_plaf_qf.new_scenario().init_single_entity(
        axes = axes if bareme else None,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
    )
    return scenario.new_simulation(debug = True)



def test(nb_enf = 2, age_enf = 0):

    start_year = 2020
    number_of_years = 30
    salaire_min = 70000
    salaire_max = 220000
    fill_year = start_year - 2
    axes = [
        dict(
            count = 1601,
            max = salaire_max * (number_of_years + 2),
            min = salaire_min * (number_of_years + 2),
            name = 'salaire_de_base',
            ),
        ]
    parent1 = dict(birth = datetime.date(start_year - 40, 1, 1), statmarit = 1,)
    parent2 = dict(birth = datetime.date(start_year - 40, 1, 1), statmarit = 1,)
    enfants = [dict(birth = datetime.date(start_year - age_enf, 1, 1))] * nb_enf
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

    simulation_modu_juillet = simul_modu_juillet(
        axes = axes,
        bareme = bareme,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = period,
        )
    return benchmark1, benchmark2, simulation_modu_juillet




def dataframe_result(nb_enf = 5, nb_year_of_simulation = 20, age_enf = 6):
    import time

    tps1 = time.clock()

    benchmark1, benchmark2, simulation_modu_juillet = test(nb_enf = nb_enf, age_enf = age_enf)
    life_cycle_impact = pd.DataFrame
#    etape1 = tps1 - time.clock()


#    print etape1

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
    'impo','salnet']

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
    end = 2020 + nb_year_of_simulation

    etape2 = tps2 - time.clock()
    print etape2

    for annee in range(start, end):
        tps_boucle_annee = time.clock()

        for var in key_list:

#            if benchmark1.calculate(var, period = annee).shape > (80,):
#                print('wrong size for: ', var)
            df1 = pd.DataFrame(benchmark1.calculate(var, period = annee), columns = [var])
            dataframe1[var] = df1.apply( np.round )
            df2 = pd.DataFrame(benchmark2.calculate(var, period = annee), columns = [var])
            dataframe2[var] = df2.apply( np.round )
        dataframe1.T.to_excel(writer1, sheet_name ='{}'.format(annee))
        dataframe2.T.to_excel(writer2, sheet_name ='{}'.format(annee))

        impact = dataframe1 - dataframe2
        impact['salaire_mensuel_brut'] = pd.DataFrame(data = benchmark2.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel']).apply( np.round ) / 12
        impact['revdisponible_qf2012'] = pd.DataFrame(data = benchmark2.calculate('revdisp', period = annee), columns = ['revdisponible'])
        if annee == 2020:
            life_cycle_impact = impact * 0
        if annee == 2020 + nb_year_of_simulation:
            life_cycle_impact += impact
        else :
            life_cycle_impact += impact
            life_cycle_impact = life_cycle_impact  #  * 1.02 # taux interet

        impact.T.to_excel(writer3, sheet_name ='impact' + '{}'.format(annee))
        print('temps_boucle_annee', tps_boucle_annee - time.clock())

#    print life_cycle_impact.T
    life_cycle_impact['base_ressource_presta_fam'] = (pd.DataFrame(data = benchmark1.calculate('br_pf', period = 2020), columns = ['br_pf'])/12).apply( np.round )
    life_cycle_impact['salaire_mensuel_brut'] = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel']) / 12
    life_cycle_impact['salaire_net_mensuel'] = (pd.DataFrame(data = benchmark1.calculate('salnet', period = 2020) [::step], columns = ['salaire_net']) / 12).apply( np.round )
    life_cycle_impact['revdisponible'] = pd.DataFrame(data = benchmark1.calculate('revdisp', period = 2020), columns = ['revdisponible'])
    life_cycle_impact['impact_en_pourcentage'] =  (-1 + (life_cycle_impact['revdisponible_qf2012'] + life_cycle_impact['revdisp'])/life_cycle_impact['revdisponible_qf2012']) * 100
    life_cycle_impact.T.to_excel(writer4, sheet_name ='impact_life_cycl_over_' + "{}".format(start - end) + "_year" )

#    print life_cycle_impact['impact_en_pourcentage']

    writer1.save()
    writer2.save()
    writer3.save()
    writer4.save()
    print 'fini pour {}'.format(nb_enf)
    return dataframe1, dataframe2, life_cycle_impact, impact



def dataframe_result_taux(nb_enf = 5, nb_year_of_simulation = 20, age_enf = 6):
    import time

    tps1 = time.clock()

    benchmark1, benchmark2, simulation_modu_juillet = test(nb_enf = nb_enf, age_enf =  age_enf)
    life_cycle_impact = pd.DataFrame
#    etape1 = tps1 - time.clock()


#    print etape1

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
    'impo', ]

    step = 2 + nb_enf
    dataframe1 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])
    dataframe2 = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base'])

    print(tps1 - time.clock())
    np.set_printoptions(precision=2, suppress=True, linewidth=140)
    writer1 = pd.ExcelWriter('modulation_af_taux' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer2 = pd.ExcelWriter('plaf_qf_2012_taux' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer3 = pd.ExcelWriter('impact_modu_vs_qf_taux' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')
    writer4 = pd.ExcelWriter('life_cycle_impact_taux' + '{}'.format(nb_enf) + 'enf.xlsx', engine = 'xlsxwriter')

    start = 2020
    end = 2020 + nb_year_of_simulation

    etape2 = tps2 - time.clock()
    print etape2

    for annee in range(start, end):
        tps_boucle_annee = time.clock()

        for var in key_list:

#            if benchmark1.calculate(var, period = annee).shape > (80,):
#                print('wrong size for: ', var)
            df1 = pd.DataFrame(benchmark1.calculate(var, period = annee), columns = [var])
            dataframe1[var] = df1.apply( np.round )
            df2 = pd.DataFrame(benchmark2.calculate(var, period = annee), columns = [var])
            dataframe2[var] = df2.apply( np.round )
        dataframe1.T.to_excel(writer1, sheet_name ='{}'.format(annee))
        dataframe2.T.to_excel(writer2, sheet_name ='{}'.format(annee))

        impact = dataframe1 - dataframe2
        impact['salaire_mensuel_brut'] = pd.DataFrame(data = benchmark2.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel']).apply( np.round ) / 12
        impact['revdisponible_qf2012'] = pd.DataFrame(data = benchmark2.calculate('revdisp', period = annee), columns = ['revdisponible'])
        if annee == 2020:
            life_cycle_impact = impact * 0
        if annee == 2020 + nb_year_of_simulation:
            life_cycle_impact += impact
        else :
            life_cycle_impact += impact
            life_cycle_impact = life_cycle_impact * 1.02 # taux interet

        impact.T.to_excel(writer3, sheet_name ='impact' + '{}'.format(annee))
        print('temps_boucle_annee', tps_boucle_annee - time.clock())

#    print life_cycle_impact.T
    life_cycle_impact['salaire_mensuel_brut'] = pd.DataFrame(data = benchmark1.calculate('salaire_de_base', period = 2020)[::step], columns = ['salaire_de_base_mensuel']) / 12
    life_cycle_impact['salaire_net_mensuel'] = (pd.DataFrame(data = benchmark1.calculate('salnet', period = 2020) [::step], columns = ['salaire_net']) / 12).apply( np.round )
    life_cycle_impact['revdisponible'] = pd.DataFrame(data = benchmark1.calculate('revdisp', period = 2020), columns = ['revdisponible'])
    life_cycle_impact['impact_en_pourcentage'] =  (-1 + (life_cycle_impact['revdisponible_qf2012'] + life_cycle_impact['revdisp'])/life_cycle_impact['revdisponible_qf2012']) * 100
    life_cycle_impact.T.to_excel(writer4, sheet_name ='impact_life_cycl_over_' + "{}".format(start - end) + "_year" )

#    print life_cycle_impact['impact_en_pourcentage']

    writer1.save()
    writer2.save()
    writer3.save()
    writer4.save()
    print 'fini pour {}'.format(nb_enf)
    return dataframe1, dataframe2, life_cycle_impact, impact



def graph( nb_year_of_simulation  = 1):
    from matplotlib import pyplot as plt
    plt.figure()
    for nb_enf in range(2, 4):
        print nb_enf
        dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = nb_enf, nb_year_of_simulation = nb_year_of_simulation )
        life_cycle_impact.T.index = life_cycle_impact.axes[1]
        life_cycle_impact = life_cycle_impact.T
        life_cycle_impact.T.plot('impact_en_pourcentage','salaire_mensuel_brut')
        plt.show()


    print u"et le graph ?"

def base_ressource_salimposable(nb_enf = 3 ):
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = nb_enf )
    print simulation_modu_juillet.calculate('br_pf', period = 2020) - simulation_modu_juillet.calculate('sal', period = 2020)[::2+nb_enf]

if __name__ == '__main__':
    import logging
    import sys

#    sys.path.append('usr/local/Cellar/')
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = 3)

#    base_ressource_salimposable(nb_enf = 3 )

#    perte_reelle(nb_enf = 5, nb_year_of_simulation = 1)

#    graph()

#    a,b,c = test()


#    nb_enf = 3
#    print perte_reelle()

    nb_year_of_simulation = 20
    age_enf = 0

    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = 1, nb_year_of_simulation =  nb_year_of_simulation, age_enf = age_enf)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = 2, nb_year_of_simulation =  nb_year_of_simulation, age_enf = age_enf)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = 3, nb_year_of_simulation =  nb_year_of_simulation, age_enf = age_enf)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = 4, nb_year_of_simulation =  nb_year_of_simulation, age_enf = age_enf)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = 5, nb_year_of_simulation =  nb_year_of_simulation, age_enf = age_enf)
###
    nb_year_of_simulation = 20
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result_taux(nb_enf = 1, nb_year_of_simulation = nb_year_of_simulation, age_enf = 0)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result_taux(nb_enf = 2, nb_year_of_simulation = nb_year_of_simulation, age_enf = 0)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result_taux(nb_enf = 3, nb_year_of_simulation = nb_year_of_simulation, age_enf = 0)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result_taux(nb_enf = 4, nb_year_of_simulation = nb_year_of_simulation, age_enf = 0)
    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result_taux(nb_enf = 5, nb_year_of_simulation = nb_year_of_simulation, age_enf = 0)


#    dataframe1, dataframe2, life_cycle_impact, impact = dataframe_result(nb_enf = 6)

#






#
#
#
#
#def perte_reelle(nb_enf = 5, nb_year_of_simulation = 1):
#    np.set_printoptions(suppress=True, precision=2)
#    print 'hello1'
#    benchmark1, benchmark2, simulation_modu_juillet = test(nb_enf = nb_enf)
#
#
#    key_list = ['revdisp',
#    'psoc',  # presations sociales
#      'pfam',  # prestations familiales
#          'af',  # allocations familiales
#            'af_base', 'af_majo', 'af_forf', 'crds_pfam',
#        'cf', 'ars', 'paje',  # commentaire là
#        'aide_logement',
#    'asf', #Allocation de soutien familial
#    'mini', 'ppe',
#    'impo']
#    dico_perte = dict()
#
#    for var in key_list:
#        print 'hello2{}'.format(var)
#        perte = np.zeros(simulation_modu_juillet.calculate(var, period = 2020).shape)
#        print 'hello3{}'.format(var)
#        sal = simulation_modu_juillet.calculate('sal', period = 2020)[::2+nb_enf]
#        for nb_year in range(1 , nb_year_of_simulation+1):
#            perte += simulation_modu_juillet.calculate(var, period = 2020+nb_year)\
#                        - benchmark2.calculate(var, period = 2020+nb_year)
#            print 'hello3{}'.format(var)
#
#        list_of_tupple = []
#        for i in range(0,sal.shape[0]):
#            list_of_tupple += [(sal[i],perte[i])]
#        dico_perte['perte {} en {} ans'.format(var, nb_year_of_simulation)] = (perte,simulation_modu_juillet.calculate('sal', period = 2020+nb_year))
#
#    print dico_perte
#    return dico_perte



#
#
#def perte_reelle(nb_enf = 5, nb_year_of_simulation = 1):
#    np.set_printoptions(suppress=True, precision=2)
#    print 'hello1'
#    benchmark1, benchmark2, simulation_modu_juillet = test(nb_enf = nb_enf)
#
#
#    key_list = ['revdisp',
#    'psoc',  # presations sociales
#      'pfam',  # prestations familiales
#          'af',  # allocations familiales
#            'af_base', 'af_majo', 'af_forf', 'crds_pfam',
#        'cf', 'ars', 'paje',  # commentaire là
#        'aide_logement',
#    'asf', #Allocation de soutien familial
#    'mini', 'ppe',
#    'impo', 'salnet']
#    dico_perte = dict()
#
#    for var in key_list:
#        print 'hello2{}'.format(var)
#        perte = np.zeros(simulation_modu_juillet.calculate(var, period = 2020).shape)
#        print 'hello3{}'.format(var)
#        sal = simulation_modu_juillet.calculate('sal', period = 2020)[::2+nb_enf]
#        for nb_year in range(1 , nb_year_of_simulation+1):
#            perte += simulation_modu_juillet.calculate(var, period = 2020+nb_year)\
#                        - benchmark2.calculate(var, period = 2020+nb_year)
#            print 'hello3{}'.format(var)
#
#        list_of_tupple = []
#        for i in range(0,sal.shape[0]):
#            list_of_tupple += [(sal[i],perte[i])]
#        dico_perte['perte {} en {} ans'.format(var, nb_year_of_simulation)] = (perte,simulation_modu_juillet.calculate('sal', period = 2020+nb_year))
#
#    print dico_perte
#    return dico_perte
