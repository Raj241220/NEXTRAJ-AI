import webbrowser
import pyautogui
import time


def youtube_search(query):

    webbrowser.open("https://www.youtube.com")

    time.sleep(5)

    pyautogui.write(query)

    pyautogui.press("enter")

    return f"Searching YouTube for '{query}'"


def google_search(query):

    webbrowser.open("https://www.google.com")

    time.sleep(4)

    pyautogui.write(query)

    pyautogui.press("enter")

    return f"Searching Google for '{query}'"