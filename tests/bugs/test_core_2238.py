#coding:utf-8
#
# id:           bugs.core_2238
# title:        UTF8 and large varchar fields, is disinct from > Implementation limit exceeded.
# decription:   
#                   Test operates with literals of utf8 charset with length = exactly 8191 symbols.
#                   We insert such literal and then try to update table with another string which differs only in last character.
#                   Confirmed exception on 2.5: 
#                       statement failed, sqlstate = 54000
#                       dynamic sql error
#                       -sql error code = -204
#                       -implementation limit exceeded
#                       -block size exceeds implementation restriction
#                 
# tracker_id:   CORE-2238
# min_versions: ['3.0']
# versions:     3.0
# qmid:         None

import pytest
from firebird.qa import db_factory, isql_act, Action

# version: 3.0
# resources: None

substitutions_1 = []

init_script_1 = """"""

db_1 = db_factory(charset='UTF8', sql_dialect=3, init=init_script_1)

test_script_1 = """
    set bail on;
    create domain dm_long_utf8 as varchar(8191) character set utf8;
    create table test (long_text dm_long_utf8);
    commit;
    set count on;
    -- Length of this literal is exact 8191 characters:
    insert into test(long_text)
    values(
        'Kaikki neuvon-antajat ja etevimmät päälliköt ja mollat ja imamit ja kadit ja kaupungin päähenkilöt olivat suuresti hämmästyksissään. Hänen tunnettu hurskautensa vaati kaikkia äänettömyyteen, sillä välin kuin hän itse lausui pitkän rukouksen, pyytäen Allah''ta ja Profeettaa hämmentämään kaikkia häväiseviä Juutalaisia ja uskottomia ja vuodattamaan totuuden sanoja jumalisten ihmisten suuhun. Ja nyt kunnian-arvoisa sheiki kutsui esiin kaikki todistajat David Alroy''ta vastaan. Heti Kisloch, Kurdilainen, joka oli koroitettu Bagdadin kadiksi, astui esiin, veti sametti-kukkarostansa paperikääryn ja luki semmoisen todistuksen, jossa arvoisa Kisloch vakuutti, että hän ensin tutustui vangin, David Alroy''n kanssa joissakin erämaan raunioissa -- muutamain rosvojen pesässä, joita Alroy johdatti; että hän, Kisloch, oli rehellinen kauppias ja että nämät konnat olivat ryöstäneet hänen karavaninsa ja hän itse joutunut vankeuteen; että hänen vankeutensa toisena yönä Alroy oli ilmestynyt hänen eteensä leijonan muodossa ja kolmantena tuimasilmäisenä härkänä; että hänen oli tapa alinomaa muuttaa itsensä; että hän usein nosti henkiä; että viimein eräänä kauheana yönä Eblis itse tuli suurella juhlasaatolla ja antoi Alroy''lle Salomonin, Davidin pojan valtikan; ja että tämä seuraavana päivänä kohotti lippunsa ja kohta sen jälkeen kukisti Hassan Subah''n ja tämän Seldshukit useitten hirmuisten paholaisten silminnähtävällä avulla.  Kalidaan, Indialaisen, Guebriläisen ja Neekerin ja muutamien muitten saman hengen lapsien todistukset vetivät täysin määrin vertoja Kisloch Kurdilaisen uhkealle kertomukselle. Hebrealaisen valloittajan vastustamaton menestys oli kieltämättömällä tavalla selitetty, Mahomettilaisten aseitten kunnia ja Moslemin uskon puhtaus olivat asetetut jälleen entiseen loistoonsa ja saastuttamattomaan maineesensa. Todeksi saatiin, että David Alroy oli Ebliin lapsi, noitamies, taikakalujen ja myrkkyjen käyttäjä. Kansa kuunteli kauhulla ja harmilla. He olisivat tunkeneet vartiaväen läpitse ja repineet hänet kappaleiksi, jolleivät olisi pelänneet Karamanialaisten sotatapparoita. Niin he lohduttivat mieltänsä sillä, että he ennen pitkää saisivat nähdä hänen kidutuksensa.  Bagdadin kadi kumarsi Karamanian kuningasta ja kuiskasi soveliaan matkan päästä jotakin kuninkaalliseen korvaan. Torvet kaikkuivat, kuuluttajat vaativat äänettömyyttä ja kuninkaan huulet liikkuivat taas.  "Kuule, oi kansa, ja ole viisas. Pääkadi aikoo nyt lukea kuninkaallisen prinsessan Schirenen, noiturin etevimmän uhrin todistuksen."  Ja todistus luettiin, joka vakuutti, että David Alroy omisti ja kantoi lähinnä sydäntänsä erästä talismania, jonka Eblis oli antanut hänelle ja jonka voima oli niin suuri, että, jos sitä kerta painettiin naisen rintaa vastaan, tämä ei enää voinut hallita tahtoansa. Tämmöinen kova onni oli kohdannut oikeauskoisten hallitsian tytärtä.  "Onko siinä niin kirjoitettu?" vanki kysyi.  "On", kadi vastasi, "ja sen alla on vielä prinsessan kuninkaallinen allekirjoitus."  "Se on väärennetty."  Karamanian kuningas kavahti valta-istuimeltansa ja oli vihoissansa astumallaan sen portaita alas. Hänen kasvonsa olivat veripunaiset, hänen partansa kuin tulen liekki. Joku lempiministeri rohkeni vienosti pidättää häntä hänen kuninkaallisesta vaipastansa.  "Tapa paikalla pois se koira", Karamanian kuningas mutisi.  "Prinsessa on itse täällä", lausui kadi, "todistamassa niitä noitakeinoja, joitten alaisena hän oli, vaan joitten vaikutuksesta hän nyt Allah''n ja Profeetan voiman kautta on pääsnyt."  Alroy''ta vävähti!  "Astu esiin, kuninkaallinen prinsessa", kadi sanoi, "ja jos se todistus, jonka kuulit, on perustettu, nosta ylös se kuninkaallinen käsi, joka koristi sen allekirjoituksellaan."  Lähellä valta-istuinta oleva eunukkien joukko teki tilaa; naishaamu, joka oli verhottu hunnulla jalkoihin saakka, astui esiin. Hän nosti ylös kätensä; koko kerääntynyt kansa tuskin hengitti mielenliikutuksesta; eunukkien rivit ummistuivat jälleen; huuto kuului ja hunnustettu haamu katosi.  "Minä odotan kidutuskoneitasi, kuningas", Alroy lausui raskaan surun äänellä. Hänen lujuutensa näytti luopuneen hänestä. Hänen silmänsä olivat luodut maahan. Hän oli nähtävästi vaipunut syvään miettimiseen taikka heittäynyt epätoivoon.  "Valmistakaat seipäät", käski Alp Arslan.  Koko kansan joukkoa värisytti vasten mieltäkin.  Yksi orja lähestyi ja tarjosi paperikääryä Alroy''lle. Hän tunsi Nubialaisen, joka oli Honainin palveluksessa. Hänen entinen ministerinsä ilmoitti hänelle, että hän oli saapuvilla; että ne ehdot, joita hän vankihuoneessa tarjosi, vielä myönnettäisiin; että jos Alroy, jota asiaa hän ei epäillyt ja jota hän rukoili, suostuisi niitä vastaan-ottamaan, hänen tuli pistää paperikäärö poveensa, mutta, jos hän yhä oli taipumaton, jos hänen yhä oli mieletön päätös kuolla hirveä ja häväisevä kuolema, hänen tuli repiä se rikki ja heittää se tanterelle. Silmänräpäyksellä Alroy otti paperikääryn ja repi sen kiivaasti tuhansiin palasiin. Tuulen puuska levitti kappaleet laajalle yliympäri. Alhaiso riiteli näistä David Alroy''n viimeisistä muistoista; ja tämä vähäinen tapaus tuotti paljon hämminkiä.  Tällä välin Neekerit varustivat kidutuksen ja kuoleman koneita.  "Tuon juutalaisen koiran itsepintaisuus tekee minun hulluksi", lausui Karamanian kuningas hovimiehillensä. "Minua haluttaa puhutella häntä vähän, ennenkuin hän kuolee." Lempiministeri pyysi hallitsiaansa olemaan levollisena; mutta kuninkaallinen parta kävi niin punaiseksi, ja kuninkaalliset silmät iskivät niin kauheata tulta, että lempiministerikin lopulta myöntyi.  Torvi kaikkui, kuuluttajat vaativat vaiti-oloa, ja Alp Arslanin ääni eroitettiin jälleen.  "Senkin koira, näetkö sinä, mikä on tarjonasi? Tiedätkö sinä, mikä vartoo sinua sinun herrasi Ebliin asunnoissa? Voiko väärä ylpeys viehättää Juutalaistakin? Eikö elämä ole suloista? Eikö olisi parempi olla minun varvaskenkieni kantaja kuin tulla seivästetyksi?"  "Jalomielinen Alp Arslan", vastasi Alroy ilmeisen ylenkatseen äänellä; "luuletko, että mikään kidutus rasittaa niin, kuin se muisto, että sinä olet voittanut minun?"  "Partani kautta, hän ivaa minua!" Karamanialaisten hallitsia huudahti; "hän tekee kiusaa minulle! Älkäät koskeko vaippaani. Minä tahdon puhua hänen kanssaan. Te ette näe kauemmaksi kuin hunnustettu haukka, te sokean äidin lapset. Se on noita; hänellä on vielä jälellä joku päätaika; hän pelastaa vielä henkensä. Hän lentää ilmaan taikka vaipuu maan sisään. Hän nauraa meidän kidutuksiamme." Karamanian kuningas astui tuota pikaa valta-istuimensa portaita alaspäin; häntä seurasivat hänen lempiministerinsä ja hänen neuvon-antajansa ja hänen etevimmät päällikkönsä ja kadit ja mollat ja imamit ja kaupungin päähenkilöt.  "Sinä noita!" Alp Arslan huudahti, "hävytön noita! halvan äidin halpa poika! koirien koira! niskotteletko sinä meitä vastaan? Kuiskaako herrasi Eblis toivoa sinun korviisi? Nauratko meidän rangaistuksiamme? Aiotko lentää ylös ilmaan? vai painua alas maahan? Niinkö, niinkö?" Hengästyneenä ja vihastansa uupuneena hallitsia vaikeni. Hän repi partaansa ja polki maata rajussa vimmassaan.  "Sinä olet viisaampi kuin neuvon-antajasi, kuningas Arslan; minä en nöyrry sinun edessäsi. Minun Herrani, vaikka hän ei ole Eblis, ei ole hylännyt minua. Minä nauran sinun rangaistuksiasi. Sinun kidutuksiasi minä ylenkatson. Minä sekä vaivun maan sisään että kohoan ilmaan. Tyydytkö nyt vastaukseeni?"  "Partani kautta", huudahti tulistunut Arslan, "minä tyydyn vastaukseesi. Pelastakoon Eblis sinut, jos hän voi;" ja Karamanian kuningas, Aasian mainioin miekan piteliä veti säilänsä, ikäänkuin salaman, tupesta ja silpaisi yhdellä säväyksellä Alroy''lta pään. Se kaatui, vaan, kun se kaatui, riemuitsevan pilkan hymy näytti vivahtelevan sankarin kylmenevillä kasvoilla ja kysyvän hänen vihollisiltansa: "missä kaikki teidän kidutuksenne nyt ovat?" Do Dzieci Gołąbki i Dziewczynka Dziecię i Koza Wróbel i Jaskółka Osieł i Chłopczyk Nieposłuszny Zajączek Kotek Brytan i Pudelek Egzamin Małego "Misia" Wilk i Owce Lis i Gąski Chłopczyk i Źrebię Gęsia Kapela Lew i Piesek Niedźwiedź i Pszczółka Śniadanie Artysta Z Zimowych Rozrywek Leniwy Chłopczyk Przygoda z Indykiem O hämmästyksissään. Leniwy ЙЦУКЕН'
    );
    insert into test(long_text)
    values(
        'Kaikki neuvon-antajat ja etevimmät päälliköt ja mollat ja imamit ja kadit ja kaupungin päähenkilöt olivat suuresti hämmästyksissään. Hänen tunnettu hurskautensa vaati kaikkia äänettömyyteen, sillä välin kuin hän itse lausui pitkän rukouksen, pyytäen Allah''ta ja Profeettaa hämmentämään kaikkia häväiseviä Juutalaisia ja uskottomia ja vuodattamaan totuuden sanoja jumalisten ihmisten suuhun. Ja nyt kunnian-arvoisa sheiki kutsui esiin kaikki todistajat David Alroy''ta vastaan. Heti Kisloch, Kurdilainen, joka oli koroitettu Bagdadin kadiksi, astui esiin, veti sametti-kukkarostansa paperikääryn ja luki semmoisen todistuksen, jossa arvoisa Kisloch vakuutti, että hän ensin tutustui vangin, David Alroy''n kanssa joissakin erämaan raunioissa -- muutamain rosvojen pesässä, joita Alroy johdatti; että hän, Kisloch, oli rehellinen kauppias ja että nämät konnat olivat ryöstäneet hänen karavaninsa ja hän itse joutunut vankeuteen; että hänen vankeutensa toisena yönä Alroy oli ilmestynyt hänen eteensä leijonan muodossa ja kolmantena tuimasilmäisenä härkänä; että hänen oli tapa alinomaa muuttaa itsensä; että hän usein nosti henkiä; että viimein eräänä kauheana yönä Eblis itse tuli suurella juhlasaatolla ja antoi Alroy''lle Salomonin, Davidin pojan valtikan; ja että tämä seuraavana päivänä kohotti lippunsa ja kohta sen jälkeen kukisti Hassan Subah''n ja tämän Seldshukit useitten hirmuisten paholaisten silminnähtävällä avulla.  Kalidaan, Indialaisen, Guebriläisen ja Neekerin ja muutamien muitten saman hengen lapsien todistukset vetivät täysin määrin vertoja Kisloch Kurdilaisen uhkealle kertomukselle. Hebrealaisen valloittajan vastustamaton menestys oli kieltämättömällä tavalla selitetty, Mahomettilaisten aseitten kunnia ja Moslemin uskon puhtaus olivat asetetut jälleen entiseen loistoonsa ja saastuttamattomaan maineesensa. Todeksi saatiin, että David Alroy oli Ebliin lapsi, noitamies, taikakalujen ja myrkkyjen käyttäjä. Kansa kuunteli kauhulla ja harmilla. He olisivat tunkeneet vartiaväen läpitse ja repineet hänet kappaleiksi, jolleivät olisi pelänneet Karamanialaisten sotatapparoita. Niin he lohduttivat mieltänsä sillä, että he ennen pitkää saisivat nähdä hänen kidutuksensa.  Bagdadin kadi kumarsi Karamanian kuningasta ja kuiskasi soveliaan matkan päästä jotakin kuninkaalliseen korvaan. Torvet kaikkuivat, kuuluttajat vaativat äänettömyyttä ja kuninkaan huulet liikkuivat taas.  "Kuule, oi kansa, ja ole viisas. Pääkadi aikoo nyt lukea kuninkaallisen prinsessan Schirenen, noiturin etevimmän uhrin todistuksen."  Ja todistus luettiin, joka vakuutti, että David Alroy omisti ja kantoi lähinnä sydäntänsä erästä talismania, jonka Eblis oli antanut hänelle ja jonka voima oli niin suuri, että, jos sitä kerta painettiin naisen rintaa vastaan, tämä ei enää voinut hallita tahtoansa. Tämmöinen kova onni oli kohdannut oikeauskoisten hallitsian tytärtä.  "Onko siinä niin kirjoitettu?" vanki kysyi.  "On", kadi vastasi, "ja sen alla on vielä prinsessan kuninkaallinen allekirjoitus."  "Se on väärennetty."  Karamanian kuningas kavahti valta-istuimeltansa ja oli vihoissansa astumallaan sen portaita alas. Hänen kasvonsa olivat veripunaiset, hänen partansa kuin tulen liekki. Joku lempiministeri rohkeni vienosti pidättää häntä hänen kuninkaallisesta vaipastansa.  "Tapa paikalla pois se koira", Karamanian kuningas mutisi.  "Prinsessa on itse täällä", lausui kadi, "todistamassa niitä noitakeinoja, joitten alaisena hän oli, vaan joitten vaikutuksesta hän nyt Allah''n ja Profeetan voiman kautta on pääsnyt."  Alroy''ta vävähti!  "Astu esiin, kuninkaallinen prinsessa", kadi sanoi, "ja jos se todistus, jonka kuulit, on perustettu, nosta ylös se kuninkaallinen käsi, joka koristi sen allekirjoituksellaan."  Lähellä valta-istuinta oleva eunukkien joukko teki tilaa; naishaamu, joka oli verhottu hunnulla jalkoihin saakka, astui esiin. Hän nosti ylös kätensä; koko kerääntynyt kansa tuskin hengitti mielenliikutuksesta; eunukkien rivit ummistuivat jälleen; huuto kuului ja hunnustettu haamu katosi.  "Minä odotan kidutuskoneitasi, kuningas", Alroy lausui raskaan surun äänellä. Hänen lujuutensa näytti luopuneen hänestä. Hänen silmänsä olivat luodut maahan. Hän oli nähtävästi vaipunut syvään miettimiseen taikka heittäynyt epätoivoon.  "Valmistakaat seipäät", käski Alp Arslan.  Koko kansan joukkoa värisytti vasten mieltäkin.  Yksi orja lähestyi ja tarjosi paperikääryä Alroy''lle. Hän tunsi Nubialaisen, joka oli Honainin palveluksessa. Hänen entinen ministerinsä ilmoitti hänelle, että hän oli saapuvilla; että ne ehdot, joita hän vankihuoneessa tarjosi, vielä myönnettäisiin; että jos Alroy, jota asiaa hän ei epäillyt ja jota hän rukoili, suostuisi niitä vastaan-ottamaan, hänen tuli pistää paperikäärö poveensa, mutta, jos hän yhä oli taipumaton, jos hänen yhä oli mieletön päätös kuolla hirveä ja häväisevä kuolema, hänen tuli repiä se rikki ja heittää se tanterelle. Silmänräpäyksellä Alroy otti paperikääryn ja repi sen kiivaasti tuhansiin palasiin. Tuulen puuska levitti kappaleet laajalle yliympäri. Alhaiso riiteli näistä David Alroy''n viimeisistä muistoista; ja tämä vähäinen tapaus tuotti paljon hämminkiä.  Tällä välin Neekerit varustivat kidutuksen ja kuoleman koneita.  "Tuon juutalaisen koiran itsepintaisuus tekee minun hulluksi", lausui Karamanian kuningas hovimiehillensä. "Minua haluttaa puhutella häntä vähän, ennenkuin hän kuolee." Lempiministeri pyysi hallitsiaansa olemaan levollisena; mutta kuninkaallinen parta kävi niin punaiseksi, ja kuninkaalliset silmät iskivät niin kauheata tulta, että lempiministerikin lopulta myöntyi.  Torvi kaikkui, kuuluttajat vaativat vaiti-oloa, ja Alp Arslanin ääni eroitettiin jälleen.  "Senkin koira, näetkö sinä, mikä on tarjonasi? Tiedätkö sinä, mikä vartoo sinua sinun herrasi Ebliin asunnoissa? Voiko väärä ylpeys viehättää Juutalaistakin? Eikö elämä ole suloista? Eikö olisi parempi olla minun varvaskenkieni kantaja kuin tulla seivästetyksi?"  "Jalomielinen Alp Arslan", vastasi Alroy ilmeisen ylenkatseen äänellä; "luuletko, että mikään kidutus rasittaa niin, kuin se muisto, että sinä olet voittanut minun?"  "Partani kautta, hän ivaa minua!" Karamanialaisten hallitsia huudahti; "hän tekee kiusaa minulle! Älkäät koskeko vaippaani. Minä tahdon puhua hänen kanssaan. Te ette näe kauemmaksi kuin hunnustettu haukka, te sokean äidin lapset. Se on noita; hänellä on vielä jälellä joku päätaika; hän pelastaa vielä henkensä. Hän lentää ilmaan taikka vaipuu maan sisään. Hän nauraa meidän kidutuksiamme." Karamanian kuningas astui tuota pikaa valta-istuimensa portaita alaspäin; häntä seurasivat hänen lempiministerinsä ja hänen neuvon-antajansa ja hänen etevimmät päällikkönsä ja kadit ja mollat ja imamit ja kaupungin päähenkilöt.  "Sinä noita!" Alp Arslan huudahti, "hävytön noita! halvan äidin halpa poika! koirien koira! niskotteletko sinä meitä vastaan? Kuiskaako herrasi Eblis toivoa sinun korviisi? Nauratko meidän rangaistuksiamme? Aiotko lentää ylös ilmaan? vai painua alas maahan? Niinkö, niinkö?" Hengästyneenä ja vihastansa uupuneena hallitsia vaikeni. Hän repi partaansa ja polki maata rajussa vimmassaan.  "Sinä olet viisaampi kuin neuvon-antajasi, kuningas Arslan; minä en nöyrry sinun edessäsi. Minun Herrani, vaikka hän ei ole Eblis, ei ole hylännyt minua. Minä nauran sinun rangaistuksiasi. Sinun kidutuksiasi minä ylenkatson. Minä sekä vaivun maan sisään että kohoan ilmaan. Tyydytkö nyt vastaukseeni?"  "Partani kautta", huudahti tulistunut Arslan, "minä tyydyn vastaukseesi. Pelastakoon Eblis sinut, jos hän voi;" ja Karamanian kuningas, Aasian mainioin miekan piteliä veti säilänsä, ikäänkuin salaman, tupesta ja silpaisi yhdellä säväyksellä Alroy''lta pään. Se kaatui, vaan, kun se kaatui, riemuitsevan pilkan hymy näytti vivahtelevan sankarin kylmenevillä kasvoilla ja kysyvän hänen vihollisiltansa: "missä kaikki teidän kidutuksenne nyt ovat?" Do Dzieci Gołąbki i Dziewczynka Dziecię i Koza Wróbel i Jaskółka Osieł i Chłopczyk Nieposłuszny Zajączek Kotek Brytan i Pudelek Egzamin Małego "Misia" Wilk i Owce Lis i Gąski Chłopczyk i Źrebię Gęsia Kapela Lew i Piesek Niedźwiedź i Pszczółka Śniadanie Artysta Z Zimowych Rozrywek Leniwy Chłopczyk Przygoda z Indykiem O hämmästyksissään. Leniwy НЕКУЦЙ'
    );
    
    update test set long_text = null
    where long_text is distinct from
        'Kaikki neuvon-antajat ja etevimmät päälliköt ja mollat ja imamit ja kadit ja kaupungin päähenkilöt olivat suuresti hämmästyksissään. Hänen tunnettu hurskautensa vaati kaikkia äänettömyyteen, sillä välin kuin hän itse lausui pitkän rukouksen, pyytäen Allah''ta ja Profeettaa hämmentämään kaikkia häväiseviä Juutalaisia ja uskottomia ja vuodattamaan totuuden sanoja jumalisten ihmisten suuhun. Ja nyt kunnian-arvoisa sheiki kutsui esiin kaikki todistajat David Alroy''ta vastaan. Heti Kisloch, Kurdilainen, joka oli koroitettu Bagdadin kadiksi, astui esiin, veti sametti-kukkarostansa paperikääryn ja luki semmoisen todistuksen, jossa arvoisa Kisloch vakuutti, että hän ensin tutustui vangin, David Alroy''n kanssa joissakin erämaan raunioissa -- muutamain rosvojen pesässä, joita Alroy johdatti; että hän, Kisloch, oli rehellinen kauppias ja että nämät konnat olivat ryöstäneet hänen karavaninsa ja hän itse joutunut vankeuteen; että hänen vankeutensa toisena yönä Alroy oli ilmestynyt hänen eteensä leijonan muodossa ja kolmantena tuimasilmäisenä härkänä; että hänen oli tapa alinomaa muuttaa itsensä; että hän usein nosti henkiä; että viimein eräänä kauheana yönä Eblis itse tuli suurella juhlasaatolla ja antoi Alroy''lle Salomonin, Davidin pojan valtikan; ja että tämä seuraavana päivänä kohotti lippunsa ja kohta sen jälkeen kukisti Hassan Subah''n ja tämän Seldshukit useitten hirmuisten paholaisten silminnähtävällä avulla.  Kalidaan, Indialaisen, Guebriläisen ja Neekerin ja muutamien muitten saman hengen lapsien todistukset vetivät täysin määrin vertoja Kisloch Kurdilaisen uhkealle kertomukselle. Hebrealaisen valloittajan vastustamaton menestys oli kieltämättömällä tavalla selitetty, Mahomettilaisten aseitten kunnia ja Moslemin uskon puhtaus olivat asetetut jälleen entiseen loistoonsa ja saastuttamattomaan maineesensa. Todeksi saatiin, että David Alroy oli Ebliin lapsi, noitamies, taikakalujen ja myrkkyjen käyttäjä. Kansa kuunteli kauhulla ja harmilla. He olisivat tunkeneet vartiaväen läpitse ja repineet hänet kappaleiksi, jolleivät olisi pelänneet Karamanialaisten sotatapparoita. Niin he lohduttivat mieltänsä sillä, että he ennen pitkää saisivat nähdä hänen kidutuksensa.  Bagdadin kadi kumarsi Karamanian kuningasta ja kuiskasi soveliaan matkan päästä jotakin kuninkaalliseen korvaan. Torvet kaikkuivat, kuuluttajat vaativat äänettömyyttä ja kuninkaan huulet liikkuivat taas.  "Kuule, oi kansa, ja ole viisas. Pääkadi aikoo nyt lukea kuninkaallisen prinsessan Schirenen, noiturin etevimmän uhrin todistuksen."  Ja todistus luettiin, joka vakuutti, että David Alroy omisti ja kantoi lähinnä sydäntänsä erästä talismania, jonka Eblis oli antanut hänelle ja jonka voima oli niin suuri, että, jos sitä kerta painettiin naisen rintaa vastaan, tämä ei enää voinut hallita tahtoansa. Tämmöinen kova onni oli kohdannut oikeauskoisten hallitsian tytärtä.  "Onko siinä niin kirjoitettu?" vanki kysyi.  "On", kadi vastasi, "ja sen alla on vielä prinsessan kuninkaallinen allekirjoitus."  "Se on väärennetty."  Karamanian kuningas kavahti valta-istuimeltansa ja oli vihoissansa astumallaan sen portaita alas. Hänen kasvonsa olivat veripunaiset, hänen partansa kuin tulen liekki. Joku lempiministeri rohkeni vienosti pidättää häntä hänen kuninkaallisesta vaipastansa.  "Tapa paikalla pois se koira", Karamanian kuningas mutisi.  "Prinsessa on itse täällä", lausui kadi, "todistamassa niitä noitakeinoja, joitten alaisena hän oli, vaan joitten vaikutuksesta hän nyt Allah''n ja Profeetan voiman kautta on pääsnyt."  Alroy''ta vävähti!  "Astu esiin, kuninkaallinen prinsessa", kadi sanoi, "ja jos se todistus, jonka kuulit, on perustettu, nosta ylös se kuninkaallinen käsi, joka koristi sen allekirjoituksellaan."  Lähellä valta-istuinta oleva eunukkien joukko teki tilaa; naishaamu, joka oli verhottu hunnulla jalkoihin saakka, astui esiin. Hän nosti ylös kätensä; koko kerääntynyt kansa tuskin hengitti mielenliikutuksesta; eunukkien rivit ummistuivat jälleen; huuto kuului ja hunnustettu haamu katosi.  "Minä odotan kidutuskoneitasi, kuningas", Alroy lausui raskaan surun äänellä. Hänen lujuutensa näytti luopuneen hänestä. Hänen silmänsä olivat luodut maahan. Hän oli nähtävästi vaipunut syvään miettimiseen taikka heittäynyt epätoivoon.  "Valmistakaat seipäät", käski Alp Arslan.  Koko kansan joukkoa värisytti vasten mieltäkin.  Yksi orja lähestyi ja tarjosi paperikääryä Alroy''lle. Hän tunsi Nubialaisen, joka oli Honainin palveluksessa. Hänen entinen ministerinsä ilmoitti hänelle, että hän oli saapuvilla; että ne ehdot, joita hän vankihuoneessa tarjosi, vielä myönnettäisiin; että jos Alroy, jota asiaa hän ei epäillyt ja jota hän rukoili, suostuisi niitä vastaan-ottamaan, hänen tuli pistää paperikäärö poveensa, mutta, jos hän yhä oli taipumaton, jos hänen yhä oli mieletön päätös kuolla hirveä ja häväisevä kuolema, hänen tuli repiä se rikki ja heittää se tanterelle. Silmänräpäyksellä Alroy otti paperikääryn ja repi sen kiivaasti tuhansiin palasiin. Tuulen puuska levitti kappaleet laajalle yliympäri. Alhaiso riiteli näistä David Alroy''n viimeisistä muistoista; ja tämä vähäinen tapaus tuotti paljon hämminkiä.  Tällä välin Neekerit varustivat kidutuksen ja kuoleman koneita.  "Tuon juutalaisen koiran itsepintaisuus tekee minun hulluksi", lausui Karamanian kuningas hovimiehillensä. "Minua haluttaa puhutella häntä vähän, ennenkuin hän kuolee." Lempiministeri pyysi hallitsiaansa olemaan levollisena; mutta kuninkaallinen parta kävi niin punaiseksi, ja kuninkaalliset silmät iskivät niin kauheata tulta, että lempiministerikin lopulta myöntyi.  Torvi kaikkui, kuuluttajat vaativat vaiti-oloa, ja Alp Arslanin ääni eroitettiin jälleen.  "Senkin koira, näetkö sinä, mikä on tarjonasi? Tiedätkö sinä, mikä vartoo sinua sinun herrasi Ebliin asunnoissa? Voiko väärä ylpeys viehättää Juutalaistakin? Eikö elämä ole suloista? Eikö olisi parempi olla minun varvaskenkieni kantaja kuin tulla seivästetyksi?"  "Jalomielinen Alp Arslan", vastasi Alroy ilmeisen ylenkatseen äänellä; "luuletko, että mikään kidutus rasittaa niin, kuin se muisto, että sinä olet voittanut minun?"  "Partani kautta, hän ivaa minua!" Karamanialaisten hallitsia huudahti; "hän tekee kiusaa minulle! Älkäät koskeko vaippaani. Minä tahdon puhua hänen kanssaan. Te ette näe kauemmaksi kuin hunnustettu haukka, te sokean äidin lapset. Se on noita; hänellä on vielä jälellä joku päätaika; hän pelastaa vielä henkensä. Hän lentää ilmaan taikka vaipuu maan sisään. Hän nauraa meidän kidutuksiamme." Karamanian kuningas astui tuota pikaa valta-istuimensa portaita alaspäin; häntä seurasivat hänen lempiministerinsä ja hänen neuvon-antajansa ja hänen etevimmät päällikkönsä ja kadit ja mollat ja imamit ja kaupungin päähenkilöt.  "Sinä noita!" Alp Arslan huudahti, "hävytön noita! halvan äidin halpa poika! koirien koira! niskotteletko sinä meitä vastaan? Kuiskaako herrasi Eblis toivoa sinun korviisi? Nauratko meidän rangaistuksiamme? Aiotko lentää ylös ilmaan? vai painua alas maahan? Niinkö, niinkö?" Hengästyneenä ja vihastansa uupuneena hallitsia vaikeni. Hän repi partaansa ja polki maata rajussa vimmassaan.  "Sinä olet viisaampi kuin neuvon-antajasi, kuningas Arslan; minä en nöyrry sinun edessäsi. Minun Herrani, vaikka hän ei ole Eblis, ei ole hylännyt minua. Minä nauran sinun rangaistuksiasi. Sinun kidutuksiasi minä ylenkatson. Minä sekä vaivun maan sisään että kohoan ilmaan. Tyydytkö nyt vastaukseeni?"  "Partani kautta", huudahti tulistunut Arslan, "minä tyydyn vastaukseesi. Pelastakoon Eblis sinut, jos hän voi;" ja Karamanian kuningas, Aasian mainioin miekan piteliä veti säilänsä, ikäänkuin salaman, tupesta ja silpaisi yhdellä säväyksellä Alroy''lta pään. Se kaatui, vaan, kun se kaatui, riemuitsevan pilkan hymy näytti vivahtelevan sankarin kylmenevillä kasvoilla ja kysyvän hänen vihollisiltansa: "missä kaikki teidän kidutuksenne nyt ovat?" Do Dzieci Gołąbki i Dziewczynka Dziecię i Koza Wróbel i Jaskółka Osieł i Chłopczyk Nieposłuszny Zajączek Kotek Brytan i Pudelek Egzamin Małego "Misia" Wilk i Owce Lis i Gąski Chłopczyk i Źrebię Gęsia Kapela Lew i Piesek Niedźwiedź i Pszczółka Śniadanie Artysta Z Zimowych Rozrywek Leniwy Chłopczyk Przygoda z Indykiem O hämmästyksissään. Leniwy ЙЦУКЕН'
    ;    
  """

act_1 = isql_act('db_1', test_script_1, substitutions=substitutions_1)

expected_stdout_1 = """
     Records affected: 1
     Records affected: 1
     Records affected: 1
  """

@pytest.mark.version('>=3.0')
def test_core_2238_1(act_1: Action):
    act_1.expected_stdout = expected_stdout_1
    act_1.execute()
    assert act_1.clean_expected_stdout == act_1.clean_stdout
