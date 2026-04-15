# Prerequisite Packages
# mysql connector
# pillow
# pandas
# tabulate

# Importing required modules
import mysql.connector
import base64
from PIL import Image
import io
import pandas
from datetime import datetime
from datetime import date
from tabulate import tabulate
import random

# Creating a connection
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password='#devnathmysql', # Review
	
)

# Creating a cursor object
cursor = mydb.cursor()

# Creating Required Database and Tables
cursor.execute("create database if not exists artgallary;")
cursor.execute("use artgallary")
# Artwork+
cursor.execute("create table if not exists artwork"
                +"("
                +"ArtID int not null auto_increment,"
                +"Artwork_Name varchar(30),"
                +"Artist_Name varchar(30),"
                +"Price int,"
                +"Currency varchar(30),"
                +"Status varchar(30),"
                +"Img longblob,"
                +"primary key(ArtID)"
                +");"
            )

#Visitor
cursor.execute(
    "create table if not exists visitor"
    +"("
    +"Name varchar(30),"
    +"Phone_No int,"
    +"Email varchar(30),"
    +"Date date,"
    +"Time varchar(30)"
    +");"
)

#Customer
cursor.execute(
    "create table if not exists customer"
    +"("
    +"Name varchar(30),"
    +"Phone_No varchar(30),"
    +"Email varchar(30),"
    +"Password varchar(30)"
    +");"
)

#Orders
cursor.execute(
    "create table if not exists orders"
    +"("
    +"Name varchar(30),"
    +"Phone_No varchar(30),"
    +"Email_ID varchar(30),"
    +"Address varchar(60),"
    +"Artwork_Name varchar(30),"
    +"Artist_Name varchar(30),"
    +"Price int,"
    +"Date date,"
    +"Time varchar(30)"
    +");"
)

# Inserting Sample Data into table artwork
cursor.execute("select ArtID,Artwork_Name,Artist_Name,Price,Currency,Status from artwork")
res = cursor.fetchall()
if res ==[]:
    cursor.execute(
        "insert into artwork (ArtID,Artwork_Name,Artist_Name,Price,Currency,Status) values"
        +"(1,'Mona Lisa','Leonardo Da Vinci', NULL, NULL, 'Not For Sale'),"
        +"(2,'Modern Art','Madam Lal',4500,'INR','Available For Sale'),"
        +"(3,'Lord Shiva','Aarthi Miller',26699,'INR','Available For Sale'),"
        +"(4,'Nreet Blue','Kara Seruda',5000,'INR','Available For Sale'),"
        +"(5,'The Soul Of Dandia','Hana Malvika',9999,'INR','Available For Sale'),"
        +"(6,'Ancient Era','Endward Salvatore',4500,'INR','Available For Sale'),"
        +"(7,'Poylaamo Scenery','Stefan Chritoff',10000,'INR','Available For Sale'),"
        +"(8,'Summer Mood','Ozge Yagiz',8999,'INR','Available For Sale'),"
        +"(9,'The Golden Tree','Margot Esme',15590,'INR','Available For Sale'),"
        +"(10,'Dancing To His Tune','Mira Sen',4999,'INR','Available For Sale');"
        )
    
    mydb.commit()

# CREATING FUNCTIONS
def Add():
    art_id      = int(input("Enter ArtID : "))
    name_art    = input("Enter name of Artwork : ")
    name_artist = input("Enter name of Artist : ")
    price       = int(input("Enter Price of Artwork : "))
    currency    = input("Enter Currency of Price : ")
    status      = input("Enter status of artwork. For/Not For Sale : ")

    pic = input("Enter image location. Type NULL to skip this prompt : ") #Review

    if pic == 'NULL':
        # data to be inserted
        args = (art_id, name_art, name_artist, price, currency, status)
        # Prepare a query
        query = 'insert into artwork (ArtID,Artwork_Name,Artist_Name,Price,Currency,Status) values(%s,%s,%s,%s,%s,%s)'
        # Execute the query and commit the database.
        cursor.execute(query,args)
        mydb.commit()    
        print("Entry Successfull.\n")

    else:
        # Open a file in binary mode
        file = open(pic,'rb').read() 
        # encode the file to get base64 string
        file = base64.b64encode(file)   
        # data to be inserted
        args = (art_id, name_art, name_artist, price, currency, status, file)
        # Prepare a query
        query = 'insert into artwork values (%s,%s,%s,%s,%s,%s,%s)'
        # Execute the query and commit the database.
        cursor.execute(query,args)
        mydb.commit()
        print("Entry Successfull.\n")


def InsertImage():
    art_id  = input("Enter ArtID : ")
    pic     = input("Enter image location : ")

    cursor.execute("select ArtID,Artwork_Name,Artist_Name,Price,Currency,Status from artwork where ArtID ="+art_id)
    data = cursor.fetchall()

    art_name    = data[0][1]
    artist_name = data[0][2]
    price       = data[0][3]
    curr        = data[0][4]
    status      = data[0][5]

    cursor.execute("delete from artwork where ArtID ="+art_id)
    
    # Open a file in binary mode
    file = open(pic,'rb').read() 
    # encode the file to get base64 string
    file = base64.b64encode(file)   
    # data to be inserted
    args = (art_id, art_name, artist_name, price, curr, status, file)
    # Prepare a query
    query = 'insert into artwork values (%s,%s,%s,%s,%s,%s,%s)'
    # Execute the query and commit the database.
    cursor.execute(query,args)
    mydb.commit()
    print("Entry Successfull.\n")


def Display():
    cursor.execute("select ArtID,Artwork_Name,Artist_Name,Price,Currency,Status from artwork")
    data = cursor.fetchall()
    print(pandas.DataFrame(
        data,columns=['  Art ID','  Artwork Name','   Artist Name','  Price','  Currency','  Status']
        ),"\n")

    while True:
        ch = input('View Image of an artwork? Y/N : ').upper()
        if ch == 'Y':

            id = input("Enter ArtID to show artwork : ")
            # Prepare the query
            query = 'SELECT Img FROM artwork WHERE ArtID='+id
            # Execute the query to get the file
            cursor.execute(query)
            data = cursor.fetchall()
            
            if data == [(None,)]:
                print("\nRecord Contains No Image.\n")
            else:
                # The returned data will be a list of list
                image = data[0][0]
                # Decode the string
                binary_data = base64.b64decode(image)
                # Convert the bytes into a PIL image
                image = Image.open(io.BytesIO(binary_data))
                # Display the image
                image.show()
        else:
            print("")
            break
#Review For Image

def UpdatePrice():
    art_id = input("Enter ArtID : ")
    nprice = input("Enter New Price of artwork : ")

    cursor.execute("update artwork set Price = "+nprice+" where ArtID = "+art_id)
    mydb.commit()

    print("Price Updated...\n")

    cursor.execute("select ArtID,Artwork_Name,Artist_Name,Price,Currency,Status from artwork where ArtID = "+art_id)
    data = cursor.fetchall()
    print(pandas.DataFrame(
        data,columns=['  Art ID','  Artwork Name','   Artist Name','  Price','  Currency','  Status']
        ),"\n")

def UpdateStatus():
    art_id = input("Enter ArtID : ")
    nstatus = input("Enter New Status of artwork. For/Not For Sale/Sold : ")

    cursor.execute("update artwork set Status = '"+nstatus+"' where ArtID = "+art_id)
    mydb.commit()

    print("Status Updated...\n")
    
    cursor.execute("select ArtID,Artwork_Name,Artist_Name,Price,Currency,Status from artwork where ArtID = "+art_id)
    data = cursor.fetchall()
    print(pandas.DataFrame(
        data,columns=['  Art ID','  Artwork Name','   Artist Name','  Price','  Currency','  Status']
        ),"\n")

def EditArtworkName():
    art_id    = input("Enter ArtID : ")
    name_art  = input("Rename Artwork : ")

    cursor.execute("update artwork set Artwork_Name = '"+name_art+"' where ArtID = "+art_id)
    mydb.commit()

    print("Artwork Name Updated...\n")
    
    cursor.execute("select ArtID,Artwork_Name,Artist_Name,Price,Currency,Status from artwork where ArtID = "+art_id)
    data = cursor.fetchall()
    print(pandas.DataFrame(
        data,columns=['  Art ID','  Artwork Name','   Artist Name','  Price','  Currency','  Status']
        ),"\n")

def EditArtistName():
    art_id      = input("Enter ArtID : ")
    name_artist = input("Rename Artist : ")

    cursor.execute("update artwork set Artist_Name = '"+name_artist+"' where ArtID = "+art_id)
    mydb.commit()

    print("Artwork Name Updated...\n")
    
    cursor.execute("select ArtID,Artwork_Name,Artist_Name,Price,Currency,Status from artwork where ArtID = "+art_id)
    data = cursor.fetchall()
    print(pandas.DataFrame(
        data,columns=['  Art ID','  Artwork Name','   Artist Name','  Price','  Currency','  Status']
        ),"\n")

def Delete():
    art_id = input("Enter ArtID : ")
    cursor.execute("delete from artwork where ArtID ="+art_id)
    print("Record Deleted.\n")


print(
    '''

██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗      █████╗ ██████╗ ████████╗     ██████╗  █████╗ ██╗     ██╗      █████╗ ██████╗ ██╗   ██╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗╚══██╔══╝    ██╔════╝ ██╔══██╗██║     ██║     ██╔══██╗██╔══██╗╚██╗ ██╔╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║    ███████║██████╔╝   ██║       ██║  ███╗███████║██║     ██║     ███████║██████╔╝ ╚████╔╝ 
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║    ██╔══██║██╔══██╗   ██║       ██║   ██║██╔══██║██║     ██║     ██╔══██║██╔══██╗  ╚██╔╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝    ██║  ██║██║  ██║   ██║       ╚██████╔╝██║  ██║███████╗███████╗██║  ██║██║  ██║   ██║   
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                                                                                                                                                                                                                                                    
    '''
    )

ch = ''
while ch != 'N' or ch != 'n':
    print("\nPLEASE CHOOSE\n" 
            "1 FOR ADMIN\n"
            "2 FOR VISITOR\n"
            "3 FOR CUSTOMER\n"
            "4 TO EXIT\n")

    choice = int(input("Enter Your Choice : "))

    if choice == 4:
        break

    if choice == 1:
        admin = input("Enter Username : ")
        password = int(input("Enter Password : "))
        if password == 1234:
            print("\n---------------------------------------\n"
                    "*** Successfully Logged In As Admin ***\n"
                    "---------------------------------------\n"
                    "Press 1 to Add new artwork\n"
                    "Press 2 to Display artworks\n"
                    "Press 3 to Update Price of an artwork\n"
                    "Press 4 to Update Status of an artwork\n"
                    "Press 5 to Edit Name of an artwork\n"
                    "Press 6 to Edit Name of an artist\n"
                    "Press 7 to Insert Image of an artwork\n" 
                    "Press 8 to Delete a Record\n"                   
                    "Press 9 to Exit\n"
                    "---------------------------------------"
                )
            
            while True:
                c = int(input("Enter Your Choice : "))
                print("")

                if c == 1:
                    Add()
                elif c == 2:
                    Display()
                elif c == 3:
                    UpdatePrice()
                elif c == 4:
                    UpdateStatus()
                elif c == 5:
                    EditArtworkName()
                elif c == 6:
                    EditArtistName()
                elif c == 7:
                    InsertImage()
                elif c == 8:
                    Delete()
                elif c == 9:
                    break
                else:
                    print("Invalid Input.")
        else:
            print("\nWrong Password.\n")        

    if choice == 2:
        name  = input("Enter Your Name    : ")
        phno  = input("Enter Phone Number : ")
        email = input("Enter Email ID     : ")
        date1 = date.today()
        time1  = datetime.now().strftime("%H:%M:%S")
        args  = (name, phno, email, date1, time1)
        query = 'insert into visitor values(%s,%s,%s,%s,%s)'
        cursor.execute(query,args)
        mydb.commit()

        print("\nHERE IS THE LIST OF ARTWORKS\n")

        Display()        

    if choice == 3:
        
        print("\n-------------------------------\n"
                "Press 1 to Register yourself\n"
                "Press 2 to Display all artworks\n"
                "Press 3 to Order an artwork\n"
                "Press 4 to Exit\n"
                "-------------------------------\n"
        )

        while True:
            c = int(input("Enter your choice : "))
            print("")

            if c == 4:
                break

            elif c == 1:
                name     = input    ("Enter your name   : ")
                phone    = int(input("Enter your ph no. : "))
                email    = input    ("Enter Email ID    : ")                
                password = input    ("Create a password : ")

                args  = (name, phone, email, password)
                query = 'insert into customer values(%s,%s,%s,%s)'
                cursor.execute(query,args)
                mydb.commit()
                print("Remember your password.\n")

            elif c==2:
                Display()
            elif c==3:
                password = input("Enter your password : ")

                cursor.execute("select Password from customer where Password ="+password)
                mydb.commit()
                data = cursor.fetchall()

                count = 0

                for i in data:    
                    if i[0] == password:

                        count = count + 1

                        cursor.execute("select * from customer where Password ="+password)
                        mydb.commit()
                        data2 = cursor.fetchall()

                        name     = data2[0][0]
                        phone    = data2[0][1]
                        email    = data2[0][2]

                        address  = input("Enter your address : ")
                        art_id = input("Enter ArtID of artwork you want to order : ")

                        cursor.execute("select Artwork_Name,Artist_Name,Price from artwork where ArtID ="+art_id)
                        data3 = cursor.fetchall()

                        art_name    = data3[0][0]
                        artist_name = data3[0][1]
                        price       = data3[0][2]

                        date2 = date.today()
                        time2  = datetime.now().strftime("%H:%M:%S")
                        args  = (name, phone, email, address, art_name, artist_name, price, date2, time2)
                        query = 'insert into orders values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                        cursor.execute(query,args)
                        mydb.commit()

                        # assign data
                        mydata = [
                            [art_name, artist_name, price]
                        ]

                        # create header
                        head = ["Artwork Name", "Artist Name", "Price (INR ₹)"]

                        print("\n"
                            "HI "+name.upper()+"!\n"
                            "THANK YOU FOR YOUR PURCHASE\n\n"
                            "YOUR ORDER INFORMATION\n\n"
                            "Order ID   : "+str(random.randint(1,100000000000))+"\n"
                            "Order Date : "+str(date2)+"\n"
                            "Time       : "+str(time2)+"\n"
                            "Bill To    : "+email +"\n"
                            "Address    : "+address+"\n"
                        )

                        # display table
                        print(tabulate(mydata, headers=head, tablefmt="grid"),'\n')
                                
                    if count == 0:
                        print("Customer Not Registered.")

            else:
                print("Invalid Input.\n")  

    else:
        print("Invalid Input.")              



                

