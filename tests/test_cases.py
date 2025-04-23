import requests
import pytest
import unittest
from unittest.mock import patch, Mock, mock_open
from apihawk.core.fuzzer import fuzz_endpoint


class TestFuzzer(unittest.TestCase):
    #Simulate a invalid wordlist file
    def test_invalid_wordlist(self):
        result = fuzz_endpoint("http://example.com/FUZZ", "nonexistent.txt", "GET")
        self.assertIsNone(result)
    
    #Simulate a invalud URL
    def test_invalid_url(self):
        result = fuzz_endpoint("http://invalid-url..com/FUZZ", "wordlist.txt", "POST")
        self.assertIsNone(result)
    
    #Simulate a invlid method
    def test_invalid_method(self):
        result = fuzz_endpoint("http://example.com/FUZZ", "wordlist.txt", "INVALID")
        self.assertIsNone(result)
        
    #Simulate an invalid FUZZ (no fuzz inside of it)
    def test_invalid_fuzz(self):
        result = fuzz_endpoint("http://example.com/", "wordlist.txt", "GET")
        self.assertIsNone(result)
    
    #Simulate a valid fuzz
    @patch("builtins.open", mock_open(read_data=r"test\n\endpoint\napi"))
    def test_valid_fuzz(self):
        result = fuzz_endpoint("http://example.com/FUZZ", "wordlist.txt", "GET")
        self.assertIsInstance(result, list)