from flask import Flask, render_template, Response, request,flash,redirect,url_for
import sqlite3, re
from datetime import datetime, date,timedelta

app = Flask(__name__)

app.config["SECRET_KEY"]="dfaksf29f29fjsf0299r8741"

@app.route('/')
def index():  # put application's code here
    thisyear = datetime.today().year;
    years=[]
    for i in range(thisyear-100, thisyear+1):
        years.append(i)
    months = ["janvier", "fevrier", "mars","avril","mai","juin","juillet","aout",
           "septembre","octobre","novembre","decembre"]
    return render_template("index.html",years=years,months=months)

#Partie POS
@app.route('/POS')
def pos():  # put application's code here
    return render_template("POS.html")

@app.route('/get_product')
def get_product():  # put application's code here
    xml = "<?xml version='1.0'?>"
    xml = xml + '<racine>'
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("SELECT id,nom,prix FROM produit ORDER BY id")
    xml = xml + "<products>"
    row = curs.fetchone()
    while row:
        xml = xml + "<product>"
        xml = xml + "<num_product>{}</num_product>".format(row[0])
        xml = xml + "<pname>{}</pname>".format(row[1])
        xml = xml + "<price>{}</price>".format(row[2])
        xml = xml + "</product>"
        row = curs.fetchone()
    xml = xml + "</products>"
    xml = xml + '</racine>'
    db.commit()
    db.close()
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/get_sub_plan')
def get_sub_plan():  # put application's code here
    xml = "<?xml version='1.0'?>"
    xml = xml + '<racine>'
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("SELECT id,nom,prix,nombre_seance FROM plan_abonnement ORDER BY nombre_seance")
    xml = xml + "<plans>"
    row = curs.fetchone()
    while row:
        xml = xml + "<plan>"
        xml = xml + "<id_plan>{}</id_plan>".format(row[0])
        xml = xml + "<sp_name>{}</sp_name>".format(row[1])
        xml = xml + "<price>{}</price>".format(row[2])
        xml = xml + "<n_prest>{}</n_prest>".format(row[3])
        xml = xml + "</plan>"
        row = curs.fetchone()
    xml = xml + "</plans>"
    xml = xml + '</racine>'
    db.commit()
    db.close()
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/get_member_details', methods=["GET"])
def get_details_member():  # put application's code here
    xml = '<?xml version="1.0"?>'
    xml = xml + "<member>"
    if request.method == "GET":
        db = sqlite3.connect("database.db")
        curs = db.cursor()
        query = "SELECT nom, prenom, date_naissance, adresse, localite, code_postal, num_tel, date_insc,num_membre FROM membre WHERE num_membre=?"
        curs.execute(query, (request.args.get("num_membre"),))
        row = curs.fetchone()
        while row:
            xml = xml + "<lname>{}</lname>".format(row[0])
            xml = xml + "<fname>{}</fname>".format(row[1])
            xml = xml + "<dob>{}</dob>".format(row[2])
            xml = xml + "<ad>{}</ad>".format(row[3])
            xml = xml + "<loc>{}</loc>".format(row[4])
            xml = xml + "<pc>{}</pc>".format(row[5])
            xml = xml + "<pn>{}</pn>".format(row[6])
            xml = xml + "<sd>{}</sd>".format(row[7])
            xml = xml + "<num_member>{}</num_member>".format(row[8])
            row = curs.fetchone()
        xml = xml + "</member>"
        db.commit()
        db.close()
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/create_user', methods=["POST"])
def create_user():
    reNameSurname = r"[a-zA-Z ,.'-]{1,50}$"
    reDOB = r"^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$"
    reAdressLocality = r"^[#.0-9a-zA-Z\s,-]+$"
    reCP = r"^[a-z0-9][a-z0-9\- ]{0,10}[a-z0-9]$"
    rePN = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"

    currentDate = date.today().strftime("%Y-%m-%d")
    currentDateList = currentDate.split("-", 3)
    currentDateList[0] = int(currentDateList[0]) - 18
    currentDateMinus18Years = str(currentDateList[0]) + "-" + currentDateList[1] + "-" + currentDateList[2]

    xml = "<?xml version='1.0'?>"
    xml = xml + "<racine>"
    if request.method == "POST":
        areset = (
                    "name" in request.form and "fname" in request.form and "dob" in request.form and "adress" in request.form and "pc" in request.form and "locality" in request.form and "pn" in request.form)
        if areset:
            flag = True
            name = request.form["name"]
            fname = request.form["fname"]
            dob = request.form["dob"]
            adress = request.form["adress"]
            locality = request.form["locality"]
            pc = request.form["pc"]
            pn = request.form["pn"]
            xml = xml + "<msgs>"
            if re.match(reNameSurname, name) is None:
                xml = xml + "<msg>Un nom est une chaine non vide sans chiffre !</msg>"
                flag = False
            if re.match(reNameSurname, fname) is None:
                xml = xml + "<msg>Un prenom est une chaine non vide sans chiffre !</msg>"
                flag = False
            if re.match(reDOB, dob) is None:
                xml = xml + "<msg>La date n'as pas ete recue au format correct !</msg>"
                flag = False
            if currentDateMinus18Years < dob:
                xml = xml + "<msg>Il faut que le client soit majeur !</msg>"
                flag = False
            if re.match(reAdressLocality, adress) is None:
                xml = xml + "<msg>L'adresse n'est pas conforme !</msg>"
                flag = False
            if re.match(reAdressLocality, locality) is None:
                xml = xml + "<msg>La localite n'est pas conforme !</msg>"
                flag = False
            if re.match(reCP, pc) is None:
                xml = xml + "<msg>Le code postal n'est pas conforme !</msg>"
                flag = False
            if re.match(rePN, pn) is None:
                xml = xml + "<msg>Le numero de telephone n'est pas conforme !</msg>"
                flag = False
            xml = xml + "</msgs>"
            if flag:
                xml = xml + "<state>1</state>"
                db = sqlite3.connect("database.db")
                curs = db.cursor()
                curs.execute(
                    "INSERT INTO membre(prenom,nom,date_naissance,adresse,code_postal,localite,num_tel,date_insc)VALUES (?,?,?,?,?,?,?,?);"
                    , (fname, name, dob, adress, pc, locality, pn, currentDate,))
                db.commit()
                db.close()
            else:
                xml = xml + "<state>0</state>"
    else:
        xml = xml + "<state>0</state>"
    xml = xml + "</racine>"
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/create_arrival', methods=["POST"])
def create_arrival():
    success = False
    xml = "<?xml version='1.0'?>"
    if request.method == "POST":
        areset = ("id_member" in request.form and "id_sub" in request.form)
        if areset:
            now = datetime.now()
            currentHour = now.hour
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            curs.execute(
                "INSERT INTO arrivee(num_membre,h_arrive,date) VALUES(?,?,?) ",
                (request.form["id_member"], currentHour, date.today().strftime("%Y-%m-%d")))
            db.commit()
            db.close()
            if success:
                xml = xml + "<state>1</state>"
            else:
                xml = xml + "<state>0</state>"
    xml = xml + '</racine>'
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/send_leaving', methods=["POST"])
def send_leaving():
    success = False
    xml = "<?xml version='1.0'?>"
    xml = xml + "<racine>"
    if request.method == "POST":
        areset = ("id" in request.form)
        if areset:
            now = datetime.now()
            nextHour = now.hour+1
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            curs.execute(" SELECT num_membre,h_arrive FROM arrivee WHERE id = ?",
                         (request.form["id"],))
            row = curs.fetchone()
            if row:
                nm = row[0]
                ah = row[1]
            curs.execute(" SELECT id,seances_restantes FROM abonnement WHERE num_membre = ?",
                         (nm,))
            row = curs.fetchone()
            if row:
                rs = row[1]
                id_abonnement = row[0]
            seances_result=rs - ( nextHour- int(ah));
            if seances_result<0:
                seances_dues=0-seances_result
                r=range(0,seances_dues)
                for i in r:
                    curs.execute("INSERT INTO achat(type,num_marchandise,nom,date_achat,prix) VALUES(?,?,?,?,?) ",
                                 ("p", 3, "Une Seance", date.today().strftime("%Y-%m-%d"), 4.5,))
                curs.execute("UPDATE abonnement SET seances_restantes = ? WHERE id = ?",
                             (0, id_abonnement,))
            else:
                curs.execute("UPDATE abonnement SET seances_restantes = ? WHERE id = ?",
                             (seances_result, id_abonnement,))
            curs.execute(" UPDATE arrivee SET h_depart=? WHERE id = ?",
                         (nextHour ,request.form["id"]))
            db.commit()
            db.close()
            if success:
                xml = xml + "<state>1</state>"
            else:
                xml = xml + "<state>0</state>"
    xml = xml + '</racine>'
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/create_purchase', methods=["POST"])
def create_purchase():
    success = False
    xml = "<?xml version='1.0'?>"
    xml = xml + "<racine>"
    if request.method == "POST":
        areset = ("idPurchase" in request.form and "type" in request.form and "idMember" in request.form)
        if areset:
            currentDate = date.today().strftime("%Y-%m-%d")
            if request.form['type'] == 'p':
                db = sqlite3.connect("database.db")
                curs = db.cursor()
                curs.execute("SELECT nom,prix FROM produit WHERE id=?", (request.form["idPurchase"],))
                row = curs.fetchone()
                while row:
                    namePurchase = row[0]
                    pricePurchase = row[1]
                    row = curs.fetchone()
                curs.execute("INSERT INTO achat(type,num_marchandise,nom,date_achat,prix) VALUES(?,?,?,?,?) ",
                             ("p", request.form["idPurchase"], namePurchase, currentDate, pricePurchase,))
                success = (curs.rowcount > 0)
                db.commit()
                db.close()

            if request.form['type'] == 's':
                db = sqlite3.connect("database.db")
                curs = db.cursor()
                curs.execute("SELECT nom,prix,nombre_seance FROM plan_abonnement WHERE id=?",
                             (request.form["idPurchase"],))
                row = curs.fetchone()
                while row:
                    namePurchase = row[0]
                    pricePurchase = row[1]
                    nombreSeance = row[2]
                    row = curs.fetchone()
                curs.execute("INSERT INTO achat(type,num_marchandise,nom,date_achat,prix) VALUES(?,?,?,?,?) ",
                             ("s", request.form["idPurchase"], namePurchase, currentDate, pricePurchase))
                curs.execute(
                    "INSERT INTO abonnement(seances_restantes,seances_totales,date_achat,num_membre) VALUES(?,?,?,?) ",
                    (nombreSeance, nombreSeance, currentDate, request.form['idMember'],))
                success = (curs.rowcount > 0)
                db.commit()
                db.close()
            if success:
                xml = xml + "<state>1</state>"
            else:
                xml = xml + "<state>0</state>"
    xml = xml + '</racine>'
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/get_members')
def get_members():  # put application's code here
    xml = "<?xml version='1.0'?>"
    xml = xml + '<members>'
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("SELECT num_membre,nom, prenom, date_insc FROM membre ORDER BY num_membre")
    row = curs.fetchone()
    while row:
        xml = xml + "<member>"
        xml = xml + "<num_member>{}</num_member>".format(row[0])
        xml = xml + "<lname>{}</lname>".format(row[1])
        xml = xml + "<fname>{}</fname>".format(row[2])
        xml = xml + "<sd>{}</sd>".format(row[3])
        xml = xml + "</member>"
        row = curs.fetchone()
    xml = xml + '</members>'
    db.commit()
    db.close()
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/get_subs')
def get_subs():  # put application's code here
    xml = "<?xml version='1.0'?>"
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("SELECT id,seances_restantes,seances_totales,date_achat,membre.num_membre,prenom,nom FROM abonnement,membre WHERE abonnement.num_membre=membre.num_membre AND seances_restantes>0 ORDER BY date_achat DESC")
    xml = xml + "<subs>"
    row = curs.fetchone()
    while row:
        xml = xml + "<sub>"
        xml = xml + "<id>{}</id>".format(row[0])
        xml = xml + "<rs>{}</rs>".format(row[1])
        xml = xml + "<ts>{}</ts>".format(row[2])
        xml = xml + "<pd>{}</pd>".format(row[3])
        xml = xml + "<nm>{}</nm>".format(row[4])
        xml = xml + "<fn>{}</fn>".format(row[5])
        xml = xml + "<ln>{}</ln>".format(row[6])
        xml = xml + "</sub>"
        row = curs.fetchone()
    xml = xml + '</subs>'
    db.commit()
    db.close()
    return Response(xml, content_type='text/xml; charset=utf-8')

@app.route('/get_arrivals')
def get_arrivals():  # put application's code here
    xml = "<?xml version='1.0'?>"
    db = sqlite3.connect("database.db")
    curs = db.cursor()
    curs.execute("SELECT id,h_arrive,prenom,nom,h_depart FROM arrivee,membre WHERE date=? AND h_depart IS NULL AND arrivee.num_membre=membre.num_membre",(date.today().strftime("%Y-%m-%d"),))
    xml = xml + "<arrivals>"
    row = curs.fetchone()
    while row:
        xml = xml + "<arrival>"
        xml = xml + "<id>{}</id>".format(row[0])
        xml = xml + "<ah>{}</ah>".format(row[1])
        xml = xml + "<fn>{}</fn>".format(row[2])
        xml = xml + "<ln>{}</ln>".format(row[3])
        xml = xml + "</arrival>"
        row = curs.fetchone()
    xml = xml + '</arrivals>'
    db.commit()
    db.close()
    return Response(xml, content_type='text/xml; charset=utf-8')

#Partie flask

@app.route('/total_day',methods=["GET"])
def total_day():
    if request.method == "GET" and request.args.get("date") is not None:
            date = request.args.get("date")
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            query = "SELECT nom,prix,date_achat from achat WHERE date_achat=?"
            curs.execute(query, (date,))
            row = curs.fetchone()
            dic = {}
            while row:
                dic[row[0]] = row[1];
                row = curs.fetchone()
            db.commit()
            db.close()
            if len(dic) == 0:
                flash("Il n' y as pas d'achat pour ce jour!")
                return redirect(url_for("index"))
            sum=0.00;
            for i in dic.values():
                sum = sum + i;
            date = datetime.strptime(date, '%Y-%m-%d').date()
            return render_template("total_day.html",dic=dic,total=sum,day=date.strftime("%d/%m/%Y"))
    flash("Il n'y as pas d'achat pour ce jour!")
    return redirect(url_for("index"))

@app.route('/total_month',methods=["GET"])
def total_month():
    if request.method == "GET" and request.args.get("month") is not None \
            and request.args.get("year") is not None:
            year = request.args.get("year")
            month = request.args.get("month")
            begin= "{}-{}-01".format(year, month)
            dayend=0
            if int(month)==2:
                if int(year) % 4 == 0:
                    dayend = 29
                else:
                    dayend = 28
            else:
                if int(month)<=7:
                    if int(month)%2==0:
                        dayend=30
                    else:
                        dayend=31
                if int(month) > 7:
                    if int(month) % 2 == 0:
                        dayend = 31
                    else:
                        dayend = 30

            end = "{}-{}-{}".format(year, month,dayend)
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            query = "SELECT nom,prix,date_achat from achat WHERE date_achat>=? and date_achat<=? ORDER BY date_achat"
            curs.execute(query, (begin,end,))
            row = curs.fetchone()
            dic = {}
            for i in range(1,dayend+1):
                dic[i] = 0
            while row:
                currentday=int(row[2].split("-")[2])
                dic[currentday]=dic[currentday]+row[1]
                row = curs.fetchone()
            db.commit()
            db.close()
            sum = 0.00;
            for i in dic.values():
                sum = sum + i;
            return render_template("total_month.html",dic=dic,date="{}/{}".format(month,year),total=sum)
    flash("Il n'y as pas d'achat pour ce mois!")
    return redirect(url_for("index"))

@app.route('/total_year',methods=["GET"])
def total_year():
    if request.method == "GET" and request.args.get("year") is not None:
            months = ["janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout",
                  "septembre", "octobre", "novembre", "decembre"]
            year = request.args.get("year")
            begin = "{}-01-01".format(year)
            end = "{}-12-31".format(year)
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            query = "SELECT nom,prix,date_achat from achat WHERE date_achat>=? and date_achat<=? ORDER BY date_achat"
            curs.execute(query, (begin,end,))
            row = curs.fetchone()
            dic = {}
            lis = [0] * 12
            while row:
                currentmonth = int(row[2].split("-")[1])
                lis[currentmonth-1] = lis[currentmonth-1]+row[1]
                row = curs.fetchone()
            db.commit()
            db.close()
            sum = 0.00
            for i in range(0, len(months)):
                dic[months[i]] = lis[i]
                sum=sum+lis[i]
            return render_template("total_year.html",dic=dic,date="{}".format(year),total=sum)
    flash("Il n'y as pas d'achat pour cette annee!")
    return redirect(url_for("index"))

@app.route('/sub_list',methods=["GET"])
def sub_list():
    if request.method == "GET":
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            query = """
                SELECT membre.num_membre,membre.prenom,membre.nom,
                SUM(abonnement.seances_restantes),
                SUM(abonnement.seances_totales)
                FROM membre,abonnement
                WHERE membre.num_membre=abonnement.num_membre
                GROUP BY membre.num_membre,membre.prenom,membre.nom
                ORDER BY membre.num_membre;
            """
            curs.execute(query)
            row = curs.fetchone()
            listres = []
            listach = []
            listutilise = []
            listnom = []
            while row:
                listres.append(row[3])
                listach.append(row[4])
                listutilise.append(row[4]-row[3])
                listnom.append( "{} {}".format(row[2], row[1]))
                row = curs.fetchone()
            db.commit()
            db.close()
            return render_template("sub_list.html",listres=listres,listach=listach,listutilise=listutilise,listnom=listnom)
    flash("Le type de requete n'est pas le bon!")
    return redirect(url_for("index"))

@app.route('/products_count',methods=["GET"])
def products_count():
    if request.method == "GET":
            today = datetime.today()
            _30days_before = (today - timedelta(days=30)).isoformat()
            today = today.isoformat()
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            query = """
                SELECT num_marchandise,nom,count(*) 
                FROM achat WHERE date_achat>=? AND date_achat<=? 
                GROUP BY num_marchandise,nom,type;
            """
            curs.execute(query,(_30days_before,today,))
            row = curs.fetchone()
            dic = {}
            while row:
                dic[row[1]] = float(row[2])/30
                row = curs.fetchone()
            db.commit()
            db.close()
            return render_template("products_count.html",dic=dic)
    flash("Le type de requete n'est pas le bon!")
    return redirect(url_for("index"))

@app.route('/present_member',methods=["GET"])
def present_member():
    if request.method == "GET" and request.args.get("date") is not None:
            date = request.args.get("date")
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            listHour={
                "8-9" : []
                ,"9-10" : []
                ,"10-11" : []
                ,"11-12": []
                ,"12-13" : []
                ,"13-14" : []
                ,"14-15" : []
                ,"15-16": []
                ,"16-17" : []
                ,"17-18": []
                ,"18-19": []
            }
            query = """SELECT DISTINCT nom,prenom,h_arrive,h_depart FROM arrivee,membre
                    where arrivee.num_membre=membre.num_membre and date=?"""
            curs.execute(query, (date,))
            row = curs.fetchone()
            while row:
                for i in range(int(row[2]),int(row[3])):
                    listHour[str(i)+"-"+str(i+1)].append(row[0]+" "+row[1])
                    row = curs.fetchone()
            db.commit()
            db.close()
            date = datetime.strptime(date, '%Y-%m-%d').date()
            return render_template("present_member.html",dic=listHour,day=date.strftime("%d/%m/%Y"))
    flash("Le type de requete n'est pas le bon!")
    return redirect(url_for("index"))

@app.route('/pers_heure',methods=["GET"])
def pers_heure():
    if request.method == "GET":
            db = sqlite3.connect("database.db")
            curs = db.cursor()
            listHour={
                "8-9" : 0
                ,"9-10" : 0
                ,"10-11" : 0
                ,"11-12": 0
                ,"12-13" : 0
                ,"13-14" : 0
                ,"14-15" : 0
                ,"15-16": 0
                ,"16-17" : 0
                ,"17-18": 0
                ,"18-19": 0
            }
            query = """SELECT DISTINCT h_arrive,h_depart FROM arrivee,membre
                    where arrivee.num_membre=membre.num_membre and date>=? and date<=?"""
            curs.execute(query, ((datetime.today()-timedelta(days=30)).isoformat(),datetime.today().isoformat()))
            row = curs.fetchone()
            while row:
                for i in range(int(row[0]),int(row[1])):
                    listHour[str(i)+"-"+str(i+1)] = listHour[str(i)+"-"+str(i+1)] + 1;
                    row = curs.fetchone()
            db.commit()
            db.close()
            for k,v in listHour.items():
                listHour[k] = listHour[k]/30
            return render_template("pers_heure.html",dic=listHour)
    flash("Le type de requete n'est pas le bon!")
    return redirect(url_for("index"))
if __name__ == '__main__':
    app.run()
