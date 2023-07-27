import requests
import os
import json
import sys
import logging
import schedule
import time
import smtplib
import win32com.client as win32
import warnings
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from colorama import init, Fore