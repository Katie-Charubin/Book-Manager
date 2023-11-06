import sys
import book_dao

menu_options = {
    1: 'Add a Publisher',
    2: 'Add a Book',
    3: 'Edit a Book',
    4: 'Delete a Book',
    5: 'Search Books',
    6: 'Exit',
}

search_menu_options = {
    1: 'Search all Books',
    2: 'Search by Title',
    3: 'Search by ISBN',
    4: 'Search by Publisher',
    5: 'Search by Year',
    6: 'Search by Price',
    7: 'Search by Title and Publisher'
}

def search_all_books():
    # Use a data access object (DAO) to
    # abstract the retrieval of data from
    # a data resource such as a database.
    results = book_dao.findAll()

    # Display results
    print("The following are the ISBNs and titles of all books.")
    for item in results:
        print(item[0], item[1])
    print("The end of books.")


def search_by_title(title):
    results = book_dao.findByTitle(title)
    print("Search by Title:")
    s_format = "%-10s %-1s %-50s"
    print(s_format % ("ISBN:", "|", "Title:"))
    if len(results) == 0:
        print("N/A")
    else:
        for item in results:
            print(s_format % (item[0], "|", item[1]))
    print("---End of Search Results---")


def search_by_ISBN(ISBN):
    results = book_dao.findByISBN(ISBN)
    print("Search by ISBN:")
    s_format = "%-10s %-1s %-50s"
    print(s_format % ("ISBN:", "|", "Title:"))
    if len(results) == 0:
        print("N/A")
    else:
        for item in results:
            print(s_format % (item[0], "|", item[1]))
    print("---End of Search Results---")


def search_by_Publisher(published_by):
    results = book_dao.findByPublisher(published_by)
    print("Search by Publisher:")
    s_format = "%-10s %-1s %-50s %-1s %-50s"
    print(s_format % ("ISBN:", "|", "Title:", "|", "Publisher:"))
    if len(results) == 0:
        print("N/A")
    else:
        for item in results:
            print(s_format % (item[0], "|", item[1], "|", item[3]))
    print("---End of Search Results---")


def search_by_Price(p1, p2):
    results = book_dao.findByPrice(p1, p2)
    print("Search by Price:")
    s_format = "%-10s %-1s %-50s %-1s %-50s"
    print(s_format % ("ISBN:", "|", "Title:", "|", "Price"))
    if len(results) == 0:
        print("N/A")
    else:
        for item in results:
            print(s_format % (item[0], "|", item[1], "|", item[5]))
    print("---End of Search Results---")


def search_by_Year(year):
    results = book_dao.findByYear(year)
    print("Search by Year:")
    s_format = "%-10s %-1s %-50s %-1s %-50s"
    print(s_format % ("ISBN:", "|", "Title:", "|", "Year"))
    if len(results) == 0:
        print("N/A")
    else:
        for item in results:
            print(s_format % (item[0], "|", item[1], "|", item[2]))
    print("---End of Search Results---")


def search_by_TP(title, pub):
    results = book_dao.findByTitlePub(title, pub)
    print("Search by Title and Publisher:")
    s_format = "%-10s %-1s %-50s %-1s %-50s"
    print(s_format % ("ISBN:", "|", "Title:", "|", "Publisher"))
    if len(results) == 0:
        print("N/A")
    else:
        for item in results:
            print(s_format % (item[0], "|", item[1], "|", item[3]))
    print("---End of Search Results---")


def print_menu():
    print()
    print("Please make a selection")
    for key in menu_options.keys():
        print (str(key)+'.', menu_options[key], end = "  ")
    print()
    print("The end of top-level options")
    print()


# print search sub-menu
def print_menu2():
    print()
    print("Please make a selection")
    for key in search_menu_options.keys():
        print (str(key)+'.', search_menu_options[key], end = "  ")
    print()
    print("The end of options")
    print()


# ADD a new publisher
def option1():
    print()
    print("-------Add Publisher-------")
    name = input("Enter Name: ")
    phone = ""
    while phone == "":
        phone = input("Enter Phone: ")
        if len(phone) != 10:
            phone = ""
            print("Error: Phone number length must be 10!")
        try:
            int(phone)
        except ValueError:
            phone = ""
            print("Error: Phone number must consist of integers!")
    city = ""
    while city == "":
        city = input("Enter City: ")
        if len(city) > 20:
            city = ""
            print("Error: City name too long (max 20 characters)!")
    result = book_dao.addPublisher(name, phone, city)
    print(result)

# ADD a new book
def option2():
    print()
    print("-------Add Book-------")
    print("Enter NULL for publisher or previous edition if no entry")
    ISBN = ""
    while ISBN == "":
        ISBN = input("Enter ISBN: ")
        if len(ISBN) != 10:
            ISBN = ""
            print("Error: ISBN must be 10 characters!")
    title = ""
    while title == "":
        title = input("Enter Title: ")
        if len(title) > 50:
            title = ""
            print("Error: Title name too long (max 50 characters)!")
    year = ""
    while year == "":
        year = input("Enter Year: ")
        if len(year) != 4:
            year = ""
            print("Error: Year number length must be 4!")
        try:
            int(year)
        except ValueError:
            year = ""
            print("Error: Year number must consist of integers!")
    pub = ""
    while pub == "":
        pub = input("Enter Publisher: ")
        if len(pub) > 25:
            if(pub != "NULL"):
                if(pub != 'null'):
                    pub = ""
                    print("Error: Publisher name too long (max 25 characters)!")
    prev = ""
    while prev == "":
        prev = input("Enter Previous edition: ")
        if len(prev) != 10:
            if(prev != 'NULL'):
                if(prev != 'null'):
                    prev = ""
                    print("Error: Previous edition must be length 10!")
    price = ""
    while price == "":
        price = input("Enter Price: ")
        try:
            float(price)
        except ValueError:
            price = ""
            print("Error: Price number must consist of integers!")
    result = book_dao.addBook(ISBN, title, year, pub, prev, price)
    print(result)

# EDIT an existing book
# user can choose which attribute to edit from numbered options
# separate function for editing publisher because of foreign key
# cannot edit ISBN because it is the primary key
def option3():
    print()
    print("-------Edit Book-------")
    ISBN = ""
    while ISBN == "":
        ISBN = input("Enter ISBN of the book to edit: ")
        if len(ISBN) != 10:
            ISBN = ""
            print("Error: ISBN must be 10 characters!")
    print("Options: (1) title (2) year (3) publisher (4) previous edition (5) price")
    opt = ""
    while opt == "":
        opt = input("Enter which attribute to edit: ")
        try:
            opt = int(opt)
        except ValueError:
            opt = ""
            print("Must select valid option number")
        if opt > 5 or opt < 1:
            opt = ""
            print("Must select valid option number")
    if opt == 1:
        op = 'title'
    elif opt == 2:
        op = 'year'
    elif opt == 3:
        op = 'published_by'
    elif opt == 4:
        op = 'previous_edition'
    else:
        op = 'price'
    val = input("Enter new value: ")
    if opt == 3:
        result = book_dao.editBookPub(ISBN, op, val)
    else:
        result = book_dao.editBook(ISBN, op, val)
    print(result)


# DELETE an existing book
def option4():
    print()
    print("-------Delete Book-------")
    ISBN = ""
    while ISBN == "":
        ISBN = input("Enter ISBN of the book to delete: ")
        if len(ISBN) != 10:
            ISBN = ""
            print("Error: ISBN must be 10 characters!")
    result = book_dao.deleteBook(ISBN)
    print(result)


# Search book based on criteria option
def option5():
    print_menu2()
    option = ""
    while option == "":
        try:
            option = int(input('Enter your choice: '))
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        except:
            print('Wrong input. Please enter a number ...')
            option = ""

    # Check what choice was entered and act accordingly
    if option == 1:
        print("Search Option 1: all books were chosen.")
        search_all_books()
    elif option == 2:
        title = ""
        while title == "":
            title = input("Search option 2: Enter Title: ")
            if len(title) > 50:
                title = ""
                print("Error: Title name too long (max 50 characters)!")
        search_by_title(title)
    elif option == 3:
        ISBN = ""
        while ISBN == "":
            ISBN = input("Search Option 3: Enter ISBN: ")
            if len(ISBN) != 10:
                ISBN = ""
                print("Error: ISBN must be 10 characters!")
        search_by_ISBN(ISBN)
    elif option == 4:
        pub = ""
        while pub == "":
            pub = input("Search option 4: Enter Publisher: ")
            if len(pub) > 25:
                pub = ""
                print("Error: Publisher name too long (max 25 characters)!")
        search_by_Publisher(pub)
    elif option == 5:
        year = ""
        while year == "":
            year = input("Search option 5: Enter year: ")
            if len(year) != 4:
                year = ""
                print("Error: invalid year")
            try:
                y = int(year)
            except ValueError:
                year = ""
                print("Error: Year number must consist of integers!")
        search_by_Year(year)
    elif option == 6:
        p1 = ""
        while p1 == "":
            p1 = input("Search Option 6: Enter lowest price: ")
            try:
                int(p1)
            except ValueError:
                p1 = ""
                print("Error: Price number must consist of integers!")
        p2 = ""
        while p2 == "":
            p2 = input("Search Option 6: Enter highest price: ")
            try:
                int(p2)
            except ValueError:
                p2 = ""
                print("Error: Price number must consist of integers!")
        search_by_Price(p1, p2)
    elif option == 7:
        title = ""
        while title == "":
            title = input("Search option 7: Enter Title: ")
            if len(title) > 50:
                title = ""
                print("Error: Title name too long (max 50 characters)!")
        pub = ""
        while pub == "":
            pub = input("Search option 7: Enter Publisher: ")
            if len(pub) > 25:
                pub = ""
                print("Error: Publisher name too long (max 25 characters)!")
        search_by_TP(title, pub)
    else:
        print('Invalid option. Please enter a number between 1 and 7.')



if __name__=='__main__':
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except KeyboardInterrupt:
            print('Interrupted')
            sys.exit(0)
        except:
            print('Wrong input. Please enter a number ...')

        # Check what choice was entered and act accordingly
        if option == 1:
           option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            option5()
        elif option == 6:
            print('Thanks your for using our database services! Bye')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 6.')











