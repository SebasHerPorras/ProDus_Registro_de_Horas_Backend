from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nombre')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        db_table = 'project'
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ['name']

    def __str__(self):
        return self.name


class CoordinatorXProject(models.Model):
    coordinator = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='coordinator_projects',
        verbose_name='Coordinador',
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='coordinators',
        verbose_name='Proyecto',
    )
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')

    class Meta:
        db_table = 'coordinator_x_project'
        verbose_name = 'Coordinador por Proyecto'
        verbose_name_plural = 'Coordinadores por Proyecto'
        constraints = [
            models.UniqueConstraint(
                fields=['coordinator', 'project'],
                name='uq_coordinator_project',
            ),
        ]

    def __str__(self):
        return f'{self.coordinator} - {self.project}'


class AssistantXProject(models.Model):
    assistant = models.ForeignKey(
        'users.Assistant',
        on_delete=models.CASCADE,
        related_name='assistant_projects',
        verbose_name='Asistente',
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='assistants',
        verbose_name='Proyecto',
    )
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de asignación')

    class Meta:
        db_table = 'assistant_x_project'
        verbose_name = 'Asistente por Proyecto'
        verbose_name_plural = 'Asistentes por Proyecto'
        constraints = [
            models.UniqueConstraint(
                fields=['assistant', 'project'],
                name='uq_assistant_project',
            ),
        ]

    def __str__(self):
        return f'{self.assistant} - {self.project}'