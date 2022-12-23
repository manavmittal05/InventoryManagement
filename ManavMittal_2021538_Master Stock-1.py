import mysql.connector
from tabulate import tabulate
import getpass

def login():
    # This function is for establishing connection
    # between python and mysql database by taking
    # input of user id and password and host name
    # then it take the input of database from the
    # user and if the database exits it will select
    # it for further queries else it will create one
    # and use it.
    try:
        global app_cursor
        global connection

        connection = mysql.connector.connect(user=input('Username: '),
                                             password=input('Password: '), host=input('Host: '))
        app_cursor = connection.cursor(buffered=True)
        app_cursor.execute("show databases")
        app_database = input('Database: ')
        database_selected = False

        for i in app_cursor.fetchall():

            for j in i:

                if app_database == j:
                    app_cursor.execute("use %s" % app_database)
                    print('\n', app_database, " is now the selected database.", '\n')
                    database_selected = True
                    break

        if database_selected is False:
            app_cursor.execute("create database %s" % app_database)
            app_cursor.execute("use %s" % app_database)
            print('\n', app_database, " is now the selected database.", '\n')

        table_menu()

    except mysql.connector.errors.ProgrammingError:

        print("\nEnter valid Username and Password!!\n")
        login()

    except mysql.connector.errors.InterfaceError:
        print("\nEnter valid Host name.\n")
        login()

    except mysql.connector.errors.DatabaseError:
        print("\nSomething went wrong try again.\n")
        login()


def table_menu():
    # This function gives the user the menu for operation
    # this is the main menu there is another menu for performing
    # operations on the table and it will be triggered on users demand.

    print('''To perform given functions enter the numerical value\nassigned to the function:-\n
    1 => Create Table.
    2 => Perform Operations on Table.
    3 => To check Stock Tables in the selected Database.
    4 => Delete table.
    5 => Logout and exit.
    
Note:- To terminate any operation you selected by 
       mistake enter '?' symbol it will take you back
       to the menu.

    ''')

    try:

        def table_menu_functions(a):
            if a == 1:
                # This set of code will be executed when user wants to create table.
                # By taking a string input for table name.
                # If the table of given name already exists in the selected database,
                # the function will be again called with parameter 1
                name = str(input("Enter table Name: "))
                if name == '?':
                    table_menu()
                else:
                    try:
                        app_cursor.execute('''Create table %s(
                            Id varchar (255) not null primary key,
                            Name varchar(255) not null,
                            Category varchar(255) not null,
                            Price int,
                            Stock int)''' % name)
                        print("Table Created successfully.\n")
                        connection.commit()
                        table_menu()
                    except mysql.connector.errors.ProgrammingError:
                        print("Table of this name already exists")
                        table_menu_functions(1)
            elif a == 4:
                # This set of code if for choice 4 that is for is for deleting table from selected database.
                # By taking a string input and further asking for confirmation for deleting the table.
                # If table not exists in the database then the exception is handled in except block.
                name = str(input("Enter table Name: "))
                try:
                    if name == '?':
                        table_menu()
                    else:
                        confirmation = str(input("Are you sure you want to delete the above table (y/n): "))
                        confirmation.lower()
                        if confirmation == 'y':
                            app_cursor.execute("Drop table %s" % name)
                            print("Table %s is deleted permanently.\n" % name)
                            connection.commit()
                            table_menu()
                        elif confirmation == 'n':
                            print("Table %s is not deleted\n." % name)
                            table_menu()
                except mysql.connector.errors.ProgrammingError:
                    print("Table of this name do not exist\n.")
                    table_menu()
            elif a == 5:
                # This set of code is choice 5 that is Save and exit application.
                # Its saves all the query processed and closes the connection and cursor.
                # After that it leave a vague input statement to prevent to sudden close of console window.
                import sys
                connection.commit()
                app_cursor.close()
                connection.close()
                input("Press any key to exit..")
                sys.exit()
            elif a == 3:
                # This set of code is choice 3 that is to print the list of stock tables in the selected database.
                # It print the list in a Table format with the help of Tabulate function of Tabulate module.
                app_cursor.execute("Show tables")
                data = app_cursor.fetchall()
                tables = []
                for i in data:
                    tables.append(i)
                print("\n", tabulate(tables, headers=['Names'], tablefmt='psql'), "\n")
                table_menu()
            elif a == 2:
                # This set of code is for performing operations on the table.
                # By taking input of the table name on which user wants to perform functions.
                # It checks whether the given table name exists in the database or not.
                # If exists it triggers the function function_menu(args: Table name).
                # If not exists it will ask again for input.
                name = str(input("Enter table Name: "))
                if name == '?':
                    table_menu()
                else:
                    app_cursor.execute("show tables")
                    existance = False
                    for i in app_cursor:
                        for j in i:
                            if j == name:
                                existance = True
                                break
                            else:
                                continue
                    if existance is True:
                        function_menu(name)
                    else:
                        print("\nEnter valid table name. This table does not exist in the current database.\n")
                        choice = int(input("To go back to main menu enter 1 and To re-enter the table name enter 2."
                                           "(1/2)"))
                        if choice == 1:
                            table_menu()
                        elif choice == 2:
                            table_menu_functions(2)
                        else:
                            print("Invalid input directing back to main menu.")
                            table_menu()

            else:
                # If users enter anything other than listed in menu then this code will be executed.
                # It again asks for the input from the user.
                print("Enter Number from The menu only.")
                choice = int(input("Your Choice: "))
                table_menu_functions(choice)
        table_menu_choice = int(input("Your Choice: "))
        table_menu_functions(table_menu_choice)

    except ValueError:
        # If user enter anything other than integer.
        print("Enter valid input.")
        table_menu()


def function_menu(name):
    #This function is for editing table
    # For tasks like Adding item to table, deleting item from table and updating item stock
    global headers
    headers = ['Id', 'Name', 'Category', 'Price', 'Stock']
    name = name
    print('''To perform given functions enter the numerical value\nassigned to the function:-\n
    1 => To print The Stock Table.
    2 => To add a product to stock table.
    3 => To delete a product from the stock table.
    4 => To Perform operations on a product.
    5 => To export data of table to excel file.
    6 => To go back to previous menu.
    
    Note:- To terminate any operation you selected by 
           mistake enter '?' symbol it will take you back
           to the menu.''')

    try:
        choice = int(input("Your choice: "))
        if choice == 1:
            app_cursor.execute("Select * from %s" % name)
            data = []
            for i in app_cursor:
                data.append(i)
            print(tabulate(data, headers=headers, tablefmt='psql'))
            function_menu(name)
        if choice == 2:
            while True:
                try:
                    p_id = input("Enter the Product ID: ")
                    if p_id == '?':
                        table_menu()
                        break
                    else:
                        break
                except ValueError:
                    print("Enter valid input.")
            while True:
                try:
                    p_name = input("Enter the Product Name: ")
                    if p_name == '?':
                        table_menu()
                    else:
                        break
                except ValueError:
                    print("Enter valid input.")
            while True:
                try:
                    p_category = input("Enter the Product Category: ")
                    if p_category == '?':
                        table_menu()
                    else:
                        break
                except ValueError:
                    print("Enter valid input.")
            while True:
                try:
                    p_price = int(input("Enter the Product Price: "))
                    break
                except ValueError:
                    print("Enter valid input.")
            while True:
                try:
                    p_quantity = int(input("Enter the Product stock: "))
                    break
                except ValueError:
                    print("Enter valid input.")

            app_cursor.execute("insert into %s values('%s','%s','%s',%d,%d)"
                               % (name, p_id, p_name, p_category, p_price, p_quantity))
            connection.commit()
            function_menu(name)

        elif choice == 3:
            p_id = input("Enter the Product ID of the product you want to delete: ")
            app_cursor.execute("select * from %s where Id='%s'" % (name, p_id))
            data = []
            for i in app_cursor:
                data.append(i)
            print(tabulate(data, headers=headers, tablefmt='psql'))
            while True:
                conf = input("Are you sure you want to this product (y/n): ")
                if conf == 'y':
                    app_cursor.execute("delete from %s where Id='%s'" % (name, p_id))
                    connection.commit()
                    break
                elif conf == 'n':
                    function_menu(name)
                    break
                else:
                    print("Enter valid input.")
            function_menu(name)
        elif choice == 6:
            table_menu()

        elif choice == 4:
            product_update(name)

        elif choice == 5:
            import xlsxwriter
            q = 0
            while q < 1:
                try:
                    filename = input("Enter file name: ")
                    print("File will be saved on the desktop")
                    workbook = xlsxwriter.Workbook("D:\\%s.xlsx" % filename)
                    worksheet = workbook.add_worksheet()
                    worksheet.write(0, 0, "ID")
                    worksheet.write(0, 1, "NAME")
                    worksheet.write(0, 2, "CATEGORY")
                    worksheet.write(0, 3, "PRICE")
                    worksheet.write(0, 4, "STOCK")
                    app_cursor.execute("SELECT * FROM %s" % name)
                    data = app_cursor.fetchall()
                    row = 1
                    coloumn = 0
                    for (a, b, c, d, e) in data:
                        worksheet.write(row, coloumn, a)
                        worksheet.write(row, coloumn + 1, b)
                        worksheet.write(row, coloumn + 2, c)
                        worksheet.write(row, coloumn + 3, d)
                        worksheet.write(row, coloumn + 4, e)
                        row = row + 1
                    workbook.close()
                    print("Data exported successfully to %s at D drive" % filename)
                    break
                except:
                    print("A file of this name already exists use a different name")
            function_menu(name)
    except ValueError:
        print("Enter valid input.")
        function_menu(name)


def product_update(name):
    name = name
    print('''To perform given functions enter the numerical value\nassigned to the function:-\n
        1 => To update stock of product.
        2 => To update name of product.
        3 => To update price of product.
        4 => To change category of product.
        5 => To go back to previous menu.
    
    Note:- To terminate any operation you selected by 
           mistake enter '?' symbol it will take you back
           to the menu.''')
    try:
        choice = int(input("Your choice: "))
        if choice == 2:
            name_p = str(input("Enter the name of the product: "))
            if name_p == '?':
                product_update(name)
            else:
                app_cursor.execute("select * from %s where Name='%s'" % (name, name_p))
                data = []
                for i in app_cursor:
                    data.append(i)
                print(tabulate(data, headers=headers, tablefmt='psql'))
                id_p = str(input("Enter the product id of product you want to change name: "))
                name_new = str(input("Enter the new name of the product: "))
                if name_new == '?' or id_p == '?':
                    product_update(name)
                    connection.commit()
                else:
                    app_cursor.execute("update %s set Name='%s' where Id='%s'" % (name, name_new, id_p))
                    print("Product name updated successfully.")
                    product_update(name)
        elif choice == 1:
            name_p = str(input("Enter the name of the product: "))
            if name_p == '?':
                product_update(name)
            else:
                app_cursor.execute("select * from %s where Name='%s'" % (name, name_p))
                data = []
                for i in app_cursor:
                    data.append(i)
                print(tabulate(data, headers=headers, tablefmt='psql'))
                id_p = str(input("Enter the product id of product you want to change stock: "))
                stock_new = int(input("New stock of the product: "))
                if id_p == '?':
                    product_update(name)
                else:
                    app_cursor.execute("update %s set Stock=%d where Id='%s'" % (name, stock_new, id_p))
                    print("Product Stock updated successfully.")
                    connection.commit()
                    product_update(name)
        elif choice == 5:
            function_menu(name)
        elif choice == 3:
            name_p = str(input("Enter the name of the product: "))
            if name_p == '?':
                product_update(name)
            else:
                app_cursor.execute("select * from %s where Name='%s'" % (name, name_p))
                data = []
                for i in app_cursor:
                    data.append(i)
                print(tabulate(data, headers=headers, tablefmt='psql'))
                id_p = str(input("Enter the product id of product you want to change price: "))
                price_new = int(input("New price of the product: "))
                if id_p == '?':
                    product_update(name)
                else:
                    app_cursor.execute("update %s set Price=%d where Id='%s'" % (name, price_new, id_p))
                    print("Product Price updated successfully.")
                    connection.commit()
                    product_update(name)
        elif choice == 4:
            name_p = str(input("Enter the name of the product: "))
            if name_p == '?':
                product_update(name)
            else:
                app_cursor.execute("select * from %s where Name='%s'" % (name, name_p))
                data = []
                for i in app_cursor:
                    data.append(i)
                print(tabulate(data, headers=headers, tablefmt='psql'))
                id_p = str(input("Enter the product id of product you want to change category: "))
                category_new = str(input("New Category of the product: "))
                if id_p == '?':
                    product_update(name)
                else:
                    app_cursor.execute("update %s set Category='%s' where Id='%s'" % (name, category_new, id_p))
                    print("Product Category updated successfully.")
                    connection.commit()
                    product_update(name)

    except ValueError:
        print("Enter valid input.")
        product_update(name)


login()
