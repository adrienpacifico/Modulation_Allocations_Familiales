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
class ir_plaf_qf(formulas.SimpleFormulaColumn):
    column = columns.FloatCol
    entity_class = entities.FoyersFiscaux
    label = u"ir_plaf_qf"

    def function(self, simulation, period):
        '''
        Impôt après plafonnement du quotient familial et réduction complémentaire
        '''
        period = period.start.offset('first-of', 'month').period('year')
        ir_brut = simulation.calculate('ir_brut', period)
        ir_ss_qf = simulation.calculate('ir_ss_qf', period)
        nb_adult = simulation.calculate('nb_adult', period)
        nb_pac = simulation.calculate('nb_pac', period)
        nbptr = simulation.calculate('nbptr', period)
        marpac = simulation.calculate('marpac', period)
        veuf = simulation.calculate('veuf', period)
        jveuf = simulation.calculate('jveuf', period)
        celdiv = simulation.calculate('celdiv', period)
        caseE = simulation.calculate('caseE', period)
        caseF = simulation.calculate('caseF', period)
        caseG = simulation.calculate('caseG', period)
        caseH = simulation.calculate('caseH', period)
        caseK = simulation.calculate('caseK', period)
        caseN = simulation.calculate('caseN', period)
        caseP = simulation.calculate('caseP', period)
        caseS = simulation.calculate('caseS', period)
        caseT = simulation.calculate('caseT', period)
        caseW = simulation.calculate('caseW', period)
        nbF = simulation.calculate('nbF', period)
        nbG = simulation.calculate('nbG', period)
        nbH = simulation.calculate('nbH', period)
        nbI = simulation.calculate('nbI', period)
        nbR = simulation.calculate('nbR', period)
        plafond_qf = simulation.legislation_at(period).ir.plafond_qf

        A = ir_ss_qf
        I = ir_brut

        aa0 = (nbptr - nb_adult) * 2  # nombre de demi part excédant nbadult
        # on dirait que les impôts font une erreur sur aa1 (je suis obligé de
        # diviser par 2)
        aa1 = min_((nbptr - 1) * 2, 2) / 2  # deux première demi part excédants une part
        aa2 = max_((nbptr - 2) * 2, 0)  # nombre de demi part restantes
        # celdiv parents isolés
        condition61 = celdiv & caseT
        B1 = plafond_qf.celib_enf * aa1 + plafond_qf.marpac * aa2
        # tous les autres
        B2 = plafond_qf.marpac * aa0  # si autre
        # celdiv, veufs (non jveuf) vivants seuls et autres conditions
        # TODO: année en dur... pour caseH
        condition63 = (celdiv | (veuf & not_(jveuf))) & not_(caseN) & (nb_pac == 0) & (caseK | caseE) & (caseH < 1981)
        B3 = plafond_qf.celib

        B = B1 * condition61 + \
            B2 * (not_(condition61 | condition63)) + \
            B3 * (condition63 & not_(condition61))
        C = max_(0, A - B)
        # Impôt après plafonnement
        IP0 = max_(I, C)

        # 6.2 réduction d'impôt pratiquée sur l'impot après plafonnement et le cas particulier des DOM
        # pas de réduction complémentaire
        condition62a = (I >= C)
        # réduction complémentaire
        condition62b = (I < C)
        # celdiv veuf
        condition62caa0 = (celdiv | (veuf & not_(jveuf)))
        condition62caa1 = (nb_pac == 0) & (caseP | caseG | caseF | caseW)
        condition62caa2 = caseP & ((nbF - nbG > 0) | (nbH - nbI > 0))
        condition62caa3 = not_(caseN) & (caseE | caseK) & (caseH >= 1981)
        condition62caa = condition62caa0 & (condition62caa1 | condition62caa2 | condition62caa3)
        # marié pacs
        condition62cab = (marpac | jveuf) & caseS & not_(caseP | caseF)
        condition62ca = (condition62caa | condition62cab)

        # plus de 590 euros si on a des plus de
        condition62cb = ((nbG + nbR + nbI) > 0) | caseP | caseF
        D = plafond_qf.reduc_postplafond * (condition62ca + ~condition62ca * condition62cb * (
            1 * caseP + 1 * caseF + nbG + nbR + nbI / 2))

        E = max_(0, A - I - B)
        Fo = D * (D <= E) + E * (E < D)
        IP1 = IP0 - Fo

        # TODO: 6.3 Cas particulier: Contribuables domiciliés dans les DOM.
        # conditionGuadMarReu =
        # conditionGuyane=
        # conitionDOM = conditionGuadMarReu | conditionGuyane
        # postplafGuadMarReu = 5100
        # postplafGuyane = 6700
        # IP2 = IP1 - conditionGuadMarReu*min( postplafGuadMarReu,.3*IP1)  - conditionGuyane*min(postplafGuyane,.4*IP1)

        # Récapitulatif

        return period, condition62a * IP0 + condition62b * IP1  # IP2 si DOM



#plafond_qf = simulation.legislation_at(period.start).ir.plafond_qf

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
                "values": [{'start': u'2010-01-01', 'stop': u'2015-12-31', 'value': 2336}],
                },
            "celib_enf": {
                "@type": "Parameter",
                "description": "Cas célibataires avec enfant(s)",
                "format": "integer",
                "unit": "currency",
                "values": [{'start': u'2010-01-01', 'stop': u'2012-12-31', 'value': 4040},{'start': u'2010-01-01', 'stop': u'2012-12-31', 'value': 4040}],
                },
            "veuf": {
                "@type": "Parameter",
                "description": "Veuf avec enfants à charge",
                "format": "integer",
                "values": [{'start': u'2010-01-01', 'stop': u'2014-12-31', 'value': 2236}],
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
    ReformFamilles.column_by_name['ir_plaf_qf'] = plafond_qf

    return reforms.Reform(
        entity_class_by_key_plural = reform_entity_class_by_key_plural,
        legislation_json = reform_legislation_json,
        name = u'Non_diminution_plaf_qf 2012',
        reference = tax_benefit_system,
        )
