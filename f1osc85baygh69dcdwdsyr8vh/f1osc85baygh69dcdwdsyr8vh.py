from typing import cast, Optional
from uuid import UUID as Uuid
from json import dumps

from sqlalchemy.event import listens_for
from sqlalchemy.orm import ORMExecuteState as OrmExecuteState, Session
from sqlalchemy.orm.unitofwork import UOWTransaction as UnitOfWorkTransaction
from sqlalchemy.sql.dml import Update

from fastapi import FastAPI as FastApiServer

import m0bz81re1oqswkavde1k4ihec as the_lifespan
import msjzm0ilrcvjjguhp29y62uzk as the_redis_client
import skkrfl6asevwuubvfioii3hlm as Model


@listens_for(Session, "after_flush")
def callback_after_creation_and_deletion(
    session: Session, flush_context: UnitOfWorkTransaction
) -> None:
    for _new_object_ in session.new:
        _new_object_ = cast(Model._, _new_object_)
        the_redis_client._.publish("insertion", str(_new_object_.id))

    for _deleted_object_ in session.deleted:
        _deleted_object_ = cast(Model._, _deleted_object_)
        the_redis_client._.publish("deletion", str(_deleted_object_.id))

    _request_id_: Optional[str] = session.info.get("request_id")
    if _request_id_ is not None:
        the_redis_client._.publish("request_completed", _request_id_)


@listens_for(Session, "do_orm_execute")
def receive_do_orm_execute(orm_execute_state: OrmExecuteState) -> None:
    session = orm_execute_state.session
    _request_id_: Optional[str] = session.info.get("request_id")
    if orm_execute_state.is_update:
        _id_: Uuid = cast(Update, orm_execute_state.statement).compile().params["id_1"]
        the_redis_client._.publish("update", str(_id_))
        the_redis_client._.publish(f"{_id_}_updated", dumps({"request_id": _request_id_}))

    if _request_id_ is not None:
        the_redis_client._.publish("request_completed", _request_id_)


f1osc85baygh69dcdwdsyr8vh: FastApiServer = FastApiServer(
    title="f1osc85baygh69dcdwdsyr8vh", lifespan=the_lifespan._
)
