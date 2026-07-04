import webbrowser
import subprocess
import os

try:
    from core.automation import youtube_search, google_search
    AUTOMATION_AVAILABLE = True
except Exception:
    AUTOMATION_AVAILABLE = False


def execute_command(command):

    if not AUTOMATION_AVAILABLE:
        return None

    cmd = command.lower().strip()

    # Smart Search

    if "open youtube and search" in cmd:

        query = cmd.replace("open youtube and search", "").strip()

        if query:
            return youtube_search(query)

        return "What should I search on YouTube?"

    if "search google for" in cmd:

        query = cmd.replace("search google for", "").strip()

        if query:
            return google_search(query)

        return "What should I search on Google?"

    # Websites

    if "youtube" in cmd:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."

    elif "google" in cmd:
        webbrowser.open("https://www.google.com")
        return "Opening Google."

    elif "github" in cmd:
        webbrowser.open("https://github.com")
        return "Opening GitHub."

    elif "chatgpt" in cmd:
        webbrowser.open("https://chatgpt.com")
        return "Opening ChatGPT."

    elif "gmail" in cmd:
        webbrowser.open("https://mail.google.com")
        return "Opening Gmail."

    elif "facebook" in cmd:
        webbrowser.open("https://facebook.com")
        return "Opening Facebook."

    elif "instagram" in cmd:
        webbrowser.open("https://instagram.com")
        return "Opening Instagram."

    elif "linkedin" in cmd:
        webbrowser.open("https://linkedin.com")
        return "Opening LinkedIn."

    # Windows Apps

    elif "notepad" in cmd:
        subprocess.Popen("notepad")
        return "Opening Notepad."

    elif "calculator" in cmd:
        subprocess.Popen("calc")
        return "Opening Calculator."

    elif "paint" in cmd:
        subprocess.Popen("mspaint")
        return "Opening Paint."

    elif "cmd" in cmd:
        subprocess.Popen("cmd")
        return "Opening Command Prompt."

    elif "explorer" in cmd:
        subprocess.Popen("explorer")
        return "Opening File Explorer."

    elif "task manager" in cmd:
        subprocess.Popen("taskmgr")
        return "Opening Task Manager."

    elif "vs code" in cmd:

        try:
            subprocess.Popen("code")
            return "Opening VS Code."
        except Exception:
            return "VS Code command not found."

    elif "downloads" in cmd:
        os.startfile(os.path.expanduser("~/Downloads"))
        return "Opening Downloads."

    elif "documents" in cmd:
        os.startfile(os.path.expanduser("~/Documents"))
        return "Opening Documents."

    elif "desktop" in cmd:
        os.startfile(os.path.expanduser("~/Desktop"))
        return "Opening Desktop."

    elif "pictures" in cmd:
        os.startfile(os.path.expanduser("~/Pictures"))
        return "Opening Pictures."

    elif "music" in cmd:
        os.startfile(os.path.expanduser("~/Music"))
        return "Opening Music."

    elif "videos" in cmd:
        os.startfile(os.path.expanduser("~/Videos"))
        return "Opening Videos."

    return None