from compare import Search

get = Search("Macbook Air 2020", 5).get()
for data in get:
    print(data)