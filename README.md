# N+1問題 体験サイト

DjangoのORMでN+1問題がどのように発生し、どう解決するかを**体験できる**Webサイトです。

## 🎯 機能

| ページ | 説明 |
|--------|------|
| `/` | トップページ |
| `/books/n1/` | ❌ N+1問題が発生するページ（発行SQL数・時間を表示） |
| `/books/optimized/` | ✅ `select_related` / `prefetch_related` で最適化済み |
| `/explain/` | 解説ページ（仕組み・コード比較・検出ツール） |

## 🚀 ローカル起動

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_data   # サンプルデータ投入
python manage.py runserver
```

ブラウザで http://127.0.0.1:8000 を開く

## ☁️ Render.com へのデプロイ（無料）

1. このリポジトリを GitHub に push
2. [render.com](https://render.com) でアカウント作成
3. **New → Blueprint** → リポジトリを選択
4. `render.yaml` が自動検出され、WebサービスとDBが作成される

## 技術スタック

- Django 5.0
- django-debug-toolbar
- WhiteNoise（静的ファイル配信）
- SQLite（ローカル） / PostgreSQL（本番）
- Gunicorn
- Render.com（無料ホスティング）

## N+1問題とは

```python
# ❌ 書籍N件 → N+1本のSQL
books = Book.objects.all()
for book in books:
    print(book.author.name)  # 毎回SQLが発行される

# ✅ 常に2本のSQL
books = Book.objects.select_related('author').prefetch_related('reviews').all()
for book in books:
    print(book.author.name)  # 追加SQLなし
```
