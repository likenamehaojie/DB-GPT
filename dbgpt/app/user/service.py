import logging


from dbgpt._private.config import Config
from dbgpt.app.user.user_db import (
    UserEntity,
    UserEDao
)
from dbgpt.app.user.schemas import (
    UserAuth,
    UserOut, UserQueryResponse,
)


user_dao = UserEDao()

logger = logging.getLogger(__name__)
CFG = Config()




class UserService:
    """KnowledgeService
    Knowledge Management Service:
        -knowledge_space management
        -knowledge_document management
        -embedding management
    """

    def __init__(self):
        pass


    def create_user(self, request: UserAuth):
        """create knowledge document
        Args:
           - request: KnowledgeDocumentRequest
        """
        query = UserEntity(email=request.email)
        users = user_dao.get_user(query)
        if len(users) > 0:
            raise Exception(f"user email:{request.email} have already named")
        user = UserEntity(
            email=request.email,
            password=request.password
        )
        user_id = user_dao.create_user(user)
        if user_id is None:
            raise Exception(f"create user failed, {request.email}")
        return user_id



    def get_users(self, request: UserAuth):
        """get knowledge documents
        Args:
            - space: Knowledge Space Name
            - request: DocumentQueryRequest
        Returns:
            - res DocumentQueryResponse
        """
        res = UserQueryResponse()
        if request.user_ids and len(request.user_ids) > 0:
            res.data = user_dao.users_by_ids(request.user_ids)
        else:
            query = UserEntity(
                email=request.email,
            )
            res.data = user_dao.get_users(
                query
            )
            res.total = user_dao.get_users_count_bulk(query)
            res.page = request.page
        return res


    def delete_document(self,  email: str):
        """delete document
        Args:
            - space_name: knowledge space name
            - doc_name: doocument name
        """
        user_query = UserEntity(email=email)
        users = user_dao.get_users(user_query)
        if len(users) != 1:
            raise Exception(f"there are no or more than one document called {email}")
        # delete document
        return user_dao.raw_delete(user_query)

