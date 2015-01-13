# -*- coding: utf-8 -*-
"""
Created on Tue Jan 13 17:32:33 2015

@author: pacificoadrien
"""

import datetime
from openfisca_core import periods
from modulation_allocations_familiales.reforms import prolongement_legislation_af_plaf_qf_2011
from openfisca_france.tests import base


def bechmark_plaf_qf():
    reform_plaf_qf = prolongement_legislation_af_plaf_qf_2011.build_reform(base.tax_benefit_system)
    scenario = reform_plaf_qf.new_scenario().init_single_entity(
        axes = axes if bareme else None,
        menage = menage,
        parent1 = parent1,
        parent2 = parent2,
        enfants = enfants,
        period = periods.period('year', year),
    )
    return scenario.new_simulation(debug = True)

if __name__ == '__main__':
    import logging
    import sys
    logging.basicConfig(level = logging.ERROR, stream = sys.stdout)
#    benchmark_perte_af_plafqf(40, 2, 2)
    year = 2012
    axes = [
            dict(
                count = 20,
                max = 200000 * 10,
                min = 0,
                name = 'sal'
                ),
            ]
    parent1 = dict(birth = datetime.date(year - 40, 1, 1))
    parent2 = dict(birth = datetime.date(year - 40, 1, 1))
    enfants = [
        dict(birth = datetime.date(year - 9, 1, 1)),
        dict(birth = datetime.date(year - 9, 1, 1)),
        ]
    menage = dict(
        loyer = 1000000,
        so = 4,
        )
    bareme = True

    benchmark2 = bechmark_plaf_qf()
    print benchmark2.calculate('af')
