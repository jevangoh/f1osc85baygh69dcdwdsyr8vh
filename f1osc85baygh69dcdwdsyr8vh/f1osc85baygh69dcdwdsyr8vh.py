from typing import cast
from uuid import UUID as Uuid

from sqlalchemy.event import listens_for
from sqlalchemy.orm import ORMExecuteState as OrmExecuteState, Session
from sqlalchemy.orm.unitofwork import UOWTransaction as UnitOfWorkTransaction
from sqlalchemy.sql.dml import Update

import msjzm0ilrcvjjguhp29y62uzk as the_redis_client
import skkrfl6asevwuubvfioii3hlm as Model


@listens_for(Session, "after_flush")
def f1osc85baygh69dcdwdsyr8vh(session: Session, flush_context: UnitOfWorkTransaction) -> None:
    for __object__ in session.new:
        _object_: Model._ = cast(Model._, __object__)
        print(str(_object_.id))
        the_redis_client._.publish("insertion", str(_object_.id))
        the_redis_client._.publish(f"{_object_.id}_inserted", "")

    for _object_ in session.deleted:
        _object_: Model._ = cast(Model._, __object__)
        the_redis_client._.publish("deletion", str(_object_.id))
        the_redis_client._.publish(f"{_object_.id}_deleted", "")


@listens_for(Session, "do_orm_execute")
def receive_do_orm_execute(orm_execute_state: OrmExecuteState):
    if orm_execute_state.is_update:
        _id_: Uuid = cast(Update, orm_execute_state.statement).compile().params["id_1"]
        the_redis_client._.publish("update", str(_id_))
        the_redis_client._.publish(f"{_id_}_updated", "")
