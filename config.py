DB = {
    'driver': 'postgresql+psycopg2',
    'user': 'gis_user',
    'pass': 'gis_pass',
    'host': 'localhost',
    'port': 5432,
    'db': 'nyc_bis'
}

def db_url():
    return f"{DB['driver']}://{DB['user']}:{DB['pass']}@{DB['host']}:{DB['port']}/{DB['db']}"