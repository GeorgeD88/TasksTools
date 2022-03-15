from taskstools import *
from auth import auth


creds = auth()
tasks = TasksTools(credentials=creds)

tasks.list_tasklists()
