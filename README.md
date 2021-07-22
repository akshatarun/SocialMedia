# SocialMedia
## A fully functional social networking app created with django development framework.

## Installation

#### Cloning the repository:

- Clone the repository using `git clone https://github.com/akshatarun/SocialMedia.git`.

#### Installing dependencies:

- Activate the virtual environment
- Run `pip install -r requirement.txt`

## Starting the server:

- Run `python manage.py runserver`.
- Open localhost to view it in the browser.

## User login page

![LOGIN PAGE](/media/login.png)

- The user login page asks the user for their username and password and uses django auth library to check if the user exists.
- The login page also has the option to redirect to the register page for new users.
## User register page

![REGISTER PAGE](/media/register.png)

- The user register page uses the django  *user creation forms* and asks the new user for their username, email, password and creates a profile for them.


## Home page 

![HOME_PAGE](/media/home.png)
- The home page presents to the user a list of posts created by different users and showing the latest posts first. Each page contains 10 posts.
- Using the search posts search form you can search any post by providing appropriate tags.
- Also if you go to some user related page then you can even search for users with their usernames.
- The user gets the option of liking and unliking every post.
- Using the timezone class of django every post carries with itself the information of when it was created.
- To comment or see which users had liked the post open the post by clicking on the post.

## Post Detail
![POST_DETAIL](/media/post_detail.png)
![COMMENTS](/media/comments.png)

- By clicking on the users who liked hyperlink, you can view the list of users who liked the post.
- If you are the user who has created the post then you have the option to update/delete the post.
- Any user can comment on the post, using the comments form.

## Liked users list 

![liked list](/media/usersWhoLiked.png)

- On clicking on the users who liked option, it provides us with a list of all the users who liked a certain post with the option of sending them friend requests.

## User profile page

![USER PROFILE](/media/profile_page.png)
- The user profile page displays the information related to the user.

- It shows the username and the posts made by the user.
- It shows the number of friends that the user has and on clicking it presents the list of friends.
- It shows to the user, the friend requests sent and received by them with the option of accepting or deleting the requests.


## Friends suggestion system

![Add new friends page](/media/add_new_friends.png)

- The add new friends page suggests the user a list of users with whom they share a mutual friend and some random users as well. It acts as a source of recommendation using which the user can make new friends.

_This project was built under the CSEA by_

- Akshat Arun
- Harshit Sureka
- Kartik Verma
- Mesharya M Choudhary
- Vineet Agarwal


                                