import tkinter
from tkinter import messagebox
from tkinter import ttk


def validate(username,connection):
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM dbo.user_yelp WHERE user_id = %(username)s', {'username': username})
    result = cursor.fetchone()[0]
    if result == 1:
        messagebox.showinfo("Message","Hey There! We hope you are doing well.")
        return True

    else:
        messagebox.showinfo("Invalid Input!")
        return False

def business(minstars,maxstars,city,name,connection):
    cursor = connection.cursor()
    
    if minstars == '' and maxstars == '':
        cursor.execute('SELECT business_id,name,address,city,stars FROM dbo.business WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND city COLLATE Latin1_General_CI_AI LIKE %(city)s ORDER BY name',{'name':f'%{name}%','city':f'%{city}%'}) 
    elif minstars != '' and maxstars == '':
        minstars = float(minstars)
        query = '''
        SELECT b.business_id,b.name,b.address,b.city,b.stars 
        FROM (SELECT business_id,name,address,city,stars
            FROM business
            WHERE stars >= %(minstars)s) AS b
        WHERE b.name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND b.city COLLATE Latin1_General_CI_AI LIKE %(city)s 
        ORDER BY b.name ASC
        '''
        cursor.execute(query,{'minstars':minstars,'name':f'%{name}%','city':f'%{city}%'})
    elif minstars == '' and maxstars != '':
        maxstars = float(maxstars)
        query = '''
        SELECT b.business_id,b.name,b.address,b.city,b.stars 
        FROM (SELECT business_id,name,address,city,stars
            FROM business
            WHERE stars <= %(maxstars)s) AS b
        WHERE b.name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND b.city COLLATE Latin1_General_CI_AI LIKE %(city)s 
        ORDER BY b.name ASC
        '''
        cursor.execute(query,{'maxstars':maxstars,'name':f'%{name}%','city':f'%{city}%'})

    else:
        minstars = float(minstars)
        maxstars = float(maxstars)
        query = '''
        SELECT b.business_id,b.name,b.address,b.city,b.stars 
        FROM (SELECT business_id,name,address,city,stars
            FROM business
            WHERE stars >= %(minstars)s AND stars <= %(maxstars)s) AS b
        WHERE b.name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND b.city COLLATE Latin1_General_CI_AI LIKE %(city)s 
        ORDER BY b.name ASC
        '''
        cursor.execute(query,{'minstars':minstars,'maxstars':maxstars,'name':f'%{name}%','city':f'%{city}%'})
    # elif stars == 'Least Rating':
    #     cursor.execute('SELECT business_id,name,address,city,stars FROM dbo.business WHERE stars = (SELECT MIN(stars) FROM dbo.business WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND city COLLATE Latin1_General_CI_AI LIKE %(city)s) AND name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND city COLLATE Latin1_General_CI_AI LIKE %(city)s ORDER BY name',{'stars':stars,'name':f'%{name}%','city':f'%{city}%'})
    # elif stars == 'Highest Rating':
    #     cursor.execute('SELECT business_id,name,address,city,stars FROM dbo.business WHERE stars = (SELECT MAX(stars) FROM dbo.business WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND city COLLATE Latin1_General_CI_AI LIKE %(city)s) AND name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI AND city COLLATE Latin1_General_CI_AI LIKE %(city)s ORDER BY name',{'stars':stars,'name':f'%{name}%','city':f'%{city}%'})

    results = cursor.fetchall()
    if not results:
        messagebox.showinfo("Message","Unfortunately, no data was found.")

    return results



def users(name,useful,funny,cool,connection):
    cursor = connection.cursor()
    useful_value = 0
    funny_value = 0
    cool_value = 0
    if useful == 'no':
        useful_value = 0
    elif useful == 'yes':
        useful_value = 1 

    if funny == 'no':
        funny_value = 0
    elif funny == 'yes':
        funny_value = 1 

    if cool == 'no':
        cool_value = 0
    elif cool == 'yes':
        cool_value = 1 
    
    query = '''
            SELECT user_id,name, 
            CASE WHEN %(useful)s = 0 THEN 0 
                ELSE CASE WHEN %(useful)s = 1 THEN useful 
                    END
            END AS useful,
            CASE WHEN %(funny)s = 0 THEN 0 
                ELSE CASE WHEN %(funny)s = 1 THEN funny
                    END
            END AS funny,
            CASE WHEN %(cool)s = 0 THEN 0 
                ELSE CASE WHEN %(cool)s = 1 THEN cool 
                    END 
            END AS cool,
            yelping_since
            FROM dbo.user_yelp 
            WHERE name COLLATE Latin1_General_CI_AI LIKE %(name)s COLLATE Latin1_General_CI_AI 
            AND ((%(useful)s = 0 AND useful = 0) OR (%(useful)s = 1 AND useful > 0))
            AND ((%(funny)s = 0 AND funny = 0) OR (%(funny)s = 1 AND funny > 0))
            AND ((%(cool)s = 0 AND cool = 0) OR (%(cool)s = 1 AND cool > 0))
            ORDER BY name'''

    cursor.execute(query,{'name':f'%{name}%','useful':useful_value,'funny':funny_value,'cool':cool_value})
    results = cursor.fetchall()
    if not results:
        messagebox.showinfo("Message","Unfortunately, no data was found.")
    return results


    

