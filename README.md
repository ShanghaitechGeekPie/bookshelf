# bookshelf

Public Book Shelf Server. 
Runs on django 2.0 and some little tools.

# Usage

The environment is already built in the django-env, you can run 
```pip install virtualenv```
```cd [the project repo] ```
```source ./django_env/bin/activate ```
to start the virtualenv, then run 
```python manage.py runserver ``` 
to start the service, the web runs on **127.0.01:8000/book** as default

# Static Files
css,js and pics
they are stored in 

./book/static

**Do not put them at random place, or the project would be a mess**

**To modify html with static files, you can use staic files as shown in item.html:line 6 to line12**



# Features
**1.Quick Add** 
you can simply use the scanner to scan for the bar code on the back of one book, then all the informations can be texted by thanks to douban API V2.

**2.Search**
you can search the book with name, author, or ISBN if you can remember that


