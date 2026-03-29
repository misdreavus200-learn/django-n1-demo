from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="著者名")),
                ("bio", models.TextField(blank=True, verbose_name="プロフィール")),
                ("country", models.CharField(default="日本", max_length=50, verbose_name="出身国")),
            ],
            options={"verbose_name": "著者", "verbose_name_plural": "著者一覧"},
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="書籍タイトル")),
                ("price", models.IntegerField(verbose_name="価格")),
                ("published_at", models.DateField(verbose_name="出版日")),
                ("genre", models.CharField(max_length=50, verbose_name="ジャンル")),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="bookstore.author",
                        verbose_name="著者",
                    ),
                ),
            ],
            options={"verbose_name": "書籍", "verbose_name_plural": "書籍一覧"},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reviewer_name", models.CharField(max_length=100, verbose_name="レビュアー")),
                (
                    "rating",
                    models.IntegerField(
                        choices=[(1, "1★"), (2, "2★"), (3, "3★"), (4, "4★"), (5, "5★")],
                        verbose_name="評価",
                    ),
                ),
                ("comment", models.TextField(verbose_name="コメント")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="投稿日時")),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="bookstore.book",
                        verbose_name="書籍",
                    ),
                ),
            ],
            options={"verbose_name": "レビュー", "verbose_name_plural": "レビュー一覧"},
        ),
    ]
