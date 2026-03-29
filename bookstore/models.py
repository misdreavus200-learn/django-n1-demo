from django.db import models


class Author(models.Model):
    name = models.CharField('著者名', max_length=100)
    bio = models.TextField('プロフィール', blank=True)
    country = models.CharField('出身国', max_length=50, default='日本')

    class Meta:
        verbose_name = '著者'
        verbose_name_plural = '著者一覧'

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField('書籍タイトル', max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books', verbose_name='著者')
    price = models.IntegerField('価格')
    published_at = models.DateField('出版日')
    genre = models.CharField('ジャンル', max_length=50)

    class Meta:
        verbose_name = '書籍'
        verbose_name_plural = '書籍一覧'

    def __str__(self):
        return self.title


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name='書籍')
    reviewer_name = models.CharField('レビュアー', max_length=100)
    rating = models.IntegerField('評価', choices=[(i, f'{i}★') for i in range(1, 6)])
    comment = models.TextField('コメント')
    created_at = models.DateTimeField('投稿日時', auto_now_add=True)

    class Meta:
        verbose_name = 'レビュー'
        verbose_name_plural = 'レビュー一覧'

    def __str__(self):
        return f'{self.book.title} - {self.reviewer_name}'
