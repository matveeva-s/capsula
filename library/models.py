from django.db import models
from django.utils import timezone
from user.models import User


class Book(models.Model):
    CLASSIC_RUSSIAN = 0
    CLASSIC_FOREIGN = 1
    SCIENCE_AND_EDUCATION = 2
    COMPUTER_SCIENCE = 3
    EDUCATION = 4
    MODERN = 5
    ADVENTURE = 6
    FANTASY = 7
    HORROR = 8
    DETECTIVES = 9
    BUSINESS = 10
    PSYCHOLOGY = 11
    HEALTH = 12
    DICTIONARY = 13
    POETRY_AND_DRAMA = 14
    COMICS = 15
    HOBBY = 16
    CULTURE_AND_ART = 17
    EROTICA = 18
    CHILD = 19
    RELIGION = 20
    PEREODIC = 21
    NOVEL = 22
    SCIENCE_FICTION = 23
    STORY = 24


    ABSTRACT_BOOK_GENRES = (
        (CLASSIC_RUSSIAN, 'Классическая русская литература'),
        (CLASSIC_FOREIGN, 'Классическая зарубежная литература'),
        (SCIENCE_AND_EDUCATION, 'Наука и образование'),
        (BUSINESS, 'Бизнес-литература и саморазвитие'),
        (COMPUTER_SCIENCE, 'Компьютерная литература'),
        (EDUCATION, 'Учебная литература'),
        (MODERN, 'Современная проза'),
        (ADVENTURE, 'Приключения'),
        (FANTASY, 'Фэнтези и фантастика'),
        (HORROR, ' Ужасы, мистика'),
        (DETECTIVES, 'Детективы'),
        (PSYCHOLOGY, 'Книги по психологии'),
        (HEALTH, 'Красота и здоровье'),
        (DICTIONARY, 'Словари, справочники'),
        (POETRY_AND_DRAMA, 'Поэзия и драматургия'),
        (COMICS, 'Комиксы, манга'),
        (HOBBY, 'Дом, семья, хобби и досуг'),
        (CULTURE_AND_ART, 'Культура и искусство'),
        (EROTICA, 'Эротика и секс, любовные романы'),
        (CHILD, 'Детские книги'),
        (RELIGION, 'Религия'),
        (PEREODIC, 'Периодические издания, газеты и журналы'),
        (NOVEL, 'Роман'),
        (SCIENCE_FICTION, 'Научная фантастика'),
        (STORY, 'Повесть'),
    )

    title = models.CharField(verbose_name='Название', max_length=255)
    authors = models.TextField(
        verbose_name='Авторы', help_text='Имена авторов через запятую',
        blank=True, null=True,
    )
    genre = models.IntegerField(verbose_name='Жанр', choices=ABSTRACT_BOOK_GENRES)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Абстрактная книга'
        verbose_name_plural = 'Абстрактные книги'
        ordering = ['title']

    def __str__(self):
        return self.title


def photo_upload_path(instance, *args, **kwargs):
    """Generates upload path for ImageField/FileField"""
    name = '%s.jpg' % str(instance.id)
    location = 'books/%s' % name
    return location


class BookItem (models.Model):
    AVAILABLE = 0
    READING = 1
    NOT_AVAILABLE = 2

    BOOK_ITEM_STATUSES = (
        (AVAILABLE, 'Доступна'),
        (NOT_AVAILABLE, 'Недоступна'),
        (READING, 'Читается другим пользователем'),
    )

    book = models.ForeignKey(Book, related_name='item', verbose_name='Книга', on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, related_name='book_items', verbose_name='Владелец',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    isbn = models.CharField(verbose_name='ISBN', max_length=255, blank=True, default='')
    status = models.IntegerField(verbose_name='Статус книги', choices=BOOK_ITEM_STATUSES, default=AVAILABLE)
    image = models.CharField('URL картинки', max_length=150, unique=True, blank=False, null=True)

    class Meta:
        verbose_name = 'Экземпляр книги'
        verbose_name_plural = 'Экземпляры книг'
        ordering = ('pk',)

    def __str__(self):
        return self.book.title


class Swap (models.Model):
    CONSIDERED = 0
    ACCEPTED = 1
    REJECTED = 2
    READING = 3
    RETURNED = 4

    SWAP_STATUSES = (
        (CONSIDERED, 'Заявка рассматривается'),
        (ACCEPTED, 'Заявка принята, книга ожидает передачи'),
        (REJECTED, 'Заявка отклонена'),
        (READING, 'Книга читается'),
        (RETURNED, 'Книга возвращена'),
    )

    reader = models.ForeignKey(User, related_name='reader', verbose_name='Читатель', on_delete=models.CASCADE)
    book = models.ForeignKey(BookItem, verbose_name='Книга в обмене', on_delete=models.CASCADE)
    status = models.IntegerField(verbose_name='Статус обмена', choices=SWAP_STATUSES)
    created_at = models.DateTimeField(verbose_name='Дата создания', default=timezone.localtime())
    updated_at = models.DateTimeField(verbose_name='Дата изменения', default=timezone.localtime())

    class Meta:
        verbose_name = 'Обмен/заявка'
        verbose_name_plural = 'Обмены и заявки'
        ordering = ('pk',)

    def __str__(self):
        return self.reader.first_name


class Wishlist (models.Model):

    user = models.ForeignKey(User, related_name='user', verbose_name='Пользователь', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, verbose_name='Книга в вишлисте', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Дата создания', default=timezone.localtime())

    class Meta:
        verbose_name = 'Вишлист'
        verbose_name_plural = 'Вишлист'
        ordering = ('pk',)

    def __str__(self):
        return self.user.first_name
