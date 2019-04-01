from .parsetree import ParseTree
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.engine import ResultProxy
from typing import List
import json
# Query the database for a type matching model (tag, experience, etc)
# that has the same id as the parameter id
def read_row_by_id(session: Session, model: DeclarativeMeta, id: int) -> Query:
    """
    get row by id

    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    model
        sqlalchemy.ext.declarative.DeclarativeMeta
        the sqlalchemy model to use
    id
        int
        the primary key

    Return
    -------
    sqlalchemy.orm.query.Query
        the resultant query object

    """
    results = session.query(model).filter(model.id == id)
    return results
def read_rows(session: Session, model: DeclarativeMeta, filters: dict = None) -> Query:
    """
    get all rows from model where the criteria in the filters is met

    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    model 
        sqlalchemy.ext.declarative.api.DeclativeMeta
        the sqlalchemy model to use
    filters
        dict
        the filters to use in query
        filters dict must be in the following structure
        [  {
                'column': {
                    'comparitor': '>=' OR '==' OR '<=' OR '>' OR '<' OR !=
                    'data': str OR int OR float  
                },
                join = "and" OR "or"
            },
            ...Other columns
        ]

    Return
    ------
    sqlalchemy.orm.query.Query
        the resultant Query object
    """
    if filters is not None:
        querier = ParseTree(model,filters)
        results = querier.query(session)
    else:
        results = session.query(model)
    return results
def create_rows(session: Session, *models: List[DeclarativeMeta]):
    """
    
    create rows in the database

    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    models
        list[sqlalchemy.ext.declarative.DeclarativeMeta]
        the sqlalchemy models representing the rows to insert

    """
    for model in models:
        session.add(model)

    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        session.flush()
        raise e
def update_row_by_id(session: Session, model: DeclarativeMeta, id: int,  updates:dict):
    """
    update the fields of a row with the particular primary key

    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    model
        sqlalchemy.ext.declarative.DeclarativeMeta
        the sqlalchemy model to use
    id
        int
        the primary key
    updates
        dict
        the fields to update as the keys and their respective values and the dictionary values
    """

    if not isinstance(updates, dict):
        raise TypeError('updates must be of type dict')

    query = read_row_by_id(session,model, id)

    try:
       query.one()
    except NoResultFound as e:
        raise NoResultFound(f"row cannot be updated because no row can be found with id: {id}")
    except MultipleResultsFound as e:
        raise MultipleResultsFound(f"the database contains multiple results for this id when only one is expected. id: {id}")
    
    matched =  query.update(updates)

    if matched == 0:
        raise ValueError(f"bad update request, no columns could be matched updates requested: {json.dumps(updates)}")
    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        session.flush()
        raise e

def update_rows(session: Session, model: DeclarativeMeta, updates: dict, filters: dict = None):
    """

    bulk update rows from model where the criteria in the filters is met by the values in the updates dict

    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    model 
        sqlalchemy.ext.declarative.api.DeclativeMeta
        the sqlalchemy model to use
    updates
        dict
        the fields to update as the keys and their respective values and the dictionary values
    filters
        dict
        filters dict must be in the following structure
        [  {
                'column': {
                    'comparitor': '>=' OR '==' OR '<=' OR '>' OR '<' OR !=
                    'data': str OR int OR float  
                },
                join = "and" OR "or"
            },
            ...Other Columns
        ]
    """
    if not isinstance(updates, dict):
        raise TypeError('updates must be of type dict')

    results = read_rows(session,model,filters)

    check_res = results.first()

    if check_res == None:
        raise NoResultFound(f"no rows can be updated because no rows can be found with the following filters: {json.dumps(filters)}")

    matched = results.update(updates)

    if matched == 0:
        raise ValueError(f"bad update request, no columns could be matched updates requested: {json.dumps(updates)}")
    
    try:
        session.commit()
        session.flush()
    except Exception as e:
        # TODO Logging.log.exception()
        session.rollback()
        session.flush()
        raise e

def delete_row_by_id(session,model, id):
    """
    delete a row with the particular primary key

    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    model
        sqlalchemy.ext.declarative.DeclarativeMeta
        the sqlalchemy model to use
    id
        int
        the primary key
    """
    results = read_row_by_id(session,model, id)

    matched = results.delete()

    if matched == 0:
        raise NoResultFound(f'a row with the id specified was not found id: {id}')
    
    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        session.flush()
        raise e

def delete_rows(session: Session, model: DeclarativeMeta, filters: dict = None):
    """

    delete all rows from model where the criteria in the filters is met

    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    model 
        sqlalchemy.ext.declarative.api.DeclativeMeta
        the sqlalchemy model to use
    filters
        dict
        filters dict must be in the following structure
        [  {
                'column': {
                    'comparitor': '>=' OR '==' OR '<=' OR '>' OR '<' OR !=
                    'data': str OR int OR float  
                },
                join = "and" OR "or"
            },
            ...Other columns
        ]
    """
    results = read_rows(session, model, filters)

    matched = results.delete()

    if matched == 0:
        raise NoResultFound(f"No rows were found to delete with the following filters: {json.dumps(filters)}")
    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        session.flush()
        raise e
def execute_sql(session:Session, sql: str)  -> ResultProxy:
    """
    execute an sql statement on the database
    
    Parameters
    ----------
    session
        sqlalchemy.orm.session.Session
        session object to be used
    sql
        sql
        the sql statement
 
    Return
    ------
    sqlalchemy.engine.ResultProxy
        DB-API cursor wrapper for results of the query
    """
    if not isinstance(sql, str):
        raise TypeError('sql must be of type str')
    try:
        results = session.execute(sql)
        session.commit()
        session.flush()
        return results
    except Exception as e:
        session.rollback()
        session.flush()
        raise e
    