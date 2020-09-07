from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url=["https://www.universityadmissions.se/intl/search?period=10&courseProgram=programs&semesterPart=0&languageOfInstruction=en"
]
#secondurl = "https://www.universityadmissions.se/intl/search?period=12&courseProgram=programs&semesterPart=0&languageOfInstruction=en&numberOfFetchedPages=3"
filename = "Sweden_English_Programs.csv"
f = open(filename, "w")

headers = "program_name, college_name, college_location, total_tuition_fee, total_credits, subject_areas, application_code, teaching_form, pace_of_study\n"

f.write(headers)
for a in my_url:

    #open up connection + grab the page
    uClient = uReq(a)
    #load content into the variable
    page_html = uClient.read()
    uClient.close()

    #html parsing
    page_soup = soup(page_html, "html.parser")

    #grabs each course
    containers = page_soup.findAll("div", {"class": "namearea"})

    

    #obtains the program information
    for container in containers:
        #Program Name
        course_container = container.find("h3", {"class":"heading4"})
        program_name = "\""+course_container.text.strip()+"\""

        #College Name, Location, Credits 
        credits=container.findAll("span", {"class": "appl_fontsmall"})[0].get_text()
        cul = container.findAll("span", {"class": "appl_fontsmall"})[1].get_text()
        if(cul.find("Credits,")!=-1):
            cul=cul.replace("Credits,","")
        if(cul.find("Location:"))!=-1:
            s=cul.split("Location:")
        if(s is not None and len(s)>1):
            uname="\""+s[0].strip()+"\""
            location="\""+s[1].strip()+"\""

        #Total Tuition Fee
        totalfees = container.find("div", {"class":"fees"})
        
        fee="\""+totalfees.findAll("p")[1].get_text().replace("Total tuition fee:", "")+"\""
       
      
        #Subject Areas
        sub = container.find("div",{"class":"coursecolumncontent"})        
        a=sub.find("p").get_text()
        if(a.find("Subject Areas:")!=-1):
            a=a.replace("Subject Areas:","")
        
        #Application Code 
        app=container.find("div", {"class": "coursecolumn"})
        if app is not None:
            app_codes2 = app.findAll("p")
            x=app_codes2[3]
            x="\""+x.get_text().replace("Application code:", "")+"\""
        
        #Teaching Form
        app2=container.findAll("div", {"class": "coursecolumn"})[1]
        if app2 is not None: 
            teach_form = app2.findAll("p")
            t=teach_form[0]
            t="\""+t.get_text().replace("Teaching form:", "")+"\""

        #Pace of Study 
        if app2 is not None: 
            pace = app2.findAll("p")
            p=pace[1]
            p=p.get_text()
            if(p.find("Pace of study:")!=-1): 
                p="\""+p.replace("Pace of study:", "")+"\""
            else:
                s=pace[2]
                p="\""+s.get_text().replace("Pace of study:", "")+"\""
        

        f.write(program_name + "," + uname.replace("\n","").replace("\t","") + "," + location.replace("\n","").replace("\t","") + "," +fee.replace("\n","").replace("\t","") + ","+ credits.replace("\n","").replace("\t","") +","+"\""+a+"\""+","+x.replace("\n","").replace("\t","") +","+ t.replace("\n","").replace("\t","")+","+p.replace("\n","").replace("\t","")+"\n")

    f.close()