import webbrowser
import time

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except Exception:
    PYAUTOGUI_AVAILABLE = False


def youtube_search(query):

    webbrowser.open("https://www.youtube.com")

    if PYAUTOGUI_AVAILABLE:

        time.sleep(5)

        pyautogui.write(query)

        pyautogui.press("enter")

    return f"Searching YouTube for '{query}'"


def google_search(query):

    webbrowser.open("https://www.google.com")

    if PYAUTOGUI_AVAILABLE:

        time.sleep(4)

        pyautogui.write(query)

        pyautogui.press("enter")

    return f"Searching Google for '{query}'"