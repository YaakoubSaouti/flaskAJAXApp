var tabContent = new Array();
var pageContent= 0;

//Ces fonctions gerent les redirection et affichage
function showMainMenu(){
    $("subtitle").innerHTML="Menu Principal";
    hide($("members_mngmt"));
    hide($("subscriptions_mngmt"));
    hide($("purchases_mngmt"));
    hide($("arrivals_mngmt"));
    hide($("member_details"));
    hide($("centerPButton"));
    hide($("register_div"));
    hide($("navigation"));
    hide("state");
    $("main_menu").style.display="flex";
}
function showMembers(){
    $("subtitle").innerHTML="Liste des membres";
    show($("members_mngmt"));
    returnMembers();
    $("return").onclick=showMainMenu;
}
function showSubs(){
    $("subtitle").innerHTML="Liste des abbonements";
    show($("subscriptions_mngmt"));
    returnSubs();
    $("return").onclick=showMainMenu;
}
function showArrivals(){
    $("subtitle").innerHTML="Liste des arrivee du jour";
    show($("arrivals_mngmt"));
    returnArrivals();
    $("return").onclick = showMainMenu;
}
function showDetails(value){
    $("subtitle").innerHTML="Voir Details";
    $("member_details").innerHTML="";
    hide($("members_mngmt"));
    hide($("navigation"));
    show($("member_details"));
    $("return").onclick = fromDetailsShowMembers;
    returnMemberDetails(value);
}
function showForm(){
    $("subtitle").innerHTML="Formulaire d'inscription";
    show($("register_div"));
    hide($("navigation"));
    hide("members_mngmt");
    $("send").onclick=sendMemberForm;
    $("return").onclick=fromFormShowMembers;
}
function showProduct(){
    $("subtitle").innerHTML="Liste des produits a vendre";
    show($("purchases_mngmt"));
    show($("Product_add"));
    hide($("Subs_add"));
    hide($("members_mngmt"));
    returnProduct();
}
function showSubscriptionPlans(){
    $("subtitle").innerHTML="Liste des abonnements";
    hide($("Product_add"));
    show($("Subs_add"));
    returnSubscriptionPlans();
}
function showState(){
    $("subtitle").innerHTML="Etat de l'achat";
    hide("members_mngmt");
    hide("navigation");
    show("state");
}
function fromDetailsShowMembers(){
    hide($("member_details"));
    showMembers();
}
function fromFormShowMembers(){
    hide($("register_div"));
    emptyTheFields();
    showMembers();
}
function fromMainMenuShowMembers() {
    showMembers();
    hide($("main_menu"));
    show($("centerPButton"));
    show($("add"));
    $("return").onclick = showMainMenu;
    $("add").onclick = showForm;
}
function fromMainMenuShowSubs() {
    showSubs();
    hide($("main_menu"));
    show($("centerPButton"));
    show($("add"));
    $("return").onclick = showMainMenu;
}
function fromMainMenuShowProduct(){
    showProduct();
    hide($("main_menu"));
    show($("centerPButton"));
    $("return").onclick = showMainMenu;
    $("changeToS").onclick=showSubscriptionPlans;
    $("changeToP").onclick=showProduct;
}
function fromProductsShowMembers(id){
    $("subtitle").innerHTML="Veuillez choisir un client"
    returnMembersForPurchase(id);
    show($("members_mngmt"));
    hide($("add"));
    hide($("purchases_mngmt"));
    $("return").onclick=showMainMenu;
}
function fromMainMenuShowArrivals() {
    showArrivals();
    hide($("main_menu"));
    show($("centerPButton"));
    $("return").onclick = showMainMenu;
}
function appendARange(list,func) {
    list.innerHTML = "";
    if(tabContent.length>0){
        tabContent[pageContent].forEach(i=>{
        list.appendChild(i);
        var bouttonDiv=i.getElementsByTagName("button")[0];
        bouttonDiv.onclick=function(){return func(bouttonDiv.id)}
        })
    }else{
        empty_list=document.createElement("div");
        empty_list.innerHTML="La liste est vide";
        empty_list.setAttribute("class","error")
        show(empty_list);
        list.appendChild(empty_list);
    }
}
function emptyTheFields(){
    $("name").value="";
    $("fname").value="";
    $("dob").value="";
    $("adress").value="";
    $("pc").value="";
    $("locality").value="";
    $("pn").value="";
}
function fromProductsShowState(){
    $("return").onclick=function(){
        showProduct();
        $("return").onclick=showMainMenu;
        hide("state");
    }
    showState();
}
//Ces fonctions permettent de contacter le serveur pour recevoir des infos
function returnMembers() {
    tabContent=new Array();
    pageContent=0;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_members");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitMembers(xhr.responseXML);
            }
        }
    };
    xhr.send(null);
}
function returnArrivals() {
    tabContent=new Array();
    pageContent=0;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_arrivals");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitArrivals(xhr.responseXML);
            }
        }
    };
    xhr.send(null);
}
function returnMemberDetails(value) {
    var param = "num_membre=" + value;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_member_details?" + param);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitMemberDetails(xhr.responseXML);
            }
        }
    };
    xhr.send(null);
}
function returnProduct(){
    tabContent=new Array();
    pageContent=0;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_product");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitProduct(xhr.responseXML);
            }
        }
    };
    xhr.send(null);
}
function returnSubscriptionPlans(){
    tabContent=new Array();
    pageContent=0;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_sub_plan");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitSubscriptionPlans(xhr.responseXML);
            }
        }
    };
    xhr.send(null);
}
function traitSubscriptionPlans(xmlDoc) {
    var sd = 0;
    var fd = 0;
    var xmlelmts = xmlDoc.getElementsByTagName("racine")[0];
    var plans = xmlelmts.getElementsByTagName("plans")[0];
    plans = plans.getElementsByTagName("plan");
    for (var i = 0; i < plans.length; i++) {
        var id = plans[i].getElementsByTagName("id_plan")[0].firstChild.nodeValue;
        var div = document.createElement("div");
        var button = btn("Vendre", "buttonBeside", "s_" + id);
        div.setAttribute("class", "sp");
        div.innerHTML = "<span class='title_product'>Plan " + id + "</span>";
        div.innerHTML += "<br>Nom: " + plans[i].getElementsByTagName("sp_name")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Prix: " + plans[i].getElementsByTagName("price")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Nombre de seance: " + plans[i].getElementsByTagName("n_prest")[0].firstChild.nodeValue;
        div.appendChild(button);
        if (sd == 0) tabContent[fd] = new Array();
        tabContent[fd].push(div);
        sd++;
        if (sd == 3) {
            sd = 0;
            fd++;
        }
    }
    appendARange($("sub_plan_list"), fromProductsShowMembers);
    setupNavigation($("sub_plan_list"),fromProductsShowMembers);
}
function returnMembersForPurchase(id){
    tabContent = new Array();
    pageContent=0;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_members");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitMembersForPurchase(id,xhr.responseXML);
            }
        }
    };
    xhr.send(null);
}
function returnSubs(){
    tabContent = new Array();
    pageContent=0;
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_subs");
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitSubs(xhr.responseXML);
            }
        }
    };
    xhr.send(null);
}
function traitArrivals(xmlDoc){
    var sd = 0;
    var fd = 0;
    var xmlelmts = xmlDoc.getElementsByTagName("arrivals")[0];
    var arrivals = xmlelmts.getElementsByTagName("arrival");
    for (var i = 0; i < arrivals.length; i++) {
        var id = arrivals[i].getElementsByTagName("id")[0].firstChild.nodeValue;
        var div = document.createElement("div");
        var button = btn("Marquer le depart", "buttonBeside", id);
        div.setAttribute("class", "arrival");
        div.innerHTML = "<span class='title_product'>Arrival " + id + "</span>";
        div.innerHTML += "<br>Heure d'arrivee: " + arrivals[i].getElementsByTagName("ah")[0].firstChild.nodeValue +".00h";
        div.innerHTML += "<br>Membre: " + arrivals[i].getElementsByTagName("fn")[0].firstChild.nodeValue + " " + arrivals[i].getElementsByTagName("ln")[0].firstChild.nodeValue;
        div.appendChild(button);
        if (sd == 0) tabContent[fd] = new Array();
        tabContent[fd].push(div);
        sd++;
        if (sd == 3) {
            sd = 0;
            fd++;
        }
    }
    appendARange($("arrivals_list"), sendLeaving);
    setupNavigation($("arrivals_list"),sendLeaving);
}
function traitSubs(xmlDoc){
    var sd = 0;
    var fd = 0;
    var xmlelmts = xmlDoc.getElementsByTagName("subs")[0];
    var subs = xmlelmts.getElementsByTagName("sub");
    for (var i = 0; i < subs.length; i++) {
        var id_sub = subs[i].getElementsByTagName("id")[0].firstChild.nodeValue;
        var id_member = subs[i].getElementsByTagName("nm")[0].firstChild.nodeValue;
        var div = document.createElement("div");
        var button = btn("Consommer", "buttonBeside", id_member + "_" + id_sub);
        div.setAttribute("class", "sub");
        div.innerHTML = "<span class='title_product'>Abonnement " + id_sub + "</span>";
        div.innerHTML += "<br>Places Restantes: " + subs[i].getElementsByTagName("rs")[0].firstChild.nodeValue + "/" + subs[i].getElementsByTagName("ts")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Date d'achat: " + subs[i].getElementsByTagName("pd")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Membre: " + subs[i].getElementsByTagName("fn")[0].firstChild.nodeValue + " " + subs[i].getElementsByTagName("ln")[0].firstChild.nodeValue;
        div.appendChild(button);
        if (sd == 0) tabContent[fd] = new Array();
        tabContent[fd].push(div);
        sd++;
        if (sd == 3) {
            sd = 0;
            fd++;
        }
    }
    appendARange($("subs_list"), sendArrival);
    setupNavigation($("subs_list"),sendArrival);
}
function sendMemberForm(){
    $("ulEM").innerHTML="";
    hide($("error_message"));
    var name=$("name").value;
    var fname=$("fname").value;
    var dob=$("dob").value;
    var adress=$("adress").value;
    var locality=$("locality").value;
    var pc=$("pc").value;
    var pn=$("pn").value;
    var param;
    param="name="+encodeURIComponent(name)+"&fname="+encodeURIComponent(fname);
    param+="&dob="+encodeURIComponent(dob)+"&adress="+encodeURIComponent(adress);
    param+="&locality="+encodeURIComponent(locality)+"&pc="+encodeURIComponent(pc);
    param+="&pn="+encodeURIComponent(pn);
    xhr=new XMLHttpRequest();
    xhr.onreadystatechange= function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitMemberForm(xhr.responseXML);
            }
        }
    };
    xhr.open("POST","/create_user");
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xhr.send(param);
}
function sendPurchase(id){
    var array=id.split("_")
    var type=array[1];
    var idMember=array[0];
    var idPurchase=array[2];
    var param;
    param="type="+encodeURIComponent(type)+"&idMember="+encodeURIComponent(idMember);
    param+="&idPurchase="+encodeURIComponent(idPurchase);
    xhr=new XMLHttpRequest();
    xhr.onreadystatechange= function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                traitPurchase(xhr.responseXML);
            }
        }
    };
    xhr.open("POST","/create_purchase");
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xhr.send(param);
}
function traitMembers(xmlDoc) {
    var sd = 0;
    var fd = 0;
    var xmlelmts = xmlDoc.getElementsByTagName("member");
    for (var i = 0; i < xmlelmts.length; i++) {
        var id = xmlelmts[i].getElementsByTagName("num_member")[0].firstChild.nodeValue;
        var div = document.createElement("div");
        var button = btn("Voir Details", "buttonBeside", id);
        div.setAttribute("class", "members");
        div.innerHTML = "<span class='title_mbrs'>Client " + id + "</span>";
        div.innerHTML += "<br>Nom: " + xmlelmts[i].getElementsByTagName("lname")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Prenom: " + xmlelmts[i].getElementsByTagName("fname")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Date d'inscription: " + xmlelmts[i].getElementsByTagName("sd")[0].firstChild.nodeValue;
        div.appendChild(button);
        if (sd == 0) tabContent[fd] = new Array();
        tabContent[fd].push(div);
        sd++;
        if (sd == 3) {
            sd = 0;
            fd++;
        }
    }
    appendARange($("members_list"),showDetails);
    setupNavigation($("members_list"),showDetails);
}
function traitProduct(xmlDoc) {
    var sd = 0;
    var fd = 0;
    var xmlelmts = xmlDoc.getElementsByTagName("racine")[0];
    var products = xmlelmts.getElementsByTagName("products")[0];
    products = products.getElementsByTagName("product");
    for (var i = 0; i < products.length; i++) {
        var id = products[i].getElementsByTagName("num_product")[0].firstChild.nodeValue;
        var div = document.createElement("div");
        var button = btn("Vendre", "buttonBeside", "p_"+id);
        div.setAttribute("class", "products");
        div.innerHTML = "<span class='title_product'>Produit " + id + "</span>";
        div.innerHTML += "<br>Nom: " + products[i].getElementsByTagName("pname")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Prix: " + products[i].getElementsByTagName("price")[0].firstChild.nodeValue;
        div.appendChild(button);
        if (sd == 0) tabContent[fd] = new Array();
        tabContent[fd].push(div);
        sd++;
        if (sd == 3) {
            sd = 0;
            fd++;
        }
    }
    appendARange($("product_list"),fromProductsShowMembers);
    setupNavigation($("product_list"),fromProductsShowMembers);
}
function traitMembersForPurchase(id,xmlDoc){
    var sd = 0;
    var fd = 0;
    var xmlelmts = xmlDoc.getElementsByTagName("member");
    for (var i = 0; i < xmlelmts.length; i++) {
        var idMember = xmlelmts[i].getElementsByTagName("num_member")[0].firstChild.nodeValue;
        var div = document.createElement("div");
        var button = btn("Selectionner", "buttonBeside", idMember+"_"+id);
        div.setAttribute("class", "members");
        div.innerHTML = "<span class='title_mbrs'>Client " + idMember + "</span>";
        div.innerHTML += "<br>Nom: " + xmlelmts[i].getElementsByTagName("lname")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Prenom: " + xmlelmts[i].getElementsByTagName("fname")[0].firstChild.nodeValue;
        div.innerHTML += "<br>Date d'inscription: " + xmlelmts[i].getElementsByTagName("sd")[0].firstChild.nodeValue;
        div.appendChild(button);
        if (sd == 0) tabContent[fd] = new Array();
        tabContent[fd].push(div);
        sd++;
        if (sd == 3) {
            sd = 0;
            fd++;
        }
    }
    appendARange($("members_list"),sendPurchase);
    setupNavigation($("members_list"),sendPurchase);
}
function traitMemberDetails(xmlDoc) {
    var xmlelmt = xmlDoc.getElementsByTagName("member")[0];
    var div = document.createElement("div");
    div.setAttribute("class", "member");
    div.innerHTML = "<span class='title_mbrs'>" + xmlelmt.getElementsByTagName("lname")[0].firstChild.nodeValue + " " + xmlelmt.getElementsByTagName("fname")[0].firstChild.nodeValue + "</span>";
    div.innerHTML += "<br>Date de naissance: " + xmlelmt.getElementsByTagName("dob")[0].firstChild.nodeValue;
    div.innerHTML += "<br>Code postal: " + xmlelmt.getElementsByTagName("pc")[0].firstChild.nodeValue;
    div.innerHTML += "<br>Localite: " + xmlelmt.getElementsByTagName("loc")[0].firstChild.nodeValue;
    div.innerHTML += "<br>Adresse: " + xmlelmt.getElementsByTagName("ad")[0].firstChild.nodeValue;
    div.innerHTML += "<br>Numero de telephone: " + xmlelmt.getElementsByTagName("pn")[0].firstChild.nodeValue;
    div.innerHTML += "<br>Date d'inscription: " + xmlelmt.getElementsByTagName("sd")[0].firstChild.nodeValue;
    div.innerHTML += "<br>Numero de membre: " + xmlelmt.getElementsByTagName("num_member")[0].firstChild.nodeValue;
    $("member_details").appendChild(div);
}
function traitMemberForm(xmlDoc){
    var xmlemts = xmlDoc.getElementsByTagName("racine")[0];
    var state = xmlemts.getElementsByTagName("state")[0].firstChild.nodeValue;
    if(state==0){
        if(xmlemts.getElementsByTagName("msgs")[0]){
            var msgs=xmlemts.getElementsByTagName("msg");
            show($("error_message"));
            for(var i=0;i<msgs.length;i++){
                var li=createElement("li");
                li.innerHTML=msgs[i].firstChild.nodeValue;
                $("ulEM").appendChild(li);
            }
        }
    }else{
        fromFormShowMembers();
        emptyTheFields();
    }
}
function traitPurchase(xmlDoc){
    var xmlemts = xmlDoc.getElementsByTagName("racine")[0];
    var state = xmlemts.getElementsByTagName("state")[0].firstChild.nodeValue;
    if(state==1){
        $("state").innerHTML="L'achat as bien ete enregistrer!";
        $("state").setAttribute("class","success");
        fromProductsShowState();
    }else{
        $("state").innerHTML="Error when registering the purchase!";
        $("state").setAttribute("class","error");
        fromProductsShowState();
    }
}
function sendArrival(id){
    var array=id.split("_");
    var id_sub=array[1];
    var id_member=array[0];
    param="id_member="+encodeURIComponent(id_member)+"&id_sub="+encodeURIComponent(id_sub);
    xhr=new XMLHttpRequest();
    xhr.onreadystatechange= function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                showSubs();
            }
        }
    };
    xhr.open("POST","/create_arrival");
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xhr.send(param);
}
function sendLeaving(id){
    param="id="+encodeURIComponent(id);
    xhr=new XMLHttpRequest();
    xhr.onreadystatechange= function() {
        if (xhr.readyState == 4) {
            if (xhr.status == 200) {
                showArrivals();
            }
        }
    };
    xhr.open("POST","/send_leaving");
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xhr.send(param);
}
//Ces fonctions sont des fonctions utilitaires
function btn(descr, classes, id) {
    var button = document.createElement("button");
    button.innerHTML = descr;
    button.setAttribute("class", classes);
    button.id = id;
    return button;
}
function setupNavigation(list,func){
    hide("nxt");
    show($("navigation"));
    if(tabContent.length>1) show($("nxt"));
    hide($("prev"));
    $("nxt").onclick=function(){
        pageContent++;
        appendARange(list,func);
        if(tabContent.length-1==pageContent){
            hide("nxt");
        }
        if(pageContent>0) show($("prev"));
    }
    $("prev").onclick=function(){
        pageContent--;
        appendARange(list,func);
        if(pageContent==0){
            hide("prev");
        }
        if(pageContent==0) show($("nxt"));
    }
}
//Cette fonction sert a initialiser l'application
function init_app() {
    $("subtitle").innerHTML="Menu Principal";
    $("manage_purchases").onclick= fromMainMenuShowProduct;
    $("manage_members").onclick = fromMainMenuShowMembers;
    $("manage_subscriptions").onclick = fromMainMenuShowSubs;
    $("manage_arrivals").onclick = fromMainMenuShowArrivals;
    $("home").onclick=showMainMenu;
}


function init(ev) {
    init_app();
}

(function () {
    var fired = 0;
    var tmr = null;

    function onReady(ev) {
        if (tmr) {
            clearTimeout(tmr);
        }
        if (fired) {
            return false;
        }
        if (document.readyState == "complete") {
            fired = 1;
            window.removeEventListener("load", onReady, false);
            document.removeEventListener("DOMContentLoaded", onReady, false);
            document.removeEventListener("readystatechange", onReady, false);
            init();
        } else {
            tmr = setTimeout(onReady, 1);
        }
    }

    window.addEventListener("load", onReady, false);
    document.addEventListener("DOMContentLoaded", onReady, false);
    document.addEventListener("readystatechange", onReady, false);
    tmr = setTimeout(onReady, 10);
    if (document.readyState == "complete") {
        onReady();
    }
}());