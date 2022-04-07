from library import *
import hashlib
import json
import os


class Login(object):
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

    def sign_in(self, req, resp):
        # print("popopo")
        data = json.loads(req.get_param('param'))
        try:
            username = data['username']
            # password = self.generate_md5(data['password'])]
            password = data['password']
        except KeyError:
            username = ""
            password = ""

        ip_access = req.access_route
        if self._is_valid_user(username, password):
            resp.status = "200"
            # print("hasil token login")
            # print(auth.Auth().create_token(self.result, username, ip_access))
            resp.body = auth.Auth().create_token(self.result, username, ip_access)
        else:
            resp.status = "400"
            resp.body = json.dumps({"status": -1, "message": "Username Password Wrong"})

    def _is_valid_user(self, username, password):
        # cek di auth.py
        sql = f"""  
                    select nik, aa.name as name, id_user, role, company_id  from (
                    select * from master_user
                    where username='{username}' and password='{password}'
                    ) aa LEFT JOIN (
                    select * from master_user_group
                    )bb on aa.user_group_name = bb.name
                """
        # print(sql)

        res = self.db.executeToDict(sql)

        rowcount = len(res)
        if rowcount > 0:
            self.result = res[0]
            return True
        else:
            return False

    def generate_md5(self, string):
        xx = hashlib.md5()
        xx.update(string.encode('utf-8'))
        return xx.hexdigest()

router.api.add_route("/api/"+Login().path_url()+ "/{action}", Login())