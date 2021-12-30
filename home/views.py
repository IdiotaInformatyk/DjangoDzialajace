import random
from django.contrib.auth import get_user_model
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, FriendRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from .forms import NewCommentForm, NewPostForm
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Like
from django.contrib.auth.decorators import login_required
import json
User = get_user_model()

# users_list — ten widok utworzy listę użytkowników, która będzie polecana każdemu użytkownikowi, aby pomóc mu odkryć nowych użytkowników, z którymi można się zaprzyjaźnić.
# Odfiltrujemy naszych znajomych z tej listy i również nas wykluczymy.
# Utworzymy tę listę, dodając najpierw znajomych naszego przyjaciela, którzy nie są naszymi przyjaciółmi.
# Następnie, jeśli nasza lista użytkowników nadal ma niską liczbę członków, dodamy losowe osoby do polecenia (głównie dla użytkownika bez znajomych).
@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    sent_to = []
    friends = []
    for user in users:
        friend = user.friends.all()
        for f in friend:
            if f in friends:
                friend = friend.exclude(user=f.user)
        friends += friend
    my_friends = request.user.profile.friends.all()
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in friends:
            random_list.remove(r)
    friends += random_list
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    for se in sent_friend_requests:
        sent_to.append(se.to_user)
    context = {
        'users': friends,
        'sent': sent_to
    }
    return render(request, "home/users_list.html", context)

# lista_przyjaciół — Ten widok wyświetla wszystkich znajomych użytkownika.


def friend_list(request):
    p = request.user.profile
    friends = p.friends.all()
    context = {
        'friends': friends
    }

    return render(request, "home/friend_list.html", context)


# send_friend_request — Pomoże nam to utworzyć instancję zaproszenia do znajomych i wyśle prośbę do użytkownika.
# Pobieramy identyfikator użytkownika, do którego wysyłamy żądanie, aby móc wysłać mu żądanie.


@login_required
def send_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest, created = FriendRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

# cancel_friend_request — It will cancel the friend request we sent to the user.


@login_required
def cancel_friend_request(request, id):
    user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


# accept_friend_request
# Zostanie użyty do zaakceptowania zaproszenia użytkownika do znajomych i dodamy użytkownika1 do listy znajomych użytkownika2 i na odwrót.
# Ponadto usuniemy zaproszenie do znajomych.

@login_required
def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    if (FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
        request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

# delete_friend_request — Pozwala użytkownikowi usunąć każde otrzymane zaproszenie do znajomych.


@login_required
def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

# delete_friend - To usunie znajomego tego użytkownika, tj. usunęlibyśmy użytkownika 1 z listy znajomych użytkownika 2 i na odwrót.


def delete_friend(request, id):
    user_profile = request.user.profile
    friend_profile = get_object_or_404(Profile, id=id)
    user_profile.friends.remove(friend_profile)
    friend_profile.friends.remove(user_profile)
    return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))

# profile_view — będzie to widok profilu dowolnego użytkownika.
# Pokaże liczbę znajomych i liczbę postów użytkownika oraz jego listę znajomych.
# Ponadto pokazywałby zaproszenie do znajomych otrzymane i wysłane przez użytkownika i może zaakceptować, odrzucić lub anulować prośbę.
# Oczywiście dodamy warunki i kontrole, tak aby tylko zainteresowany użytkownik był pokazywany zapytaniami i wysłanymi listami i miał tylko uprawnienia do akceptowania lub odrzucania wniosków, a nie każdy, kto przegląda jego / jej profil.


@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
    user_posts = Post.objects.filter(user_name=u)

    friends = p.friends.all()

    # czy uzytkownik jest naszym znajomym
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # jezeli wyslalismy mu zaproszenie do znajomych
        if len(FriendRequest.objects.filter(
                from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'friend_request_sent'

        # jezeli dostalismy zaproszenie do znajomych
        if len(FriendRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u': u,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'post_count': user_posts.count
    }

    return render(request, "home/profile.html", context)


# register — Umożliwi to użytkownikom zarejestrowanie się w naszej witrynie. Wyrenderuje formularz rejestracyjny, który stworzyliśmy w pliku form.py.

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'home/Registration.html', {'form': form})

# edit_profile — To pozwoli użytkownikom edytować swój profil za pomocą utworzonych przez nas formularzy.


@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('my_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'home/edit_profile.html', context)


# my_profile — To to samo co profile_view, ale wyrenderuje tylko Twój profil.


@login_required
def my_profile(request):
    p = request.user.profile
    you = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=you)
    rec_friend_requests = FriendRequest.objects.filter(to_user=you)
    user_posts = Post.objects.filter(user_name=you)
    friends = p.friends.all()

    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        if len(FriendRequest.objects.filter(
                from_user=request.user).filter(to_user=you)) == 1:
            button_status = 'friend_request_sent'

        if len(FriendRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u': you,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'post_count': user_posts.count
    }

    return render(request, "home/profile.html", context)

# search_users — To obsłuży funkcję wyszukiwania użytkowników.
# Pobiera zapytanie, a następnie odfiltrowuje odpowiednich użytkowników.


@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains=query)
    context = {
        'users': object_list
    }
    return render(request, "home/search_users.html", context)


def home(response):
    return render(response, "home/home.html", {})


def Registration(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("/login")
    form = RegisterForm()
    return render(request, "home/Registration.html", {"form": form})


def login(request):
    return render(request, "home/login.html", {})


# PostListView — This view handles the display of all the posts in an order which puts newer posts first up.
# Each page displays 10 posts and then we need to move to the next page to view more.
# Also, if the user is not authenticated, we do not give him the option to like on the post.
# If the user is authenticated, we show whether the user has liked or not.


class PostListView(ListView):
    model = Post
    template_name = 'home/home.html'
    context_object_name = 'posts'
    ordering = ['-likes']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            liked = [i for i in Post.objects.all() if Like.objects.filter(user=self.request.user, post=i)]
            context['liked_post'] = liked
        return context


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home/users_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        liked = [i for i in Post.objects.filter(user_name=user) if Like.objects.filter(user=self.request.user, post=i)]
        context['liked_post'] = liked
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(user_name=user).order_by('-date_posted')


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_liked = [i for i in Post.objects.filter(user_name=user) if Like.objects.filter(user=user, post=post)]
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.username = user
            data.save()
            return redirect('post-detail', pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'home/post_detail.html', {'post': post, 'is_liked': is_liked, 'form': form})


@login_required
def create_post(request):
    user = request.user
    if request.method == "POST":
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user_name = user
            data.save()
            messages.success(request, f'Posted Successfully')
            return redirect('home')
    else:
        form = NewPostForm()
    return render(request, 'home/create_post.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['description', 'pic', 'tags']
    template_name = 'home/create_post.html'

    def form_valid(self, form):
        form.instance.user_name = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user_name:
            return True
        return False


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user_name:
        Post.objects.get(pk=pk).delete()
    return redirect('home')


@login_required
def search_posts(request):
    query = request.GET.get('p')
    object_list = Post.objects.filter(tags__icontains=query)
    liked = [i for i in object_list if Like.objects.filter(user=request.user, post=i)]
    context = {
        'posts': object_list,
        'liked_post': liked
    }
    return render(request, "home/search_posts.html", context)


@login_required
def like(request):
    post_id = request.GET.get("likeId", "")
    user = request.user
    post = Post.objects.get(pk=post_id)
    liked = False
    like = Like.objects.filter(user=user, post=post)
    if like:
        like.delete()
    else:
        liked = True
        Like.objects.create(user=user, post=post)
    resp = {
        'liked': liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")
