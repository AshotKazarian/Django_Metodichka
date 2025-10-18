from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    """Модель жанра"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название жанра')
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tool(models.Model):
    """Модель инструмента"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название инструмента')
    
    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Proportion(models.Model):
    """Модель соотношения сторон"""
    option = models.CharField(max_length=50, unique=True, verbose_name='Вариант соотношения')
    
    class Meta:
        verbose_name = 'Соотношение'
        verbose_name_plural = 'Соотношения'
        ordering = ['option']
    
    def __str__(self):
        return self.option

class Work(models.Model):
    """Модель работы"""
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Автор',
        related_name='works'
    )
    title = models.CharField(max_length=255, verbose_name='Название работы')
    description = models.TextField(blank=True, verbose_name='Описание')
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2025)],
        verbose_name='Год создания'
    )
    genre = models.ForeignKey(
        Genre, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Жанр'
    )
    tools = models.ManyToManyField(
        Tool, 
        blank=True, 
        verbose_name='Инструменты'
    )
    proportion = models.ForeignKey(
        Proportion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='Соотношение сторон'
    )
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='Рейтинг'
    )
    tags = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name='Теги (через запятую)'
    )
    image = models.ImageField(
        upload_to='works/%Y/%m/%d/', 
        verbose_name='Изображение работы'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.author.username}"
    
    def get_tags_list(self):
        """Получить теги в виде списка"""
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def get_tools_list(self):
        """Получить инструменты в виде списка названий"""
        return [tool.name for tool in self.tools.all()]