from os import path
import json

def get_chrome_bookmark_list(items):
    def _get_bookmark_list(items, path):
        return_list = [] 

        if isinstance(items, list):
            for item in items:
                return_list += _get_bookmark_list(item, path + "/" + item["name"])

        if isinstance(items, dict):
            if not (("name" in items) and ("type" in items)):
                return return_list

            if(items["type"] == "folder"):
                return_list += _get_bookmark_list(items['children'], path)
            else:
                bookmark = items['name'] + " ~ " + items['url']
                return_list.append(bookmark)

        return return_list

    return _get_bookmark_list(items, "")

class ChromeBookmarksParser:
    def parse(self, folder=None, file_path=None) -> str:
        if file_path is None:
            bookmarks_path = path.expanduser("~") + "/.config/google-chrome/Default/Bookmarks"
        else:
            bookmarks_path = path.expanduser(file_path)


        if not path.isfile(bookmarks_path):
            print("No bookmarks file found!")
            exit()

        with open(bookmarks_path) as file:
            data = json.load(file)

        bookmark_list = get_chrome_bookmark_list(data['roots']["bookmark_bar"])

        return "\n".join(bookmark_list)

