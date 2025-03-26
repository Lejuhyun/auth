1. ## 장고설치 및 프로젝트 시작 ##
```shell
python -m venv venv
source venv/script/activate
pip install django
git init 
django-admin startproject auth . 
django-admin startapp accounts
```
2. ## 앱 등록(settings.py) ##
installed_apps에 'accounts' 추가하기

3. ## 베이스 html 등록(settings.py) ##
- templates에 'DIRS': [BASE_DIR/'templates'] 쓰기
- 최상단에 templates 폴더 만들기
- templates 폴더에 base.html 파일 생성

4. ## base.html ##
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

5. ## model 생성(accounts) ##
```python
from django.contrib.auth.models import AbstractUser
class User(AbstractUser): # AbstractUser를 상속받음
    pass
```
- AbstractUser는 Django에서 기본 제공하는 User 모델(username, email, password 같은 필드 포함)
- class User(AbstractUser)는 기본 User 모델을 상속해서 새로운 User 모델을 만드는 것.

6. ## 장고가 만든 user 모델과 내가 만든 user 모델의 충돌 방지하기(settings.py) ##
```python
AUTH_USER_MODEL = 'accounts.User' # account라는 앱에 User라는 클래스 사용할거야.
```
7. ## migration 파일 생성하기 ##
```shell
python manage.py makemigrations
python manage.py migrate
```
8. ## url 설정하기 ##
- auth -> urls.py 
```python
python('accounts/', include('accounts.url'))
```
## 8-1. accounts 앱 하위에 urls.py 생성 ##
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name="signup"),
]
```

9. ## signup 함수 생성 (views.py) ##
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
10. ## account 앱 하위에 templates 폴더 생성 => signup.html 생성 ##
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

## login 기능 설정 ##
- url 설정 => 함수생성
## 1. path 설정(urls.py) ##
```python
path('login/', views.login, name='login'),
```
## 2. 로그인 함수 생성 (views.py) ##
```python
def login(request):
    pass
```
- model, form , 함수 차이
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

- render(request, '템플릿파일.html', context)
    - 템플릿과 데이터를 결합하여 웹 페이지를 사용자에게 제공.
    - context는 템플릿에 전달할 데이터를 담고 있는 딕셔너리 객체
    - 템플릿에서 {{ variable_name }}과 같은 방식으로 데이터를 출력
