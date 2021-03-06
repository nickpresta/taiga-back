# Copyright (C) 2014 Andrey Antukh <niwi@niwi.be>
# Copyright (C) 2014 Jesús Espino <jespinog@gmail.com>
# Copyright (C) 2014 David Barragán <bameda@dbarragan.com>
# Copyright (C) 2014 Anler Hernández <hello@anler.me>
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

from tests import factories as f

from taiga.projects.userstories.models import UserStory

import pytest

pytestmark = pytest.mark.django_db


@pytest.fixture
def data():
    m = type("Models", (object,), {})
    m.us_closed_status = f.UserStoryStatusFactory(is_closed=True)
    m.us_open_status = f.UserStoryStatusFactory(is_closed=False)
    m.task_closed_status = f.TaskStatusFactory(is_closed=True)
    m.task_open_status = f.TaskStatusFactory(is_closed=False)
    m.user_story1 = f.UserStoryFactory(status=m.us_open_status)
    m.user_story2 = f.UserStoryFactory(status=m.us_open_status)
    m.task1 = f.TaskFactory(user_story=m.user_story1, status=m.task_open_status)
    m.task2 = f.TaskFactory(user_story=m.user_story1, status=m.task_open_status)
    m.task3 = f.TaskFactory(user_story=m.user_story1, status=m.task_open_status)
    return m


def test_us_without_tasks_open_close_us_status(data):
    assert data.user_story2.is_closed is False
    data.user_story2.status = data.us_closed_status
    data.user_story2.save()
    data.user_story2 = UserStory.objects.get(pk=data.user_story2.pk)
    assert data.user_story2.is_closed is True
    data.user_story2.status = data.us_open_status
    data.user_story2.save()
    data.user_story2 = UserStory.objects.get(pk=data.user_story2.pk)
    assert data.user_story2.is_closed is False


def test_us_with_tasks_open_close_us_status(data):
    assert data.user_story1.is_closed is False
    data.user_story1.status = data.us_closed_status
    data.user_story1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.user_story1.status = data.us_open_status
    data.user_story1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False


def test_us_on_task_delete_empty_close(data):
    data.user_story1.status = data.us_closed_status
    data.user_story1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task3.delete()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task2.delete()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task1.delete()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True


def test_us_on_task_delete_empty_open(data):
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.task2.status = data.task_closed_status
    data.task2.save()
    data.task3.status = data.task_closed_status
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    data.task3.delete()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    data.task2.delete()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    data.task1.delete()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False


def test_us_with_tasks_on_move_empty_open(data):
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.task2.status = data.task_closed_status
    data.task2.save()
    data.task3.status = data.task_closed_status
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    data.task3.user_story = data.user_story2
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    data.task2.user_story = data.user_story2
    data.task2.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    data.task1.user_story = data.user_story2
    data.task1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False


def test_us_with_tasks_on_move_empty_close(data):
    data.user_story1.status = data.us_closed_status
    data.user_story1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task3.user_story = data.user_story2
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task2.user_story = data.user_story2
    data.task2.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task1.user_story = data.user_story2
    data.task1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True


def test_us_close_last_tasks(data):
    assert data.user_story1.is_closed is False
    data.task3.status = data.task_closed_status
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task2.status = data.task_closed_status
    data.task2.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True


def test_us_reopen_tasks(data):
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.task2.status = data.task_closed_status
    data.task2.save()
    data.task3.status = data.task_closed_status
    data.task3.save()

    assert data.user_story1.is_closed is True
    data.task3.status = data.task_open_status
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task2.status = data.task_open_status
    data.task2.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
    data.task1.status = data.task_open_status
    data.task1.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False


def test_us_delete_task_then_all_closed(data):
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.task2.status = data.task_closed_status
    data.task2.save()
    assert data.user_story1.is_closed is False
    data.task3.delete()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True


def test_us_change_task_us_then_all_closed(data):
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.task2.status = data.task_closed_status
    data.task2.save()
    assert data.user_story1.is_closed is False
    data.task3.user_story = data.user_story2
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True


def test_us_change_task_us_then_any_open(data):
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.task2.status = data.task_closed_status
    data.task2.save()
    data.task3.user_story = data.user_story2
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    data.task3.user_story = data.user_story1
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False


def test_task_create(data):
    data.task1.status = data.task_closed_status
    data.task1.save()
    data.task2.status = data.task_closed_status
    data.task2.save()
    data.task3.status = data.task_closed_status
    data.task3.save()
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    f.TaskFactory(user_story=data.user_story1, status=data.task_closed_status)
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is True
    f.TaskFactory(user_story=data.user_story1, status=data.task_open_status)
    data.user_story1 = UserStory.objects.get(pk=data.user_story1.pk)
    assert data.user_story1.is_closed is False
