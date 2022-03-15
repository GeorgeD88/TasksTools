from googleapiclient.discovery import build #, Resource
from googleapiclient.errors import HttpError
from myutils import *
# temporary VVV
from auth import auth


class TasksTools:

    def __init__(self, credentials):
        """ Creates a TasksTools object given the authorized creds. """
        # Google Tasks API authentication and service
        try:
            self.api = build('tasks', 'v1', credentials=credentials)
        except HttpError as err:
            print(err)
            quit()
        self.tasklists = None  # tasklists cache

    def __get_tasklists_cache__(self):
        """ Caches tasklists to avoid repeat requests. """
        if self.tasklists is None:
            return None
        else:
            return self.tasklists

    def __reset_tasklists_cache__(self):
        """ Empty tasklists cache as it's going to be changed. """
        if self.tasklists is not None:
            self.tasklists = None

    def __page__(self, body, original_request, results: dict):
        """ Pages API call. """
        # puts together paging request and then returns the new response
        next_request = body.list_next(original_request, results)
        return next_request.execute()

    def get_tasklists(self, max_results: int = None):
        """ Gets all user's task lists. """
        check_cache = self.__get_tasklists_cache__()
        if check_cache is not None:
            return check_cache

        body = self.api.tasklists()  # would be .tasks() for getting tasks
        request = body.list(maxResults=max_results)  # full request with list method
        results = request.execute()  # executes request and saves result

        # creates total dict to hold all tasklists acquired
        self.tasklists = {"kind": results["kind"], "items": results["items"]}

        # keeps paging result as long there's a next page token
        while 'nextPageToken' in results:
            # (base request + method, previous results)
            results = self.__page__(body, request, results)  # gets next result
            # adds new tasklists acquired to total dict
            self.tasklists["items"].extend(results["items"])

        return self.tasklists

    def get_tasklist(self, _id: str):
        """ Gets specified tasklist. """
        return self.api.tasklists().get(tasklist=_id).execute()

    def get_tasks(self, _id: str, max_results: int = None):
        """ Gets tasks from specified tasklist. """
        body = self.api.tasks()
        request = body.list(tasklist=_id, maxResults=max_results)
        results = request.execute()

        # creates total dict to hold all tasks acquired
        tasks = {}
        for k in results:
            if k == 'nextPageToken':
                continue
            tasks[k] = results[k]

        # keeps paging result as long there's a next page token
        while 'nextPageToken' in results:
            # (base request + method, previous results)
            results = self.__page__(body, request, results)  # gets next result
            # adds new tasklists acquired to total dict
            tasks["items"].extend(results["items"])

        return tasks

    def new_tasklist(self, title: str):
        """ Creates new tasklist. """
        # NOTE: Fails with HTTP code 403 or 429 after reaching the storage limit of 2,000 lists.
        response = self.api.tasklists().insert(body={'title': title}).execute()

        # Checks if there's a tasklist cached and appends it to it
        check_cache = self.__get_tasklists_cache__()
        if check_cache is not None:
             self.tasklists["items"].append(response)
             return response
        self.__reset_tasklists_cache__()

    def delete_tasklist(self, _id: str):
        """ Deletes tasklist. """
        return self.api.tasklists().delete(tasklist=_id).execute()


creds = auth()
tasks = TasksTools(credentials=creds)  # API object

edc_prep_id = "TkliYV82a1Zvb1VjQmQ0bA"
# edc_prep = tasks.get_tasks(edc_prep_id)
# write_json(edc_prep, 'edc_prep')
print(tasks.delete_tasklist(edc_prep_id))