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


import unittest

from webob import Request

from . import common


class TestForms(common.TestCaseWithApp):
    cookie = None

    def test_accept_cookie_url(self):
        req = Request.blank(
            '/accept-cookies',
            method = 'POST',
            POST = {
                'accept-checkbox': 'on',
                'accept': '',
                },
            )
        res = req.get_response(common.app)
        self.assertEqual(res.status_code, 302)
        assert 'Set-Cookie' in res.headers
        self.cookie = res.headers['Set-Cookie']

    def test_root_url_without_cookie(self):
        req = Request.blank('/', method = 'GET')
        res = req.get_response(common.app)
        self.assertEqual(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
