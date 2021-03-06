"""Admin site configuration for the jobs app."""
import logging

from django.contrib import admin

from .models import Post, Job, TagVariant, UserJob

logger = logging.getLogger(__name__)


def remove_tags(modeladmin, request, queryset):
    """Remove tags."""
    logger.debug('MA: %s, request: %s', modeladmin, request)
    for obj in queryset:
        obj.tags.clear()


def set_is_removed(modeladmin, request, queryset):
    """Soft Delete objects."""
    logger.debug('MA: %s, request: %s', modeladmin, request)
    queryset.update(is_removed=True)


def set_as_garbage(modeladmin, request, queryset):
    """Set posts as garbage."""
    logger.debug('MA: %s, request: %s', modeladmin, request)
    queryset.update(garbage=True)


def set_as_freelance(modeladmin, request, queryset):
    """Set posts as freelance."""
    logger.debug('MA: %s, request: %s', modeladmin, request)
    queryset.update(is_freelance=True)


remove_tags.short_description = "Remove Tags"
set_is_removed.short_description = "Soft Delete"
set_as_garbage.short_description = 'Mark Garbage'
set_as_freelance.short_description = 'Mark Freelance'


class JobAdmin(admin.ModelAdmin):
    """The Job model admin has some special tag handling."""

    model = Job
    actions = [remove_tags]

    # List fields
    list_display = ('title', 'tag_list', 'created', 'modified')
    search_fields = ('title',)

    # Detail screen fields
    fields = ('title', 'description', 'tags', 'created', 'modified', 'fingerprint')
    readonly_fields = ('created', 'modified', 'fingerprint')

    def get_queryset(self, request):
        """Prefetch the tags data to make this more efficient."""
        return super(JobAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        """Concatenate all tags for each job."""
        logger.debug('Called Tag_list in admin: %s', self)
        return u", ".join(o.name for o in obj.tags.all())


class UserJobAdmin(admin.ModelAdmin):
    """The UserJob model admin."""

    model = UserJob
    actions = [set_is_removed]

    # List fields
    list_display = ('job', 'user', 'is_removed', 'created', 'modified')
    search_fields = ('job__title', 'user__username')
    list_filter = ('user__username', 'is_removed')

    # Detail screen fields
    fields = ('job', 'user', 'is_removed', 'created', 'modified')
    readonly_fields = ('created', 'modified')

    def get_queryset(self, request):
        """Don't use the default manager."""
        querys = self.model.all_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            querys = querys.order_by(*ordering)
        return querys


class PostAdmin(admin.ModelAdmin):
    """The Post model needs no special admin configuration."""

    model = Post
    actions = [remove_tags, set_as_garbage, set_as_freelance]

    # List fields
    list_display = ('title', 'source', 'subarea', 'tag_list', 'is_freelance', 'processed', 'garbage', 'created')
    search_fields = ('title',)
    list_filter = ('source__name', 'garbage', 'is_freelance')

    # Detail screen fields
    fields = ('title', 'url', 'source', 'subarea', 'description', 'unique', 'tags', 'is_freelance', 'processed', 'garbage', 'created', 'modified')
    readonly_fields = ('created', 'modified')

    def get_queryset(self, request):
        """Prefetch the tags data to make this more efficient."""
        querys = self.model.all_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            querys = querys.order_by(*ordering)
        return querys.prefetch_related('tags')

    def tag_list(self, obj):  # pylint: disable=no-self-use
        """Concatenate all tags for each post."""
        return u", ".join(o.name for o in obj.tags.all())


class TagVariantAdmin(admin.ModelAdmin):
    """The TagVariant admin lets the user put in new tags."""

    model = TagVariant
    list_display = ('variant', 'tag')
    search_fields = ('variant', 'tag')
    fields = ('variant', 'tag')


admin.site.register(Job, JobAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(TagVariant, TagVariantAdmin)
admin.site.register(UserJob, UserJobAdmin)
