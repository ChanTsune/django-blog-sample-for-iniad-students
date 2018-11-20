from django.shortcuts import render, redirect
from django.http import Http404
from django.http.response import JsonResponse
from . import models
# Create your views here.


def index(request):
    """http://localhost:8000/
    トップページ
    """
    # templates以下のパスを書く(アプリケーション名[blog] / ファイル名[index.html])
    template_name = "blog/index.html"
    # request に http 通信の情報がいろいろ入っている
    return render(request, template_name)


def new(request):
    """http://localhost:8000/new/
    新規記事の投稿ページ
    """
    template_name = "blog/new.html"
    if request.method == "POST": # POSTメソッドで通信されたとき(記事が投稿されたとき)
        # request.POST <- にフォームで入力されたデータが入っている
        # フォーム内の各要素の id属性の名前でアクセスできる
        article = models.Article.objects.create( # データベースに記事を新規保存
            title=request.POST["title"], text=request.POST["text"]) # それぞれのフィールドに何を入れるか指定
        return redirect(view_article, article.pk) # 記事の詳細ページにリダイレクト
    return render(request, template_name)


def article_all(request):
    """http://localhost:8000/article/all/
    記事の詳細ページ
    """
    template_name = "blog/article_all.html"
    # models.Article.objects.all() で記事を全件取得
    # models.Article.objects.order_by("フィールド名")で昇順ソートもできる
    # models.Article.objects.order_by("-フィールド名")で降順ソート
    context = {"articles": models.Article.objects.all()}
    return render(request, template_name, context) # 第三引数に辞書を渡すことでテンプレート内で変数として使える、辞書のキーの値がテンプレート内での変数名


def view_article(request, pk):
    """http://localhost:8000/article/<int:pk>/
    記事の詳細ページ
    """
    template_name = "blog/view_article.html"
    try:
        # models.Article.objects.get(pk=pk) アクセスされた数字(pk)に該当する記事をデータベースから取得
        article = models.Article.objects.get(pk=pk)
    except models.Article.DoesNotExist:
        # 該当する記事がなければ 404エラーページを表示
        raise Http404
    if request.method == "POST": # コメントが投稿されたとき
        models.Comment.objects.create( # コメントをデータベースに新規保存
            # 投稿されたデータはフォーム内の各要素の id属性の名前でアクセスできる
            text=request.POST["text"], article=article)# <- 記事に対してリレーションを指定
    context = {"article": article}
    return render(request, template_name, context)


def edit(request, pk):
    """http://localhost:8000/article/<int:pk>/edit/
    記事の編集ページ
    """
    template_name = "blog/edit.html"
    try:
        article = models.Article.objects.get(pk=pk) # アクセスされた数字(pk)に該当する記事をデータベースから取得
    except models.Article.DoesNotExist: 
        raise Http404 # 該当する記事が無かったら 404 エラーページ
    if request.POST == "POST":
        article.title = request.POST["title"] # 記事の内容を投稿されたデータに置き換え
        article.text = request.POST["text"] # 同上
        article.save() # saveメソッドを実行しないと変更が反映されない！！
        return redirect(view_article, pk) # 詳細ページにリダイレクト
    context = {"article": article}
    return render(request, template_name, context)


def delete(request, pk):
    """http://localhost:8000/article/<int:pk>/delete/
    記事の削除
    """
    try:
        article = models.Article.objects.get(pk=pk) #アクセスされた数字(pk)に該当する記事をデータベースから取得
    except models.Article.DoesNotExist:
        raise Http404  # 該当する記事が無かったら 404 エラーページ
    article.delete() # 記事をデータベースから削除
    return redirect(article_all) # i一覧ページにリダイレクト


def like(request, pk):
    """http://localhost:8000/article/<int:pk>/like/
    いいね
    """
    try:
        article = models.Article.objects.get(pk=pk) #アクセスされた数字(pk)に該当する記事をデータベースから取得
    except models.Article.DoesNotExist:
        raise Http404  # 該当する記事が無かったら 404 エラーページ
    article.like += 1  # ここでいいねの数を増やす
    article.save()  # 保存をする
    return redirect(view_article, pk) # 詳細ページにリダイレクト


def api_like(request, pk):
    """http://localhost:8000/api/like/<int:pk>/"""
    try:
        article = models.Article.objects.get(pk=pk) #アクセスされた数字(pk)に該当する記事をデータベースから取得
    except models.Article.DoesNotExist:
        raise Http404  # 該当する記事が無かったら 404 エラーページ
    article.like += 1  # ここでいいねの数を増やす
    article.save()  # 保存をする
    return JsonResponse({"like": article.like}) # json形式のデータを送信
    # ブラウザ側では '{"like": 1}' のような形の文字列として受け取られる
