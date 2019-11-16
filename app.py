from molten import App, Route


def hello(name: str, age: int) -> str:
    return f"Hello {name}! I hear you're {age} years old."


app = App(routes=[Route("/hello/{name}/{age}", hello)])
