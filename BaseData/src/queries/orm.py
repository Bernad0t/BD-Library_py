from sqlalchemy import text, insert, select, update, delete, func, cast, and_
from sqlalchemy.orm import selectinload, joinedload
import datetime

from BaseData.src.database import engine, session, date_issue
from BaseData.src.models import AuthorOrm, Base, BookOrm, AuthorBookOrm, HistoryOrm, NowDateOrm, ReaderOrm, ResultHistory, ExtendOrm,\
CompensationLosses
def create_tables():
    engine.echo = False
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.echo = True


def change_date_now(date):
    with session() as sess:
        query = (
            delete(NowDateOrm)
        )
        sess.execute(query)
        new_date = NowDateOrm(Дата=date)
        sess.add(new_date)
        sess.commit()

def insert_reader(name):
    with session() as sess:
        reader = ReaderOrm(ФИО=name)
        sess.add(reader)
        sess.commit()


def get_status_lose(reader_id, book_id):
    with session() as sess:
        query = (
            select(HistoryOrm)
            .where(and_(HistoryOrm.Книга_id == book_id, HistoryOrm.Читатель_id == reader_id))
        )
        result = sess.execute(query).scalars().first()
        if result == None:
            return 1
        stmt = sess.query(HistoryOrm).filter(and_(HistoryOrm.Книга_id == book_id, HistoryOrm.Читатель_id == reader_id)) \
            .update({HistoryOrm.РезультатИстории: ResultHistory.lost})
        sess.commit()
        return 0


def lose_book():
    with session() as sess:
        query_history = (
            select(HistoryOrm)
            .where(HistoryOrm.РезультатИстории == ResultHistory.not_time)
            .options(selectinload(HistoryOrm.Продление))
        )
        history = sess.execute(query_history).scalars().all()
        if len(history) == 0:
            # print("Утерянных книг нет")
            return 1
        query = (
            select(NowDateOrm.Дата)
        )
        date_now = sess.execute(query).scalars().first()

        for hist in history:
            if len(hist.Продление) == 0:
                date_delivery = hist.ДатаВзятия + datetime.timedelta(date_issue)
            else:
                date_delivery = hist.Продление[-1].ПродленДо
            if (date_now - date_delivery > datetime.timedelta(365 * 2)):
                get_status_lose(hist.Читатель_id, hist.Книга_id)
        return 0


def insert_book(name, number, genre, price, name_author):
    with session() as sess:
        flag_exist = search_for_author_name(name_author, name)
        if flag_exist == 0:
            return 1
        book = BookOrm(Название=name, Жанр=genre,Цена=price, Количество= number)
        author = AuthorOrm(ФИО=name_author)
        sess.add_all([book, author])
        sess.flush()
        author_book = AuthorBookOrm(Книга_id=book.id, Автор_id=author.id)
        sess.add(author_book)
        sess.commit()
        return 0


def update_fonds(fond_id: int, number: int):
    with session() as sess:
        query = (
            select(BookOrm)
            .where(BookOrm.id == fond_id)
        )
        result = sess.execute(query).unique().all()
        if len(result) == 0:
            return 1
        stmt = sess.query(BookOrm).filter(BookOrm.id == fond_id)\
            .update({BookOrm.Количество : BookOrm.Количество + number})
        sess.commit()
        return 0


def search_reader_for_id(id):
    with session() as sess:
        query = (
            select(ReaderOrm.ФИО)
            .where(ReaderOrm.id == id)
        )
        result = sess.execute(query).unique().first()
        return result

def search_for_name_book(book_name):
    with session() as sess:
        stmt = (
            select(BookOrm, AuthorOrm.ФИО.label('ФИО'))
            .join(AuthorBookOrm, AuthorBookOrm.Книга_id == BookOrm.id)
            .join(AuthorOrm, AuthorOrm.id == AuthorBookOrm.Автор_id)
            .where(BookOrm.Название == book_name)
        )
        return sess.execute(stmt).all()
        #print(res)

def search_for_author(author_name):
    with session() as sess:
        stmt = (
            select(BookOrm, AuthorOrm.ФИО.label('ФИО'))
            .join(AuthorBookOrm, AuthorBookOrm.Книга_id == BookOrm.id)
            .join(AuthorOrm, AuthorOrm.id == AuthorBookOrm.Автор_id)
            .where(AuthorOrm.ФИО == author_name)
        )
        return sess.execute(stmt).all()

def search_for_author_name(name_author, name_book):
    with session() as sess:
        query = (
            select(BookOrm, AuthorOrm.ФИО)
            .join(AuthorBookOrm, AuthorBookOrm.Книга_id == BookOrm.id)
            .join(AuthorOrm, AuthorBookOrm.Автор_id == AuthorOrm.id)
            .where(and_(AuthorOrm.ФИО == name_author, BookOrm.Название == name_book))
        )
        result = sess.execute(query).unique().all()
        #print(result)
        return result

def deduction_user(): # не надо с учетом продления, тк это учтено, история уже закрыта
    with session() as sess:
        query = (
            delete(ReaderOrm)
            .where(
                ReaderOrm.id.in_(
                    select(HistoryOrm.Читатель_id)
                    .where(HistoryOrm.РезультатИстории != "not_time")
                    .group_by(HistoryOrm.Читатель_id)
                    .having(
                        select(NowDateOrm.Дата).scalar_subquery() - func.max(HistoryOrm.ДатаВозвратаФакт) > 365
                    )
                )
            )
        )
        result = sess.execute(query).scalars().all()
        print(result)
        sess.commit()

def refund_cost(reader_id, book_id):
    with session() as sess:
        query = (
            select(HistoryOrm)
            .where(and_(HistoryOrm.Читатель_id == reader_id, HistoryOrm.Книга_id == book_id))
            .options(joinedload(HistoryOrm.Продление))
        )
        res = sess.execute(query).unique().scalars().first()
        if (res == None):
            return 2
        if (res.РезультатИстории != ResultHistory.not_time):
            return 3
        if len(res.Продление) > 0:
            date_delivery = res.Продление[-1].ПродленДо
        else:
            date_delivery = res.ДатаВзятия + datetime.timedelta(30)
        query = (
            select(NowDateOrm.Дата)
        )
        date_now = sess.execute(query).scalars().first()
        if date_now < date_delivery + datetime.timedelta(365):
            stmt = sess.query(HistoryOrm).filter(
                and_(HistoryOrm.Книга_id == book_id, HistoryOrm.Читатель_id == reader_id)) \
                .update({HistoryOrm.РезультатИстории: ResultHistory.in_price, HistoryOrm.ДатаВозвратаФакт: date_now})
            query = (
                select(BookOrm.Цена)
                .where(BookOrm.id == book_id)
            )
            price = sess.execute(query).scalars().first()
            comp = CompensationLosses(История_id=res.id, СуммаВозмещения=price)
            sess.add(comp)
            sess.commit()
            return 0
        else:
            #print("Просрочка")
            return 1


def book_issuance(reader_id, book_id):
    with session() as sess:
        query_reader = (
            select(func.count())
            .where(ReaderOrm.id == reader_id)
        )
        flag_reader = sess.execute(query_reader).scalars().first()

        if (flag_reader == 0):
            # print("Такого читатетля нет. Хотите получить абонимент?")
            return 0

        query_book = (
            select(func.count())
            .where(BookOrm.id == book_id)
        )
        flag_book = sess.execute(query_book).scalars().first()
        if (flag_book == 0):
            # print("Такой книги нет")
            return 1
        query_book = (
            select(BookOrm.Количество)
            .where(BookOrm.id == book_id)
        )
        flag_book = sess.execute(query_book).scalars().first()
        if flag_book == 0:
            # print("Этой книги нет в наличии")
            return 2

        query_hist = (
            select(func.count())
            .where(and_(HistoryOrm.Книга_id == book_id, HistoryOrm.Читатель_id == reader_id))
        )
        flag_book = sess.execute(query_hist).scalars().first()
        if flag_book > 0:
            # print("Этот пользователь уже взял эту книгу")
            return 3
        query_time = (
            select(NowDateOrm.Дата)
        )
        date_now = sess.execute(query_time).scalars().first()
        History = HistoryOrm(Книга_id=book_id, Читатель_id=reader_id, ДатаВзятия=date_now,
                              ДатаВозвратаФакт=None, РезультатИстории=ResultHistory.not_time)
        sess.query(BookOrm).filter(BookOrm.id == book_id) \
            .update({BookOrm.Количество: BookOrm.Количество - 1})
        sess.add(History)
        sess.commit()
        return 4

def book_reception(reader_id, book_id):
    with session() as sess:
        query_history = (
            select(func.count())
            .where(and_(HistoryOrm.Читатель_id == reader_id, HistoryOrm.Книга_id == book_id))
        )
        flag_reader = sess.execute(query_history).scalars().first()
        if flag_reader == 0:
            #print("Данный читатель не брал данную книгу")
            return 0

        query_history = (
            select(HistoryOrm)
            .where(and_(HistoryOrm.Читатель_id == reader_id, HistoryOrm.Книга_id == book_id))
            .options(selectinload(HistoryOrm.Продление))
        )
        history = sess.execute(query_history).scalars().first()

        query = (
            select(NowDateOrm.Дата)
        )
        date_now = sess.execute(query).scalars().first()

        if len(history.Продление) == 0:
            date_delivery = history.ДатаВзятия + datetime.timedelta(date_issue)
        else:
            date_delivery = history.Продление[-1].ПродленДо
        if (date_now - date_delivery > datetime.timedelta(365)):
            #print("Вам придется заплатить трехкратный штраф")
            return 1

        if date_delivery > date_now:
            status_delivery = ResultHistory.in_time
        else:
            status_delivery = ResultHistory.out_time
        sess.query(HistoryOrm).filter(
            and_(HistoryOrm.Книга_id == book_id, HistoryOrm.Читатель_id == reader_id)) \
            .update({HistoryOrm.РезультатИстории: status_delivery, HistoryOrm.ДатаВозвратаФакт: date_now})

        sess.query(BookOrm).filter(BookOrm.id == book_id) \
            .update({BookOrm.Количество: BookOrm.Количество + 1})

        sess.commit()
        return 2

def book_extend(reader_id, book_id):
    with session() as sess:
        query_history = (
            select(func.count())
            .where(and_(HistoryOrm.Читатель_id == reader_id, HistoryOrm.Книга_id == book_id))
        )
        flag_reader = sess.execute(query_history).scalars().first()
        if flag_reader == 0:
            #print("Данный читатель не брал данную книгу")
            return 0

        query_history = (
            select(HistoryOrm)
            .where(and_(HistoryOrm.Читатель_id == reader_id, HistoryOrm.Книга_id == book_id))
            .options(selectinload(HistoryOrm.Продление))
        )
        history = sess.execute(query_history).scalars().first()
        if history.РезультатИстории != ResultHistory.not_time:
            #print("Вы уже вернули книгу")
            return 1
        query = (
            select(NowDateOrm.Дата)
        )
        date_now = sess.execute(query).scalars().first()

        if len(history.Продление) == 0:
            date_delivery = history.ДатаВзятия + datetime.timedelta(date_issue)
        else:
            date_delivery = history.Продление[-1].ПродленДо

        if date_delivery < date_now:
            #print("Вы просрочили книгу. Вам придется ее вернуть")
            return 2

        if len(history.Продление) >= 3:
            #print("Вы не можете продлить больше 3 раз")
            return 3

        extend_hist = ExtendOrm(История_id=history.id, ПродленДо=date_delivery + datetime.timedelta(date_issue))
        sess.add(extend_hist)
        sess.commit()
        return 4


def create_letter_to_reader():
    with session() as sess:
        query = (
            select(NowDateOrm.Дата)
        )
        data_now = sess.execute(query).scalars().first()

        query = (
            select(HistoryOrm)
            .join(ExtendOrm, ExtendOrm.История_id == HistoryOrm.id, isouter=True)
            .group_by(HistoryOrm.id)
            .having(and_(data_now - func.coalesce(func.max(ExtendOrm.ПродленДо),
                         HistoryOrm.ДатаВзятия + datetime.timedelta(date_issue)) > datetime.timedelta(date_issue),
                         HistoryOrm.РезультатИстории == ResultHistory.not_time,
                         data_now - func.coalesce(func.max(ExtendOrm.ПродленДо),
                         HistoryOrm.ДатаВзятия + datetime.timedelta(date_issue)) <= datetime.timedelta(365)))
        )
        result = sess.execute(query).scalars().all()
        return result


def search_list_receipt_to_reader():
    with session() as sess:
        query = (
            select(NowDateOrm.Дата)
        )
        data_now = sess.execute(query).scalars().first()

        query = (
            select(HistoryOrm)
            .join(ExtendOrm, ExtendOrm.История_id == HistoryOrm.id, isouter=True)
            .group_by(HistoryOrm.id)
            .having(and_(data_now - func.coalesce(func.max(ExtendOrm.ПродленДо),
                         HistoryOrm.ДатаВзятия + datetime.timedelta(date_issue)) > datetime.timedelta(365),
                         HistoryOrm.РезультатИстории == ResultHistory.not_time))
        )
        result = sess.execute(query).scalars().all()
        list_result = []
        list_reader_id = []
        list_history_id = []
        for i in result:
            # get_status_lose(i.Читатель_id[0], i.Книга_id[0])
            # query = (
            #     select(BookOrm.Цена)
            #     .where(BookOrm.id == i.Книга_id[0])
            # )
            # price = sess.execute(query).scalars().first() * 3
            # comp = CompensationLosses(История_id=i.id[0], СуммаВозмещения=price)
            # sess.add(comp)
            list_reader_id.append(i.Читатель_id)
            list_history_id.append(i.id)
        # sess.commit()
        list_result.append(list_reader_id)
        list_result.append(list_history_id)
        return list_result


def actions_wth_receipt_to_reader(history_id):
    with session() as sess:
        query = (
            select(HistoryOrm)
            .where(HistoryOrm.id == history_id)
        )
        result = sess.execute(query).scalars().first()
        get_status_lose(result.Читатель_id, result.Книга_id)
        query = (
            select(BookOrm.Цена)
            .where(BookOrm.id == result.Книга_id)
        )
        price = sess.execute(query).scalars().first() * 3
        comp = CompensationLosses(История_id=result.id, СуммаВозмещения=price)
        query = (
            select(ReaderOrm.ФИО)
            .where(ReaderOrm.id == result.Читатель_id)
        )
        name = sess.execute(query).scalars().first()
        sess.add(comp)
        sess.commit()
        return [name, price]



def most_popular_book(for_date):
    with session() as sess:
        query = (
            select(BookOrm.id, BookOrm.Название, func.count().label("count"))
            .join(HistoryOrm, HistoryOrm.Книга_id == BookOrm.id)
            .where(HistoryOrm.ДатаВзятия >= for_date)
            .group_by(BookOrm.id)
            .order_by(func.count().desc())
            .limit(5)
        )
        result = sess.execute(query).all()
        #print(result)
        return result

def most_popular_author(for_date):#TODO легко заменить null на 0
    with session() as sess:
        sub_query = (
            select(HistoryOrm.Книга_id, func.count().label("count_1"))
            .where(HistoryOrm.ДатаВзятия >= for_date)
            .group_by(HistoryOrm.Книга_id)
            .cte("popular_book")
        )
        query = (
            select(AuthorOrm.id, AuthorOrm.ФИО, func.coalesce(func.sum(sub_query.c.count_1), 0).label("Прочитано книг"))
            .join(AuthorBookOrm, AuthorBookOrm.Автор_id == AuthorOrm.id, isouter=True)
            .join(sub_query, sub_query.c.Книга_id == AuthorBookOrm.Книга_id, isouter=True)
            .group_by(AuthorOrm.id)
            .order_by(func.coalesce(func.sum(sub_query.c.count_1), 0).desc())
            .limit(5)
        )
        result = sess.execute(query).all()
        #print(result)
        return result


def book_on_reader_year():
    with session() as sess:
        query = (
            select(NowDateOrm.Дата)
        )
        date_now = sess.execute(query).scalars().first()

        query = (
            select(ReaderOrm.ФИО, func.coalesce(func.count(), 0).label("Брал книг"))
            .join(HistoryOrm, HistoryOrm.Читатель_id == ReaderOrm.id, isouter=True)
            .where(and_(HistoryOrm.РезультатИстории != ResultHistory.not_time, date_now - HistoryOrm.ДатаВзятия < 365))
            .group_by(ReaderOrm.id)
            .order_by(func.coalesce(func.count(), 0).desc())
        )
        result = sess.execute(query).all()
        return result


def statistic_for_genre():
    with session() as sess:
        query = (
            select(BookOrm.Жанр, func.coalesce(func.count(), 0).label("Взятых книг с таким жанром"))
            .join(HistoryOrm, HistoryOrm.Книга_id == BookOrm.id, isouter=True)
            .group_by(BookOrm.Жанр)
            .order_by(func.coalesce(func.count(), 0).desc())
            .limit(10)
        )
        result = sess.execute(query).all()
        return result

def finance_result_for_year():
    with session() as sess:
        query = (
            select(func.count(), func.sum(BookOrm.Цена * BookOrm.Количество))
            .select_from(BookOrm)
        )
        number_and_total_price = sess.execute(query).first()
        number, price = number_and_total_price[0], number_and_total_price[1]
        query = (
            select(func.sum(CompensationLosses.СуммаВозмещения))
        )
        comp = sess.execute(query).scalars().first()
        return [number, price, comp]
