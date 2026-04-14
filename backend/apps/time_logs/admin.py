from django.contrib import admin
from apps.time_logs.models import TimeLog, TimeLogStatus


@admin.register(TimeLogStatus)
class TimeLogStatusAdmin(admin.ModelAdmin):
	list_display = ('code', 'is_final')
	list_filter = ('is_final',)
	search_fields = ('code',)
	ordering = ('code',)


@admin.register(TimeLog)
class TimeLogAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'assistant_full_name',
		'assistant_username',
		'status',
		'check_in',
		'check_out',
		'project',
		'manager_user',
		'break_minutes',
		'has_close_form_data',
	)
	list_display_links = ('id', 'assistant_full_name')
	list_filter = ('status', 'project', 'manager_user', 'check_in', 'check_out')
	search_fields = (
		'assistant__user__full_name',
		'assistant__user__username',
		'project__name',
		'manager_user__full_name',
		'manager_user__username',
		'activities',
		'decision_comment',
	)
	ordering = ('-check_in',)
	readonly_fields = (
		'assistant',
		'project',
		'check_in',
		'check_out',
		'work_description',
		'break_minutes',
		'status',
		'decided_by',
		'manager_user',
		'decided_at',
		'decision_comment',
		'activities',
	)

	fieldsets = (
		('Información general', {
			'fields': ('assistant', 'status', 'check_in', 'check_out')
		}),
		('Formulario de cierre', {
			'fields': ('project', 'manager_user', 'activities', 'decision_comment', 'break_minutes')
		}),
		('Aprobación / decisión', {
			'fields': ('decided_by', 'decided_at', 'work_description')
		}),
	)

	@admin.display(description='Asistente', ordering='assistant__user__full_name')
	def assistant_full_name(self, obj):
		return obj.assistant.user.full_name

	@admin.display(description='Usuario', ordering='assistant__user__username')
	def assistant_username(self, obj):
		return obj.assistant.user.username

	@admin.display(description='Tiene datos de formulario', boolean=True)
	def has_close_form_data(self, obj):
		return bool(
			obj.project_id
			or obj.manager_user_id
			or (obj.activities or '').strip()
			or (obj.decision_comment or '').strip()
		)

	def has_add_permission(self, request):
		return False
