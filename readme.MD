# Database Application for Yelp Dataset

## Table of Contents
1. [Introduction](#introduction)
2. [Login](#login)
3. [Search Business](#search-businesses)
4. [Search Users](#search-users)
5. [Make Friends](#make-friends)
6. [Write Review](#write-review)
6. [Reference Article](#reference-article)


## Introduction
The Database Application was implemented in the GUI, using python. For the GUI implementation, Tkinter, a python library was used. The application was connected to the csil systems using another Python library called pymssql. 

Connection was performed as follows:

```python
def createServerConnection(host,user,password,database):
conection = None
try: 
    connection = pymssql.connect(host = host ,user = user,
                        password = password,database = database)
    print("MySQL Database connection successful")
except Error as err:
    print(f"Error:'{err}' ")
return connection
```

## Login
Once the Application opens, the user has to input their user-id in order to access the Database.
The input is passed into a query in backend.py to ensure validity.

![Login](/assets/Login.png)

Once the user has entered a valid user-id, the Application's front page opens where they can choose from one of the following options: 
![FrontPage](/assets/frontpage.png)

## Search Businesses
The user can choose the first option to search for businesses and rate those businesses that satisfy certain criteria.

1. Least Rating and Highest Rating: User can enter a range for the ratings of the business
2. City: User can enter a city 
3. Name: User can enter a part of the name or the whole name


![searchBus](/assets/searchBus.png)

## Search Users
Similarly, the user can also choose the second option to search for users and make friends that satisfy certain criteria

1. Name: Users can enter a name or a part of their name
2. Useful/Funny/Cool: If the value is more than 0 for any of the parameters then the users are considered useful or funny or cool

![makeFriends](/assets/makeFriends.png)

## Make Friends

A user can make friends by double clicking on one of the rows in the provided table. A messagebox appears that confirms whether the logged in user would like to be friends with another user.

![friendsq](/assets/friendsq.png)

Once the user confirms, a message box appears that confirms the insertion of the relation in the friendship table
![yesfriends](/assets/yesfriends.png)
![friendshipdb](/assets/freindshipdb.png)

## Write Review

Similarly, a user can also write a review for a business by double clicking on one of the rows in the table provided. A messagebox appears that confirms whether the logged in user would like to rate the business.
![review](/assets/review.png)

Once, the user confirms, a message box appears that asks the user to input the rating on a 5 point scale.
![yesreview](/assets/yesreview.png)
![confirmReview](/assets/confirmReview.png)

The input affects the business and the review table accordingly.



## Reference Article

https://www.mssqltips.com/sqlservertip/7587/python-gui-with-tkinter/




