from time import sleep
from uuid import uuid4
from concurrent.futures import ThreadPoolExecutor


def test_multithreaded_context_managed():
    from contextmanaged_objects import HasContextManagedFocus

    class Foo(HasContextManagedFocus):
        def __init__(self, x):
            self.x = x

    def test_single_thread(index):
        foo1_val = uuid4()
        foo2_val = uuid4()

        foo1 = Foo(foo1_val)
        foo2 = Foo(foo2_val)

        assert Foo.current() is None

        with foo1.as_current():
            assert Foo.current() is foo1
            assert foo1.x == foo1_val
            sleep(0.1)
            assert foo2.x == foo2_val
            sleep(0.1)
            with foo2.as_current():
                assert Foo.current() is foo2
                assert foo1.x == foo1_val
                sleep(0.1)
                assert foo2.x == foo2_val
                sleep(0.1)
            assert Foo.current() is foo1
            assert foo1.x == foo1_val
            sleep(0.1)
            assert foo2.x == foo2_val
            sleep(0.1)

        assert Foo.current() is None

        return True

    def test_parallel():
        with ThreadPoolExecutor(max_workers=100) as executor:
            results = list(executor.map(test_single_thread, range(100)))

        assert all(
            result == True for result in results
        ), "Not all threads returned True"

    HasContextManagedFocus.enable_threaded_context()
    test_parallel()
    HasContextManagedFocus.disable_threaded_context()
    try:
        test_parallel()
        assert False, "Should have raised AssertionError"
    except AssertionError:
        pass
