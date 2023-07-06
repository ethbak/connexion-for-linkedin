"""
The Google Search API module of the LinkedIn Search Tool.

This module allows the program to interact with Google's Custom Search
API and facilitates the conversion of user filter preferences into 
search queries.

Author: Ethan Baker
"""
import random
import requests
import pandas as pd
import consts as c
from search_tool.indexed_data import IndexedData

class GoogleSearchAPI:
    """
    A class representing a custom Google search engine.

    The class contains properties key and engine_id, which represent
    the API key, and custom search engine ID, respectively. The class contains
    methods to generate search queries and to return search results of a 
    query.
    """

    def __init__(self, key, engine_id):
        """
        Creates a new GoogleSearchAPI object.

        Parameter key: The API key used in the Google Search.
        Precondition: key is a String object representing a valid API key.

        Parameter engine_id: The ID of the Custom Google search engine.
        Precondition: engine_id is a String object representing a 
        valid search engine engine ID.
        """
        self.key = key
        self.id = engine_id

    def generate_queries(self, preferences):
        """
        Generates a list of search terms to input into Google.

        These queries are based on the user's preferences as per 
        consts.py. Used to input into Google, as each search term is
        limited to 100 results per Google's API. Generating a list of
        search terms instead of using Google's AND operator allows for
        more clients to be found as each term generates 100 new results.

        Returns: A list of strings that represent search queries.

        Parameter preferences: A dictionary of user search preferences.
        Precondition: preferences is generated by 
        search_for_profiles.load_preferences() and is based on a consts.py 
        configuration which follows the rules outlined in that file.
        """
        queries = []
        # Generate list of queries
        for pos in preferences["position"]:
            for loc in preferences["location"]:
                if preferences["exp_op"] == ">":
                    for years in list(range(int(preferences["exp_num"]), 31)):
                        s = ""
                        if years != 1: s = "s"
                        queries.append('site:linkedin.com/in intitle:("'+loc+
                                       '") AND ("'+pos+'") AND ("'+
                                       str(years)+' year' + s + '")')
                elif preferences["exp_op"] == "<":
                    for years in list(range(0, int(preferences["exp_num"]))):
                        s = ""
                        if years != 1: s = "s"
                        if years == 0:
                            queries.append('site:linkedin.com/in intitle:("'+loc+
                                       '") AND ("'+pos
                                       +'") -"year" -"years"')
                        else:
                            queries.append('site:linkedin.com/in intitle:("'+loc+
                                       '") AND ("'+pos+'") AND ("'+
                                       str(years)+' year' + s + '")')
                elif preferences["exp_op"] == "=":
                    s = ""
                    if preferences["exp_num"] != 1: s = "s"
                    queries.append('site:linkedin.com/in intitle:("'+loc+
                                    '") AND ("'+pos+'") AND ("'+
                                        str(preferences["exp_num"])+' year")')
                    
        # Remove previously searched queries if necessary
        if c.REPEAT_QUERIES == False:
            indexed = IndexedData(c.PROFILE_INDEX_LOCATION, c.QUERY_INDEX_LOCATION)
            temp = queries.copy()
            for query in temp:
                if indexed.check_dup_query(query):
                    queries.remove(query)
        return queries

    def search(self, terms):
        """
        Searches google for terms as per user preferences in consts.py.

        Uses the list of terms from generate urls to search google until
        the daily free API request limit is reached. Records client profiles
        in a pandas DataFrame that includes the page Title, Url, and Snippets.
        After using a search query from terms, it records it so it doesnt get
        used again later. As it compiles the list of clients, the method checks 
        for and removes any previously indexed profiles from the DataFrame. The 
        method stops when it encounters an error from the API, either returning
        the error code, or in the case of the API request limit filling up, it
        returns a message signaling that.

        Returns: A list of length 2 where the first element is a pandas DataFrame
        that contains new profile information, and the second element is an error 
        message, if one occured.
        
        Parameter terms: The list of terms used to search Google.
        Precondition: terms is made up of Strings that represent Google 
        search terms.
        """
        # Set up DataFrame
        df = pd.DataFrame()
        titles = []
        links = []
        snippets = []

        er_msg = ""

        indexed = IndexedData(c.PROFILE_INDEX_LOCATION, c.QUERY_INDEX_LOCATION)
        code = ""
        brk = False
        random.shuffle(terms)
        for term in terms:
            num_results = 100
            start = 1
            while num_results > start:
                url = f"https://www.googleapis.com/customsearch/v1?key="
                url = url + f"{self.key}&cx={self.id}&q={term}&start={start}"
                data = requests.get(url).json()
                
                # Look for error
                if data.get("error") is not None:
                    brk = True
                    error = data.get("error")
                    code = error.get("code")
                    break

                # Get search result data
                search_info = data.get("searchInformation")
                if search_info is not None:
                    total_results = search_info.get("totalResults")
                    if total_results is not None:
                        num_results = min(100, int(total_results))
                start += 10

                if data.get("items") is not None:
                    for result in data.get("items"):
                        if not indexed.check_dup_profile(result.get("link")):
                            indexed.add_indexed_profile(result.get("link"))
                            titles.append(result.get("title"))
                            links.append(result.get("link"))
                            snippets.append(result.get("snippet"))
            # Index search query
            indexed.add_indexed_query(term)
            if brk:
                if code != 429:
                    er_msg = "Google API Error " + str(code)
                else:
                    er_msg = "API request limit reached."
                break

        indexed.save_indexed_queries()
        indexed.save_indexed_profiles()
        
        # Create and return data frame
        df["Title"] = titles
        df["Link"] = links
        df["Snippets"] = snippets

        lst = [df, er_msg]
        return lst
