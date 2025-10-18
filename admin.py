from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Genre, Tool, Proportion, Work

# Расширяем стандартного пользователя
class WorkInline(admin.StackedInline):
    """Инлайн для отображения работ пользователя"""
    model = Work
    extra = 0
    fields = ('title', 'year', 'genre', 'rating')
    readonly_fields = ('created_at',)

class CustomUserAdmin(UserAdmin):
    """Кастомная админка пользователя с работами"""
    inlines = [WorkInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_works_count', 'is_staff')
    
    def get_works_count(self, obj):
        return obj.works.count()
    get_works_count.short_description = 'Количество работ'

# Перерегистрируем User админку
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Админка для жанров"""
    list_display = ('name', 'get_works_count')
    search_fields = ('name',)
    list_per_page = 20
    
    def get_works_count(self, obj):
        return obj.work_set.count()
    get_works_count.short_description = 'Количество работ'

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    """Админка для инструментов"""
    list_display = ('name', 'get_works_count')
    search_fields = ('name',)
    list_per_page = 20
    
    def get_works_count(self, obj):
        return obj.work_set.count()
    get_works_count.short_description = 'Количество работ'

@admin.register(Proportion)
class ProportionAdmin(admin.ModelAdmin):
    """Админка для соотношений"""
    list_display = ('option', 'get_works_count')
    search_fields = ('option',)
    list_per_page = 20
    
    def get_works_count(self, obj):
        return obj.work_set.count()
    get_works_count.short_description = 'Количество работ'

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    """Админка для работ"""
    list_display = ('title', 'author', 'year', 'genre', 'rating', 'created_at')
    list_filter = ('genre', 'year', 'proportion', 'created_at', 'author')
    search_fields = ('title', 'description', 'tags', 'author__username')
    list_editable = ('rating',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tools',)
    list_per_page = 20
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('author', 'title', 'description', 'year', 'image')
        }),
        ('Классификация', {
            'fields': ('genre', 'tools', 'proportion', 'tags')
        }),
        ('Рейтинги и даты', {
            'fields': ('rating', 'created_at', 'updated_at')
        }),
    )
    
    def get_queryset(self, request):
        """Оптимизация запросов к базе данных"""
        return super().get_queryset(request).select_related('author', 'genre', 'proportion').prefetch_related('tools')