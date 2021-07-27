from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from feed.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Profile, FriendRequest
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import random

User = get_user_model()

@login_required
def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
    my_friends = request.user.profile.friends.all()
    sent_to = []
	
    #friends[] is the list of users to be recommended
    friends = [] 
	
    for user in my_friends:
	
	#Here friend[] is a list of friends_of_my_friend
        friend = user.friends.all()
	
        for f in friend:
            if f in friends:
                friend = friend.exclude(user=f.user)
        friends += friend
    
    #removing those users from friends[] who are already my friend
    for i in my_friends:
        if i in friends:
            friends.remove(i)
    #removing myself from friends[]
    if request.user.profile in friends:
        friends.remove(request.user.profile)
    
    #adding a list of 10 random users to friends[] and again removing my friends ,myself and users already in friends[] from the list.
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

    return render(request, "users/users_list.html", context)

def friend_list(request):
	p = request.user.profile
	friends = p.friends.all()
	context={
	'friends': friends
	}
	return render(request, "users/friend_list.html", context)

@login_required
def send_friend_request(request, id):
	user = (get_object_or_404(Profile, id=id)).user
	frequest, created = FriendRequest.objects.get_or_create(
			from_user=request.user,
			to_user=user)
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def cancel_friend_request(request, id):
	user = (get_object_or_404(Profile, id=id)).user
	frequest = FriendRequest.objects.filter(
			from_user=request.user,
			to_user=user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

@login_required
def accept_friend_request(request, id):
	from_user = (get_object_or_404(Profile, id=id)).user
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	user1 = frequest.to_user
	user2 = from_user
	user1.profile.friends.add(user2.profile)
	user2.profile.friends.add(user1.profile)
	if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
		request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
		request_rev.delete()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

@login_required
def delete_friend_request(request, id):
	from_user = (get_object_or_404(Profile, id=id)).user
	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
	frequest.delete()
	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

def delete_friend(request, id):
	user_profile = request.user.profile
	friend_profile = get_object_or_404(Profile, id=id)
	user_profile.friends.remove(friend_profile)
	friend_profile.friends.remove(user_profile)
	return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))

@login_required
def profile_view(request, slug):
	p = Profile.objects.filter(slug=slug).first()
	u = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
	rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
	user_posts = Post.objects.filter(user_name=u)

	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
		if len(FriendRequest.objects.filter(
			from_user=request.user).filter(to_user=p.user)) == 1:
				button_status = 'friend_request_sent'

		# if we have recieved a friend request
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

	return render(request, "users/profile.html", context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Your account has been created! You can now login!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form':form})

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
	context ={
		'u_form': u_form,
		'p_form': p_form,
	}
	return render(request, 'users/edit_profile.html', context)

@login_required
def my_profile(request):
	p = request.user.profile
	you = p.user
	sent_friend_requests = FriendRequest.objects.filter(from_user=you)
	rec_friend_requests = FriendRequest.objects.filter(to_user=you)
	user_posts = Post.objects.filter(user_name=you)
	friends = p.friends.all()

	# is this user our friend
	button_status = 'none'
	if p not in request.user.profile.friends.all():
		button_status = 'not_friend'

		# if we have sent him a friend request
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

	return render(request, "users/profile.html", context)

#from search users, we remove those users whom we have already sent friend request
#and those who are already our frinds
@login_required
def search_users(request):
	query = request.GET.get('q')
	sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
	sent_to = []
	friend_profile_list = list(request.user.profile.friends.all())
	friend_list = []
	for profile in friend_profile_list:
		friend_list.append(profile.user)
	for se in sent_friend_requests:
		sent_to.append(se.to_user)
	object_list = User.objects.filter(username__icontains=query)
	context ={
		'users': object_list,
		'sent': sent_to,
		'friends': friend_list
	}
	return render(request, "users/search_users.html", context)

#users to whom we have send friends request, with whom we are friends with will have different 
#button status from rest of the users who liked our post.
@login_required
def liked_users_list(request, pk):
	post = Post.objects.get(pk=pk)
	sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
	sent_to = []
	for se in sent_friend_requests:
		sent_to.append(se.to_user)
	friend_profile_list = list(request.user.profile.friends.all())
	friend_list = []
	for profile in friend_profile_list:
		friend_list.append(profile.user)
	liked_users_object_list=list(post.likes.all())
	liked_users_list = []
	for instance in liked_users_object_list:
		liked_users_list.append(instance.user)
	context ={
		"users" : liked_users_list,
		'sent': sent_to,
		'friends': friend_list
	}
	return render(request, "users/liked_users.html", context)
