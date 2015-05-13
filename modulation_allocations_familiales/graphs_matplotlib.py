# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 17:24:19 2015

@author: pacificoadrien
"""

import matplotlib.pyplot as plt
from openfisca_matplotlib import graphs

from datetime import date  # module nécessaire pour la définition des dates, dont notamment les dates de naissances
import openfisca_france    # module décrivant le système socio-fiscal français
from openfisca_france.tests import base
from modulation_allocations_familiales.reforms import af_modulation

#TaxBenefitSystem = openfisca_france.init_country()  # Initialisation de la classe décrivant le système socio-fiscal français
#print TaxBenefitSystem
#tax_benefit_system = TaxBenefitSystem()  # Création d'une instance du système socio-fiscal français
#tax_benefit_system = TaxBenefitSystem()
##tax_benefit_system = af_modulation.build_reform(base.tax_benefit_system)
#
#salaire_imposable_minimal = 0
#salaire_imposable_maximal = 400000
#
#
#def couple_avec_enfants(nombre_enfants = 0, year = 2014):
#    enfant = [dict(
#        birth = date(2005, 1, 1),
#        )]
#    enfants = enfant * nombre_enfants
#    simulation = tax_benefit_system.new_scenario().init_single_entity(
#        axes = [
#            dict(
#                count = 200,
#                min = 0,
#                max = salaire_imposable_maximal * 3,
#                name = 'sal',
#                ),
#            ],
#        period = "{}:3".format(year-2),
#        parent1 = dict(
#            birth = date(1980, 1, 1),
#            ),
#        parent2 = dict(
#            birth = date(1980, 1, 1)
#            ),
#        enfants = enfants,
#        menage = dict(
#            loyer = 1000 * 3,
#            so = 4,
#            ),
#        ).new_simulation(debug = True)
#    return simulation
#
#
#def gain_enfant_marginal(rang_enfant, variable = "revdisp", year = 2014): #on défini une fonction faisant la différence
#    assert rang_enfant >= 1                                               #de revenu disp pour un enfant suplémentaire
#    situation_initiale = couple_avec_enfants(rang_enfant-1, year)         #en fonction du rang de l'enfant
#    situation_finale = couple_avec_enfants(rang_enfant, year)
#    revdisp_initial = situation_initiale.calculate(variable, period = year)
#    revdisp_final = situation_finale.calculate(variable, period = year)
#    return revdisp_final - revdisp_initial
#
#
#fig = plt.figure()
#salaire_imposable = couple_avec_enfants(nombre_enfants = 0).calculate('sal', period = 2014)[::2]
## salaire imposable 'sal' est une variable associée à l'entité individu
#for rang_enfant in range(1, 4):
#    plt.plot(salaire_imposable, gain_enfant_marginal(rang_enfant, year = 2014), label = "{}e enfant".format(rang_enfant))
#plt.legend(loc = 4, shadow=True, fancybox=True)
#plt.xlim([0,salaire_imposable_maximal])
#plt.suptitle(u"Gain marginal à l'enfant en fonction du rang de l'enfant et du revenu", fontsize=16)
#
#
#smic = 1128.70 * 12
#fig2 = plt.figure()
#salaire_imposable_par_smic = couple_avec_enfants(nombre_enfants = 0).calculate('sal', period = 2014)[::2] / smic
## salaire imposable 'sal' est une variable associée à l'entité individu
#sans_enfant = couple_avec_enfants(nombre_enfants = 0).calculate('revdisp', period = 2014)/12
#for nombre_enfants in range(1, 5):
#    plt.plot(salaire_imposable_par_smic , (couple_avec_enfants(nombre_enfants = nombre_enfants).calculate('revdisp', period = 2014)/12) - sans_enfant, \
#             label = "{} enfant".format(nombre_enfants))
#plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., shadow=True, fancybox=True)
#plt.xlim([0, 10])
#plt.suptitle(u"Supplément de transfert public lié au nombre d'enfants, pour un couple biactif, en fonction du revenu du 1er conjoint (en parts de Smic)", fontsize=16)
#plt.ylabel(u'euros/mois')
#plt.xlabel(u'Smics')
#
#plt.show()



from modulation_allocations_familiales.reforms import af_modulation
from modulation_allocations_familiales.reforms import prolongement_legislation_af_plaf_qf_2011

from openfisca_france.tests import base
from openfisca_france import init_country
import numpy as np
from datetime import date  # module nécessaire pour la définition des dates, dont notamment les dates de naissances
TaxBenefitSystem = init_country()  # Initialisation de la classe décrivant le système socio-fiscal français
tax_benefit_system = TaxBenefitSystem()  # Création d'une instance du système socio-fiscal français





def cas_type():
    parent1 = dict(birth = date(1976, 1, 1), salbrut = 50000,) #père né en 1976 gagnant 50k euros brut/an
    parent2 = dict(birth = date(1979, 1, 1), salbrut = 40000) #mère née en 1979 gagnant 40k euros brut/an
    enfants = [dict(birth = date(2008 , 1, 1)), #premier enfant né en 2008
               dict(birth = date(2004 , 1, 1))] #deuxième enfant né en 2004
    print(enfants)
    menage = dict(     #les parents sont locataires ('so' = 4) d'un appartement à 1000 euros par mois
        loyer = 1000,
        so = 4,
        )
    return parent1, parent2, enfants, menage


import datetime
import numpy as np
import pandas as pd

from modulation_allocations_familiales.reforms import af_modulation
from modulation_allocations_familiales.reforms import prolongement_legislation_af_plaf_qf_2011
from modulation_allocations_familiales.reforms import modu_af_juillet
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


parent1, parent2, enfants, menage = cas_type()
period = "2016:2"
from modulation_allocations_familiales import benchmark_idep_mahdi
benchmark1 = benchmark_modu_af(
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        )

benchmark2 = bechmark_plaf_qf(
    menage = menage,
    parent1 = parent1,
    parent2 = parent2,
    enfants = enfants,
    period = period,
        )