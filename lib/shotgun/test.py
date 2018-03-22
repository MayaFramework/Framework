import shotgun_api3 as sapi
# sg = sapi.Shotgun("https://esdip.shotgunstudio.com",
#                   login="asierra", password="Ba090313ba-")
# #print sg.authenticate_human_user(user_login="asierra", user_password="Ba090313ba-")
# print sg.find_one("HumanUser", filters=[["name", "is", "Alberto Sierra"]], fields=["login", "image"])

"""

TODO Hay que dividir las clases de tal manera que esten todas relacionadas y conectadas. Por ejemplo. A un Shotgun, le puedes pedir un User, 
y te va a devolver un User Class. El User Class, a su vez, tiene sus properties y sus metodos. Un User tiene Task, asi que por cada tarea, te devuelve
una Task Class, y asi recursivamente

"""

from shotgunInit import ShotgunInit

a = ShotgunInit()
user = a.getUser("Alberto Sierra")
print user.getUserImage()
