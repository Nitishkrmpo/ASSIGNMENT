from flask import Flask , request  ,render_template  #flask provide the utility named  request for to read whatever is send to the sever(flask application )
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='ideaapp'

mysql=MySQL(app)
@app.route('/')
def Home():
    cur=mysql.connection.cursor()
    cur.execute("")   ##SQL QUERY
    fetchdata = cur.fetchall()
    cur.close()

    return render_template('home.html', data= fetchdata)

#Create the idea repository
ideas ={
    1: {
        "id": 1,
        "idea_name": "ONDC",
        "idea_description": "Details about ONDC",
        "idea_author": "Adeeb"
    },
    2: {
        "id" : 2,
        "idea_name": "Save Soil",
        "idea_ description" : "Details  about Saving soil",
        "idea_author":"Ankit Sharma" }
}
'''
Create an Restful endpoint for fetching all the data
'''
#first api
@app.get("/ideaapp/api/v1/ideas")  #decorator   
def get_all_ideas():
    #Logic to fetch all the ideas and support query params {support query parameter is used for conditional fetching }

    #I need to read the query param
    idea_author = request.args.get('idea_author') #check for idea_author is present or not  
    if idea_author:
        #filter the idea created by this author 
        idea_res={}
        for key, value in ideas.items():
            if value["idea_author"]== idea_author:
                idea_res[key] = value
        return idea_res
    #Logic to fetch all the ideas and support query params 
    return ideas

    #Logic to fetch all the ideas 
    idea_author = request.args.get('idea_author')
    return ideas 


# testing of the restful api  postman is used 

'''
Create a Restful endpoint for creating  a new idea 
'''
@app.post("/ideaapp/api/v1/ideas")
def create_idea():
    #logic to create a new idea 
    try:
    #first read the request body
        request_body = request.get_json()  #this represents the request body passed by the user is converted to json format  
    #check if the idea id passed is not present already
        if request_body["id"] and request_body["id"] in ideas:
            return "ideas with the same id is already present",400  #HTTP status code 
    #Insert the passed idea in the ideas dictionary 
        ideas[request_body["id"]] = request_body
    #return the response saying idea got saved 
        return "ideas created and saved successfully",201
    except KeyError:
        return "id is missing",400
    except:
        return "Some internal server error ", 500
    
'''
End point to fetch idea based on the id 
'''
@app.get("/ideaapp/api/v1/ideas/<idea_id>")
def get_idea_id(idea_id):
    try:
        if int(idea_id) in ideas:
            return ideas[int(idea_id)],200
        else:
            return "Idea id passed is not present",400
    except:
        return "Some internal error happened",500
    

'''
End point for updating the idea 
'''
@app.put("/ideaapp/api/v1/ideas/<idea_id>")
def update_idea(idea_id):
    try:
        if int(idea_id) in ideas:
            ideas[int(idea_id)]=request.get_json()
            return ideas[int(idea_id)],200
        else:
            return "Idea is passed is not present",400
    except:
        return "Some internal error happened",500

'''
End point to delete an idea 
'''
@app.delete("/ideaapp/api/v1/ideas/<idea_id>")
def delete_idea(idea_id):
    try:
        if int(idea_id) in ideas:
            ideas.pop(int(idea_id))
            return "Idea got successfully removed"
        else:
            return "Idea id passed is not present",400
    except:
        return "Some internal error happened",500




if __name__ =='__main__':
    app.run(port=8080)

'''
#stored in memory of the file in ram so,whenever it is we store the data it get lost 
path param:take you to a specific resource {Get 127.0.0.1:8080/ideaapp/api/v1/ideas/3}
query param: give you a filtered result  {ideas? author_name = Nitish}
'''

'''
Flask uses single thred doen't able to manage large about data
'''

'''
monogodb:Dyanamic schema(if one server can't accomodate the data )

mysql: fixed scehma (Time tested database means older than mongo and Transcation work very well
'''









































