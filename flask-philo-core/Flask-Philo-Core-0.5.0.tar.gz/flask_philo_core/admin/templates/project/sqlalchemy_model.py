from flask_philo_sqlalchemy.orm import BaseModel
from sqlalchemy import Column, Integer


class User(BaseModel):
    __tablename__ = '{{project_name}}'
    id = Column(Integer, primary_key=True)
