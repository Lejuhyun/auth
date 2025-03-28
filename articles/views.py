from django.shortcuts import render,redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid(): 
            article = form.save(commit=False) #게시물에 유저 정보가 없으므로 임시 저장해준다
            article.user = request.user # request 에서 user 정보를 article.user에 저장한다
            article.save() # 최종적으로 저장해준다
            return redirect('articles:index')
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)

def detail(request,id):
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article':article,
        'form': form,
    }
    return render(request, 'detail.html', context)

@login_required
def comment_create(request, article_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit = False)

        # 객체를 저장하는 경우
        # comment.user = request.user # 현재 로그인한 사람에 대한 정보
        # article = Article.objects.get(id=article_id)
        # comment.article = article

        # id 값을 저장하는 경우
        comment.user_id = request.user.id
        comment.article_id= article_id
        comment.save()
        return redirect('articles:detail', id=article_id)

@login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    if request.user == comment.user:
        comment.delete()

    return redirect('articles:detail', id = article_id)

@login_required
def delete(request,id):
    article = Article.objects.get(id=id)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')

@login_required
def update(request, id):
    article = Article.objects.get(id=id)
    if request.user != article.user:
        return redirect('articles:index')
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', id = id)
    else:
        form = ArticleForm(instance = article)

    context = {
        'form': form,
    }
    return render(request, 'update.html', context)