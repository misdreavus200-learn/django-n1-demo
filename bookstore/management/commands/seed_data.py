"""
サンプルデータを投入するmanagement command
python manage.py seed_data
python manage.py seed_data --books 500   # 書籍数を指定（デフォルト: 300）
"""
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from bookstore.models import Author, Book, Review

FIRST_NAMES = [
    '太郎', '花子', '次郎', '美咲', '健太', 'さくら', '雄一', 'あかり', '誠', '恵子',
    '翔', '葵', '蓮', '陽菜', '湊', '凛', '大翔', '咲', '悠', '莉子',
    '拓海', '七海', '颯', '結衣', '蒼', '愛', '隼', '栞', '陸', '優菜',
]
LAST_NAMES = [
    '田中', '佐藤', '山田', '鈴木', '伊藤', '渡辺', '中村', '小林', '加藤', '吉田',
    '山本', '松本', '井上', '木村', '林', '清水', '山崎', '池田', '橋本', '阿部',
    '石川', '前田', '藤田', '後藤', '岡田', '長谷川', '村上', '近藤', '石田', '坂本',
]
COUNTRIES = ['日本'] * 80 + ['アメリカ', 'イギリス', 'フランス', 'ドイツ', '韓国', '中国']
BIO_TEMPLATES = [
    '{pref}生まれ。受賞歴多数の実力派作家。',
    '{pref}出身。デビュー作からベストセラーを連発。',
    '{pref}在住。独自の世界観で多くの読者を魅了。',
    '{pref}育ち。文学賞の常連として知られる。',
    '{pref}在住のベテラン作家。幅広いジャンルを手がける。',
]
PREFS = [
    '東京都', '大阪府', '京都府', '神奈川県', '愛知県', '福岡県', '北海道',
    '埼玉県', '千葉県', '兵庫県', '広島県', '宮城県', '長野県', '静岡県',
]

GENRES = ['文学', 'ミステリ', 'SF', 'ファンタジー', 'サスペンス', '歴史', 'ホラー', '恋愛', 'エッセイ']
TITLE_PREFIXES = [
    '夜の', '朝の', '青い', '赤い', '白い', '黒い', '遠い', '近い', '深い', '高い',
    '静かな', '激しい', '消えた', '残された', '失われた', '見えない', '隠された',
]
TITLE_NOUNS = [
    '星', '海', '山', '川', '空', '月', '太陽', '風', '雨', '雪',
    '影', '光', '声', '夢', '記憶', '時間', '場所', '約束', '秘密', '真実',
    '扉', '窓', '橋', '道', '家', '森', '丘', '島', '砂漠', '都市',
    '少女', '少年', '女', '男', '老人', '子供', '教師', '探偵', '医師', '詩人',
]
TITLE_SUFFIXES = ['', 'の物語', 'の記憶', 'の果て', 'の彼方', 'を探して', 'との別れ', 'への旅', 'の秘密', '']

COMMENTS = [
    '読み始めたら止まらなかった。素晴らしい作品です。',
    '文章が美しく、情景が目に浮かびます。',
    '期待以上でした。著者の新境地を感じます。',
    'ちょっと難しかったけど、最後は感動しました。',
    '友人に薦められて読みました。大正解でした！',
    '伏線の回収が見事。二度読みしたくなります。',
    '登場人物の心理描写が細かくてリアル。',
    'テンポが良くてあっという間に読み終えました。',
    '深いテーマを扱っているが読みやすい。',
    '続編が待ち遠しい傑作です。',
    '久しぶりに心を揺さぶられる読書体験でした。',
    '独特の文体がクセになります。',
    'ラストが予想外で鳥肌が立ちました。',
    '何度でも読み返したい一冊。',
    '主人公の成長に自分を重ねてしまいました。',
    '重いテーマだが後味は爽やか。',
    'ページをめくる手が止まらなかった。',
    '日常の切り取り方が秀逸です。',
    '読後感が最高。しばらく余韻が続きました。',
    '著者の他の作品も読みたくなりました。',
]


class Command(BaseCommand):
    help = 'N+1デモ用サンプルデータを大量投入します'

    def add_arguments(self, parser):
        parser.add_argument(
            '--books', type=int, default=300,
            help='生成する書籍数（デフォルト: 300）'
        )

    def handle(self, *args, **options):
        num_books = options['books']
        num_authors = max(30, num_books // 5)

        self.stdout.write('既存データを削除中...')
        Review.objects.all().delete()
        Book.objects.all().delete()
        Author.objects.all().delete()

        # ── 著者を bulk_create ──────────────────────────────
        self.stdout.write(f'著者を {num_authors} 件作成中...')
        author_objs = []
        used_names = set()
        for _ in range(num_authors):
            while True:
                name = random.choice(LAST_NAMES) + random.choice(FIRST_NAMES)
                if name not in used_names:
                    used_names.add(name)
                    break
            pref = random.choice(PREFS)
            bio = random.choice(BIO_TEMPLATES).format(pref=pref)
            country = random.choice(COUNTRIES)
            author_objs.append(Author(name=name, bio=bio, country=country))

        Author.objects.bulk_create(author_objs)
        authors = list(Author.objects.all())

        # ── 書籍を bulk_create ──────────────────────────────
        self.stdout.write(f'書籍を {num_books} 件作成中...')
        base_date = date(2015, 1, 1)
        book_objs = []
        used_titles = set()
        for _ in range(num_books):
            while True:
                title = (
                    random.choice(TITLE_PREFIXES)
                    + random.choice(TITLE_NOUNS)
                    + random.choice(TITLE_SUFFIXES)
                )
                if title not in used_titles:
                    used_titles.add(title)
                    break
            pub_date = base_date + timedelta(days=random.randint(0, 365 * 9))
            book_objs.append(Book(
                title=title,
                author=random.choice(authors),
                price=random.choice([638, 748, 770, 858, 880, 990, 1100, 1320, 1540, 1760, 1980]),
                published_at=pub_date,
                genre=random.choice(GENRES),
            ))

        Book.objects.bulk_create(book_objs)
        books = list(Book.objects.all())

        # ── レビューを bulk_create（チャンク分割）──────────
        num_reviews_total = num_books * 10  # 平均10件/冊
        self.stdout.write(f'レビューを約 {num_reviews_total} 件作成中...')
        reviewer_names = [
            random.choice(LAST_NAMES) + random.choice(FIRST_NAMES) for _ in range(200)
        ]
        review_objs = []
        for book in books:
            for _ in range(random.randint(7, 15)):
                review_objs.append(Review(
                    book=book,
                    reviewer_name=random.choice(reviewer_names),
                    rating=random.randint(1, 5),
                    comment=random.choice(COMMENTS),
                ))

        # SQLiteのバインド変数上限を避けるため500件ずつ投入
        chunk_size = 500
        for i in range(0, len(review_objs), chunk_size):
            Review.objects.bulk_create(review_objs[i:i + chunk_size])

        total_reviews = Review.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ 完了！\n'
            f'   著者:   {len(authors):,} 件\n'
            f'   書籍:   {len(books):,} 件\n'
            f'   レビュー: {total_reviews:,} 件\n'
            f'\nN+1ページでは書籍 {len(books):,} 件 × 著者取得 = {len(books)+1:,} 本以上のSQLが発行されます！'
        ))
