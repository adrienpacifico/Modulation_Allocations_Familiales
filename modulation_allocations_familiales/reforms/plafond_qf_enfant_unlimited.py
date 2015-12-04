# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import reforms


# TODO : actualise parameters with respect to inflation


def build_reform(tax_benefit_system):
    # Removing the formula starting in 2015-07-01
    # TODO: improve because very dirty
    # may be by creating the following functions
    # get_formulas(entity, variable, period), set_formulas(entity, variable, period)

    Reform = reforms.make_reform(
        key = 'plafond_qf_enfant_unlimited',
        name = u"Legislion du plafond qf de 2012 et des af sans modulations",
        reference = tax_benefit_system,
        )
    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "marpac": {
            "@type": "Parameter",
            "description": "Mariés ou PACS",
            "format": "integer",
            "unit": "currency",
            "values": [
                {'start': u'2000-01-01', 'stop': u'2100-12-31', 'value': 10**10}
                ],
            },
        "celib_enf": {
            "@type": "Parameter",
            "description": "Cas célibataires avec enfant(s)",
            "format": "integer",
            "unit": "currency",
            "values": [
                {'start': u'2000-01-01', 'stop': u'2010-12-31', 'value': 10**10},
                {'start': u'2013-01-01', 'stop': u'2100-12-31', 'value': 10**10}
                ],
            },
        "veuf": {
            "@type": "Parameter",
            "description": "Veuf avec enfants à charge",
            "format": "integer",
            "values": [
                {'start': u'2000-01-01', 'stop': u'2014-12-31', 'value': 10**10}
                ],
            },
        }
    reference_legislation_json_copy['children']['ir']['children']['plafond_qf']['children'].update(
        reform_legislation_subtree)
    return reference_legislation_json_copy
