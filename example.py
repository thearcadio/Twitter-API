import scrape

# query is what you are actually searching
# start and end time are based on "Zulu" or "UTC" time
# max results is how many are returned per page not per API call
# tweet.fields is what you want to expand on
# more information can be found at: 
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all

query_params = {'query': '@nycgov OR New York',
                'start_time': '2021-04-24T07:20:50.52Z', #
                'end_time': None,
                'max_results': 200,
                'tweet.fields': 'geo'
                }

my_results = scrape.search(query_params)

scrape.save(my_results, 'my_results.json')

# after you run a query the gloval variables count and pages, uncomment the lines below to do this
# scrape.count = 0
# scrape.pages = 0
