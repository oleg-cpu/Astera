import uuid
import datetime


class Task:
    _id_task: uuid.UUID
    _title: str
    _description: str
    _status: str
    _creation_date: datetime.datetime
    _due_date: datetime.datetime
    ALLOWED_STATUSES = ("To Do", "In Progress", "Done")

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
        self.status = status
        self._creation_date = datetime.datetime.now()
        self.due_date = due_date

    def __repr__(self):

        return (
            f"Task("
            f"title={self.title !r}, "
            f"description={self.description !r}, "
            f"status={self.status !r}, "
            f"due_date={self.due_date !r})"
        )

    def __str__(self):
        if self.due_date is None:
            due_date_str = "Due date not set"
        else:
            due_date_str = self.due_date.strftime("%d.%m.%Y")
        return f"Task title: {self.title} Status name: {self.status}. Dedline: {due_date_str}"

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

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: str):
        status = status.strip().title()
        if not status:
            raise ValueError("Status can't be empty")
        elif status not in self.ALLOWED_STATUSES:
            raise ValueError("Status doesn't exists")
        else:
            self._status = status

    @property
    def due_date(self):
        return self._due_date

    @due_date.setter
    def due_date(self, due_date: datetime.datetime):
        if due_date is None:
            self._due_date = due_date
        elif type(due_date) is not datetime.datetime:
            raise TypeError("incorrect format date and time")
        elif due_date < datetime.datetime.now():
            raise ValueError("Due date cannot be in the past")
        else:
            self._due_date = due_date

    def to_dict(self):

        description_str = None
        due_date_str = None

        if self.description is not None:
            description_str = str(self.description)

        if self.due_date is not None:
            due_date_str = str(self.due_date)

        task_data = {
            "id_task": str(self._id_task),
            "title": self.title,
            "description": description_str,
            "status": self.status,
            "creation_date": str(self._creation_date),
            "due_date": due_date_str,
        }
        return task_data
