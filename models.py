from sqlalchemy import Column, Integer, String
from db import Base, engine

class Logpass(Base):
    __tablename__ = 'logpasses'
    id = Column(Integer, primary_key=True)
    logpass = Column(String, nullable=False)

    def __repr__(self):
        return f'Name {self.id} - {self.logpass}'


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
