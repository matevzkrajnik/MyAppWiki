function preveriPrijavo() {
    document.getElementById("napakamail").style.visibility = "hidden";
    if (document.getElementById("vnosemail").value == "") {
        console.log("prazen email input");
        $("vnosemail").setCustomValidity("sam da dela");
        document.getElementById("napakamail").style.visibility = "visible";
        return false;
    }
    else if (document.getElementById("vnosgeslo").value == "") {
        console.log("prazen geslo input");
        $("vnosgeslo").setCustomValidity("sam da dela");
        document.getElementById("napakamail").style.visibility = "visible";
        return false;
    }
    else {
        var regex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
        console.log("kaaaj")
        if (regex.test(document.getElementById("vnosemail").value)) {
            return true;
        }
        else {
            console.log("Napačen format email-a");
            document.getElementById("napakamail").style.visibility = "visible";
            return false;
        }
    }

    return false;
}

function preveriRegistracijo() {
    document.getElementById("napaka").style.visibility = "hidden";
    var ime = document.getElementById("geslo1").value;
    var priimek = document.getElementById("priimek").value;
    var mail = document.getElementById("mail").value;
    var geslo1 = document.getElementById("geslo1").value;
    var geslo2 = document.getElementById("geslo2").value;
    var regexIme = /[A-Za-z]+/i;
    var regexMail = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    var mailKul = regexMail.test(mail);
    //console.log(regexIme.test(ime));
    if (ime == "" || priimek == "" || !mailKul || geslo1 == "" || geslo2 == "" || geslo1 != geslo2) {
        document.getElementById("napaka").style.visibility = "visible";
    }
    else {
        return true;
    }
    return false;
}

function pokazi(vrstica) {
    document.getElementById("sporocilo").style.visibility = "visible";
    var dogodek = vrstica.getElementsByTagName('td')[0].innerHTML;
    var stran = vrstica.getElementsByTagName('td')[1].innerHTML;
    var string = "<p><b>";
    var avtor = vrstica.getElementsByTagName('td')[2].innerHTML;
    if(dogodek === "Sprememba strani"){
        string += "Spremenil sem vsebino strani <i>" + stran;
    }
    else if (dogodek === "Dodana stran"){
        string += "Dodal sem stran z naslovom <i>" + stran;
    }
    string += "</i>.</b><br>Lep pozdrav,  " + avtor + "</p>";
    document.getElementById("sporocilo").innerHTML = string;
}

function skrij() {
    document.getElementById("sporocilo").style.visibility = "hidden";
}

function zapolni() {
    document.getElementById("naslov").value = "Splošno";
    document.getElementById("vsebina").value = "MyApp spletna storitev uporablja najnovejše tehnologije, da uporabnikom omogoči " +
        "vpogled v statistiko njihovih aplikacij. S povezavo do Google Play Store, iTunes App Store ter Windows Phone Apps naša storitev " +
        "dobi vse potrebne informacije ter jih predstavi na uporabniku prijazen način. Tako lahko tudi vsak začetnik razvijalec vidi, kako pogosto " +
        "uporabniki uporabljajo njegovo aplikacijo, kako dolgo jo imajo odprto, na katerih napravah jo uporabljajo, ... Te informacije so za vsakega " +
        "razvijalca pomembne, saj lahko na podlagi statistike uporabe svojo aplikacijo prilagodi za kar največjo uspešnost."
}

$(document).ready(function () {
    $("#ponovi").hide();
    $("#shrani").hide();
    $("#shranjujem").hide();

    if ($("#prostor").length) {

        var canvas = $("#prostor").get(0);
        var context = canvas.getContext("2d");
        var video = document.getElementById("video");
        var videoObj = { "video": true };

        var errBack = function(error) {
            console.log("Video capture error: ", error.code);
        };

        if (navigator.getUserMedia) { // Standard
            navigator.getUserMedia(videoObj, function(stream) {
                video.src = stream;
                video.play();
                $("#slikaj").show();
            }, errBack);
        } else if (navigator.webkitGetUserMedia) {  // WebKit-prefixed
            navigator.webkitGetUserMedia(videoObj, function(stream){
                video.src = window.webkitURL.createObjectURL(stream);
                video.play();
                $("#slikaj").show();
            }, errBack);
        } else if (navigator.mozGetUserMedia) { // moz-prefixed
            navigator.mozGetUserMedia(videoObj, function(stream){
                video.src = window.URL.createObjectURL(stream);
                video.play();
                $("#slikaj").show();
            }, errBack);
        }

        $("#slikaj").get(0).addEventListener("click", function() {
            context.drawImage(video, 0, 0, 640, 480);
            $("#video").hide();
            $("#prostor").show();
            $("#slikaj").hide();
            $("#ponovi").show();
            $("#shrani").show();
        });

        $("#ponovi").get(0).addEventListener("click", function() {
            $("#video").show();
            $("#prostor").hide();
            $("#slikaj").show();
            $("#ponovi").hide();
            $("#shrani").hide();
        });

        $("#shrani").get(0).addEventListener("click", function(){
            $("#shranjujem").show();
            history.go(-1);
        });
    }
});