def scrapper(targetusername) :
    import time
    import appium
    import instaloader
    from appium import webdriver
    from selenium.common import StaleElementReferenceException
    from selenium.webdriver.common.actions import interaction
    from selenium.webdriver.common.actions.action_builder import ActionBuilder
    from selenium.webdriver.common.actions.pointer_input import PointerInput
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from appium.webdriver.common.touch_action import TouchAction
    from selenium.webdriver.common.action_chains import ActionChains
    from appium.webdriver.common.touch_action import TouchAction
    import re
    import os


    userpass = open("userpass.txt","r")
    UserPassR = userpass.read()
    UserPassL = UserPassR.split(":")
    userid = UserPassL[0]
    password = UserPassL[1]

    #print("id: ",userid,"\n","pass: ",password)
    #input()

    Xrate = open ("Xrate.txt","r")
    XrateR = Xrate.read()
    XrateNumber = int(XrateR)
    print ("X rate number: ",XrateNumber)


    def capabilities():
        desired_caps = {}
        desired_caps['automationName'] = "UIAutomator2"
        desired_caps['platformName'] = 'Android'
        #For running server:
        #appium --platform-name "Android"
        desired_caps['deviceName'] = 'OnePlus5'
        desired_caps["appPackage"] = 'com.instagram.android'
        desired_caps['appActivity'] = '.activity.MainTabActivity'
        desired_caps["noReset"] = "true"
        desired_caps["fullReset"] = "false"

        # ANDROID_HOME = {}
        # ANDROID_HOME[]

        # desired_caps['ANDROID_SDK_ROOT'] = r'C:\Users\Safir\Desktop\SDK'

        return webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


    driver = capabilities()
    #input ("test:")



    driver.implicitly_wait(2)


    #Trying to login
    try :
        username_field = driver.find_element("xpath","//*[starts-with(@content-desc, 'Username, email or mobile number')]")
        password_field = driver.find_element("xpath","//*[starts-with(@content-desc, 'Password')]")
        username_field.click()

        entryfields = driver.find_elements("xpath","//*[starts-with(@class, 'android.widget.EditText')]")


        entryfields[0].send_keys(userid)

        password_field.click()
        #entryfield = driver.find_element("xpath","//*[starts-with(@class, 'android.widget.EditText')]")
        entryfields[1].send_keys(password)
        #

        login_button = driver.find_element("xpath","//*[starts-with(@content-desc, 'Log in')]")
        login_button.click()


        #Avoid saving info
        notNowButton = driver.find_element("xpath","//*[starts-with(@content-desc, 'Not now')]")
        notNowButton.click()

        pass

        try :
            notNowButton = driver.find_element("xpath", "//*[starts-with(@content-desc, 'Not now')]")
            notNowButton.click()
        except:
            pass

    except:
        print ("passing the sector 1")
        pass


    #try :
    #    BUTTONS = driver.find_elements("xpath","//*[starts-with(@class, 'android.widget.FrameLayout')]")
    #    for button in BUTTONS :
    #        searchbutton = driver.find_element("xpath","//*[starts-with(@content-desc, 'com.instagram.android:id/search_tab')]")
    #        searchbutton.click()
    #except:
    #    # open notifications section to avoid main page element mix bug
    #    notifButton = driver.find_element("xpath", "//*[starts-with(@resource-id, 'com.instagram.android:id/news_tab')]")
    #    notifButton.click()
    #    pass

    #driver.swipe(1500, 0, 5000, 0, 1000)

    wait = WebDriverWait(driver, 1)
    ### Searching user names



    #going to EXPLORE section
    #wait = WebDriverWait(driver,10)
    #time.sleep(10)

    wait.until(EC.visibility_of_element_located((By.XPATH, '//android.widget.FrameLayout[@content-desc="Search and explore"]/android.widget.ImageView')))
    exploreBTN = driver.find_element(By.XPATH, '//android.widget.FrameLayout[@content-desc="Search and explore"]/android.widget.ImageView')
    exploreBTN.click()




    #>using searchbar in EXPLORE section

    searchbar = driver.find_element(By.ID, "com.instagram.android:id/action_bar_search_edit_text")
    searchbar.click()
    entrysearchfield = driver.find_element(By.ID, "com.instagram.android:id/action_bar_search_edit_text")
    searchUser = "@" + targetusername
    entrysearchfield.send_keys(searchUser)

    # press enter to do the search
    driver.press_keycode(66)


    # Verify the found username
    #time.sleep(2)
    validateUSERNAMEtext = driver.find_element(By.ID,"com.instagram.android:id/row_search_user_username").text
    validateUSERNAME = driver.find_element(By.ID,"com.instagram.android:id/row_search_user_username")
    if validateUSERNAMEtext == targetusername :
        print ("validated!")
        # Enter the page
        validateUSERNAME.click()
    else :
        print ("invalid username , check your spelling")

    #full name of user
    user = driver.find_element(By.ID,"com.instagram.android:id/profile_header_full_name").text
    #print (user)




    # Scrolling function
    def scrollDown(X1,X2,Y1,Y2) :
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(X1, X2)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(Y1, Y2)
        actions.w3c_actions.pointer_action.release()
        actions.perform()


    # locate posts

    #first post
    #! problem , only one of those works and the other one gets ignored , so all posts won't be scanned
    #use full user name , and by to locate all posts
    contentDesc_list = []
    text = "by "+user
    #For identifying the end of posts
    scrollCounter = 0
    PostCounter = 0
    ListOfPostsParams = []
    ListOfLikes = []

    while True :
        #after checking 3 posts of a row
        for i in range(3) :
            try :
                xpath_expression = "//*[contains(@content-desc, '{}')]".format(text)
                posts = driver.find_elements("xpath", xpath_expression)
                for post in posts :
                    content = post.get_attribute("content-desc")
                    if content not in contentDesc_list :
                        print(content)
                        contentDesc_list.append(content)

                        #Defining post type for copy link section based on content text
                        PostType = "IGTV"
                        if "IGTV" in content :
                            PostType = "IGTV"
                        else:
                            PostType = "Others"
                        post.click()
                        #extracting data
                        #use try except cause there are two types of posts
                        ##likes
                        try :
                            PostContent = driver.find_element(By.ID, "com.instagram.android:id/carousel_image")
                        except :
                            PostContent = driver.find_element(By.ID, "com.instagram.android:id/media_group")
                        likesData = PostContent.get_attribute("content-desc")
                        Likes = likesData.split(",")
                        Likes = Likes[1].strip()
                        LikesNum = Likes.replace("likes","")
                        LikesNum = int(LikesNum)
                        print("Likes: ",LikesNum)
                        ##date
                        #date might be unaccessible in some posts , so if it was , just a little scroll
                        dateStat = False
                        while dateStat == False :
                            try:
                                date = driver.find_element("xpath", "//*[contains(@content-desc, 'ago')]")
                                dateText = date.get_attribute("content-desc")

                                m = re.search(r'(\w+\W+\w+)\W+ago', dateText)
                                # dateTest = dateText.split("ago")
                                if m:
                                    dateOfPost = m.group(1)
                                print("Date: ",dateOfPost)
                                dateStat = True
                            except:
                                scrollDown(312,988,309,884)
                        #input(PostContent.get_attribute("content-desc"))

                        PostCounter += 1
                        print("Post count: ",PostCounter)


                        #Getting links of posts and downloading
                        PostLink = None
                        if PostType == "IGTV":
                            #three dots
                            MoreActionsBTN = driver.find_element(By.ID,"com.instagram.android:id/feed_more_button_stub").click()
                            #copy link
                            CopyLinkBTN = driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]").click()
                            time.sleep(0.5)
                            PostLink = driver.get_clipboard('clipboard')
                            PostLink = PostLink.decode()
                            print(PostLink)
                            PostLink = PostLink.replace("https://","")
                            PostLink = PostLink.split("/")
                            #>postDownload = instaloader.Post.from_shortcode(L.context, PostLink[2])
                            downloadPATH = "IDs/"+validateUSERNAMEtext
                            #setting path and file name
                            #>post.download(filepath=downloadPATH,filename=validateUSERNAMEtext)

                            #> No need for backbutton , the scroll up window gets closed automatically after copying link
                            #driver.press_keycode(4)
                        elif PostType == "Others" :
                            shareBTN = driver.find_element(By.ID,"com.instagram.android:id/row_feed_button_share").click()
                            CopyLinkBTN = driver.find_element(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[3]/android.widget.ImageView").click()
                            time.sleep(0.5)
                            PostLink = driver.get_clipboard('clipboard')
                            PostLink = PostLink.decode()
                            print(PostLink)
                            PostLink = PostLink.replace("https://","")
                            PostLink = PostLink.split("/")
                            #>postDownload = instaloader.Post.from_shortcode(L.context, PostLink[2])
                            downloadPATH = "IDs/" + validateUSERNAMEtext
                            # setting path and file name
                            #>post.download(filepath=downloadPATH, filename=validateUSERNAMEtext)

                            driver.press_keycode(4)
                        #input(PostLink)





                        #variable that contains all info of one post
                        PostParameters = str(PostLink)+","+str(dateOfPost)+","+str(LikesNum)+","+str(user)+","+str(content)



                        #appending data to lists for main process of checking likes
                        ListOfPostsParams.append(PostParameters)
                        ListOfLikes.append(LikesNum)



                        print("---------------")


                        #click back to go to target page
                        backButton = driver.find_element(By.ID,"com.instagram.android:id/action_bar_button_back").click()
                        #Post has been seen , so set this to 0 cause it is used for time out and detecting the end of posts
                        scrollCounter = 0


            except StaleElementReferenceException:
                continue


        if scrollCounter > 2 :
            print ("this page is out of posts")
            len(contentDesc_list)
            break
        else :
            scrollDown(245, 559, 248, 335)
            scrollCounter += 1
            print(scrollCounter)

        if PostCounter == 1000 :
            print ("1000 posts scanned")
            break


    def datasaver(FileName,Data) :
        FileName = str(FileName)+".txt"
        datafile = open(FileName,"w")
        datafile.write(Data)
        datafile.close()

    def datacopy(FileName) :
        try:
            path = "IDs\\_"+validateUSERNAMEtext+"\\"+str(FileName)
            with open(FileName, 'r') as fp1, \
                open(path, 'w') as fp2:
                results = fp1.read()
                fp2.write(results)
        except Exception as e:
            print('Error: ' + str(e))

    # calculation based on client's order
    indexNum = 0
    for index in ListOfPostsParams:
        print(index)
        # The lower indexes
        try:
            Last1 = ListOfLikes[indexNum] - ListOfLikes[indexNum - 1]
            Last2 = ListOfLikes[indexNum] - ListOfLikes[indexNum - 2]
            print(Last1, Last2)
        except:
            pass
        # The higher indexes
        try:
            next1 = ListOfLikes[indexNum] - ListOfLikes[indexNum + 1]
            next2 = ListOfLikes[indexNum] - ListOfLikes[indexNum + 2]
            print(next1, next2)
        except:
            pass

        if next1 > XrateNumber or next2 > XrateNumber or Last1 > XrateNumber or Last2 > XrateNumber:
            print(ListOfLikes[indexNum]," This index is selected ", indexNum)
            TheSelectedPost = ListOfPostsParams[indexNum]
            TheSelectedPostS = TheSelectedPost.split(",")
            SelectedLink = TheSelectedPostS[0]

            #break
        else:
            indexNum += 1


    ##>> Move try except out of loop
    # Download , save details.
    ## Try to download , cause there might be a connection problem
    #Downloads file + create txt
    try :
        L = instaloader.Instaloader()
        L.login(userid, password)
        postDownload = instaloader.Post.from_shortcode(L.context, PostLink[2])
        downloadPATH = "IDs/" + validateUSERNAMEtext
        # setting path and file name
        post.download(filepath=downloadPATH, filename=validateUSERNAMEtext)
        # File data save
        ##Data

        FileName = validateUSERNAMEtext + "_X" + str(XrateNumber) + "_" + str(dateOfPost) + "_" + str(LikesNum)
        Data = ListOfPostsParams[indexNum]
        ##Files
        ###Save data to a file
        datasaver(FileName, Data)
        ###copy it to desired directory

        ### delete the recent file in main directory
        FileNameActual = FileName + ".txt"
        datacopy(FileNameActual)
        os.remove(FileNameActual)
        #x = awdawd
    except:
        #Only creates txt
        #File data save
        # File data save
        ##Data
        FileName = validateUSERNAMEtext+"_X"+str(XrateNumber)+"_"+str(dateOfPost)+"_"+str(LikesNum)
        Data = ListOfPostsParams[indexNum]
        ##Files
        ###Save data to a file
        datasaver(FileName, Data)
        ###copy it to desired directory

        ### delete the recent file in main directory
        FileNameActual = FileName+".txt"
        datacopy(FileNameActual)
        os.remove(FileNameActual)

    ###########################
    #
    # Loop = True
    # NewPost = True
    # #List of all elements and posts
    # ElementsList = []
    # while Loop == True :
    #     #try except is for the time that program hasn't scrolled enough to locate object , so scroll again
    #     #try :
    #     #element that might be post
    #     Post = driver.find_element(By.ID,"com.instagram.android:id/zoomable_view_container")
    #
    #     #Getting data of posts
    #     try :
    #         if NewPost == True :
    #             PostContent = driver.find_element(By.ID,"com.instagram.android:id/media_group")
    #             if PostContent in ElementsList :
    #                 NewPost = False
    #             else :
    #                 ElementsList.append(PostContent)
    #                 PostContent_desc = PostContent.get_attribute("content-desc")
    #
    #                 likes = PostContent_desc.split(",")
    #                 Likes = likes[1].strip()
    #                 print(Likes)
    #
    #             #if "ago" in PostContent_desc :
    #             #    pass
    #             #else:
    #             date = driver.find_element("xpath","//*[contains(@content-desc, 'ago')]")
    #             if date in ElementsList :
    #                 NewPost = False
    #             else:
    #                 ElementsList.append(date)
    #
    #                 dateText = date.get_attribute("content-desc")
    #                 #m = re.search('(.+?)ago', dateText)
    #                 #dateTest = dateText.split("ago")
    #                 m = re.search(r'(\w+\W+\w+)\W+ago', dateText)
    #                 if m:
    #                     dateOfPost = m.group(1)
    #                 print(dateOfPost)
    #                 ElementsList.append(Post)
    #                 NewPost = False
    #                 print(":::")
    #
    #
    #
    #     except:
    #         if NewPost == True:
    #             PostContent = driver.find_element(By.ID,"com.instagram.android:id/carousel_image")
    #             if PostContent in ElementsList :
    #                 NewPost = False
    #             else :
    #                 ElementsList.append(PostContent)
    #                 PostContent_desc = PostContent.get_attribute("content-desc")
    #
    #                 likes = PostContent_desc.split(",")
    #                 Likes = likes[1].strip()
    #                 print(Likes)
    #
    #
    #             #if "ago" in PostContent_desc :
    #             #    pass
    #             #else:
    #             date = driver.find_element("xpath","//*[contains(@content-desc, 'ago')]")
    #             if date in ElementsList :
    #                 NewPost = False
    #             else :
    #                 ElementsList.append(date)
    #
    #                 dateText = date.get_attribute("content-desc")
    #
    #                 m = re.search(r'(\w+\W+\w+)\W+ago', dateText)
    #                 #dateTest = dateText.split("ago")
    #                 if m:
    #                     dateOfPost = m.group(1)
    #                 print(dateOfPost)
    #                 ElementsList.append(Post)
    #                 NewPost = False
    #                 print(":::")
    #
    #
    #
    #
    #
    # ## com.instagram.android:id/media_group_container resource-id
    #
    #     #com.instagram.android:id/media_group
    #     #com.instagram.android:id/carousel_image
    # #>>>>>
    #     #scroll to next post
    #     #scrollDown(325,834,338,289)
    #     #scrollDown(335, 951, 341, 782)
    #     num = 0
    #     #required posts to scrap data if the page has this amount
    #     PostNum = 1000
    #     test_element = driver.find_element(By.ID,"com.instagram.android:id/zoomable_view_container")
    #     test_date_element = driver.find_element("xpath","//*[contains(@content-desc, 'ago')]")
    #     try:
    #         test_content_element = driver.find_element(By.ID, "com.instagram.android:id/carousel_image")
    #     except:
    #         test_content_element = driver.find_element(By.ID, "com.instagram.android:id/media_group")
    #     while test_element == Post :
    #         test_element = driver.find_element(By.ID, "com.instagram.android:id/zoomable_view_container")
    #         #scrollDown(325,834,338,289)
    #         scrollDown(245, 559, 248, 335)
    #         test_element = driver.find_element(By.ID, "com.instagram.android:id/zoomable_view_container")
    #         test_date_element = driver.find_element("xpath","//*[contains(@content-desc, 'ago')]")
    #         try :
    #             test_content_element = driver.find_element(By.ID,"com.instagram.android:id/carousel_image")
    #         except :
    #             test_content_element = driver.find_element(By.ID,"com.instagram.android:id/media_group")
    #         #time.sleep(1)
    #         #scrollDown(335,951,341,782)
    #         if test_element != Post:
    #             if test_element not in ElementsList:
    #                 if test_date_element not in ElementsList:
    #                     NewPost = True
    #                     break
    #
    #
    #         scrollDown(245, 559, 248, 335)
    #         #scrollDown(245, 559, 248, 335)
    #         #test_element = driver.find_element(By.ID, "com.instagram.android:id/zoomable_view_container")
    #         num = num + 1
    #         print (num)
    #         PostNum = PostNum - 1
    #         # Posts time out , if program searches 5 times for new posts and doesn't find any , it understands it' the end
    #         if num == 5 :
    #             #meaning we reached the end of posts
    #             Loop = False
    #             print ("all posts visited")
    #             break
    #
    #         if PostNum <= 0 :
    #             print('1000 posts visited')
    #             break
    #     #except :
    #     #    scrollDown(335, 951, 341, 782)
    #     #    time.sleep(5)
    #
    #
    #
    #
