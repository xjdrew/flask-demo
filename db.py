from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine('mysql://localhost/test?charset=utf8', encoding='utf-8', convert_unicode = False)

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))

class Server(Base):
    __tablename__ = 'server'
    __table_args__ = {  
        'mysql_engine': 'InnoDB',  
        'mysql_charset': 'utf8'  
    } 

    id = Column(Integer, primary_key = True)
    name = Column(String(40), primary_key = True)
    ip   = Column(String(40))

    def __init__(self, name, ip):
        self.name = name
        self.ip   = ip

    def __str__(self):
        return "<Server ('%s', '%s')>" % (self.name.encode('utf8'), self.ip.encode('utf-8'))

    def __repr__(self):
        return "<Server ('%s', '%s')>" % (self.name, self.ip)

def init_db(filename):
    Base.metadata.create_all(engine)

    f = open(filename, 'r')
    for l in f.readlines():
        l = l.rstrip()
        name, ip = l.split(' ')
        server = Server(name, ip)
        db_session.add(server)
    db_session.commit()

if __name__ == '__main__':
    init_db('server_list.txt')
    s = db_session.query(Server).first()
    print(unicode(s))


