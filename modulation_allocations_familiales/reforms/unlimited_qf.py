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
            }
        }
    }



def build_reform(tax_benefit_system):
    # Update legislation
    reform_legislation_json = copy.deepcopy(tax_benefit_system.legislation_json)
    reform_legislation_json['children']['ir']['children']['plafond_qf']['children'].update(
        reform_legislation_subtree['plafond_qf']['children'])

    Reform = reforms.make_reform(
        legislation_json = reform_legislation_json,
        name = u"Supprime le plafond du quotient familial",
        reference = tax_benefit_system,
        )

    return Reform()
