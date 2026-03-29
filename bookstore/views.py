import time
from contextlib import contextmanager
from django.db import connection
from django.shortcuts import render
from .models import Book


@contextmanager
def capture_queries():
    """
    DEBUG=False でもクエリをキャプチャできるコンテキストマネージャ。
    connection.execute_wrapper を使い、実行されたSQLを自前で収集する。
    """
    captured = []

    def recorder(execute, sql, params, many, context):
        start = time.perf_counter()
        result = execute(sql, params, many, context)
        elapsed = time.perf_counter() - start
        # パラメータをSQLに埋め込んで人間が読みやすい形にする
        try:
            if params:
                readable = sql % tuple(
                    f"'{p}'" if isinstance(p, str) else p for p in (params if many else params)
                )
            else:
                readable = sql
        except Exception:
            readable = sql
        captured.append({'sql': readable, 'time': f'{elapsed:.6f}'})
        return result

    with connection.execute_wrapper(recorder):
        yield captured


def _build_stats(captured, elapsed_ms):
    total_time = sum(float(q['time']) for q in captured)
    return {
        'count': len(captured),
        'total_time_ms': round(total_time * 1000, 2),
        'queries': captured[:100],
        'truncated': len(captured) > 100,
    }


def index(request):
    from .models import Author, Review
    context = {
        'book_count': Book.objects.count(),
        'author_count': Author.objects.count(),
        'review_count': Review.objects.count(),
    }
    return render(request, 'bookstore/index.html', context)


def books_n1(request):
    """N+1問題が発生するビュー"""
    start = time.perf_counter()

    with capture_queries() as captured:
        # ❌ N+1問題: 全件取得後、ループ内でLAZY LOADしている
        books = list(Book.objects.all())
        book_data = []
        for book in books:
            book_data.append({
                'title': book.title,
                'author_name': book.author.name,      # 毎回 SELECT author 発行!
                'genre': book.genre,
                'price': book.price,
                'avg_rating': _get_avg_rating(book),  # 毎回 SELECT review も発行!
            })

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    return render(request, 'bookstore/books.html', {
        'book_data': book_data,
        'stats': _build_stats(captured, elapsed_ms),
        'elapsed_ms': elapsed_ms,
        'mode': 'n1',
        'title': '❌ N+1問題あり',
        'description': 'Book.objects.all() で全件取得後、ループ内で book.author.name と review集計を呼ぶと…',
    })


def books_optimized(request):
    """最適化済みビュー"""
    start = time.perf_counter()

    with capture_queries() as captured:
        # ✅ select_related / prefetch_related で一括取得
        books = list(
            Book.objects
            .select_related('author')
            .prefetch_related('reviews')
            .all()
        )
        book_data = []
        for book in books:
            reviews = book.reviews.all()
            avg = sum(r.rating for r in reviews) / len(reviews) if reviews else 0
            book_data.append({
                'title': book.title,
                'author_name': book.author.name,
                'genre': book.genre,
                'price': book.price,
                'avg_rating': round(avg, 1),
            })

    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    return render(request, 'bookstore/books.html', {
        'book_data': book_data,
        'stats': _build_stats(captured, elapsed_ms),
        'elapsed_ms': elapsed_ms,
        'mode': 'optimized',
        'title': '✅ N+1問題なし（最適化済み）',
        'description': 'select_related("author") と prefetch_related("reviews") を使うと…',
    })


def _get_avg_rating(book):
    """個別にSQLを2本発行する（N+1をさらに悪化させる例）"""
    reviews = book.reviews.all()
    if not reviews:
        return 0
    return round(sum(r.rating for r in reviews) / reviews.count(), 1)


def explain(request):
    return render(request, 'bookstore/explain.html')
