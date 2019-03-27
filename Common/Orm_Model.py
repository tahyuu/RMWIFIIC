# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class Socket(Base):
    # Python 对象对应关系数据库的表名
    __tablename__ = 't_Sockets'
    # 定义自动，参数含义分别为：数据库字段名，字段类型，其他选项
    id = Column('id',Integer, primary_key=True)
#    socketId = 0
    ip =Column("ip",String(30))
    comPort = Column("comPort",String(20))
    socketName = Column("socketName",String(30))
    backgroundImage= Column("backgroundImage",String(30))
    groupId= Column('groupId',Integer)
    comPort = Column("comPort",String(20))
    enable = Column("enable",Boolean)
    sn=""

class User(Base):
    # Python 对象对应关系数据库的表名
    __tablename__ = 't_Users'
    # 定义自动，参数含义分别为：数据库字段名，字段类型，其他选项
    id = Column('id',Integer, primary_key=True)
#    socketId = 0
    userName =Column("userName",String(30))
    password = Column("password",String(30))
    userType = Column("userType",Integer)


class Program(Base):
    # Python 对象对应关系数据库的表名
    __tablename__ = 't_Programs'
    # 定义自动，参数含义分别为：数据库字段名，字段类型，其他选项
    id = Column('id',Integer, primary_key=True)
#    socketId = 0
    progName =Column("progName",String(30))
    progRev = Column("progRev",String(10))
    progRoot = Column("progRoot",String(30))
    progTSL = Column("progTSL",String(30))
#    progLimit = Column("progLimit",String(30))
    progConfig = Column("progConfig",String(30))
    #progVar = Column("progVar",String(30))
    progDesc = Column("progDesc",String(50))

class Product(Base):
    # Python 对象对应关系数据库的表名
    __tablename__ = 't_Products'
    # 定义自动，参数含义分别为：数据库字段名，字段类型，其他选项
    id = Column('id',Integer, primary_key=True)
#    socketId = 0
    prodName =Column("prodName",String(30))
    prodRev = Column("prodRev",String(10))
    prodDesc = Column("prodDesc",String(50))
    progID = Column("progID",Integer)

