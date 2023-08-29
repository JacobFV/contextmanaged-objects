from contextmanaged_objects import make_current


def test_has_contextmanaged_methods():
    from contextmanaged_objects import HasContextManagedFocus

    class Foo(HasContextManagedFocus):
        def __init__(self, x):
            self.x = x

        @make_current()
        def bar(self):
            store_current_foo_x()

    output = []

    def store_current_foo_x():
        nonlocal output
        output += [Foo.current().x]

    foo1 = Foo(1)
    foo2 = Foo(2)

    assert output == []

    foo1.bar()

    assert output == [1]

    foo2.bar()

    assert output == [1, 2]
