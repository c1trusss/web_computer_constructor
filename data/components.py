import sqlalchemy

from .db_session import SqlAlchemyBase


class CPU(SqlAlchemyBase):
    __tablename__ = 'cpu'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    socket = sqlalchemy.Column(sqlalchemy.String)
    cpu_group = sqlalchemy.Column(sqlalchemy.String)
    delivery_type = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, socket, cpu_group, delivery_type, cost, link, image
    ]


class GPU(SqlAlchemyBase):
    __tablename__ = 'gpu'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    memory = sqlalchemy.Column(sqlalchemy.Integer)
    developer = sqlalchemy.Column(sqlalchemy.String)
    memory_type = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, memory, developer, memory_type, cost, link, image
    ]


class Core(SqlAlchemyBase):
    __tablename__ = 'core'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    core_type = sqlalchemy.Column(sqlalchemy.String)
    form_factor = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, core_type, form_factor, cost, link, image
    ]


class CPUCoolers(SqlAlchemyBase):
    __tablename__ = 'cpu_coolers'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    tdp = sqlalchemy.Column(sqlalchemy.Integer)
    socket = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, tdp, socket, cost, link, image
    ]


class Disk(SqlAlchemyBase):
    __tablename__ = 'disk'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    capacity = sqlalchemy.Column(sqlalchemy.Integer)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, capacity, cost, link, image
    ]


class Motherboard(SqlAlchemyBase):
    __tablename__ = 'motherboard'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    socket = sqlalchemy.Column(sqlalchemy.String)
    chipset = sqlalchemy.Column(sqlalchemy.String)
    form_factor = sqlalchemy.Column(sqlalchemy.String)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, socket, chipset, form_factor, cost, link, image
    ]


class Power(SqlAlchemyBase):
    __tablename__ = 'power'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    power = sqlalchemy.Column(sqlalchemy.Integer)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, power, cost, link, image
    ]


class RAM(SqlAlchemyBase):
    __tablename__ = 'memory'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    brand = sqlalchemy.Column(sqlalchemy.String)
    memory = sqlalchemy.Column(sqlalchemy.Integer)
    memory_type = sqlalchemy.Column(sqlalchemy.String)
    freq = sqlalchemy.Column(sqlalchemy.Integer)
    cost = sqlalchemy.Column(sqlalchemy.Integer)
    link = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)

    columns = [
        id, title, brand, memory, memory_type, freq, cost, link, image
    ]