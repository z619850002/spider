from database import connection
import datetime

class Element:
    #The constructor.
    def __init__(self, title, date, url):
        self.title = title
        self.url = url
        self.date = date

    #Save this model in the database.
    def save(self):
        db = connection.DB()
        result = db.select("SELECT * FROM link WHERE title = ? AND url = ?"  , [str(self.title) , str(self.url)])
        #This item has not in the database.
        if len(result) > 0:
            #Delete the old item.
            db.modify("DELETE FROM link WHERE title = ? AND url = ?" , [str(self.title) , str(self.url)])
        result = db.modify("INSERT INTO link (title , url , dat) VALUES (? , ? , ?)", [str(self.title) , str(self.url) , self.date.strftime('%Y-%m-%d')])
        return result

    #Delete this model in the database.
    def delete(self):
        db = connection.DB()
        result = db.modify("DELETE FROM link WHERE title = ? AND url = ?", [str(self.title), str(self.url)])
        return result

    #Check if this model exist in the database.
    def check_exist(self):
        db = connection.DB()
        result = db.select("SELECT * FROM link WHERE title = ? AND url = ?", [str(self.title), str(self.url)])
        # This item has not in the database.
        if len(result) <= 0:
            return False
        return True

    #Some setters below.
    #Set the date.
    def set_date(self , date):
        self.date = date

    #Set the title.
    def set_title(self , title):
        self.title = title

    #Set the url.
    def set_url(self , url):
        self.url = url

def main():
    element = Element("test" , datetime.date.today() , "test")
    db = connection.DB()
    result = db.select("SELECT * FROM link WHERE title = ? AND url = ?" , [str(element._title) , str(element._url)])
    print(result)
    element.save()
    result = db.select("SELECT * FROM link WHERE title = ? AND url = ?", [str(element._title), str(element._url)])
    print(result)
    element.delete()
    result = db.select("SELECT * FROM link WHERE title = ? AND url = ?", [str(element._title), str(element._url)])
    print(result)

if __name__ == '__main__':
    main()