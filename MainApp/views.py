from django.http import Http404, HttpResponse,HttpResponseNotFound,HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

@login_required(login_url='index-page') #"home"
# добавлять новый сниппет может только авторизированный пользователь
def add_snippet_page(request):
    # Создаем пустую форму при запросе методом GET
    if request.method == "GET":
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form 
            }
        return render(request, 'pages/add_snippet.html', context)
    # Получаем данные из формы и на их основе создаем новый snippet в БД
    if request.method == "POST":
       form = SnippetForm(request.POST)
       if form.is_valid():
           #form.save()
           snippet = form.save(commit=False)
           if request.user.is_authenticated:
               snippet.user = request.user
               snippet.save()
           return redirect("snippets-page") # GET /snippets/list
       return render(request,'pages/add_snippet.html',{'form': form})

def snippets_page(request):
    #snippets = Snippet.objects.all()
    snippets = Snippet.objects.filter(is_public=True)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'count': snippets.count()
        }
    return render(request, 'pages/view_snippets.html', context)

#@login_required(login_url='login-url') #index-page') #"home"
@login_required
def my_snippets_page(request):
    snippets = Snippet.objects.filter(user_id=request.user.id)
    context = {
        'pagename': 'Мои сниппетов',
        'snippets': snippets
        }
    return render(request, 'pages/view_snippets.html', context)

def snippet_detail(request, snippet_id: int):
    context = { 'pagename': 'Просмотр сниппета' }
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except  ObjectDoesNotExist:
        #return HttpResponseNotFound(f'Snippet with id={ snippet_id } not found')
        return render(request, 'pages/errors.html', context | {"error":f'Snippet with id={ snippet_id } not found'})
    # context = {
    #     'pagename': 'Просмотр сниппета',
    #     'snippet': snippet
    #     }
    comments_form = CommentForm()
    context['snippet'] = snippet
    context['type'] = "view"
    context["comments_form"] = comments_form
    return render(request, 'pages/snippet_detail.html', context) 

@login_required
def snippet_edit(request, snippet_id:int):
    #pass
    context = { 'pagename': 'Редактирование сниппета' }
    try:
        #snippet = Snippet.objects.get(id=snippet_id)
        snippet = Snippet.objects.filter(user=request.user).get(id=snippet_id)
    except  ObjectDoesNotExist:
        return Http404
    
    ## Variant 1
    # ====== Получение данных сниппета с помощью SnippetForm
    # if request.method == "GET":
    #     form = SnippetForm(instance=snippet)
    #     return render(request,'pages/add_snippet.html',{'form': form})
    # ======================================================

    ## Variant 2
    # Хотим получить страницу с данными сниппета
    if request.method == "GET":
        context = {
            'snippet': snippet,
            'type': "edit" 
            }
        return render(request, 'pages/snippet_detail.html', context)
    # Получаем данные из формы и на их основе создаем новый snippet в БД
    if request.method == "POST":
        data_form = request.POST
        snippet.name = data_form["name"]
        #snippet.lang = data_form["lang"]
        snippet.code = data_form["code"]
        #snippet.creation_date = data_form["creation_date"]
        # Если ключ is_public усть в словаре, берем значение.
        # Если нет - присваиваем атрибуту is_public значение False
        snippet.is_public = data_form.get("is_public", False)
        snippet.save()
        return redirect("snippets-page") # GET /snippets/list

@login_required
def snippet_delete(request, snippet_id:int):
    #if request.method == "POST":
    if request.method == "POST" or request.method == "GET": #GET для рис=Корзина     
        #snippet = get_object_or_404(Snippet, id=snippet_id)
        snippet = get_object_or_404(Snippet.objects.filter(user=request.user), id=snippet_id)
        snippet.delete()
    return redirect('snippets-page')

# def create_snippet(request):
#     #если в запросе метод POST, то распечатает значения
#     #<QueryDict: {'csrfmiddlewaretoken': ['vRxqcWoOa4fXwxHZnu1H6Qtrn4mKGN54jefQ8Jqewc2TKcjYo65tpt2ro5yZWDyA'], 
#     # 'name': ['third'], 'lang': ['cpp'], 'code': ['cout']}>
#     #[31/Oct/2024 13:26:12] "POST /snippets/create HTTP/1.1" 200 4

#     #from pprint import pprint

#     # if request.method == "POST":
#     #     pprint(vars(request))
#     #     pprint(request.POST)
#     #     return HttpResponse("Done")
    
#     if request.method == "POST":
#         form = SnippetForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("snippets-page") # GET /snippets/list
#         return render(request,'pages/add_snippet.html',{'form': form})

def login(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       #print("username =", username)
       #print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           # Return error message
           # pass
           # если пользователь не верно вводит логин-пароль, то сообщать ему
           context = {
               "pagename": "PythonBin",
               "errors": ['wrong username or password']
           }
           return render(request, "pages/index.html", context)
   return redirect("index-page") #"home"

# def login_url(request):
#     return render(request, "pages/only_login.html", {"pagename": "Only login"}) 

def logout(request):
    auth.logout(request)
    return redirect("index-page") #"home"

def create_user(request):
    context = { "pagename": "Регистрация нового пользователя" }
    # Создаем пустую форму  при запросе методом GET
    if request.method == "GET":
        form = UserRegistrationForm()
        context['form'] = form
        return render(request, 'pages/registration.html', context)
    
    # Получаем данные из формы и на их основе создаем новый snippet в БД
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index-page') #"home"
        context['form'] = form
        return render(request,'pages/registration.html', context)
    
@login_required    
def comments_add(request):
    if request.method =="POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            snippet_id = request.POST.get("snippet_id")
            snippet = Snippet.objects.get(id=snippet_id)
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = snippet
            comment.save()
            return redirect("snippet-detail", snippet_id=snippet.id)
    return HttpResponseNotAllowed(['POST'])


        