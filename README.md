# SocialMedia
## A fully functional social networking app created with django development frame.

## Installation

#### Cloning the repository:

- Clone the repository using `git clone https:/https://github.com/KartikVerma044/SocialMedia.git`.

#### Installing dependencies:

- Run `pip install django`

## Starting the server:

- Run `python manage.py runserver`.
- Open localhost to view it in the browser.



![LOGIN PAGE](/media/login.png)
### The user login page asks the user for his/her username and password and using django auth library checks if the user exists.The login page also has the option too redirect to the register page for new users and forgot password option for users who forgot their password.
![HOME_PAGE](/media/home_page.png)
### The home page presents to the user list of posts made by him/her and his/her friends with the latest post at the top.Each page contains 10 posts.
### The user gets the option of liking and unliking every post and also of seeing the users who liked a particular post.
### Using the timezone class of django every post carries with the itself the information of when it was created.
![USER PROFILE](/media/profile_page.png)
### The user profile page displays the information related to the user.
1.It shows the username and the posts made by the user.
2.It shows the number of friends the user has and on clicking it presents the list of friends.
3.It shows the user the friend requests sent and received by him/her with the option of accepting or deleting the requests.
![Add new friends page](/media/addnewfreinds.png)
### The add new friends page suggests the user a list of users with whom they share a mutual friend and some random users as well.It acts as a source of recommendation using which the user can make new friends.


                                
