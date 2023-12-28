from rich.prompt import Prompt


def prompt_user():
    user_choices = ["dijkstra", "--imerla--", "goga_", "-fisherman-_"]
    user = Prompt.ask("Enter your name", choices=user_choices, default="dijkstra")
    return user

