## Personal Blog

This a is very simple blog application using **python flask**.

 [Demo](https://jackmrzhou.me)

### Python package requirements

* flask
* flask_migrate
* flask_login
* flask_sqlalchemy
* flask_wtf
* markdown

### brief introduction

First I should claim that this application is not a framework, so there is no way to modify the **front-end** using configurations.

The application is half static because in some pages I use **js** to dynamicly render a part of the page, but in some pages I use static **html**. This inconsistent is due my early idea that I just want to write a static blog, which I paid great efforts to rewrite some of the pages.

### Future Work

* Add comment system.
* Separate different users and give different permissions.
* Improve writing experience.
* ......