## -*- coding: utf-8 -*-


## OpenFisca -- A versatile microsimulation software
## By: OpenFisca Team <contact@openfisca.fr>
##
## Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
## https://github.com/openfisca
##
## This file is part of OpenFisca.
##
## OpenFisca is free software; you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.
##
## OpenFisca is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.


<%!
from biryani1 import strings

from openfisca_web_ui import model, urls, uuidhelpers
%>


<%inherit file="/site.mako"/>


<%namespace name="render_legislation" file="/legislations/render-legislation.mako"/>
<%namespace name="view" file="admin-view.mako"/>


<%def name="appconfig_script()" filter="trim">
    <%render_legislation:appconfig_script/>
</%def>


<%def name="breadcrumb()" filter="trim">
</%def>


<%def name="container_content()" filter="trim">
<%
    user = model.get_user(ctx)
    dated_legislation = False
    owner_or_admin = False
    editable = False
    if user is not None:
        dated_legislation = legislation.json is not None and legislation.json.get('datesim') is not None
        owner_or_admin = model.is_admin(ctx) or user._id == legislation.author_id
        editable = owner_or_admin and dated_legislation
%>\
        <div class="page-header">
            <h1>${_(u'Legislation')} <small>${legislation.get_title(ctx)}</small></h1>
        </div>

        <div class="panel panel-default">
            <div class="panel-body">
                <%view:view_fields/>
                ${view.view_content(user = user)}
            </div>
            <div class="panel-footer">
                <a class="btn btn-default" href="${legislation.get_api1_url(ctx, 'json')}" rel="external" \
target="_blank">
                    ${_(u'View as JSON')}
                </a>
    % if owner_or_admin:
                <a class="btn btn-default" href="${legislation.get_admin_url(ctx, 'edit')}">${_(u'Edit')}</a>
                <a class="btn btn-danger"  href="${legislation.get_admin_url(ctx, 'delete')}">${_(u'Delete')}</a>
    % elif user is not None and user.email is not None:
                <a class="btn btn-default" data-toggle="modal" data-target="#modal-duplicate-and-edit" href="#">
                    ${_(u'Duplicate and edit')}
                </a>
    % endif
            </div>
        </div>
</%def>


<%def name="modals()" filter="trim">
    <%parent:modals/>
    ${render_legislation.modal_change_legislation_date(date = date)}
    <%render_legislation:modal_duplicate_and_edit/>
</%def>


<%def name="title_content()" filter="trim">
${legislation.get_title(ctx)} - ${parent.title_content()}
</%def>
