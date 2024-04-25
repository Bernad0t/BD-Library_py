import datetime

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from BaseData.src.database import Base, str_256
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

#metadata_obj = MetaData() # тут хранится инф обо всех таблицах, которые создадим

class AuthorOrm(Base):
    __tablename__ = "Автор"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ФИО: Mapped[str_256]

    #Книга: Mapped[list["BookOrm"]] = relationship()

class BookOrm(Base):
    __tablename__ = "Книга"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Название: Mapped[str_256]
    Жанр: Mapped[str_256]
    Количество: Mapped[int]
    Цена: Mapped[int]

    #Автор: Mapped[list["AuthorOrm"]] = relationship()
    #История: Mapped[list["HistoryOrm"]] = relationship()

# class GenreOrm(Base):
#     __tablename__ = "Жанр"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     Жанр: Mapped[str_256]

class AuthorBookOrm(Base):
    __tablename__ = "АвторКнига"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Автор_id: Mapped[int] = mapped_column(ForeignKey("Автор.id"))
    Книга_id: Mapped[int] = mapped_column(ForeignKey("Книга.id"))

# class BookGenreOrm(Base):
#     __tablename__ = "КнигаЖанр"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     Книга_id: Mapped[int] = mapped_column(ForeignKey("Книга.id"))
#     Жанр_id: Mapped[int] = mapped_column(ForeignKey("Жанр.id"))

class ReaderOrm(Base):
    __tablename__ = "Читатель"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ФИО: Mapped[str_256]

    #История: Mapped[list["HistoryOrm"]] = relationship()

class ResultHistory(enum.Enum):
    in_time = "Вернули вовремя"
    out_time = "Вернули с просрочкой"
    not_time = "Не вернули"
    in_price = "Возместили"
    lost = "Списано"

class HistoryOrm(Base):
    __tablename__ = "История"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Книга_id: Mapped[int] = mapped_column(ForeignKey("Книга.id"))
    Читатель_id: Mapped[int | None] = mapped_column(ForeignKey("Читатель.id", ondelete="SET NULL"))
    ДатаВзятия: Mapped[datetime.date]
    ДатаВозвратаФакт: Mapped[datetime.date | None]
    РезультатИстории: Mapped[ResultHistory]

    #Книга: Mapped["BookOrm"] = relationship()
    #Читатель: Mapped["ReaderOrm"] = relationship()
    Продление: Mapped[list["ExtendOrm"]] = relationship()

class ExtendOrm(Base):
    __tablename__ = "Продление"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    История_id: Mapped[int] = mapped_column(ForeignKey("История.id"))
    ПродленДо: Mapped[datetime.date]

    История: Mapped["HistoryOrm"] = relationship()


class CompensationLosses(Base):
    __tablename__ = "ВозмещениеУбытков"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    История_id: Mapped[int] = mapped_column(ForeignKey("История.id"))
    СуммаВозмещения: Mapped[int]

class NowDateOrm(Base):
    __tablename__ = "ДатаСейчас"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    Дата: Mapped[datetime.date]



