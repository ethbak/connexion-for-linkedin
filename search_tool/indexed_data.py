"""
The Indexed Data module of the LinkedIn Search Tool.

This module allows the program to retrieve and record information
about profiles that have been indexed and query terms that have been
searched in the past. This ensures that the application does not return
repreat profiles or unnecessarily rely on search terms that have
recently been used.

Author: Ethan Baker
"""
import pickle

class IndexedData():
    """
    A class representing data that has previously been recorded by the application.

    Contains properties profiles and queries, which represent alphabetically sorted
    lists of previously indexed profiles and previously used search queries. Also 
    includes properties profile_file and query_file, which are the String filepaths
    to the indexes This class contains methods to load, check for duplicates, 
    add to, and save both of the lists.
    """

    def __init__(self, profile_file, query_file):
        """
        Creates an Indexed Data Object.

        This object contains two alphabetically sorted lists of strings 
        that represent profiles (represented by self.profiles) and queries 
        (represented by self.queries) which were indexed after running the 
        program a previous time.

        Parameter profile_file: the filepath to the profile index.
        Precondition: profile_file is a String containing a valid .pkl filepath.

        Parameter query_file: the filepath to the query index.
        Precondition: query_file is a String containing a valid .pkl filepath.
        """
        self.profile_file = profile_file
        self.query_file = query_file
        self.profiles = self.load_indexed_profiles()
        self.queries = self.load_indexed_queries()

    def load_indexed_profiles(self):
        """
        Loads the list of alphabetically sorted accounts from self.profile_file.
        """
        try:
            with open(self.profile_file, 'rb') as file:
                return pickle.load(file)
        except:
            return []
        
    def check_dup_profile(self, profile):
        """
        Checks for duplicate profiles using a recursive binary search algorithm.
        
        Returns: True if self.profiles contains profile, otherwise False.

        Parameter profile: the profile of the user that is being searched for.
        Precondition: profile is a String that represents a url. 
        """
        left = 0
        right = len(self.profiles) - 1

        while left <= right:
            mid = (left + right) // 2
            value = self.profiles[mid]

            if value == profile: return True
            elif value < profile: left = mid + 1
            else: right = mid - 1

        return False

    def add_indexed_profile(self, profile):
        """
        Adds a new profile url to its correct location in the sorted list.

        Modifies self.profiles to add the url of the new profile
        to its correct position based on alphabetical order.

        Parameter profile: The profile being added.
        Precondition: profile is a String that is not already in the list.
        """
        left = 0
        right = len(self.profiles) - 1

        while left <= right:
            mid = (left + right) // 2
            value = self.profiles[mid]

            if value < profile:
                left = mid + 1
            else:
                right = mid - 1
        
        self.profiles.insert(left, profile)

    def save_indexed_profiles(self):
        """
        Saves the updated list of indexed accounts to self.profile_file.
        """
        with open(self.profile_file, 'wb') as file:
            pickle.dump(self.profiles, file)
    
    def load_indexed_queries(self):
        """
        Loads the list of alphabetically sorted queries from self.query_file.
        """
        try:
            with open(self.query_file, 'rb') as file:
                return pickle.load(file)
        except: 
            return []

    def check_dup_query(self, query):
        """
        Checks for duplicate queries using a recursive binary search algorithm.
        
        Returns: True if self.queries contains query, otherwise False.

        Parameter query: A query search term.
        Precondition: query is a String that represents a valid query. 
        """
        left = 0
        right = len(self.queries) -1

        while left <= right:
            mid = (left + right) // 2
            value = self.queries[mid]

            if value == query: return True
            elif value < query: left = mid + 1
            else: right = mid - 1

        return False

    def add_indexed_query(self, query):
        """
        Adds a new query to its correct location in the sorted list.

        Modifies self.queries to add the new query search term
        to its correct position based on alphabetical order.

        Parameter query: A query search term.
        Precondition: query is a String that is not already in the list.
        """
        left = 0
        right = len(self.queries) - 1

        while left <= right:
            mid = (left + right) // 2
            value = self.queries[mid]

            if value < query:
                left = mid + 1
            else:
                right = mid - 1
        
        self.queries.insert(left, query)

    def save_indexed_queries(self):
        """
        Saves the updated list of indexed queries to self.query_file.
        """
        with open(self.query_file, 'wb') as file:
            pickle.dump(self.queries, file)