from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, Integer, String, Text, func

from dbgpt._private.config import Config
from dbgpt.storage.metadata import BaseDao, Model

CFG = Config()


class UserEntity(Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    password = Column(String(100))
    email = Column(String(100))

    def __repr__(self):
        return f"UserEntity(id={self.id}, email='{self.email}')"


class UserEDao(BaseDao):
    def create_user(self, user: UserEntity):
        session = self.get_raw_session()
        user = UserEntity(
            password= user.password,
            email=user.email,
        )
        session.add(user)
        session.commit()
        user_id = user.id
        session.close()
        return user_id

    def get_user(self, query, page=1, page_size=20):
        """Get a list of documents that match the given query.
        Args:
            query: A KnowledgeDocumentEntity object containing the query parameters.
            page: The page number to return.
            page_size: The number of documents to return per page.
        """
        session = self.get_raw_session()
        print(f"current session:{session}")
        users = session.query(UserEntity)
        if query.id is not None:
            users = users.filter(
                UserEntity.id == query.id
            )
        if query.email is not None:
            users = users.filter(
                UserEntity.email == query.email
            )


        users = users.order_by(
            UserEntity.id.desc()
        )
        users = users.offset((page - 1) * page_size).limit(
            page_size
        )
        result = users.all()
        session.close()
        return result

    def users_by_ids(self, ids) -> List[UserEntity]:
        """Get a list of documents by their IDs.
        Args:
            ids: A list of document IDs.
        Returns:
            A list of KnowledgeDocumentEntity objects.
        """
        session = self.get_raw_session()
        print(f"current session:{session}")
        users = session.query(UserEntity)
        users = users.filter(
            users.id.in_(ids)
        )
        result = users.all()
        session.close()
        return result

    def get_users(self, query):
        session = self.get_raw_session()
        print(f"current session:{session}")
        users = session.query(UserEntity)
        if query.id is not None:
            users = users.filter(
                UserEntity.id == query.id
            )
        if query.email is not None:
            users = users.filter(
                UserEntity.email == query.email
            )
        result = users.all()
        session.close()
        return result

    def get_users_count_bulk(self,query) :
        session = self.get_raw_session()
        """
        Perform a batch query to count the number of documents for each knowledge space.

        Args:
            space_names: A list of knowledge space names to query for document counts.
            session: A SQLAlchemy session object.

        Returns:
            A dictionary mapping each space name to its document count.
        """
        counts_query = (
            session.query(
                func.count(UserEntity.id).label("user_count"),
            )
        )

        results = counts_query.all()
        user_count = {result.user_count for result in results}
        return user_count

    def get_user_count(self, query):
        session = self.get_raw_session()
        users = session.query(func.count(UserEntity.id))
        if query.id is not None:
            users = users.filter(
                UserEntity.id == query.id
            )
        if query.doc_type is not None:
            users = users.filter(
                UserEntity.email == query.email
            )

        count = users.scalar()
        session.close()
        return count

    def update_user(self, user: UserEntity):
        session = self.get_raw_session()
        updated_user = session.merge(user)
        session.commit()
        return updated_user.id

    #
    def raw_delete(self, query: UserEntity):
        session = self.get_raw_session()
        users = session.query(UserEntity)
        if query.id is not None:
            users = users.filter(
                UserEntity.id == query.id
            )
        if query.email is not None:
            users = users.filter(
                UserEntity.email == query.doc_name
            )

        users.delete()
        session.commit()
        session.close()
