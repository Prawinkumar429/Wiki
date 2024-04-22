"""ats_wiki URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wiki.views import add_information1, retrieve_information, update_information1, base_view,base_view1,category_filter,search_wiki_entries,live_search_results,item_detail1,approval,permanent_delete_file
from django.conf.urls.static import static
from django.conf import  settings
from django.views.static import serve 
from django.conf.urls import url




handler404 = 'wiki.views.error_404'
handler500 = 'wiki.views.error_500'
handler403 = 'wiki.views.error_403'
handler400 = 'wiki.views.error_400'

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('add/', add_information1, name='add_information1'),
    path('', base_view, name='base_view'),
    path('update/<int:pk>/', update_information1, name='update_information1'),
    path('category/<str:category>/', category_filter, name='category_filter'),
    path('list/', retrieve_information, name='retrieve_information'),
    path('search/', search_wiki_entries, name='search_wiki_entries'),
    path('live_search_results/', live_search_results, name='live_search_results'),
    path('item/<int:item_id>/', item_detail1, name='item_detail1'),
    path('approval/<int:item_id>/', approval, name='approval'),
    path('permanent-delete-file/', permanent_delete_file, name='permanent_delete_file'),
]

if settings.DEBUG:
    
    urlpatterns  += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
