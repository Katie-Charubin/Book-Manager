from mysql_connector import connection
import mysql.connector

# returns all tuples in Book
def findAll():
    cursor = connection.cursor()
    query = "select * from bookmanager.Book"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


# returns all tuples in Book with specified title attribute
def findByTitle(title):
    cursor = connection.cursor()
    query = "select * from bookmanager.Book where Book.title='" + title + "' order by ISBN"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


# returns all tuples in Book with specified ISBN attribute
def findByISBN(ISBN):
    cursor = connection.cursor()
    query = "select * from bookmanager.Book where Book.ISBN='" + ISBN + "'"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


# returns all tuples in Book with specified publisher attribute
def findByPublisher(publisher):
    cursor = connection.cursor()
    query = "select * from bookmanager.Book where Book.published_by='" + publisher + "' order by title"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# returns all tuples in Book with specified price range
def findByPrice(low, high):
    cursor = connection.cursor()
    query = "select * from bookmanager.Book where book.price >" + low + " and book.price <" + high + " order by price"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# returns all tuples in Book with specified year attribute
def findByYear(year):
    cursor = connection.cursor()
    query = "select * from bookmanager.Book where Book.year='" + year + "' order by ISBN"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# returns all tuples in Book with specified title and publisher
def findByTitlePub(title, pub):
    cursor = connection.cursor()
    query = "select * from bookmanager.Book where Book.published_by='" + pub + "' and Book.title ='" + title +"' order by title"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results


# inserts a tuple into Publisher
# returns error if duplicate entry
def addPublisher(name, phone, city):
    cursor = connection.cursor()
    query = "insert into Publisher values('" + name + "', '" + phone + "', '" + city + "')"
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.errors.IntegrityError:
        cursor.close()
        return "Duplicate entry: publisher <" + name + "> already exists!"
    cursor.close()
    return "Publisher <" + name + "> added successfully"


# inserts a tuple into Book
# if publisher doesn't exist, new tuple added to publisher
# if previous edition book doesn't exist, returns an error
def addBook(ISBN, title, year, published_by, prev, price):
    curs = connection.cursor()
    p = "select * from Publisher where Publisher.name='" + published_by + "'"
    curs.execute(p)
    pubExists = curs.fetchall()
    connection.commit()
    curs.close()
    if len(pubExists) == 0:
        addPublisher(published_by, 'NULL', 'NULL')
    cursor = connection.cursor()
    if(published_by == 'NULL' and prev == 'NULL') or (published_by == 'null' and prev == 'null'):
        query = "insert into Book values('" + ISBN + "', '" + title + "', '" + year + "', " + published_by + ", " + prev + ", '" + price +"')"
    elif(published_by == 'NULL') or (published_by == 'null'):
        query = "insert into Book values('" + ISBN + "', '" + title + "', '" + year + "', " + published_by + ", '" + prev + "', '" + price +"')"
    elif(prev == 'NULL') or (prev == 'null'):
        query = "insert into Book values('" + ISBN + "', '" + title + "', '" + year + "', '" + published_by + "', " + prev + ", '" + price +"')"
    else:
        query = "insert into Book values('" + ISBN + "', '" + title + "', '" + year + "', '" + published_by + "', '" + prev + "', '" + price +"')"
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.errors.Error:
        cursor.close()
        return "Previous edition must exist!"
    except mysql.connector.errors.IntegrityError:
        cursor.close()
        return "Duplicate entry: publisher <" + ISBN + "> already exists!"
    cursor.close()
    return "Book <" + ISBN + "> added successfully"


# delete a tuple from Book
# if book is referenced as a foreign key, its reference is set to null
def deleteBook(ISBN):
    curs = connection.cursor()
    q = "update Book set Book.previous_edition= NULL where Book.previous_edition= '" + ISBN + "'"
    curs.execute(q)
    connection.commit()
    curs.close()
    cursor = connection.cursor()
    query = "delete from Book where ISBN='" + ISBN + "'"
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.errors.Error:
        cursor.close()
        return "Book doesn't exist"
    cursor.close()
    return "Book <" + ISBN + "> deleted successfully"


# edit a tuple in Book
# user chooses which attribute to edit
def editBook(ISBN, val, new):
    cursor = connection.cursor()
    query = "update Book set " + val + "= '" + new + "' where book.ISBN ='" + ISBN + "'"
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.errors.Error:
        cursor.close()
        return "Book doesn't exist"
    cursor.close()
    return val + " in book <" + ISBN + "> udated to <" + new + "> successfully"


# edit publisher attribute
# if publisher doesn't exist, new publisher added
def editBookPub(ISBN, val, new):
    cursor = connection.cursor()
    query = "update Book set " + val + "= '" + new + "' where book.ISBN ='" + ISBN + "'"
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.errors.Error:
        curs = connection.cursor()
        q = "select * from Publisher where name ='" + new + "'"
        curs.execute(q)
        pubs = curs.fetchall()
        connection.commit()
        curs.close()
        if (len(pubs) > 0):
            cursor.close()
            return "Book doesn't exist"
        else:
            addPublisher(new, "NULL", "NULL")
            editBookPub(ISBN, val, new)
    cursor.close()
    return val + " in book <" + ISBN + "> udated to <" + new + "> successfully"





