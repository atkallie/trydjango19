"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

#This is for static files
from django.conf import settings
from django.conf.urls.static import static

#these are called regular expressions ('r' means raw expression)
#https://www.tutorialspoint.com/python/python_reg_expressions.htm
# '^' matches beginning of line, while '$' matches end of line (see above for more detail)

from Posts import urls as posturls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^posts/', include(posturls, namespace="posts")),
]

if settings.DEBUG:
    #static is a helper function to return a URL pattern for serving files in debug mode (not for production!)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)