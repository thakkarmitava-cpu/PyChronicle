def outer(x):
    def inner(y):
        return y * 2

    return inner(x)

result = outer(10)
print(result)