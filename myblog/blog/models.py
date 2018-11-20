from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=128) # max_length で保存できる最大文字数の指定が必須
    text = models.TextField() # 文字数制限なしの文字列を保存する
    posted_at = models.DateTimeField(auto_now_add=True) # auto_now_add=True を指定することで自動的にデータが保存されたときの日時が保存される
    last_modify = models.DateTimeField(auto_now=True)  # auto_now=True データに変更が加えられた日時は保存されるようになる
    like = models.IntegerField(default=0) # default=0 でデータ作成時に何も指定しなかった場合に自動的に 0 が保存されるようにする設定、デフォルト値
    def __str__(self):
        """print()されたときに表示する文字列"""
        return self.title

class Comment(models.Model):
    text = models.TextField()  # 文字数制限なしの文字列を保存する
    posted_at = models.DateTimeField(auto_now_add=True) # 自動的にデータが保存されたときの日時が保存される
    article = models.ForeignKey(to=Article, related_name='comments', on_delete=models.CASCADE)
    # to=ArticleとすることでArticleモデルへのリレーションを指定できる
    # related_name='comments' で Article から comments という名前で Comment にアクセスできるようにする
    # ex) Article.comments.all()でその記事に対するコメントを全件取得
    # on_delete=models.CASCADE で参照先の記事が削除されたときにコメントも自動的に削除されるようになる
    def __str__(self):
        """print()されたときに表示する文字列"""
        return self.text
