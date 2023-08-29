# Context-Managed Objects in Python

This project provides a way to manage objects in a context-aware manner in Python. It includes a class HasContextManagedFocus and a decorator make_current. These tools can be particularly useful in scenarios where you need to manage context-specific objects like user credentials or other parameters that are frequently passed around in a backend application.

## Getting Started

This project is available on PyPI. You can install it using pip:

```bash
pip install contextmanaged-objects
```

## Usage

Consider a scenario where you're building a web application and you need to keep track of the current user's credentials. Instead of passing the user credentials as arguments to every function, you can use HasContextManagedFocus and make_current to manage the current user context.

```python
from contextmanaged_objects import HasContextManagedFocus, make_current

class User(HasContextManagedFocus):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @make_current()
    def start_doing_something(self):
        # do something with the current user
        call_first_library_function()

...

fiftieth_library_function():
    # do something with the current user
    current_user = User.get_current()
    # we didn't have to pass current_user as an argument along the entire 1st-49th library function chain

user1 = User('user1', 'password1')
user2 = User('user2', 'password2')
```

In this example, User is a subclass of `HasContextManagedFocus`. The `do_something` method is decorated with `make_current`, so whenever `do_something` is invoked, `user1` or `user2` (whichever is the current instance) is placed on top of the context stack. This allows you to easily manage the current user context without having to pass user credentials around.

## API Reference

### HasContextManagedFocus

This class allows objects to be context-managed. It maintains a context stack where instances can be placed on top of the stack and retrieved. The as_current method is a context manager that puts the instance on top of its context stack.

###  make_current

This function is a decorator for instance methods. It automatically puts the instance on top of its context stack during invocation and removes it after invocation is over.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

We use pytest for testing. To run the tests, run the following command from the root directory of the project:

```bash
poetry run pytest
```

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
