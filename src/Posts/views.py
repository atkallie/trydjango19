from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #for pagination
from urllib import quote_plus #for url-encoded text
from django.utils import timezone
from django.db.models import Q

from Posts.models import Post
from Posts.forms import PostForm

# Create your views [from the 6] here.

#function-based views
def postsHomeView(request):
    querySetOfAllObjs_list = Post.objects.active() #.order_by("-timestamp")
    if request.user.is_superuser or request.user.is_staff:
        querySetOfAllObjs_list = Post.objects.all()

    searchItem = request.GET.get("search")
    if searchItem:
        querySetOfAllObjs_list = querySetOfAllObjs_list.filter(
            Q(title__icontains=searchItem) |
            Q(content__icontains=searchItem) #|
            #Q(user__first_name__icontains=searchItem) |
            #Q(user__last_name__icontains=searchItem)
        ).distinct()

    paginator = Paginator(querySetOfAllObjs_list, 6) # Initialize paginator (Show 10 posts per page)
    createPostURL = reverse("posts:create_post")

    #'page' is the desired display name for the paging URL (can be changed, but also need to change in template)
    page = request.GET.get('page')
    try:
        querySetOfAllObjs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        querySetOfAllObjs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        querySetOfAllObjs = paginator.page(paginator.num_pages)

    context = {
        "allPostObjs": querySetOfAllObjs,
        "createPostURL": createPostURL,
        "todayDate":timezone.now().date()
    }

    return render(request, 'allPostsView.html', context)

def postsCreateView(request):
    #this is for user permissions (creating posts is restricted to superuser or staff)
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404 #could also redirect to a sign-in page instead (preferred)

    #only need one of these (either above or below) -- above is more strict
    if not request.user.is_authenticated():
        raise Http404 #could also redirect to a sign-in page instead (preferred)

    #'or None' is so that it doesn't always say '... is required'
    postForm = PostForm(request.POST or None, request.FILES or None) #request.FILES is so that we can pass in images (not just text)

    if postForm.is_valid():
        #commit=False means that the form generates SOME data for the model object, but we can also add model details from elsewhere
        newPost = postForm.save(commit=False)
        #print data from your form
        print(postForm.cleaned_data.get("title"))

        #save the user
        newPost.user = request.user

        #b/c of 'commit=False' that's why we don't save the newPost instance until later
        newPost.save()
        messages.success(request,"New <a href='someSite'> Post </a> Created",extra_tags="html_safe")
        return HttpResponseRedirect(newPost.get_absolute_url())


    #One method of creating a new object (Not Recommended since it does not do form validation)
    #if request.method=="POST":
    #   title = request.POST.get("title")
    #   content = request.POST.get("content")
    #   Post.objects.create(title=title,content=content)


    context = {
        "postForm":postForm
    }

    return render(request, "createView.html", context)

def singlePostView(request,id=None):
    #singleObj = Post.objects.get(id=1) ---> This one prone to error
    singleObj = get_object_or_404(Post,id=id)

    if singleObj.draft or singleObj.publishDate>timezone.now().date():
        if not request.user.is_superuser and not request.user.is_staff:
            raise Http404

    #create URL-encoded content to share stuff
    content_share_string = quote_plus(singleObj.content) #note how we made the template tag 'urlify' to replace this (see singlePostView.html)

    context = {
        "singleObj":singleObj,
        "share_string":content_share_string
    }

    return render(request, "singlePostView.html", context)


def singlePostEditView(request,id=None):
    # this is for user permissions (editing posts is restricted to superuser or staff)
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404 #could also redirect to a sign-in page instead (preferred)

    #grab post to edit
    singleObjToEdit = get_object_or_404(Post,id=id)
    editPostForm = PostForm(request.POST or None, request.FILES or None, instance=singleObjToEdit)

    if editPostForm.is_valid():
        newlyEditedPost = editPostForm.save(commit=False)

        # save the user
        newlyEditedPost.user = request.user

        newlyEditedPost.save()
        messages.success(request,"Edits Successfully made")
        return HttpResponseRedirect(newlyEditedPost.get_absolute_url())

    context = {
        "objToEdit":singleObjToEdit,
        "editPostForm":editPostForm,
    }

    return render(request,"editView.html",context)

def postsDeleteView(request, id=None):
    if not request.user.is_superuser and not request.user.is_staff:
        raise Http404

    postToDelete = get_object_or_404(Post,id=id)
    postToDelete.delete()
    messages.success(request,"Post Successfully Deleted")
    return redirect("posts:all_posts")