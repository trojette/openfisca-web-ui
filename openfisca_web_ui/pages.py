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


"""Pages meta-data"""


import datetime

from korma.base import Button
from korma.choice import Select
from korma.condition import Condition
from korma.date import Date
from korma.group import Group
from korma.repeat import Repeat
from korma.text import Number, Text

from . import conv


bootstrap_control_inner_html_template = u'''
<label class="col-sm-6 control-label" for="{self.full_name}">{self.label}</label>
<div class="col-sm-6">
  {self.control_html}
</div>'''


bootstrap_group_outer_html_template = u'<div class="form-group">{self.inner_html}</div>'


make_prenoms_condition = lambda personnes_choices: Condition(
    base_question = Select(
        choices = personnes_choices,
        input_to_data = conv.input_to_uuid,
        label = u'Prénom',
        ),
    conditional_questions = {
        person_idx: make_personne_group(prenom)
        for person_idx, prenom in personnes_choices
        },
    )


make_personne_group = lambda prenom: Group(
    inner_html_template = u'''
<div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
        <h4 class="modal-title" id="myModalLabel">{prenom}</h4>
      </div>
      <div class="modal-body">
        {{self[prenom].html}}
        {{self[salaire].html}}
        {{self[statmarit].html}}
      </div>
      <div class="modal-footer">
        <input class="btn btn-primary" type="submit" value="Valider">
      </div>
    </div>
  </div>
</div>'''.format(prenom=prenom),
    name = 'personne',
    questions = [
        Text(label = u'Prénom'),
        Date(label = u'Date de naissance', max = datetime.datetime.now().date()),
        Number(label = u'Salaire', min = 0, step = 1),
        # TODO(rsoufflet) add values
        Select(
            choices = [
                u'Marié',
                u'Célibataire',
                u'Divorcé',
                u'Veuf',
                u'Pacsé',
                u'Jeune veuf',
                ],
            label = u'Statut marital',
            name = 'statmarit',
            ),
        ],
    )


def make_personne_in_declaration_impots_group(personnes_choices):
    return Group(
        name = u'personne_in_declaration_impots',
        questions = [
            Select(
                choices = (
                    ('déclarants', u'Déclarant'),
                    ('déclarants', u'Conjoint'),
                    ('personnes_à_charge', u'Personne à charge'),
                    ),
                label = u'Rôle',
                ),
            make_prenoms_condition(personnes_choices),
            Button(
                control_attributes = {
                    'class': 'btn btn-primary',
                    'data-target': '#myModal',
                    'data-toggle': 'modal',
                },
                inner_html_template = bootstrap_control_inner_html_template,
                label = u'Éditer',
                outer_html_template = u'<div class="col-sm-offset-6 col-sm-10">{self.inner_html}</div>',
                ),
            ],
        )


def make_personne_in_famille_group(personnes_choices):
    return Group(
        name = u'personne_in_famille',
        questions = [
            Select(
                choices = (('parents', u'Parent'), ('enfants', u'Enfant')),
                label = u'Rôle',
                ),
            make_prenoms_condition(personnes_choices),
            Button(
                control_attributes = {
                    'class': 'btn btn-primary',
                    'data-target': '#myModal',
                    'data-toggle': 'modal',
                },
                inner_html_template = bootstrap_control_inner_html_template,
                label = u'Éditer',
                outer_html_template = u'<div class="col-sm-offset-6 col-sm-10">{self.inner_html}</div>',
                ),
            ],
        )


def make_personne_in_logement_principal_group(personnes_choices):
    return Group(
        name = u'personne_in_logement_principal',
        questions = [
            Select(
                choices = (
                    (u'personne_de_référence', u'Personne de référence'),
                    (u'conjoint', u'Conjoint de la personne de référence'),
                    (u'enfant', u'Enfant de la personne de référence ou de son conjoint'),
                    (u'autre', u'Autre'),
                    ),
                label = u'Rôle',
                ),
            make_prenoms_condition(personnes_choices),
            Button(
                control_attributes = {
                    'class': 'btn btn-primary',
                    'data-target': '#myModal',
                    'data-toggle': 'modal',
                },
                inner_html_template = bootstrap_control_inner_html_template,
                label = u'Éditer',
                outer_html_template = u'<div class="col-sm-offset-6 col-sm-10">{self.inner_html}</div>',
                ),
            ],
        )


pages_data = [
    {
        'name': 'famille',
        'slug': 'famille',
        'title': u'Famille',
        'korma_data_to_personnes': conv.famille_korma_data_to_personnes,
        'korma_data_to_familles': conv.famille_korma_data_to_familles,
        },
    {
        'name': 'declaration_impots',
        'slug': 'declaration-impots',
        'title': u'Déclaration d\'impôts',
        },
    {
        'name': 'logement_principal',
        'slug': 'logement-principal',
        'title': u'Logement principal',
        },
    ]


def build_personnes_choices(ctx):
    personnes_choices = []
    if ctx.session.user is not None:
        api_data = ctx.session.user.api_data
        if api_data is not None:
            api_personnes = api_data.get('personnes')
            if api_personnes is not None:
                for api_personne_id, api_personne in api_personnes.iteritems():
                    personnes_choices.append((api_personne_id, api_personne.get('prenom') or u'Inconnu'))
    personnes_choices.append(('new', u'Nouvelle personne'))
    return personnes_choices


def page_form(ctx, page_name):
    assert ctx.session is not None
    personnes_choices = build_personnes_choices(ctx)
    page_form_by_page_name = {
        'declaration_impots': Repeat(
            name = u'declaration_impots',
            template_question = Repeat(
                name = u'personnes',
                outer_html_template = u'''
<div class="repeated-group">
  {self.inner_html}
  <a class="btn btn-primary" href="/all-questions?entity=foy&idx={self.parent_data[declaration_impots][index]}">
    Plus de détails
  </a>
</div>''',
                template_question = make_personne_in_declaration_impots_group(personnes_choices=personnes_choices),
                ),
            ),
        'famille': Repeat(
            name = u'familles',
            template_question = Repeat(
                name = u'personnes',
                outer_html_template = u'''
<div class="repeated-group">
  {self.inner_html}
  <a class="btn btn-primary" href="/all-questions?entity=fam&idx={self.parent_data[familles][index]}">
    Plus de détails
  </a>
</div>''',
                template_question = make_personne_in_famille_group(personnes_choices=personnes_choices),
                ),
            ),
        'logement_principal': Repeat(
            children_attributes = {
                '_outer_html_template': u'''
<div class="repeated-group">
  {self.inner_html}
  <a class="btn btn-primary" href="/all-questions?entity=men&idx={self.parent_data[logements_principaux][index]}">
    Plus de détails
  </a>
</div>''',
                },
            name = 'logements_principaux',
            template_question = Group(
                name = 'logement_principal',
                questions = [
                    Select(
                        choices = [
                            u'Non renseigné',
                            u'Accédant à la propriété',
                            u'Propriétaire (non accédant) du logement',
                            u'Locataire d\'un logement HLM',
                            u'Locataire ou sous-locataire d\'un logement loué vide non-HLM',
                            u'Locataire ou sous-locataire d\'un logement loué meublé ou d\'une chambre d\'hôtel',
                            u'Logé gratuitement par des parents, des amis ou l\'employeur',
                            ],
                        label = u'Statut d\'occupation',
                        name = u'so',
                        ),
                    Number(label = u'Loyer'),
                    Text(label = u'Localité'),
                    Repeat(
                        name = u'personnes',
                        template_question = make_personne_in_logement_principal_group(
                            personnes_choices=personnes_choices),
                        ),
                    ]
                ),
            ),
        }
    return page_form_by_page_name[page_name]