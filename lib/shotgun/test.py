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

# fields = ['id', 'name', 'sg_shot', 'code']


# sg = sapi.Shotgun("https://esdip.shotgunstudio.com",
#                                     script_name="shotgunAPI", api_key="f8da64a710923a25352e3d0e06bd31c56395cb5943e03bfaf9a90a73794e1ac1")

# print sg.schema_entity_read()
# print sg.find("Sequence", [["project", "is", {"type":"Project", "id":86}]], ["code", "name"])
# secId = sg.find_one("Sequence", [["code", "is", "TST"]], fields)
# print sg.find("Shot", [["sg_sequence", "is", {"type":"Sequence", "id":secId.get("id")}]], ["code"])
# print sg.find("Shot", [["code", "is", "tst.180"]], ["sg_sequence"])

# seqs = sg.find("Sequence",filters ,fields)
# print seqs

# from shotgunInit import ShotgunInit

# a = ShotgunInit()
# user = a.getUser("Alberto Sierra")
# print user.getUserImage()

from shotgunInit import ShotgunInit

sg = ShotgunInit()
print sg.getSeqs(names=True)