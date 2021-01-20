from django.core import paginator
from django.db.models.fields import PositiveIntegerRelDbTypeMixin
from django.db.models.manager import EmptyManager
from django.forms.fields import TypedMultipleChoiceField
from django.shortcuts import  render, get_object_or_404
from .models import Post,Comments
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.mail import send_mail
from .forms import EmailSendForm,CommentForm
from taggit.models import Tag

        
def post_list(request,tag_slug=None):
    # bulk_post()
    # tag_slug='it'
    # print(2/0)
    print(tag_slug)
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts,3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
        print(posts,'from ',page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,'blog/posts.html',{
                                                'posts':posts,
                                                'tag': tag,
                                            })


def post_detail(request,year,month,day,slug):
    post = get_object_or_404(Post,  slug=slug,
                                    # status='published',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    comments = post.comments.filter(active=True).order_by('-updated')
    submitted = False
    tags = post.tags.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.active = True
            new_comment.save()
            submitted = True
    else:
        form = CommentForm()
    return render(request,"blog/post_detail.html",{
                                                    'post':post,
                                                    'comments':comments,
                                                    'submitted':submitted,
                                                    'form':form,
                                                    'tags':tags
                                                    })


def send_email_view(request,id):
    post = get_object_or_404(Post,id=id,status='published')
    sent = False
    if request.method == 'POST':
        form = EmailSendForm(request.POST)
        if form.is_valid():
            print('Data valid')
            data = form.cleaned_data
            # print(data['to'])
            try:
                
                subject = f"{data['name']} recommends {post.title}"
                post_url = request.build_absolute_uri(post.get_absolute_url())
                message = 'Read post at :\n {}\n\n{}\'s Comments:\n\n{}'.format(post_url,data['name'],data['comments'])
                send_mail(subject,message,'siva@blog.com',[data['to'],])
                print(message)
                sent = True
            except Exception as e:
                print(e)
                # pass
        else:
            print('INvalid')
    
    print(f'Value of sent is {sent}')
        

    form = EmailSendForm()
    return render(request,'blog/share_email.html',{'form':form,'post':post,'sent':sent})




