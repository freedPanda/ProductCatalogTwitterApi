# ProductCatalogTwitterApi
Product catalog website with twitter api requests. The twitter api that is involved with this incldue the following:tweet button and requesting mentions. The api is intended as a way for a webstie owner(whomever is trying to use this site to sell) to track the date when someone tweets as well as find out who mentioned. To use the twitter api you must have a twitter account. This website was designed for businesses. It features an admin portal viewing sales, adding products, deleting products, update products, track requests. This site does not have built in payment, so it uses email requests to conduct "purchases".

To view, admin portal I can make a youtube video, or possible provide a temp login credentials.

https://capstone-prodcatalog.herokuapp.com/index

1. Install requirements.txt
2. Get twitter developer account
3. save api key and secret api key from twitter to reallysecret.py. Names these variables
TW_API_KEY AND TW_SECRET_API_KEY respectively.
4. configure os environment vars for api keys and db. configure os environment vars for mail_settings and must use a google account unless you can modify it to work with another domain. With google you will need to allow 3rd party applications full access https://support.google.com/accounts/answer/3466521
5. create a db and modify app.py to match db name.
6. run the seedfile.py to create the tables.
7. execute fill_db() from the seedfile.py
8. run secret.py from command line or ipython. if youre going to deploy to heroku make sure to do this from your local machines cli, NOT heroku cli.
- secret.py has 4 functions. You must execute register(username,password) to get full access to secret.py. Then exectue login() and provide username password from before. create an admin which will be used to login online. Then run login() again select change route. In this part you are creating a secret string to add to the url to get to the admin portal online. Just create a string of characters DO NOT INCLUDE LOCAL HOST OR IPs OR PROTOCOLS just a random string of characters do not use /\#:
9. The tweet button and facebook share button are both disabled. You'll need to uncomment these and fill in some meta data. FOLLOW THE COMMENTS. look for comments with facebook or twitter. More detailed information can be found at developer.twitter.com search for cards or twitter for websites. Also, visit developers.facebook.com for info about share buttons.
10. Now you can use that secret string like this localhost/<the_secret_string> or a_website.com/<the_secret_string> and you'll be routed to the admin portal. Enter the 2nd username and password. 

Test files
1. to run test files must execute steps that involve secret.py
2. need to run seedfile.py to create tables
3. test_request_route requires you provide a working email address