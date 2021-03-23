class Logger:
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        print(f'[INFO]: the function {self._func.__name__}() is running...')
        return self._func(*args, **kwargs)



