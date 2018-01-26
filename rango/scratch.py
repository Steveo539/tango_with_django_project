python_pages = [
{"title":"Official Python Tutorial",
"url":"http://docs.python.org/2/tutorial/"},
{"title":"How to Think like a Computer Sicentist",
"url":"http://www.greenteapress.com/thinkpython/"},
{"title":"Learn Python in 10 Minutes",
"url":"http://www.korokithakis.net/tutorials/python/"}]

django_pages = [
{"title":"Official Django Tutorial",
"url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
{"title":"Django Rocks",
"url":"http://www.djangorocks.com/"},
{"title":"How to Tango with Django",
"url":"http://www.tangowithdjango.com/"}]

other_pages = [
{"title":"Bottle",
"url":"http://bottleypy.org/docs/dev/"},
{"title":"Flask",
"url":"http://flask.pocoo.org"}]

cats = {"Python": {"pages": python_pages, "views":128, "likes":64}, #views and likes for 5.8   128,64
        "Django": {"pages": django_pages, "views":64, "likes":32}, #64 ,32
        "Other Frameworks": {"pages": other_pages, "views":32, "likes":16}} #32 ,16

def test():
    for cat in cats.keys():
        print(cat,cats[cat]["views"],cats[cat]["likes"])
        #print(cat["pages"])

if __name__ == "__main__":
    test()
