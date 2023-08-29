def test_contextmanaged_focus():
    from contextmanaged_objects import HasContextManagedFocus

    class Foo(HasContextManagedFocus):
        def __init__(self, x):
            self.x = x

    foo1 = Foo(1)
    foo2 = Foo(2)

    assert Foo.current() is None

    with foo1.as_current():
        assert Foo.current() is foo1
        assert foo1.x == 1
        assert foo2.x == 2
        with foo2.as_current():
            assert Foo.current() is foo2
            assert foo1.x == 1
            assert foo2.x == 2
        assert Foo.current() is foo1
        assert foo1.x == 1
        assert foo2.x == 2

    assert Foo.current() is None
