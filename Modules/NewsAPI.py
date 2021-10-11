from newsapi import NewsApiClient
import os

class NewsAPI(object):
    def __init__(self):
        self.api = NewsApiClient(api_key=os.environ.get("NEWSAPI_KEY"))
    
    def getTopHeadlines(self):
        req = self.api.get_everything(language="de", domains="tagesschau.de")
        reqArticle = req["articles"]
        headlineList = ""
        try:
            for x in range(5):
                if (reqArticle[x]["title"] not in headlineList):
                    headlineList += reqArticle[x]["title"] + "/PAUSE"
        except:
            pass

        return headlineList

    
    def getTopArticles(self):
        req = self.api.get_everything(language="de", domains="tagesschau.de")
        reqArticle = req["articles"]
        articleList = ""
        
        try:
            for x in range(3):
                if (reqArticle[x]["title"] not in articleList):
                    articleList += reqArticle[x]["title"] + "/PAUSE"
                    articleList += reqArticle[x]["content"].split("…")[0] + "/PAUSE/PAUSE"
        except:
            pass

        return articleList
        
    def getArticlesAbout(self, topic):
        req = self.api.get_everything(language="de", q=topic)
        reqArticle = req["articles"]
        articleList = ""
        try:
            for x in range(3):
                if (reqArticle[x]["title"] not in articleList):
                    articleList += reqArticle[x]["title"] + "/PAUSE"
                    articleList += reqArticle[x]["content"].split("…")[0] + "/PAUSE/PAUSE"
        except:
            pass

        return articleList

NA = NewsAPI()