import sys
import resource


class PersonWithSlots:
    __slots__ = ('name', 'age')

    def __init__(self, name, age):
        self.name = name
        self.age = age


class PersonWithDict:
    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == '__main__':
    mem_init = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print('Initial RAM Usage: {:12,}'.format(mem_init))
    if sys.argv[1] == '--use-slots':
        persons = [PersonWithSlots('xxx', 20) for i in range(10 ** 6)]
    elif sys.argv[1] == '--use-dict':
        persons = [PersonWithDict('xxx', 20) for i in range(10 ** 6)]
    mem_final = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print('  Final RAM Usage: {:12,}'.format(mem_final))
