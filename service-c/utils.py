import mysql.connector

def store_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="username",
        password="password"
    )
    cursor = mydb.cursor()
    cursor.execute("CREATE DATABASE mydatabase")

    cursor.execute("""CREATE TABLE IF NOT EXISTS weather_records (
                       id INT, PRIMARY_KEY, AUTO_INCREMENT, 
                       timestamp DATETIME, 
                       location_name VARCHAR, 
                       country VARCHAR, 
                       latitude FLOAT, "
                       longitude FLOAT, "
                       temperature FLOAT, "
                       wind_speed FLOAT, "
                       humidity INT, "
                       temperature_category VARCHAR, "
                       wind_category VARCHAR)
                       """)

    values = [
        ('Peter', 'Lowstreet 4'),
        ('Amy', 'Apple st 652'),
        ('Hannah', 'Mountain 21'),
        ('Michael', 'Valley 345'),
        ('Sandy', 'Ocean blvd 2'),
        ('Betty', 'Green Grass 1'),
        ('Richard', 'Sky st 331'),
        ('Susan', 'One way 98'),
        ('Vicky', 'Yellow Garden 2'),
        ('Ben', 'Park Lane 38'),
        ('William', 'Central st 954'),
        ('Chuck', 'Main Road 989'),
        ('Viola', 'Sideway 1633')
    ]

    cursor.executemany("INSERT INTO customers (name, address) VALUES (%s, %s)", values)

    mydb.commit()
