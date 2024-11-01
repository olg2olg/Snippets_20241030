from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='index-page'), #"home"
    path('snippets/add', views.add_snippet_page, name='add-snippet-page'),
    path('snippets/list', views.snippets_page, name='snippets-page'),
    #path("snippets/create", views.create_snippet, name="snippet-create"),
    path("snippets/<int:snippet_id>/", views.snippet_detail, name="snippet-detail"),
    path("snippets/<int:snippet_id>/edit", views.snippet_edit, name="snippet-edit"),
    path("snippets/<int:snippet_id>/delete", views.snippet_delete, name="snippet-delete"),
    path('snippets/my_list', views.my_snippets_page, name='my-snippets-page'),
    path('comments/add', views.comments_add, name='comments-add'),    
    path('login', views.login, name='login'),
    #path('login_url', views.login_url, name='login-url'),
    path('logout', views.logout, name='logout'),
    path('register', views.create_user, name='register')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
