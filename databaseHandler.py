
import sqlite3
from passlib.hash import bcrypt
import jwt, datetime, json

dictt = {}

# def dataSetup():
#     urlNames = 'itemList.xlsx'

#     namescsv = pandas.read_excel(urlNames)

#     Items = namescsv["Name"].head(283).tolist()
#     Needed = namescsv["Needed"].head(283).tolist()
#     last = ""
#     for i in range(len(Items)):
#         Name = Items[i]
#         if str(Name) == "nan" : Name = last
#         if Name == " Lower half-mask" : Name = "Lower half-mask"
#         if "FIR" in Needed[i]:
#             cont = 0
#             for l in Needed[i]:  # Mirar cuantos cuadrados tiene
#                 if l.encode() == b'\xe2\x96\xa2':
#                     cont+=1
#             questName = Needed[i].split(") (")[1][:-1]
                    
#             if Name in dictt.keys():
#                 contador, listaQuests = dictt[Name]
#                 cont+=contador
#                 listaQuests.append(questName)
#                 dictt[Name] = cont,listaQuests
#             else:
#                 dictt[Name] = cont,[questName]
                
            
#             last = Name
   
#     conn = sqlite3.connect('database.db')
    
#     c = conn.cursor()
#     c.execute("DROP TABLE IF EXISTS questItems")
        
#     c.execute('''CREATE TABLE questItems (itemName TEXT, neededCont INTEGER, questNames TEXT, image TEXT)''')

#     conn.commit()    

#     for k,(dc,q) in dictt.items():

#         strquest = ", ".join(q)
       
#         k = k.replace("'","")
#         strquest = strquest.replace("'","")
#         c.execute(f"INSERT INTO questItems VALUES ('{k}',{dc},'{strquest}','')")
#     conn.commit()    

def printData():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM questItems")
    print(c.fetchall())

def setImagev2(name,link):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"UPDATE questItems SET image='{link}' WHERE itemName = '{name}'")   
    conn.commit() 
    
# def setImage(name):
#     headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
#     }

#     json_data = {
#         'searchEntities': [
#             'Quest',
#             'Item',
#         ],
#         'query': f'{name}',
#     }
#     try:
#         response = requests.post('https://tarkov.help/en/search/entities/suggestion', headers=headers, json=json_data)
#         soup = BeautifulSoup(response.text, 'html.parser')
#         a_tag = soup.find('a')
#         href = a_tag['href']    
#         r = requests.get(f"https://tarkov.help{href}").text
#         soup = BeautifulSoup(r, 'html.parser')
#         meta_tag = soup.find("meta",  attrs={"name":"twitter:image"})
#         content = meta_tag["content"]
#         imagelink =f"https://tarkov.help{content}"
#         conn = sqlite3.connect('database.db')
#         c = conn.cursor()
#         c.execute(f"UPDATE questItems SET image='{imagelink}' WHERE itemName = '{name}'")
#         conn.commit()
#     except:
#         print("error")

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        # col[0] is the column name
        d[col[0]] = row[idx]
    return d

def getItemNames():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT itemName FROM questItems")
    rst = c.fetchall() # rst is a list of dict
    return rst

def getItems():
    conn = sqlite3.connect("database.db")
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("SELECT * FROM questItems")
    rst = c.fetchall() # rst is a list of dict
    return rst

def setupCredentials():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS credentials") 
    c.execute("CREATE TABLE credentials (nickname TEXT, password TEXT, token TEXT)")
    conn.commit()
    
def signUp(user, pwd):
    hash = bcrypt.using(rounds=12).hash(pwd)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    token = generate_token(user)
    c.execute("INSERT INTO credentials VALUES (?,?,?)", (user,hash,token))
    conn.commit() 
    initializeUser(user)


    
def login(user,pwd):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credentials WHERE nickname = ?", (user,))
    username,phash,token = c.fetchone()
    if bcrypt.verify(pwd,phash):
        if check_token(token) == "Token expired":
            token = generate_token(user) 
            c.execute(f"UPDATE credentials SET token='{token}' WHERE itemName = '{username}'")
        return token
    else:
        return "Invalid credentials"

def printCredentials():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM credentials") 
    l = c.fetchall()
    print(l)

def check_token(token):
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'
    user_id = payload['user_id']
    return user_id

secret_key = "my_secret_key"

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def setItemsTable():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS userItems") 
    c.execute("CREATE TABLE userItems (user TEXT, items JSON)")
    conn.commit() 

def getUserItems(user):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    print(user)
    c.execute(f"SELECT items FROM userItems WHERE user ='{user}' ")
    data = c.fetchone()[0]
    return data

def updateItems(user, items):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f"UPDATE userItems SET items = '{items}' WHERE user ='{user}'")  
    conn.commit()    
    return True

def initializeUser(user):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    initial = {}
    for item in getItemNames():
        initial[item[0]] = 0
    # if    
    c.execute("INSERT INTO userItems VALUES (?,?)", (user,json.dumps(initial)))
    conn.commit()
    
if __name__ == "__main__":
    # dataSetup()
    # printData()
    # namesList = getItemNames()
    # print(namesList)
    # for item in namesList:
    #        name, =item
    #        print(name)
    #        setImage(name)
    # setupCredentials()
    #signUp("pacorro","12343")
    # print(login("pacorro","12333"))
    # print(login("pacorro","12343"))
    # printCredentials()
    # setItemsTable()
    #initializeUser("manu")
    # setItemsTable()
    #initializeUser("manu")
    # print(getUserItems("manuwrwer"))
    # print(getItemNames())
    # setImagev2("42nd Signature Blend English Tea","https://cdn.tarkov-market.app/images/items/42nd_Signature_Blend_English_Tea_sm.png")
    # setImagev2("A-2607 knifes (brown)","https://cdn.tarkov-market.app/images/items/bars_a-2607-_95x18_sm.png")
    # setImagev2("Aramid fiber cloth","https://cdn.tarkov-market.app/images/items/aramid_fiber_cloth_sm.png")
    # setImagev2("Clin wiper","https://cdn.tarkov-market.app/images/items/Clin_wiper_sm.png")
    # setImagev2("CPU Fan","https://cdn.tarkov-market.app/images/items/CPU_Fan_sm.png")
    # setImagev2("Fleece cloth","https://cdn.tarkov-market.app/images/items/fleece_cloth_sm.png")
    # setImagev2("Heat-exchange alkali surface washer","https://cdn.tarkov-market.app/images/items/Heat-exchange_alkali_surface_washer_sm.png")
    # setImagev2("Iskra lunchbox","https://cdn.tarkov-market.app/images/items/Iskra_lunch_box_sm.png")
    # setImagev2("Ripstop cloth","https://cdn.tarkov-market.app/images/items/ripstop_cloth_sm.png")
    # setImagev2("Tushonka (long can)","https://cdn.tarkov-market.app/images/items/Can_of_delicious_beef_stew_sm.png")
    # setImagev2("Tushonka (short can)","https://cdn.tarkov-market.app/images/items/Can_of_beef_stew_sm.png")
    # setImagev2("UHF RFID Reader","https://cdn.tarkov-market.app/images/items/UHF_RFID_Reader_sm.png")
    # setImagev2("Ushanka ear-flap cap","https://cdn.tarkov-market.app/images/items/Ushanka_ear-flap_cap_sm.png")
    print("Main")