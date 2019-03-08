import enum

class EventType(enum.Enum):

    TASK_STARTED = 'task_started'
    TASK_COMPLETED = 'task_completed'
    TASK_INTERRUPTED = 'task_interrupted'