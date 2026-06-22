from itertools import count

import  pandas as pd
import  numpy as np
from csv import  reader

# opening data set
opened_file = open(r"C:\Users\Administrator\Desktop\Projects\App Profile\AppleStore.csv",encoding='utf8')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]

opened_file = open(r"C:\Users\Administrator\Desktop\Projects\App Profile\googleplaystore.csv", encoding= 'utf8')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

# creating a function to explore the data set easily( with an option to view the rows and columns)

def explore_data(dataset,start,end,rows_and_columns = False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')
    if rows_and_columns:
        print('Number of rows:',len(dataset))
        print('Number of columns:', len(dataset[0]))

# Exploring android and ios data set using the explore_data function

print(android_header)
print('\n')
explore_data(android,0,3,True)

print('\n')

print(ios_header)
print('\n')

explore_data(ios,0,3,True)

print('\n')

print('length of header',len(android_header))
for i in range(len(android)):
     if len(android[i]) != len(android_header):
        print('Incorrect row',i)

print('\n')
print(android[10472]) #incorrect row
print('\n')
print(android_header) #header
print('\n')
print(android[1]) #correct row

print(len(android))
del android[10472]
print(len(android))
#Removing duplicate entries

duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
print('Number of duplicate apps:',len(duplicate_apps))
print('Number of uniques apps:',len(unique_apps))
print('\n')
print('Example of duplicate apps',duplicate_apps[:5])

# To remove the duplicates I keep the app with max review and removed remainging
# Separating the apps wiht maximum review
reviews_max = {}
for app in android:
    name = app[0]
    reviews = app[3]
    if name not in reviews_max:
        reviews_max[name] = reviews
    else:
        if reviews_max[name] < reviews:
            reviews_max[name] = reviews
print('Expected length',len(android) -1181)
print('Actual length',len(reviews_max))

android_clean =[]
already_added=[]

for app in android:
    name = app[0]
    reviews = app[3]
    if (reviews_max[name] == reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
explore_data(android_clean,0,3,True)
print('Expected number of apps in the cleaned data set:',len(android)-1181)

#Removing non English apps
#check if app names are in english using ASCii
def is_it_english(string):
    for character in string:
        if ord(character)>127:
            return False
    return True
print(is_it_english('Sketch - Draw & Paint'))
print(is_it_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))

#Removing non English apps

def is_english(string):
    not_ascii = 0
    for character in string:
        if ord(character)> 127:
            not_ascii +=1
    if not_ascii >3:
        return False
    else:
        return  True
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))

#Removing Non-English apps from both our datasets and including emojis too
def english_apps(dataset,index):
    english_dataset = []
    for app in dataset:
        name = app[index]
        english_app = is_english(name)
        if english_app:
            english_dataset.append(app)
    return english_dataset

android_english = english_apps(android_clean,0)
ios_english = english_apps(ios,1)

explore_data(android_english,0,3,True)
print('\n')
explore_data(ios_english,0,3,True)
# isolating free apps
#checking index value for the pricing column

print(android_header)
print(ios_header)

#funtion for free apps
def free_apps(dataset,index):
    free_set=[]
    for app in dataset:
        price = app[index]
        if price == '0' or price =='0.0':
            free_set.append(app)
    return free_set
android_free = free_apps(android_english,7)
ios_free = free_apps(ios_english,4)

explore_data(android_free,0,3,True)
print('\n')
explore_data(ios_free,0,3,True)

#Most common apps by genre
#freequency table to display perc of share of each genre
def freq_table(dataset,index):
    total = 0
    genres = {}
    for app in dataset:
        total += 1
        genre = app[index]
        if genre in genres:
            genres[genre] +=1
        else:
            genres[genre] = 1
    for app in genres:
        genres[app] = (genres[app]/total)*100
    return genres
ios_freq = freq_table(ios_free,11)
android_cat = freq_table(android_free,1) # category
android_genre = freq_table(android_free,-4) # genre column

print(ios_freq)
print('\n')
print(android_cat)
print('\n')
print(android_genre)
#Examine cat and genre column in google store
#function to display genre shares in order
def genre_in_order(perc_dict):
    table = []
    for key in perc_dict:
        genre_perc = perc_dict[key],key
        table.append(genre_perc)
    table_sorted = sorted(table, reverse=True)
    for entry in table_sorted:
        print(entry[1],';',entry[0])

ios_ordered = genre_in_order(ios_freq)
android_ordered_cat = genre_in_order(android_cat)
android_ordered_genre = genre_in_order(android_genre)
print('\n')
#Most popular apps by genre on the App store

#Average number of user ratings per app genre on the App Store bcs there is no install in app store file
rating_count ={}

for genre in ios_freq:
    count = 0
    length_genre = 0
    for app in ios_free:
        app_genre = app[11]
        rating = app[5]
        if app_genre == genre:
            count += float(rating)
            length_genre +=1
    rating_count[genre] = count/length_genre

genre_in_order(rating_count)
#app skewing the average and why

for app in ios_free:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # printing app name and number of ratings
for app in ios_free:
    if app[-5] == 'Reference':
        print(app[1],';',app[5]) # printinh app name and number of ratings

#Analyzing google play market
installs_freq= freq_table(android_free,5)
isntalls_ordered = genre_in_order(installs_freq)
print(isntalls_ordered)

installs_count = {}

for category in android_cat:
    total_installs = 0
    length_category = 0
    for app in android_free:
        app_category = app[1]
        if app_category == category:
            installs = app[5]
            installs = installs.replace(',', '')
            installs = installs.replace('+', '')
            total_installs += float(installs)
            length_category += 1
    installs_count[category] = total_installs / length_category

genre_in_order(installs_count)

#Apps skewing the average like before On average, communication apps have the most installs: 38,456,119.
for app in android_free:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5]) #app name : installs

#Removing apps with over 100 millions installs
under_100_mil = []

for app in android_free:
    installs = app[5]
    installs = installs.replace(',', '')
    installs = installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(installs) < 100000000):
        under_100_mil.append(float(installs))

sum(under_100_mil) / len(under_100_mil)

#Checking to see if we can suggest to invest in a book app
print('\n')
for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5]) # App name : Installs

for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])
#Removing these apps as they skew our average:
for app in android_free:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])
