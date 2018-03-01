from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import MetaData 

db = SQLAlchemy()


def truncate_all(db):
    # delete all table data (but keep tables)
    # we do cleanup before test 'cause if previous test errored,
    # DB can contain dust
    meta = MetaData(bind=db.engine, reflect=True)
    con = db.engine.connect()
    trans = con.begin()
    con.execute('PRAGMA foreign_keys = OFF;')
    for table in meta.sorted_tables:
        con.execute(table.delete())
    con.execute('PRAGMA foreign_keys = ON;')
    trans.commit()

