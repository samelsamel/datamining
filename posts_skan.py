# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import os
import csv 
selfProfile = "https://mbasic.facebook.com/profile.php?fref=pb"


def mfacebookToBasic(url):
    """Reformat a url to load mbasic facebook instead of regular facebook, return the same string if
    the url don't contains facebook"""

    if "m.facebook.com" in url:
        return url.replace("m.facebook.com", "mbasic.facebook.com")
    elif "www.facebook.com" in url:
        return url.replace("www.facebook.com", "mbasic.facebook.com")
    else:
        return url


class Person():
    """Basic class for people's profiles"""

    def __init__(self):
        self.name = ""
        self.profileLink = ""
        self.addLink = ""

    def __str__(self):
        s = ""
        s += self.name + ":\n"
        s += "Profile Link: " + self.profileLink
        if self.addLink != "":
            s += "Addlink ->: " + self.addLink
        return s

    def __repr__(self):
        self.__str__()


class Post():
    """Class to contain information about a post"""

    def __init__(self):
        self.posterName = ""
        self.text = ""
        self.numLikes = 0
        self.time = ""
        self.privacy = ""
        self.posterLink = ""
        self.linkToComment = ""
        self.linkToLike = ""
        self.linkToLikers = ""
        self.linkToReport = ""
        self.groupLink = ""
        self.linkToShare = ""
        self.linkToMore = ""
        self.numComents = 0
        self.commentsList = []

    def toDict(self):
        return self.__dict__.copy()

    def fromDict(self, d):
        self.__dict__ = d.copy()


    def __str__(self):
        s = "\nPost by " + self.posterName + ": "
        s += self.text + "\n"
        s += "Likes: " + str(self.numLikes) + " - "
        s += "Comments: " + str(self.numComents) + " - "
        s += self.time + " "
        s += " - Privacy: " + self.privacy + "\n-"
        s += "\n Comment -> " + self.linkToComment + "\n"
        return s

    def __repr__(self):
        return self.__str__()


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
    "(KHTML, like Gecko) Chrome/15.0.87"
)


class FacebookBot(webdriver.PhantomJS):
    """Main class for browsing facebook"""

    def __init__(self):
        # pathToPhantomJs ="
        """relativePhatomJs = "\\phantomjs.exe"
        service_args = None
        if images == False:
            service_args = ['--load-images=no', ]
        if pathToPhantomJs == None:
            path = self, os.getcwd() + relativePhatomJs
        else:
            path = pathToPhantomJs
            webdriver.PhantomJS.__init__(self, path, service_args=service_args)
        """
        webdriver.PhantomJS.__init__(self, executable_path="C:\\Users\\Ska\\AppData\\Roaming\\npm\\node_modules\\phantomjs-prebuilt\\lib\\phantom\\bin\\phantomjs.exe",desired_capabilities=dcap)
        
        self.set_window_size (1000,500)
    def get(self, url):
        """The make the driver go to the url but reformat the url if is for facebook page"""
        super().get(mfacebookToBasic(url))
        self.save_screenshot("Debug.png")

    def login(self, email, password):
        """Log to facebook using email (str) and password (str)"""

        url = "https://mbasic.facebook.com"
        self.get(url)
        email_element = self.find_element_by_name("email")
        email_element.send_keys(email)
        pass_element = self.find_element_by_name("pass")
        pass_element.send_keys(password)
        pass_element.send_keys(Keys.ENTER)
        try:
            #self.find_element_by_name("x_message")
            print("Logged in")
            return True
        except NoSuchElementException as e:
            print("Fail to login")
            return False

    def logout(self):
        """Log out from Facebook"""

        url = "https://mbasic.facebook.com/logout.php?h=AffSEUYT5RsM6bkY&t=1446949608&ref_component=mbasic_footer&ref_page=%2Fwap%2Fhome.php&refid=7"
        try:
            self.get(url)
            return True
        except Exception as e:
            print("Failed to log out ->\n", e)
            return False
    def getReviews(self,url) :
        self.get(url)
        links_list =[]
        
        for d in self.find_elements_by_class_name('be') :
            for a in d.find_elements_by_tag_name('a'):
                links_list.append (a.get_attribute('href'))
        links_list=list ( set(links_list) ) 
        for l in links_list :
            self.get(l)
            try : 
                post = self.find_element_by_tag_name('p').text
                yield [post]
            except Exception as e:
                #print(e)
                print(" Can't get more posts")             
    def getPostInGroup(self, url, deep=10, moreText="Afficher plus de publications"):
        """Get a list of posts (list:Post) in group url(str) iterating deep(int) times in the group
        pass moreText depending of your language, i couldn't find a elegant solution for this"""

        self.get(url)
        ids = [chr(i) for i in range(ord('a'),ord('z')+1)]
        for i in range (10) :
            ids.append (str(i) )
        
        posts = []
        for n in range(deep):
            print("Searching, deep ",n)
            for i in ids:
                # print(i)
                post = Post()
                try:
                    p = self.find_element_by_id("u_0_" + str(i))
                    # print(p.text)
                    a = p.find_elements_by_tag_name("a")
                    
                    
                    post.posterName = a[0].text
                    try:
                        post.numLikes = int(a[3].text.split(" ")[0])
                    except ValueError:
                        post.numLikes = 0
                    post.text = p.find_element_by_tag_name("p").text
                    post.time = p.find_element_by_tag_name("abbr").text
                    # p.text.split("")[1].split("\n")[0]
                    post.privacy = self.title
                    post.posterLink = a[0].get_attribute('href')
                    # p.find_element_by_class_name("du").get_attribute('href')
                    post.linkToComment = a[2].get_attribute('href')
                    post.linkToLike = a[4].get_attribute('href')
                    try:
                        post.numComents = int(a[6].text.split(" ")[0])
                    except ValueError:
                        post.numComents = 0
                    # post.linkToShare = a[5].get_attribute('href')
                    post.linkToLikers = a[1].get_attribute('href')
                    post.linkToMore = a[6].get_attribute('href')
                    if post not in posts:
                        posts.append(post)
                except Exception:
                    continue
            try:
                more = self.find_element_by_partial_link_text(
                    moreText).get_attribute('href')
                self.get(more)
            # self.find_element_by_partial_link_text(moreText)
            except Exception as e:
                print(e)
                print(" Can't get more posts")
        print ( posts)
        return posts
    def getCommentsInPost(self, url, deep=10, moreText="Commentaires précédents…"):
        """Get a list of posts (list:Post) in group url(str) iterating deep(int) times in the group
        pass moreText depending of your language, i couldn't find a elegant solution for this"""

        self.get(url)    
        comments = []
        for n in range(deep):
            print("Searching, deep ",n)
            h_list = self.find_elements_by_tag_name('h3')
            for h in h_list :
                c = h.find_elements_by_xpath('following-sibling::div[1]')
                for comment in c :
                    comments.append(comment.text)
                    print ( comment.text )
            try:
                more = self.find_element_by_partial_link_text(
                    moreText).get_attribute('href')
                self.get(more)
            # self.find_element_by_partial_link_text(moreText)
            except Exception as e:
                print(e)
                print(" Can't get more posts")                
        return comments
if __name__ == '__main__':
    bot = FacebookBot()
    bot.login("phion140@gmail.com", "Jihen93513")
    for rv in bot.getReviews(url="https://mbasic.facebook.com/smugslamarsa/reviews?refid=17&ref=places_top_module_see_more"):
        print (rv)
    
    #posts = bot.getPostInGroup(deep=1,url="https://mbasic.facebook.com/groups/search/?groupID=1898374047109403&query=smug")
    
    #output_file = open ('comment.csv','w',newline='',
                            #encoding='utf-8')
    #output = csv.writer(output_file, delimiter=';',quotechar='"')    
    #for post in posts:
        #output.writerow([post.text, bot.getCommentsInPost(deep=8,url=post.linkToComment )] ) 
    #output_file.close()
    bot.save_screenshot("debug.png")  
    bot.close()
    
    