def test_has_contextmanaged_methods():
    from contextmanaged_objects import HasContextManagedMethods

    class Foo(HasContextManagedMethods):
        def __init__(self, x):
            self.x = x

        def bar(self):
            store_current_foo_x()

    output = []

    def store_current_foo_x():
        output += [Foo.current().x]

    foo1 = Foo(1)
    foo2 = Foo(2)

    assert output == []

    foo1.bar()

    assert output == [1]

    foo2.bar()

    assert output == [1, 2]
