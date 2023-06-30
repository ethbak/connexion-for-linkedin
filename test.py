"""
Test script for ConneXion.

Author: Ethan Baker
"""
import os
import time
import random
import pickle
import pandas as pd
import numpy as np
import search_tool.search_for_profiles as search_for_profiles
import consts as c
from search_tool.google_api import GoogleSearchAPI
from search_tool.indexed_data import IndexedData
from connection_automator.linkedin_bot import LinkedinBot

def test_load_preferences():
    # 1 Location and Position
    c.LOCATIONS = ["Cazenovia"]
    c.POSITIONS = ["Intern"]
    c.EXPERIENCE_OPERATOR = "="
    c.EXPERIENCE_YEARS = 10
    expected = {"location":["Cazenovia"], "position":["Intern"], 
                "exp_op":"=", "exp_num":10}
    actual = search_for_profiles.load_preferences()
    assert expected == actual, "test_load_preferences failed."

    # Multiple locations and positions
    c.LOCATIONS = ["Cazenovia", "Philadelphia"]
    c.POSITIONS = ["Intern", "CEO", "COO"]
    c.EXPERIENCE_OPERATOR = ">"
    c.EXPERIENCE_YEARS = 5
    expected = {"location":["Cazenovia", "Philadelphia"], 
                "position":["Intern", "CEO", "COO"], 
                "exp_op":">", "exp_num":5}
    actual = search_for_profiles.load_preferences()
    assert expected == actual, "test_load_preferences failed."
    print("load_preferences passed.")

def test_save_results():
    # Create results input
    titles = ["Ethan Baker - Intern",
              "Alec Price - Financial Advisor",
              "Ana Yavorska - Intern"]
    links = ["https://www.linkedin.com/ethbak",
             "www.pricefm.com",
             "google.com"]
    snippets = ["1 year of experience",
                "33 years of experience",
                "2 years of experience"]
    results = pd.DataFrame()
    results["Title"] = titles
    results["Link"] = links
    results["Snippets"] = snippets

    # Empty excel file already exists
    c.EXCEL_FILE_LOCATION = r"tests/excel_tests/excel_empty.xlsx"
    search_for_profiles.save_results(results)
    xl = pd.read_excel(c.EXCEL_FILE_LOCATION)
    assert xl.equals(results), "test_save_results failed."
    reset = pd.DataFrame()
    reset.to_excel(c.EXCEL_FILE_LOCATION, index=False)

    # Excel file already exists with some client data
    c.EXCEL_FILE_LOCATION = r"tests/excel_tests/excel_data.xlsx"
    before = pd.read_excel(c.EXCEL_FILE_LOCATION)
    search_for_profiles.save_results(results)
    xl = pd.read_excel(c.EXCEL_FILE_LOCATION)
    titles = ["The Person", "Ethan Baker - Intern",
              "Alec Price - Financial Advisor",
              "Ana Yavorska - Intern"]
    links = ["yelp.com", "https://www.linkedin.com/ethbak",
             "www.pricefm.com",
             "google.com"]
    snippets = ["99 years of experience",
                "1 year of experience",
                "33 years of experience",
                "2 years of experience"]
    expected = pd.DataFrame()
    expected["Title"] = titles
    expected["Link"] = links
    expected["Snippets"] = snippets
    assert expected.equals(xl), "test_save_results failed."
    before.to_excel(c.EXCEL_FILE_LOCATION, index=False)

    # Excel file already exists with other type of data
    c.EXCEL_FILE_LOCATION = r"tests/excel_tests/excel_different_data.xlsx"
    before = pd.read_excel(c.EXCEL_FILE_LOCATION)
    search_for_profiles.save_results(results)
    xl = pd.read_excel(c.EXCEL_FILE_LOCATION)
    job = ["Intern", "Owner", "CEO", np.nan, np.nan, np.nan]
    location = ["Cazenovia", "Voorhees", "Berlin", np.nan, np.nan, np.nan]
    titles = [np.nan, np.nan, np.nan, "Ethan Baker - Intern",
              "Alec Price - Financial Advisor",
              "Ana Yavorska - Intern"]
    links = [np.nan, np.nan, np.nan, "https://www.linkedin.com/ethbak",
             "www.pricefm.com",
             "google.com"]
    snippets = [np.nan, np.nan, np.nan, "1 year of experience",
                "33 years of experience",
                "2 years of experience"]
    expected = pd.DataFrame()
    expected["Job Title"] = job
    expected["Location"] = location
    expected["Title"] = titles
    expected["Link"] = links
    expected["Snippets"] = snippets
    assert expected.equals(xl), "test_save_results failed."
    before.to_excel(c.EXCEL_FILE_LOCATION, index=False)

    # Excel file doesnt exist
    c.EXCEL_FILE_LOCATION = r"tests/excel_tests/excel_new.xlsx"
    search_for_profiles.save_results(results)
    xl = pd.read_excel(c.EXCEL_FILE_LOCATION)
    assert xl.equals(results), "test_save_results failed."
    os.remove(c.EXCEL_FILE_LOCATION)
    print("save_results passed.")

def test_generate_queries():
    # 1 position and location, operator is "="
    preferences = {"location":["Cazenovia"], "position":["Intern"], 
                "exp_op":"=", "exp_num":10}
    expected = ['site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("10 year")']
    actual = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID).generate_queries(preferences)
    assert expected == actual, "test_generate_queries failed."

    # Multiple positions and locations, operator is ">"
    preferences = {"location":["Cazenovia", "Syracuse"], 
                   "position":["Intern", "CEO"], 
                    "exp_op":">", "exp_num":28}
    expected = ['site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("28 years")',
                'site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("29 years")',
                'site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("30 years")',
                'site:linkedin.com/in intitle:("Intern") AND ("Syracuse") AND ("28 years")',
                'site:linkedin.com/in intitle:("Intern") AND ("Syracuse") AND ("29 years")',
                'site:linkedin.com/in intitle:("Intern") AND ("Syracuse") AND ("30 years")',
                'site:linkedin.com/in intitle:("CEO") AND ("Cazenovia") AND ("28 years")',
                'site:linkedin.com/in intitle:("CEO") AND ("Cazenovia") AND ("29 years")',
                'site:linkedin.com/in intitle:("CEO") AND ("Cazenovia") AND ("30 years")',
                'site:linkedin.com/in intitle:("CEO") AND ("Syracuse") AND ("28 years")',
                'site:linkedin.com/in intitle:("CEO") AND ("Syracuse") AND ("29 years")',
                'site:linkedin.com/in intitle:("CEO") AND ("Syracuse") AND ("30 years")']
    actual = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID).generate_queries(preferences)
    assert expected == actual, "test_generate_queries failed."

    # Operator is "<"
    preferences = {"location":["Cazenovia"], 
                   "position":["Intern"], 
                    "exp_op":"<", "exp_num":3}
    expected = ['site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") -"year" -"years"',
                'site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("1 year")',
                'site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("2 years")']
    actual = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID).generate_queries(preferences)
    assert expected == actual, "test_generate_queries failed."

    # operator is ">", number is 30
    preferences = {"location":["Cazenovia"], 
                   "position":["Intern"], 
                    "exp_op":">", "exp_num":30}
    expected = ['site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("30 years")']
    actual = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID).generate_queries(preferences)
    assert expected == actual, "test_generate_queries failed."

    # operator is "<", number is 1"
    preferences = {"location":["Cazenovia"], 
                   "position":["Intern"], 
                    "exp_op":"<", "exp_num":1}
    expected = ['site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") -"year" -"years"']
    actual = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID).generate_queries(preferences)
    assert expected == actual, "test_generate_queries failed."

    # Filter out some of the search queries
    c.REPEAT_QUERIES = False
    c.QUERY_INDEX_LOCATION = "tests/pkl_tests/indexed_queries_generated.pkl"
    preferences = {"location":["Cazenovia"], 
                   "position":["Intern"], 
                    "exp_op":"<", "exp_num":3}
    expected = ['site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("1 year")',
                'site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("2 years")']
    actual = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID).generate_queries(preferences)
    assert expected == actual, "test_generate_queries failed."

    # Filter out all of the search queries
    c.REPEAT_QUERIES = False
    c.QUERY_INDEX_LOCATION = "tests/pkl_tests/indexed_queries_generated_all.pkl"
    preferences = {"location":["Cazenovia"], 
                   "position":["Intern"], 
                    "exp_op":"<", "exp_num":3}
    with open("tests/pkl_tests/indexed_queries_generated_all.pkl", 'wb') as file:
        pickle.dump(['site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") -"year" -"years"',
                'site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("1 year")',
                'site:linkedin.com/in intitle:("Intern") AND ("Cazenovia") AND ("2 years")'],
                file)
    expected = []
    actual = GoogleSearchAPI(c.API_KEY, c.SEARCH_ENGINE_ID).generate_queries(preferences)
    assert expected == actual, "test_generate_queries failed."

    print("generate_queries passed.")

def test_load_indexed_profiles():
    # Empty file
    index = IndexedData("tests/pkl_tests/indexed_profiles_empty.pkl",
                        "tests/pkl_tests/indexed_queries_empty.pkl")
    assert index.profiles == [], "test_load_indexed_profiles failed."

    # File with some data already in it
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    assert index.profiles == ["alec", "ethan", "sharon"], "test_load_indexed_profiles failed."
    print("load_indexed_profiles passed.")

def test_check_dup_profile():
    # No duplicate
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    assert index.check_dup_profile("Anastasiya Yavorska") is False, "test_check_dup_profile failed."

    # Duplicate
    assert index.check_dup_profile("ethan") is True, "test_check_dup_profile failed."
    print("check_dup_profile passed.")

def test_add_indexed_profile():
    # Add to empty list
    index = IndexedData("tests/pkl_tests/indexed_profiles_empty.pkl",
                        "tests/pkl_tests/indexed_queries_empty.pkl")
    index.add_indexed_profile("fred")
    assert index.profiles == ['fred'], "test_add_indexed_profile failed."

    # Add to full list
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    index.add_indexed_profile("fred")
    assert index.profiles == ['alec', 'ethan', 'fred', 'sharon'], "test_add_indexed_profile failed."
    print("add_indexed_profile passed.")

def test_save_indexed_profiles():
    # Empty list
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    index.profile_file = "tests/pkl_tests/save.pkl"
    index.profiles = []
    index.save_indexed_profiles()
    assert IndexedData("tests/pkl_tests/save.pkl",
                       "tests/pkl_tests/indexed_queries_full.pkl").profiles == [], "test_save_indexed_profiles failed."

    # Full list
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    index.profile_file = "tests/pkl_tests/save.pkl"
    index.profiles = ['alec','anastasiya','ethan','zoe']
    index.save_indexed_profiles()
    assert IndexedData("tests/pkl_tests/save.pkl",
                       "tests/pkl_tests/indexed_queries_full.pkl").profiles == index.profiles, "test_save_indexed_profiles failed."

    os.remove("tests/pkl_tests/save.pkl")
    with open ("tests/pkl_tests/save.pkl", 'wb'):
        pass

    print("save_indexed_profiles passed.")

def test_load_indexed_queries():
    # Empty file
    index = IndexedData("tests/pkl_tests/indexed_profiles_empty.pkl",
                        "tests/pkl_tests/indexed_queries_empty.pkl")
    assert index.queries == [], "test_load_indexed_queries failed."

    # File with some data already in it
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    assert index.queries == ["CEO", "Manager", "Owner"], "test_load_indexed_queries failed."
    print("load_indexed_queries passed.")

def test_check_dup_query():
    # No duplicate
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    assert index.check_dup_query("Chief Executive Officer") is False, "test_check_dup_query failed."

    # Duplicate
    assert index.check_dup_query("CEO") is True, "test_check_dup_query failed."
    print("check_dup_query passed.")

def test_add_indexed_query():
    # Add to empty list
    index = IndexedData("tests/pkl_tests/indexed_profiles_empty.pkl",
                        "tests/pkl_tests/indexed_queries_empty.pkl")
    index.add_indexed_query("CFO")
    assert index.queries == ['CFO'], "test_add_indexed_query failed."

    # Add to full list
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    index.add_indexed_query("CFO")
    assert index.queries == ['CEO', 'CFO', 'Manager', 'Owner'], "test_add_indexed_query failed."
    print("add_indexed_query passed.")

def test_save_indexed_queries():
    # Empty list
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    index.query_file = "tests/pkl_tests/save.pkl"
    index.queries = []
    index.save_indexed_queries()
    assert IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                       "tests/pkl_tests/save.pkl").queries == [], "test_save_indexed_queries failed."

    # Full list
    index = IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                        "tests/pkl_tests/indexed_queries_full.pkl")
    index.query_file = "tests/pkl_tests/save.pkl"
    index.queries = ['CEO', 'CFO', 'Intern', 'Manager', 'Owner']
    index.save_indexed_queries()
    assert IndexedData("tests/pkl_tests/indexed_profiles_full.pkl",
                       "tests/pkl_tests/save.pkl").queries == index.queries, "test_save_indexed_queries failed."

    os.remove("tests/pkl_tests/save.pkl")
    with open ("tests/pkl_tests/save.pkl", 'wb'):
        pass

    print("save_indexed_queries passed.")

def test_login():
    # Valid login
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    result = bot1.login()
    assert result, "test_login failed."
    bot1.driver.quit()

    # Invalid login
    c.USERNAME = "hello"
    c.PASSWORD = "world"
    bot2 = LinkedinBot()
    result = bot2.login()
    assert not result, "test_login failed."
    bot2.driver.quit()

    time.sleep(random.uniform(3,5))
    print("login passed.")

def test_send_connection_request():
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()
    
    # Has a connect button
    bot1.driver.get("https://www.linkedin.com/in/daniel-lines-2b2045232/")
    time.sleep(random.uniform(3,5))
    assert bot1.send_connection_request("Lets connect!"), "test_send_connection_request failed."

    # Follow instead of connect
    bot1.driver.get("https://www.linkedin.com/in/mark-cuban-06a0755b/")
    time.sleep(random.uniform(3,5))
    assert not bot1.send_connection_request("Lets connect!"), "test_send_connection_request failed."

    # Has a connect button but requires more info to send request
    bot1.driver.get("https://www.linkedin.com/in/david-m-solomon/")
    time.sleep(random.uniform(3,5))
    assert not bot1.send_connection_request("Lets connect!"), "test_send_connection_request failed."

    # Is already a connection
    bot1.driver.get("https://www.linkedin.com/in/ethbak/")
    time.sleep(random.uniform(3,5))
    assert not bot1.send_connection_request("Lets connect!"), "test_send_connection_request failed."

    # Profile has an outgoing connection request towards the user
    bot1.driver.get("https://www.linkedin.com/in/ayavorska/")
    time.sleep(random.uniform(3,5))
    assert not bot1.send_connection_request("Lets connect!"), "test_send_connection_request failed."

    # User has already sent the profile a request
    bot1.driver.get("https://www.linkedin.com/in/ethanbakertest/")
    time.sleep(random.uniform(3,5))
    assert not bot1.send_connection_request("Lets connect!"), "test_send_connection_request failed."

    bot1.driver.quit()
    print("send_connection_request passed.")

def test_more_then_connect():
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()

    # Has a connect button
    bot1.driver.get("https://www.linkedin.com/in/daniel-lines-2b2045232/")
    time.sleep(random.uniform(3,5))
    assert not bot1.more_then_connect("Lets connect!"), "test_more_then_connect failed."

    # Has hidden connect button
    bot1.driver.get("https://www.linkedin.com/in/mark-cuban-06a0755b/")
    time.sleep(random.uniform(3,5))
    assert bot1.more_then_connect("Lets connect!"), "test_more_then_connect failed."

    # Following
    bot1.driver.get("https://www.linkedin.com/in/david-m-solomon/")
    time.sleep(random.uniform(3,5))
    assert not bot1.more_then_connect("Lets connect!"), "test_more_then_connect failed."

    # Is already a connection
    bot1.driver.get("https://www.linkedin.com/in/ethbak/")
    time.sleep(random.uniform(3,5))
    assert not bot1.more_then_connect("Lets connect!"), "test_more_then_connect failed."

    # Profile has an outgoing connection request towards the user
    bot1.driver.get("https://www.linkedin.com/in/ayavorska/")
    time.sleep(random.uniform(3,5))
    assert not bot1.more_then_connect("Lets connect!"), "test_more_then_connect failed."

    # User has already sent the profile a request
    bot1.driver.get("https://www.linkedin.com/in/ethanbakertest/")
    time.sleep(random.uniform(3,5))
    assert not bot1.more_then_connect("Lets connect!"), "test_more_then_connect failed."

    # Not famous but has hidden connect button
    bot1.driver.get("https://www.linkedin.com/in/marc-sperg-a4696721/")
    time.sleep(random.uniform(3,5))
    assert bot1.more_then_connect("Lets connect!"), "test_more_then_connect failed." 

    bot1.driver.quit()
    print("more_then_connect passed.")

def test_accept_request():
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()

    # Has a connect button
    bot1.driver.get("https://www.linkedin.com/in/daniel-lines-2b2045232/")
    time.sleep(random.uniform(3,5))
    assert not bot1.accept_request(), "test_accept_request failed."

    # Follow instead of connect
    bot1.driver.get("https://www.linkedin.com/in/mark-cuban-06a0755b/")
    time.sleep(random.uniform(3,5))
    assert not bot1.accept_request(), "test_accept_request failed."

    # Has a connect button but requires more info to send request
    bot1.driver.get("https://www.linkedin.com/in/david-m-solomon/")
    time.sleep(random.uniform(3,5))
    assert not bot1.accept_request(), "test_accept_request failed."

    # Is already a connection
    bot1.driver.get("https://www.linkedin.com/in/ethbak/")
    time.sleep(random.uniform(3,5))
    assert not bot1.accept_request(), "test_accept_request failed."

    # Profile has an outgoing connection request towards the user
    bot1.driver.get("https://www.linkedin.com/in/ayavorska/")
    time.sleep(random.uniform(3,5))
    assert bot1.accept_request(), "test_accept_request failed."

    # User has already sent the profile a request
    bot1.driver.get("https://www.linkedin.com/in/ethanbakertest/")
    time.sleep(random.uniform(3,5))
    assert not bot1.accept_request(), "test_accept_request failed."

    bot1.driver.quit()
    print("accept_request passed.")

def test_extract_connection_count():
    # Login
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()

    # No connections
    bot1.driver.get("https://www.linkedin.com/in/ethbaktest")
    assert bot1.extract_connection_count() == 0, "test_extract_connection_count failed."
    time.sleep(random.uniform(3,5))

    # 0 < connections < 500
    bot1.driver.get("https://www.linkedin.com/in/ethanbakertest")
    assert bot1.extract_connection_count() == 1, "test_extract_connection_count failed."
    time.sleep(random.uniform(3,5))

    # 500+ connections and someone who has already connected with
    bot1.driver.get("https://www.linkedin.com/in/ethbak")
    assert bot1.extract_connection_count() == 500, "test_extract_connection_count failed."

    # Shows follower count and connection count
    bot1.driver.get("https://www.linkedin.com/in/aryaaagarwal/")
    assert bot1.extract_connection_count() > 730, "test_extract_connection_count failed."

    # Only shows follower count
    bot1.driver.get("https://www.linkedin.com/in/arnesorenson/")
    assert bot1.extract_connection_count() > 800000, "test_extract_connection_count failed"

    time.sleep(random.uniform(3,5))
    print("extract_connection_count_passed")

def test_has_connect_button():
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()

    # Has a connect button
    bot1.driver.get("https://www.linkedin.com/in/daniel-lines-2b2045232/")
    time.sleep(random.uniform(3,5))
    assert bot1.has_connect_button(), "test_has_connect_button failed."

    # Follow instead of connect
    bot1.driver.get("https://www.linkedin.com/in/mark-cuban-06a0755b/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_connect_button(), "test_has_connect_button failed."

    # Following instead of connect
    bot1.driver.get("https://www.linkedin.com/in/david-m-solomon/")
    time.sleep(random.uniform(3,5))
    assert bot1.has_connect_button(), "test_has_connect_button failed."

    # Is already a connection
    bot1.driver.get("https://www.linkedin.com/in/ethbak/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_connect_button(), "test_has_connect_button failed."

    # Profile has an outgoing connection request towards the user
    bot1.driver.get("https://www.linkedin.com/in/ayavorska/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_connect_button(), "test_has_connect_button failed."

    # User has already sent the profile a request
    bot1.driver.get("https://www.linkedin.com/in/ethanbakertest/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_connect_button(), "test_has_connect_button failed."

    bot1.driver.quit()
    print("has_connect_button passed.")

def test_has_accept_button():
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()

    # Profile has an outgoing connection request towards the user
    bot1.driver.get("https://www.linkedin.com/in/ayavorska/")
    time.sleep(random.uniform(3,5))
    assert bot1.has_accept_button(), "test_has_accept_button failed."

    # Has a connect button
    bot1.driver.get("https://www.linkedin.com/in/daniel-lines-2b2045232/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_accept_button(), "test_has_accept_button failed."

    # Follow instead of connect
    bot1.driver.get("https://www.linkedin.com/in/mark-cuban-06a0755b/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_accept_button(), "test_has_accept_button failed."

    # Following instead of connect
    bot1.driver.get("https://www.linkedin.com/in/david-m-solomon/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_accept_button(), "test_has_accept_button failed."

    # Is already a connection
    bot1.driver.get("https://www.linkedin.com/in/ethbak/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_accept_button(), "test_has_accept_button failed."

    # User has already sent the profile a request
    bot1.driver.get("https://www.linkedin.com/in/ethanbakertest/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_accept_button(), "test_has_accept_button failed."

    bot1.driver.quit()
    print("has_accept_button passed.")

def test_has_hidden_connect_button():
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()

    # Profile has an outgoing connection request towards the user (No hidden button)
    bot1.driver.get("https://www.linkedin.com/in/ayavorska/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_hidden_connect_button(), "test_has_hidden_connect_button failed."

    # Has a connect button (No hidden button)
    bot1.driver.get("https://www.linkedin.com/in/daniel-lines-2b2045232/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_hidden_connect_button(), "test_has_hidden_connect_button failed."

    # Follow instead of connect (Has a button)
    bot1.driver.get("https://www.linkedin.com/in/mark-cuban-06a0755b/")
    time.sleep(random.uniform(3,5))
    assert bot1.has_hidden_connect_button(), "test_has_hidden_connect_button failed."

    # Following instead of connect (No hidden button)
    bot1.driver.get("https://www.linkedin.com/in/david-m-solomon/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_hidden_connect_button(), "test_has_hidden_connect_button failed."

    # Is already a connection (No button)
    bot1.driver.get("https://www.linkedin.com/in/ethbak/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_hidden_connect_button(), "test_has_hidden_connect_button failed."

    # User has already sent the profile a request (No button)
    bot1.driver.get("https://www.linkedin.com/in/ethanbakertest/")
    time.sleep(random.uniform(3,5))
    assert not bot1.has_hidden_connect_button(), "test_has_hidden_connect_button failed."

def test_write_message():
    # No custom features
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    c.MESSAGE = "Hello there!"
    bot1 = LinkedinBot()
    bot1.login()
    bot1.driver.get("https://www.linkedin.com/in/ethbak")
    time.sleep(random.uniform(3,5))

    msg = bot1.write_message()
    assert msg == "Hello there!", "test_write_message failed."
    bot1.driver.quit()

    # Custom full name
    c.MESSAGE = "Hi [FULL NAME]! Nice to meet you!"
    bot2 = LinkedinBot()
    bot2.login()
    bot2.driver.get("https://www.linkedin.com/in/ethbak")
    time.sleep(random.uniform(3,5))

    msg = bot2.write_message()
    assert msg == "Hi Ethan Baker! Nice to meet you!", "test_write_message failed."
    bot2.driver.quit()

    # Custom first name
    c.MESSAGE = "Hi [FIRST NAME]! Nice to meet you!"
    bot3 = LinkedinBot()
    bot3.login()
    bot3.driver.get("https://www.linkedin.com/in/ethbak")
    time.sleep(random.uniform(3,5))

    msg = bot3.write_message()
    assert msg == "Hi Ethan! Nice to meet you!", "test_write_message failed."
    bot3.driver.quit()

    # Name starts with a Dr.
    c.MESSAGE = "Hi [FIRST NAME]! Nice to meet you!"
    bot4 = LinkedinBot()
    bot4.login()
    bot4.driver.get("https://www.linkedin.com/in/dambisamoyo/")
    time.sleep(random.uniform(3,5))

    msg = bot4.write_message()
    assert msg == "Hi Dambisa! Nice to meet you!", "test_write_message failed."
    bot4.driver.quit()

    print("write_message passed.")

def test_check_weekly_limit():
    # No limit message
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot1 = LinkedinBot()
    bot1.login()

    bot1.driver.get("https://www.linkedin.com/in/brandon-wu-60aa26266/")
    time.sleep(random.uniform(3,5))
    bot1.send_connection_request("Lets connect!")
    time.sleep(random.uniform(3,5))
    assert not bot1.check_weekly_limit(), "test_check_weekly_limit failed."
    bot1.driver.quit()

    # Limit message
    c.USERNAME = "8ethanbaker@gmail.com"
    c.PASSWORD = "Testpassword123!"
    bot2 = LinkedinBot()
    bot2.login()

    bot2.driver.get("https://www.linkedin.com/in/kinza-ceesay-0845b41a6/")
    time.sleep(random.uniform(3,5))
    bot2.send_connection_request("Lets connect!")
    time.sleep(random.uniform(3,5))
    assert bot2.check_weekly_limit(), "test_check_weekly_limit failed."
    bot2.driver.quit()

    print("check_weekly_limit passed.")

def test_search_for_profiles():
    """
    Tests all functions in search_for_profiles
    """
    test_load_preferences()
    test_save_results()
    print("All search_for_profiles.py functions passed.")

def test_google_api():
    """
    Tests all methods in the class GoogleSearchAPI
    Does not test search as it uses API requests.
    """
    test_generate_queries()
    print("All GoogleSearchAPI methods passed.")

def test_indexed_data():
    """
    Tests all methods in the class IndexedData.
    """
    test_load_indexed_profiles()
    test_check_dup_profile()
    test_add_indexed_profile()
    test_save_indexed_profiles()
    test_load_indexed_queries()
    test_check_dup_query()
    test_add_indexed_query()
    test_save_indexed_queries()
    print("All IndexedData methods passed.")

def test_linkedin_bot():
    """
    Tests all methods in the class LinkedinBot.

    Some of the test cases WILL FAIL as the connect / accept
    methods change the state of the LinkedIn profiles used in the tests.
    """
    test_login()
    test_send_connection_request()
    test_more_then_connect()
    test_accept_request()
    test_extract_connection_count()
    test_write_message()
    test_has_connect_button()
    test_has_hidden_connect_button()
    test_has_accept_button()
    test_check_weekly_limit()
    print("All LinkedinBot methods passed.")

def test_all():
    """
    Tests all functions for the Linkedin Client Search Tool.
    """
    test_search_for_profiles()
    test_google_api()
    test_indexed_data()
    test_linkedin_bot()
    print("All functions passed.")

if __name__ == "__main__":
    test_all()
