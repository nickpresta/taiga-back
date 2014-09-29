# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from taiga.base import response
from taiga.base.api import viewsets

from . import permissions
from . import serializers
from . import services


class FeedbackViewSet(viewsets.ViewSet):
    permission_classes = (permissions.FeedbackPermission,)

    def create(self, request, **kwargs):
        self.check_permissions(request, "create", None)

        serializer = serializers.FeedbackViewSet(data=request.DATA)
        serializer.full_name = request.user.get_full_name()
        serializer.email = request.user.email

        if not serializer.is_valid():
            return response.BadRequest(serializer.errors)

        self.object = serializer.save(force_insert=True)
        services.send_feedback(self.object)

        return response.Ok(serializer.data)
