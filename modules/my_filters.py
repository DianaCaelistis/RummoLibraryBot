from telegram.ext import UpdateFilter
import ujson


class UserEditing(UpdateFilter):
    def filter(self, update):
        database = ujson.load(open("db.json", "r"))
        uid = update.effective_chat.id
        if database["users"][str(uid)]["status"] == "adding_books":
            return True
        else:
            return False


class UserSearching(UpdateFilter):
    def filter(self, update):
        database = ujson.load(open("db.json", "r"))
        uid = update.effective_chat.id
        if database["users"][str(uid)]["status"]:
            search = database["users"][str(uid)]["status"]
            search = search.split("_")
            if search[0] == "search":
                return True
            else:
                return False
        else:
            return False


class UserAddingContactInfo(UpdateFilter):
    def filter(self, update):
        database = ujson.load(open("db.json", "r"))
        uid = update.effective_chat.id
        if database["users"][str(uid)]["status"] == "adding_contact_info":
            return True
        else:
            return False
