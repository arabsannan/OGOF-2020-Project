"""Updated program"""
import csv
import tweepy
import pycountry
import os

# API Keys
api_key = 'uZDCs7x8kCZdAsHdAezSgWwiU'
api_secret_key = 'JMcpmYFTe26VRE49K7QXt0x0ubW8HTSf4zOhVvtK980kgnGPQg'
access_token = '1297929482125312000-ZYOOCxup34eyVwMox3R0FeQMdBYqAX'
access_token_secret = 'ENbqMR5dZcwn0lIECZqpFWsMvjMqbvGSKIgEBwjJQ6JQy'

# setting up twitter APIs
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

count = 0
country_name = ""


def name_country():
    countries = [i.name for i in list(pycountry.countries)]
    country_name = str(input("Please specify country name: ")).title().strip()
    if country_name in countries:
        return tweet_count(country_name)
    else:
        print("Country doesn't exist!")
        return name_country()


def tweet_count(country_name):
    try:
        count = int(input("Please specify number of tweets: "))
        excess_count = count * int(1.15 * count)  # increases the count by 15%
    except ValueError:
        print("Please enter a number!")
        return tweet_count(country_name)
    else:
        if (count >= 10) and (count <= 100):
            return [country_name, count, excess_count]
        else:
            print("The number of tweets must be between 100 and 1000!.")
            return tweet_count(country_name)


def capture_tweets():
    results = name_country()  # a list containing the country's name, tweet count and excess count
    tweet_timestamps = []
    tweet_texts = []

    print(f'Capturing tweets from {results[0]}...')

    # get the tweets and their corresponding timestamps into lists, removing duplicates
    for tweet in tweepy.Cursor(api.search, q=results[0]).items(results[2]):
        if 'RT' in tweet.text:  # my update
            pass
        else:
            t_timestamp = tweet.created_at
            t_text = tweet.text.encode('utf-8')

            if not tweet_texts.__contains__(t_text):  # checks if the tweet has already been captured
                tweet_timestamps.append(t_timestamp)
                tweet_texts.append(t_text)

            # if the captured tweets are equal to the count specified continue
            if len(tweet_texts) == results[1]:
                break

    __dir = './Tweets'
    if os.path.exists(__dir):
        pass
    else:
        os.mkdir(__dir)  # creates Tweets directory

    csv_file = open(f'{__dir}/{results[0]}.csv', 'a')
    csv_writer = csv.writer(csv_file)

    for i in range(len(tweet_texts)):  # writes captured tweets to the file
        csv_writer.writerow([tweet_timestamps[i], tweet_texts[i]])

    print('Done!')


def read_tweets():
    filename = input('Kindly enter the filename: ')
    if os.path.isfile(f'./Tweets/{filename.title()}.csv'):
        with open(f'./Tweets/{filename.title()}.csv', 'r') as file:
            print(file.read())
    else:
        print('File does not exist!')
        read_tweets()


def menu():
    print('a: Capture tweets from any given country')
    print('b: Read existing tweets from file')
    choice = str(input('Choose an option: ')).lower()
    if choice == "a":
        capture_tweets()
    elif choice == "b":
        read_tweets()
    else:
        print('Select a valid option!')
        return menu()


try:
    api.verify_credentials()
    print("Authenticated")
except:
    print("Unauthorized!")

menu()
