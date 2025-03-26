from django.shortcuts import render,redirect
from .forms import ArticleForm
# Create your views here.
def index(request):
    return render(request, 'index.html')

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