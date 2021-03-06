"""Tests for the users.utils functions."""

from django.contrib.auth.models import Group

from ..utils import is_in_group


def test_user_in_a_group(django_user_model):
    """Test a user who is in one group returns true."""
    user = django_user_model.objects.create_user(username='test', email='test@example.com')
    group = Group.objects.create(name='Cool Kids')

    user.groups.add(group)
    user.save()

    result = is_in_group(user, "Cool Kids")
    assert result


def test_user_not_in_a_group(django_user_model):
    """Test a user who is not in one group returns false."""
    user = django_user_model.objects.create_user(username='test', email='test@example.com')
    group = Group.objects.create(name='Cool Kids')

    user.groups.add(group)
    user.save()

    result = is_in_group(user, "Bad Kids")
    assert not result


def test_user_in_one_of_groups(django_user_model):
    """Test a user who is in one of a list of groups returns true."""
    user = django_user_model.objects.create_user(username='test', email='test@example.com')
    group = Group.objects.create(name='Cool Kids')

    user.groups.add(group)
    user.save()

    result = is_in_group(user, "Cool Kids|Bears|Teachers")
    assert result


def test_user_in_two_of_groups(django_user_model):
    """Test a user who is in two of a list of groups returns true."""
    user = django_user_model.objects.create_user(username='test', email='test@example.com')
    group = Group.objects.create(name='Cool Kids')
    group2 = Group.objects.create(name='Bears')

    user.groups.add(group)
    user.groups.add(group2)
    user.save()

    result = is_in_group(user, "Cool Kids|Bears|Teachers")
    assert result


def test_user_not_in_one_of_groups(django_user_model):
    """Test a user who is not in one of a list of groups returns false."""
    user = django_user_model.objects.create_user(username='test', email='test@example.com')
    group = Group.objects.create(name='Cool Kids')

    user.groups.add(group)
    user.save()

    result = is_in_group(user, "Bad Kids|Bears|Teachers")
    assert not result


def test_username_only_returns_false(django_user_model):
    """Test that a username string instead of a user returns false."""
    user = django_user_model.objects.create_user(username='test', email='test@example.com')
    group = Group.objects.create(name='Cool Kids')

    user.groups.add(group)
    user.save()

    result = is_in_group(user.email, "Cool Kids")
    assert not result


def test_user_id_only_returns_false(django_user_model):
    """Test that a username string instead of a user returns false."""
    user = django_user_model.objects.create_user(username='test', email='test@example.com')
    group = Group.objects.create(name='Cool Kids')

    user.groups.add(group)
    user.save()

    result = is_in_group(user.id, "Cool Kids")
    assert not result
