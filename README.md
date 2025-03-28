## 1. 장고설치 및 프로젝트 시작 
```shell
python -m venv venv
source venv/script/activate
pip install django
git init 
django-admin startproject auth . 
django-admin startapp accounts
```
## 2. 앱 등록(settings.py) 
installed_apps에 'accounts' 추가하기

## 3. 베이스 html 등록(settings.py) 
- templates에 'DIRS': [BASE_DIR/'templates'] 쓰기
- 최상단에 templates 폴더 만들기
- templates 폴더에 base.html 파일 생성

## 4. base.html 
- head 끝나기 전에 bootstrap 삽입 (include via cdn)
- body 끝나기 전에 bootstrap 삽입 
- body에 블럭 넣기
```html
    <div class="container">
        {% block body %}
        {% endblock %}
    </div>
```
- {% block body %}: Django 템플릿에서 블록(block) 을 정의하는 부분. 자식 템플릿에서 덮어쓰기(override)할 수 있는 영역을 의미.

## 5. model 생성(accounts) 
```python
from django.contrib.auth.models import AbstractUser
class User(AbstractUser): # AbstractUser를 상속받음
    pass
```
- AbstractUser는 Django에서 기본 제공하는 User 모델(username, email, password 같은 필드 포함)
- class User(AbstractUser)는 기본 User 모델을 상속해서 새로운 User 모델을 만드는 것.

## 6. 장고가 만든 user 모델과 내가 만든 user 모델의 충돌 방지하기(settings.py) 
```python
AUTH_USER_MODEL = 'accounts.User' # account라는 앱에 User라는 클래스 사용할거야.
```
## 7. migration 파일 생성하기 
```shell
python manage.py makemigrations
python manage.py migrate
```
## 8. url 설정하기 
- auth -> urls.py 
```python
python('accounts/', include('accounts.url'))
```
### 8-1. accounts 앱 하위에 urls.py 생성 
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
]
```

## 9. signup 함수 생성 (views.py) 
- accounts 앱 하위에 forms.py 생성하기

```python
from .models import User
from django.contrib.auth.forms import UserCreationForm # 장고가 미리 만들어놓은 form임

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User # 사용할 모델은 커스텀 user 모델
        fields = ('username',) # username 필드를 회원가입 폼에서 입력받도록 설정
```
- signup 함수 생성하기
```python
from django.shortcuts import render, redirect
# render: HTML 페이지를 보여줄때 사용
# redirect: 회원가입 후 로그인페이지로 이동
from .forms import CustomUserCreationForm
# CustomUserCreationForm: 커스텀 회원가입 폼

def signup(request):
    if request.method == "POST": #사용자가 POST 요청을 보내면
        form = CustomUserCreationForm(request.POST)
        #사용자가 입력한 데이터 받기
        # request.POST: 사용자가 제출한 데이터를 담는 객체
        if form.is_valid():
            #입력값 검증
            form.save()
            # DB에 저장
            return redirect("accounts:login")
            # 회원가입 후 로그인 페이지로 이동
    else: # GET 요청일 때
        form = CustomUserCreationForm()
        # 빈 폼을 보여준다
    
    context = {
        'form': form
    } # form 을 템플릿에 전달

    return render(request, 'signup.html', context) # signup.html에서 폼을 출력한다
```
## 10. account 앱 하위에 templates 폴더 생성 => signup.html 생성 
```html
{% extends 'base.html' %}
{% block body %}
<form action="" method = "POST">
    {% csrf_token %}
    {{form}}
    <input type="submit"> 
</form>
{% endblock %}
```

# login 기능 설정 
- url 설정 => 함수생성
## 1. path 설정(urls.py) 
```python
path('login/', views.login, name='login'),
```
## 2. 로그인 함수 생성 (views.py) 
```python
def login(request):
    pass
```
## 3. GET 요청이 들어왔을 때 보여줄 폼 생성(forms.py)
```python
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    pass
```
## 4. 로그인함수에서 폼 받아오기(views.py)
```python
from .forms import  CustomAuthenticationForm
def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('accounts:login')
    else:
        form = CustomAuthenticationForm()
    
    context = {
        'form': form
    }

    return render(request, 'login.html', context)
```
## 5. login.html 생성하기 (accounts=> templates)
```html
{% extends 'base.html' %}
{% block body %}
    <form action="" method='POST'>
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>
{% endblock %}
```

# logout 기능설정 
## 1. path 설정 (urls.py) 
```python
path('logout/', view.logout, name='logout')
```
## 2. logout 함수 생성 (views.py)
```python
from django.contrib.auth import logout as auth_logout
```


## base.html 수정
```html
    <nav class="nav">
        {% if user.is_authenticated %}
            <a href="" class = "nav-link disabled">{{user}}</a>
            <a href="{% url 'accounts:logout' %}" class = 'nav-link'>logout</a>
        {% else %}
        <a href="{% url 'accounts:signup' %}" class = "nav-link">signup</a>
        <a href="{% url 'accounts:login' %}" class= 'nav-link'>login</a>
        {% endif %}
    </nav>
```
# 새로운 앱 생성 
## 1. 시작
```shell
django-admin startapp articles
```
- auth => settings.py => 앱 등록하기

## 2. model 생성 (models.py)
```python
from django.db import models
from accounts.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    # 1. 직접참조 
    # user = models.ForeignKey(User, on_delete = models.CASCADE)
    # 2. settings.py 변수 활용
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    # 3. get_user_model
    # user = models.ForeignKey(get_user_model(),on_delete = models.CASCADE)
```
### 2-1. 참조하기
```shell
python manage.py makemigrations
python manage.py migarte
```
## 3. url 생성하기
- project 파일(auth)에 url 생성
```python
path('articles/', include('articles.urls')),
```

- article 파일 하단에 urls.py 생성
```python
from django.urls import path
from  . import views
app_name = 'articles'
urlpatterns = [
    path('', views.index, name='index'),
]
```
# index 기능 구현
## 1. index 함수 생성 (views.py)
```python
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'index.html', context)
```
## 2. articles 하위에 templates 파일 생성 (=> index.html 생성)
```html
{% extends 'base.html' %}

{% block body %}
    <h1>index</h1>
    {% for article in articles %}
        <h3>{{article.title}}</h3>
        <p>{{article.content}}</p>
        <p>{{article.user}}</p>
        <hr>
    {% endfor %}
{% endblock %}
```
# create 기능 구현

## 1. base.html 에 추가하기
```html
<a href="{% url 'articles:create' %}" class = 'nav-link'>create</a>
```

## 2. url 생성하기 (articles => urls.py)
```python
path('create/', views.create, name='create'),
```

## 3. create 함수 생성하기 (articles => views.py)

### 3-1. form 생성하기 (articles => forms.py)
```python
from django.forms import ModelForm
from . models import Article

class ArticleForm(ModelForm):
    class Meta():
        model= Article
        exclude = ('user',)
```
### 3-2. form 받아와서 create 함수 생성하기 (articles => views.py)
```python
from .forms import ArticleForm
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
```

## 4. html 생성하기 (articles 하위에 templates 폴더 생성 => create.html 생성)
```html
{% extends 'base.html' %}

{% block body %}
    <form action="" method = "POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>
{% endblock %}
```





# model, form , 함수 차이
- model: 데이터 저장 및 관리
        - ex) class User(): User라는 테이블이 DB에 생성된다
        - 데이터를 추가/조회/삭제할때 사용한다
- form: 사용자 입력을 처리 
        - ex) class UserForm(): 폼을 자동으로 생성해준다
        - 입력값이 올바른지 검증해준다
- function: 특정 작업을 수행
        - ex) 회원가입을 처리하는 함수
        - POST: 폼 데이터를 받아서 저장
        - GET: 빈 폼을 보여줌

# render(request, '템플릿파일.html', context)
- 템플릿과 데이터를 결합하여 웹 페이지를 사용자에게 제공.
- context는 템플릿에 전달할 데이터를 담고 있는 딕셔너리 객체
- 템플릿에서 {{ variable_name }}과 같은 방식으로 데이터를 출력


# 댓글 기능 생성

## 1. 모델 구현하기 (models.py)
```python
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
```
- migration 작업
```shell
python manage.py makemigrations
python manage.py migrate
```
## 2. url 만들기
- index.html
```html
<a href="{% url 'articles:deatil' article.id %}">detail</a>
```
- (articles => urls.py)
```python
path('<int:id>/', views.detail, name = 'detail')
```

## 3. views 만들기
```python
def detail(request,id):
    article = Article.objects.get(id=id)
    context = {
        'article':article,
    }
    return render(request, 'detail.html', context)
```

## 4. html 만들기
```html
{% extends 'base.html' %}

{% block body %}
    <h1>{{article.title}}</h1>
    <p>{{article.content}}</p>
    <p>{{article.user}}</p>

{% endblock %}
```

## 5. comment form 만들기
- forms.py
```python
class CommentForm(ModelForm):
    class Meta():
        model= Comment
        fields = ('content', )
```
- views.py
```python
from .forms import ArticleForm, CommentForm
def detail(request,id):
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article':article,
        'form': form, # comment를 변수형태로 저장해서 article에 보냄
    }
    return render(request, 'detail.html', context)
```

## 6. detail.html 수정하기
```html
    <form action="{% url 'articles: comment_create' article.id }" method = "POST">
        {% csrf_token %}
        {{form}}
        <input type="submit">
    </form>
```
- action을 해야하는 이유: 

## 7. urls.py
```python
path('<int:article_id>/comments/create/', views.comment_create, name = 'comment_create'),
```

## 8. comment_create 함수 생성(views.py)
```python
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
```

## 9. 댓글 출력 (detail.html)
```html
    <hr>
    {% for comment in article.comment_set.all %}
        <li>{{comment.user.username}}-{{comment.content}}</li>
    {% endfor %}
```

# 댓글 삭제 기능 구현

## 1. delete 버튼 생성 (detail.html)
```html
<a href="{% url 'articles:commetn_delete' article.id comment.id %}">delete</a>
```

## 2. 경로 설정 (urls.py)
```python
path('<int:article_id>/comments/<int:comment_id>/delete/', views.comment_delete, name = 'comment_delete')
```

## 3. 함수 생성(views.py)

```python
from .models import Article, Comment
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    comment.delete()
    return redirect('articles:detail', id = article_id)
```

## 4. 자기 댓글만 삭제할 수 있게(detail.html)
- 자기 댓글에만 delete버튼 보이게
```html
        {% if user == comment.user %}
            <a href="{% url 'articles:comment_delete' article.id comment.id %}">delete</a>
        {% endif %}
```
- 자기 댓글만 삭제할수 있도록 함수 구현(views.py)
```python
@login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id = comment_id)
    if request.user == comment.user:
        comment.delete()
        
    return redirect('articles:detail', id = article_id)
```

# 게시물 삭제 
## 1. 버튼 생성 (detail.html)
```html
    {% if user == article.user %} 
    <a href="">update</a>
    <a href="{%url 'articles:delete' article.id %}">delete</a>
```

## 2. 경로생성 (urls.py)
```python
 path('<int:article_id>/delete/', views.delete, name = 'delete')
```

## 3. 함수생성 (views.py)
```python
@login_required
def delete(request,id):
    article = Article.objects.get(id=id)
    if request.user == article.user:
        article.delete()
    return redirect('articles:index')
```