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

from numpy import maximum as max_
from openfisca_core import columns, formulas, reforms

from openfisca_france import entities


# Reform formulas


# Reform legislation

#reform_legislation_subtree = {
#    "plafond_qf": {
#        "@type": "Node",
#        "description": "Plafonnement du quotient familial",
#        "children": {
#            "marpac": {
#                "@type": "Parameter",
#                "description": "Mariés ou PACS",
#                "format": "integer",
#                "unit": "currency",
#                "values": [
#                    {'start': u'2010-01-01', 'stop': u'2015-12-31', 'value': 2336}
#                    ],
#                },
#            "celib_enf": {
#                "@type": "Parameter",
#                "description": "Cas célibataires avec enfant(s)",
#                "format": "integer",
#                "unit": "currency",
#                "values": [
#                    {'start': u'2010-01-01', 'stop': u'2012-12-31', 'value': 4040},
#                    {'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 4040}
#                    ],
#                },
#            "veuf": {
#                "@type": "Parameter",
#                "description": "Veuf avec enfants à charge",
#                "format": "integer",
#                "values": [
#                    {'start': u'2010-01-01', 'stop': u'2014-12-31', 'value': 2236}
#                    ],
#                },
#            }
#        }
#    }


def build_reform(tax_benefit_system):
    # Update legislation
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)

    from openfisca_core import periods
    period = periods.period("year", 2013)
    reform_legislation_json = reforms.update_legislation(
        legislation_json = reform_legislation_json,
        path = ('children', 'ir', 'children', 'plafond_qf', 'children', 'marpac'),
        period = period,
        value = 2336,
        )
    reform_legislation_json = reforms.update_legislation(
        legislation_json = reform_legislation_json,
        path = ('children', 'ir', 'children', 'plafond_qf', 'children', 'celib_enf'),
        period = period,
        value = 4040,
        )
    reform_legislation_json = reforms.update_legislation(
        legislation_json = reform_legislation_json,
        path = ('children', 'ir', 'children', 'plafond_qf', 'children', 'veuf'),
        period = period,
        value = 2336,
        )

#    reform_legislation_json['children']['ir']['children'].update(reform_legislation_subtree)

    # Update formulas

    reform_entity_class_by_key_plural = reforms.clone_entity_classes(entities.entity_class_by_key_plural)

    return reforms.Reform(
        entity_class_by_key_plural = reform_entity_class_by_key_plural,
        legislation_json = reform_legislation_json,
        name = u'Non_diminution_plaf_qf 2012',
        reference = tax_benefit_system,
        )
