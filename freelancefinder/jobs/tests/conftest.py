"""Fixtures to create models in jobs app."""

from pytest_factoryboy import register

from .factories import JobFactory, PostFactory, FreelancerFactory, SourceFactory


register(JobFactory)
register(PostFactory)
register(FreelancerFactory)
register(SourceFactory)
