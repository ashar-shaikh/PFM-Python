from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, DateTime
from internal.storage.models.base import Base


class BackgroundTasks(Base):
    """
    Background Tasks Model

    Fields:
    id (int): Primary Key
    task_name (str): Task Name
    update_time (datetime): Update Time
    row_count (int): Row Count
    status (str): Status
    completed_rows (int): Completed Rows
    failure_reason (str): Failure Reason
    created_at (datetime): Created at timestamp
    updated_at (datetime): Updated at timestamp
    """
    __tablename__ = 'background_tasks'
    id = Column(Integer, Sequence('background_tasks_id_seq'), primary_key=True)
    task_name = Column(String(50), nullable=False)
    update_time = Column(DateTime, default=datetime.utcnow)
    row_count = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False)
    completed_rows = Column(Integer, default=0)
    failure_reason = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get(self):
        data = {
            'id': self.id,
            'task_name': self.task_name,
            'update_time': self.update_time,
            'row_count': self.row_count,
            'status': self.status,
            'completed_rows': self.completed_rows,
            'failure_reason': self.failure_reason,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        return data
