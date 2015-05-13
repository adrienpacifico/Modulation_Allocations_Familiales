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

from openfisca_core import reforms
from openfisca_france import entities

# Reform legislation

reform_legislation_subtree = {
    "plafond_qf": {
        "@type": "Node",
        "description": "Plafonnement du quotient familial",
        "children": {
            "marpac": {
                "@type": "Parameter",
                "description": "Mariés ou PACS",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2010-01-01', 'stop': u'2020-12-31', 'value': 10000000000000000000}
                    ],
                },
            "celib_enf": {
                "@type": "Parameter",
                "description": "Cas célibataires avec enfant(s)",
                "format": "integer",
                "unit": "currency",
                "values": [
                    {'start': u'2010-01-01', 'stop': u'2012-12-31', 'value': 4040},
                    {'start': u'2013-01-01', 'stop': u'2020-12-31', 'value': 4040}
                    ],
                },
            "veuf": {
                "@type": "Parameter",
                "description": "Veuf avec enfants à charge",
                "format": "integer",
                "values": [
                    {'start': u'2010-01-01', 'stop': u'2014-12-31', 'value': 2236}
                    ],
                },
            }
        }
    }



def build_reform(tax_benefit_system):
    # Update legislation
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children']['ir']['children']['plafond_qf']['children'].update(
        reform_legislation_subtree['plafond_qf']['children'])

    # Update formulas
    reform_entity_class_by_key_plural = reforms.clone_entity_classes(entities.entity_class_by_key_plural)
    ReformFamilles = reform_entity_class_by_key_plural['familles']

    # Removing the formula starting in 2015-07-01
    # TODO: improve because very dirty
    # may be by creating the following functions
    # get_formulas(entity, variable, period), set_formulas(entity, variable, period)
    af_base = ReformFamilles.column_by_name['af_base']
    if len(af_base.formula_class.dated_formulas_class) > 1:
        del af_base.formula_class.dated_formulas_class[1]
        af_base.formula_class.dated_formulas_class[0]['stop_instant'] = None

    return reforms.Reform(
        entity_class_by_key_plural = reform_entity_class_by_key_plural,
        legislation_json = reform_legislation_json,
        name = u'prolongement législation af et plaf_qf depuis 2011',
        reference = tax_benefit_system,
        )
