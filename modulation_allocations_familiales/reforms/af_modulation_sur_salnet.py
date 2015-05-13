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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

import copy

from numpy import maximum as max_
from openfisca_core import columns, formulas, reforms

from openfisca_france import entities


# Reform formulas



class allocations_familiales(formulas.SimpleFormulaColumn):
    column = columns.FloatCol
    entity_class = entities.Familles
    label = u"Modulation ddes allocations familiales (issu PLFSS2015)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        params = simulation.legislation_at(period.start).modulation_alloc

        af_base = simulation.calculate('af_base', period)
        af_forf = simulation.calculate('af_forf', period)
        af_majo = simulation.calculate('af_majo', period)
        af_nbenf = simulation.calculate('af_nbenf', period)


        sal_net_holder = simulation.compute('salnet', period)
        sal_net = self.sum_by_entity(sal_net_holder)
#        rng = simulation.calculate('rng', period)

        af = af_majo + af_forf + af_base
        plafond1 = params.plafond1 + ((af_nbenf - 2) * 500) * (af_nbenf >= 2)
        plafond2 = params.plafond2 + ((af_nbenf - 2) * 500) * (af_nbenf >= 2)
        new_af = (
            (sal_net <= plafond1) * af +
            (sal_net > plafond1) * (sal_net <= plafond2) * af / params.diviseur_plafond_1 +
            (sal_net > plafond2) * af / params.diviseur_plafond_2
            )
        modulation_af = (
            (sal_net <= plafond1) * (af + sal_net) + (
                (sal_net > plafond1) * (sal_net <= plafond2) *
                max_(plafond1 + af, sal_net + new_af)
                ) +
            (sal_net > plafond2) *
            max_(
                af / params.diviseur_plafond_1 + plafond2,
                sal_net + new_af
                )
            ) - sal_net
        return period, modulation_af


# Reform legislation

reform_legislation_subtree = {
    "modulation_alloc": {
        "@type": "Node",
        "description": "Modulation des allocations familiales",
        "children": {
            "plafond1": {
                "@type": "Parameter",
                "description": "Montant plafond1 des allocations familales",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2004-01-01', 'stop': u'2014-12-31', 'value': 6000}],
                },
            "plafond2": {
                "@type": "Parameter",
                "description": "Montant plafond2 des alocations familiales",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2004-01-01', 'stop': u'2014-12-31', 'value': 8000}],
                },
            "diviseur_plafond_1": {
                "@type": "Parameter",
                "description": "coefficient après les pallier 1 des allocations familiales",
                "format": "integer",
                "values": [ {'start': u'2004-01-01', 'stop': u'2014-12-31', 'value': 1},
                            {'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': 2},
                ],
                },
            "diviseur_plafond_2": {
                "@type": "Parameter",
                "description": "coefficient après les pallier 2 des allocations familiales",
                "format": "integer",
                "values": [ {'start': u'2004-01-01', 'stop': u'2014-12-31', 'value': 1},
                            {'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': 4},
                ],
                },
            }
        }
    }


def build_reform(tax_benefit_system):
    # Update legislation
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(reform_legislation_subtree)

    # Update formulas

    reform_entity_class_by_key_plural = reforms.clone_entity_classes(entities.entity_class_by_key_plural)
    ReformFamilles = reform_entity_class_by_key_plural['familles']
    ReformFamilles.column_by_name['af'] = allocations_familiales

    return reforms.Reform(
        entity_class_by_key_plural = reform_entity_class_by_key_plural,
        legislation_json = reform_legislation_json,
        name = u'Modulations 2014',
        reference = tax_benefit_system,
        )