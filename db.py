import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


class Users(SqlAlchemyBase):
    __tablename__ = 'users'

    tg_id = sqlalchemy.Column(sqlalchemy.String,
                              primary_key=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    period_name = sqlalchemy.Column(sqlalchemy.String)
    period_amount = sqlalchemy.Column(sqlalchemy.Integer)
    cookie = sqlalchemy.Column(sqlalchemy.String)


class Lessons(SqlAlchemyBase):
    __tablename__ = 'lessons'
    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    owner_tg_id = sqlalchemy.Column(sqlalchemy.String)
    lesson_name = sqlalchemy.Column(sqlalchemy.String)
    middle = sqlalchemy.Column(sqlalchemy.String)
    final = sqlalchemy.Column(sqlalchemy.String)
    marks = sqlalchemy.Column(sqlalchemy.String)

