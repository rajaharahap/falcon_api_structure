from library import *
import os


class Class__(object):
    def __init__(self):
        self.db = db.dbQuery

    def path_url(self):
        if os.name == "nt":
            path_split = str(__file__).split('\\')
        else :
            path_split = str(__file__).split('/')
        # print(__file__)

        # print(path_split)
        start = False
        i = 0
        total = len(path_split)
        url_path_modul = ''
        while (i < (total - 1)):

            if start:
                url_path_modul = url_path_modul + path_split[i] + "/"
            elif path_split[i] == "modules":
                start = True
            i += 1
        return url_path_modul + self.__class__.__name__.lower()

    def on_get(self, req, resp, action):
        getattr(self, action)(req, resp)

    def on_post(self, req, resp, action):
        getattr(self, action)(req, resp)


router.api.add_route("/api/"+Class__().path_url()+ "/{action}", Class__())