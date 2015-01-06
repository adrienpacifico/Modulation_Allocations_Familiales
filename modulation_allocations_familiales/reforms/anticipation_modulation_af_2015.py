# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
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

from openfisca_core import periods, reforms
from openfisca_france import entities

# Reform legislation

reform_legislation_subtree = {
    "modulation": {
        "@type": "Node",
        "description": "Modulation des allocations familiales en fonction des ressources",
        "children": {
            "plafond1": {
                "@type": "Parameter",
                "description": "Plafond mensuel de ressources n°1",
                "format": "float",
                "unit": "currency",
                "values": [
                    {'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': 6000}
                    ],
                },
            "plafond2": {
                "@type": "Parameter",
                "description": "Plafond mensuel de ressources n°2",
                "format": "float",
                "unit": "currency",
                "values": [
                    {'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': 8000}
                    ],
                },
            "enfant_supp": {
                "@type": "Parameter",
                "description": "Majoration du plafond mensuel de ressources par enfant supplémentaire (à partir du 3e enfant)",
                "format": "float",
                "unit": "currency",
                "values": [
                    {'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': 500}
                    ],
                },
            "taux1": {
                "@type": "Parameter",
                "description": "Taux de modulation au delà du plafond 1",
                "format": "percent",
                "values": [
                    {'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': .5}
                    ],
                },
            "taux2": {
                "@type": "Parameter",
                "description": "Taux de modulation au delà du plafond 2",
                "format": "percent",
                "values": [
                    {'start': u'2015-01-01', 'stop': u'2015-12-31', 'value': .25}
                    ],
                },
            }
        }
    }



def build_reform(tax_benefit_system):
    # Update legislation
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children']['fam']['children']['af']['children'].update(
        reform_legislation_subtree)

    # Update formulas
    reform_entity_class_by_key_plural = reforms.clone_entity_classes(entities.entity_class_by_key_plural)
    ReformFamilles = reform_entity_class_by_key_plural['familles']

    # Removing the formula starting in 2015-07-01
    # TODO: improve because very dirty
    # may be by creating the following functions
    # get_formulas(entity, variable, period), set_formulas(entity, variable, period)
    af_base = ReformFamilles.column_by_name['af_base']
    print af_base.formula_class.dated_formulas_class
    af_base.formula_class.dated_formulas_class[1]['start_instant'] = periods.instant("2015-01-01")
    af_base.formula_class.dated_formulas_class[0]['stop_instant'] = periods.instant("2014-12-31")
    print af_base.formula_class.dated_formulas_class

    return reforms.Reform(
        entity_class_by_key_plural = reform_entity_class_by_key_plural,
        legislation_json = reform_legislation_json,
        name = u'anticipation modulation des af au 1er janvier 2015',
        reference = tax_benefit_system,
        )
