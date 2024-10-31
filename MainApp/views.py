from django.http import Http404, HttpResponse #HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from MainApp.models import Snippet
from django.core.exceptions import ObjectDoesNotExist
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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
           form.save()
           return redirect("snippets-page") # GET /snippets/list
       return render(request,'pages/add_snippet.html',{'form': form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {
        'pagename': 'Просмотр сниппетов',
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
    context['snippet'] = snippet
    context['type'] = "view"
    return render(request, 'pages/snippet_detail.html', context) 

def snippet_edit(request, snippet_id:int):
    pass

def snippet_delete(request, snippet_id:int):
    #if request.method == "POST":
    if request.method == "POST" or request.method == "GET": #GET для рис=Корзина     
        snippet = get_object_or_404(Snippet, id=snippet_id)
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



