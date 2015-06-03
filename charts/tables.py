#
# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# BitBake Toaster Implementation
#
# Copyright (C) 2015        Intel Corporation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from widgets import ToasterTable
from charts.models import TestRun
from django.db.models import Q, Max
from django.conf.urls import url

class TestReportTable(ToasterTable):
    """Table of layers in Toaster"""

    def __init__(self, *args, **kwargs):
        ToasterTable.__init__(self)
        self.default_orderby = "testrun_id"

    def setup_queryset(self, *args, **kwargs):
        self.queryset = TestRun.objects.filter(release=kwargs[release])

    def setup_columns(self, *args, **kwargs):

        self.add_column(title="ID",
                        hideable=False,
                        orderable=True,
                        field_name="testrun_id")


        product_template='<a href="?{{data.product}}">{{data.product}}</a>'

        self.add_column(title="Release",
                        hideable=False,
                        orderable=True,
                        field_name="release")
 
        ## ....


# This needs to be staticaly defined here as django reads the url patterns
# on start up
urlpatterns = (
    url(r'testreport/(?P<cmd>\w+)*', TestReportTable.as_view(release=release), name=TestReportTable.__name__.lower()),
)
