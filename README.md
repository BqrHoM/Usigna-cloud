# Usigna cloud services
#### Video Demo:  https://www.youtube.com/watch?v=g8h9U3A5FZ0
#### Description:
*** Why Usigna Cloud Services ?***
The idea of usigna come from an issue which everyone faces nowadays , espacially
with the growth of the pricy cloud services and the increasing demand for it ,
It is the problem of missing storage
Indoutably Having your personal cloud hosted at home is a good solution to have an
illimited access for storage bought one time , or could maybe referbich some old hdd !

*** How I came up with that particular design ? ***
In the beggening the idea started as making an external lunix host (Which is my router)
but then I understood that such a router cannot handel a server , I honestly asked the AI
as a support to know the possible way , moving forward I had an alternative idea which is
enabling the storage through the public netword with an ftp service or even smp (From the router)
but I realised that such an idea is both not safe and not as applicable as I though , so
I finally come up with the idea of simply hosting the uploading app in my personal computer
with the full access of the storage through a local network and tunneling it with ngrok through
port 5000 .
About the website itself , I managed to code it with purely flask for the back end , css , html and
bootstrap and even some use of js in the designing (AOS library)

*** What is the use of each file ? ***

** /drive **
This folder is the folder that should contain folders for each user in which he can store (mainly the drive)

** /static **
This folder contains :

    1-The syling (style.css):
        for the styling I mainly used bootstrap , though I used some row css for some of the layout
        espacially if the default estetic of bootstrap doesn't match my aspirations , also I took care
        for the smaller screens and made a speachal layout for them

    2-The images :
        Thoes images I used for my project are generated from the AI with a script
** /templates **

    - layout.html : This is the core of the projects' template , it mainly consist of a basic html code
    with a lot of css classes and some local also . I tried to integrate an estetic touch for the upper
    navbar as if you are in the particular page , the button intencifies so you know in which page you are, I used flask conditioning to accomplish it !
    Besides i made a stable banner in the bottom showing the copy rights and a hyperlink for my linkedin
    This layout contains two blocks : the title and the body

    - activate.html :This documant is mainly designed for the use of activation code to access the premium
    features , it consist of a simple form with a button !

    - add.html : This page is designed to add services or should I say storage for your account , noting that this page handels the checking if the user had a premium account or not so it could decide either
    to provide the user with one free offer , or with both the free and the premium versions , let alone that it desplays the current storage in use and the avaible storage stil not used

    - backup_check.html : this page is so simple , it just checks for the successful apploads and the failed ones by reciving the message from the app.py , it also shows one of the images mentioned above !

    - index.html : This template is the main template of the webpage , it gives a general idea of the website with an illustating image

    - login.html : This is the login page , it mainly has a form that get submitted with the method POST so it enables the user to login it has a html based checking for email format and the hiding of passwords

    - manage.html : This template enables the user to upload images (or even files) to the drive folder ,
    also it iterate through the files that the drive of the user contains so it shows any image in the bottom area

    - problem.html : This template is mainly designed for the problem or the maluse of users , even for malitous use , it accepts a message with the error code , and shows an illustating image

    - push.html : This template is designed for the successful pursh (sort of gaining the premium version or adding a new service) , it has a dynamic tick to show the validation of the user request , this page was hugely inspired from an AI generated code , especially for the parts that handels the animation

    - register.html : This is the register page , it mainly has a form that get submitted with the method POST so it enables the user to register , it has a html based checking for email format and the hiding of passwords

** Python (mainly flask) **
    - app.py :

    - add.py :

** Database **
    - database.db :
    
** requirements.txt **
