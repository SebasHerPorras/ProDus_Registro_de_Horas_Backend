from django.contrib import admin
from apps.projects.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'is_active', 'created_at', 'updated_at')
	list_display_links = ('id', 'name')
	list_editable = ('is_active',)
	list_filter = ('is_active', 'created_at')
	search_fields = ('name',)
	ordering = ('name',)
	readonly_fields = ('created_at', 'updated_at')
	actions = ('mark_as_active', 'mark_as_inactive')

	@admin.action(description='Marcar proyectos seleccionados como activos')
	def mark_as_active(self, request, queryset):
		queryset.update(is_active=True)

	@admin.action(description='Marcar proyectos seleccionados como inactivos')
	def mark_as_inactive(self, request, queryset):
		queryset.update(is_active=False)
