import uuid
import datetime


class Task:
    _id_task: uuid.UUID = None
    _title: str = None
    _description: str = None
    _status: str = None
    _creation_date: datetime.datetime = None
    _due_date: datetime.datetime = None

    def __init__(
        self,
        title: str,
        description: str | None = None,
        status: str = "To Do",
        due_date: datetime.datetime | None = None,
    ):
        self._id_task = uuid.uuid4()
        self.title = title
        self.description = description
        self._status = status
        self._creation_date = datetime.datetime.now()
        self._due_date = due_date

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        title = title.strip()
        if not title:
            raise ValueError("Title can't be empty")
        elif len(title) > 50:
            raise ValueError("Title can't be more than 50 characters")
        else:
            self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):

        if description is None:
            self._description = description
        else:
            description = description.strip()
            if not description:
                raise ValueError(
                    "Description can contain only characters not just spaces"
                )
            elif len(description) > 500:
                raise ValueError("Description can't be more than 500 characters")
            else:
                self._description = description


# my_task = Task(
#    title="Test Task", status="Done", due_date=datetime.datetime(2025, 12, 15)
# )
# print(my_task._description)
