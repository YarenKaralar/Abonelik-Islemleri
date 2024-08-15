import json
import time
with open("abonelik.json","r") as file:           # abonelik.json DOSYASININ KAYITLI OLDUĞU DİZİN YOLUNU BURAYA YAZMAMIZ GEREKİYOR! (Eğer bu satırda hata alıyorsak dosyanın kayıtlı olduğu yeri ve buraya yazılan dizin yolunu kontrol etmeliyiz.)
    icerikpy=json.load(file)     #json dosyasındaki verileri python objesine dönüştürdük.

    idler=[]
    for kisi in icerikpy["kullanicilar"]:
        idler.append(kisi["id"])


    #1
    def tumdosya():
        icerikjson = json.dumps(icerikpy,indent=3)  # python objesini daha okunabilir olması açısından 3 girinti olacak şekilde json string verisine dönüştürdük.
        print(icerikjson)

    #2
    def isimden_id():              #çoğu abonelik işlemlerinde kişi ismi yerine id üzerinden işlem yapıldığı için kişi isminden id sorgulamak amacıyla tasarlanmıştır.
        print("\nTum Kullanicilar ve Id'leri:")
        isimler = []
        for kisi in icerikpy["kullanicilar"]:
            isimler.append(kisi["ad"])
        id_isim = list(zip(idler, isimler))
        for id,isim in id_isim:
            print("Id:", id, "- Ad:", isim)

        secenek = input("\nSadece bir kullanicinin adini ve id'sini gormek icin 'e' tusuna basiniz (gecmek icin 'h' tusuna basiniz): ")
        if secenek == "e":
            isim = input("\nId'sini ogrenmek istediginiz kisinin adini giriniz: ")
            for kisi in icerikpy["kullanicilar"]:
                if kisi["ad"] == isim:
                    print("Ad:", kisi["ad"], "\nId:", kisi["id"])
                    break
                if kisi["id"] == idler[-1]:
                    print("Aradiginiz kullanici kayitlarda bulunmamaktadir!")

    # 3
    def kullanici_bilgileri():
        secim = input("\nBilgilerini gormek istediginiz kullanicinin id'sini veya adini giriniz: ")
        for kisi in icerikpy["kullanicilar"]:
            if str(kisi["id"]) == secim or kisi["ad"] == secim:
                print("Id:",kisi["id"],"\nAd:",kisi["ad"],"\nYas:",kisi["yas"],"\nE-posta:",kisi["eposta"],"\nTel:",kisi["tel"],"\nAdres:[\nSokak:",kisi["adres"]["sokak"])
                print("Sehir:",kisi["adres"]["sehir"],"\nPosta kodu:",kisi["adres"]["posta_kodu"],"\n]")
                print("Abonelikler:")
                for abonelik in kisi["abonelikler"]:
                    print("---\nHizmet:",abonelik["hizmet"],"\nDurum:",abonelik["durum"],"\nAylik Ucret:",abonelik["aylik_ucret"],"\nDevam Suresi:",abonelik["sure_ay"],"ay")
                    print("Taahhut Suresi:",abonelik["taahhut_suresi"],"ay")
                    if abonelik["durum"]=="pasif":
                        print("Pasif Nedeni:",abonelik["pasif_nedeni"])
                break
            if kisi["id"] == idler[-1]:
                print("Aradiginiz id kayitlarda bulunmamaktadir!")


    #4
    def iletisim_bilgileri():          #kullanıcı ile iletişim kurulması gerektiğinde bütün bilgilerini ekrana getirmek yerine sadece iletişim bilgilerini görebilmek için tasarlanmıştır.
        iletisim = []
        iletisim_bilgileri = {}
        for kisi in icerikpy["kullanicilar"]:        #ayrıca bu yöntemden farklı olarak yani 3 kategoriyi de(ad,telefon no ve eposta) aynı listede toplamak yerine 3'ü için ayrı listeler oluşturulup zip fonksiyonu ile birleştirilebilir.
            iletisim.append(kisi["ad"])
            iletisim.append(kisi["tel"])
            iletisim.append(kisi["eposta"])
        index = 0
        for i in idler:
            iletisim_bilgileri[i] = [iletisim[index], iletisim[index + 1], iletisim[index + 2]]  # iletişim bilgileri adında bir sözlük oluşturuldu, anahtar olarak id seçildi bu sayede sadece id girilerek kişilerin iletişim bilgilerine ulaşılabilir.
            index += 3   #her bir kullanıcının 3 tane verisi olduğu için diğer kullanıcıya geçerken indexi 3 arttırıyoruz.

        secim = int(input("\nIletisim bilgilerini gormek istediginiz kisinin id'sini giriniz: "))
        for kisi in icerikpy["kullanicilar"]:
            if kisi["id"] == secim:
                print(iletisim_bilgileri[secim])
                break
            if kisi["id"] == idler[-1]:
                print("Aradiginiz id kayitlarda bulunmamaktadir!")

        secenek = input("\nTum kullanicilarin iletisim bilgilerini gormek icin 'e' tusuna basiniz (gecmek icin 'h' tusuna basiniz): ")
        if secenek == "e":
            print("\nTum kullanicilarin iletisim bilgileri:")
            for i in iletisim_bilgileri:
                print("Id:",i, "---", iletisim_bilgileri[i])


    #5
    def aktif_abonelikler():
        aktifler = {}
        hizmetler = []
        adet = 0
        for kisi in icerikpy["kullanicilar"]:
            for abonelik in kisi["abonelikler"]:
                if abonelik["durum"] == "aktif":
                    adet += 1
                    hizmetler.append(abonelik["hizmet"])
                    hizmetler.append((abonelik["taahhut_suresi"] - abonelik["sure_ay"]))
            hizmetler.append(adet)  # bir kullanıcıya ait aktif hizmetlerin bulunduğu listenin son elemanı olarak kaç adet aktif abonelik olduğu eklenir.
            aktifler[kisi["id"]] = hizmetler
            hizmetler = []
            adet = 0

        secim = int(input("Aktif aboneliklerini gormek istediginiz kullanicinin id'sini giriniz: "))
        for kisi in icerikpy["kullanicilar"]:
            if kisi["id"] == secim:
                print("\nId:", kisi["id"], "- Ad:", kisi["ad"], "\nAktif abonelikler:\n---")
                for i in range(0, len(aktifler[secim]) - 1, 2):
                    print("Hizmet:", aktifler[secim][i], "--", "Kalan sure:", aktifler[secim][i + 1], "ay\n---")
                print("Id'si", kisi["id"], "olan kullaniciya ait", aktifler[secim][-1],"adet aktif abonelik mevcuttur.\n")
                break
            if kisi["id"] == idler[-1]:
                print("Aradiginiz id kayitlarda bulunmamaktadir!")

        secenek = input("Tum kullanicilarin aktif aboneliklerini gormek icin 'e' tusuna basiniz (gecmek icin 'h' tusuna basiniz): ")
        if secenek == 'e':
            print("\nTUM KULLANICILARIN AKTIF ABONELIKLERI\n")
            for kisi in icerikpy["kullanicilar"]:
                print("Id:", kisi["id"], "- Ad:", kisi["ad"])
                for i in range(0, len(aktifler[kisi["id"]]) - 1, 2):
                    print("Hizmet:", aktifler[kisi["id"]][i], "--", "Kalan sure:", aktifler[kisi["id"]][i + 1], "ay")
                print("Id'si", kisi["id"], "olan kullaniciya ait", aktifler[kisi["id"]][-1],"tane aktif abonelik mevcuttur.\n-----------------")


    #6
    def taahhut_1ay():         #kullanıcıların aktif olarak kullandıkları aboneliklerin taahhutunun bitmesine 1 ay kalanları bir arada görebilmek bu sayede de kullanıcıyı bilgilendirebilmek için tasarlanmıştır.
        bir_ay = {}
        liste = []
        print("\nTUM KULLANICILARIN TAAHUTUNUN BITMESINE 1 AY KALAN AKTIF ABONELIKLERI:")
        isim = False
        for kisi in icerikpy["kullanicilar"]:
            for abonelik in kisi["abonelikler"]:
                if abonelik["durum"]=="aktif":
                    if abonelik["taahhut_suresi"] - abonelik["sure_ay"] == 1:
                        if isim == False:  # kullanıcının adı ve id'si ekrana yazıldıysa tekrar aynı ismin yazılmaması için bir değişken ile kontrol ediliyor.
                            print("\nId:", kisi["id"], "- Ad:", kisi["ad"])
                            isim = True
                        liste.append(abonelik["hizmet"])
                        print("Hizmet:", abonelik["hizmet"], "- Kalan Sure: 1 ay")
            bir_ay[kisi["id"]] = liste  # verilerin kaybolmaması için bir sözlükte topluyoruz.
            liste = []
            isim = False


    #7
    def pasif_abonelikler():
        pasifler = {}    # aktif olan abonelikleri toplarken kullanılan yöntemden farklı bir yöntem kullanarak pasifleri buluyoruz.
        hizmetler = []
        neden = []
        sure = []
        adet = 0
        for kisi in icerikpy["kullanicilar"]:
            for abonelik in kisi["abonelikler"]:
                if abonelik["durum"] == "pasif":
                    adet += 1
                    hizmetler.append(abonelik["hizmet"])
                    neden.append(abonelik["pasif_nedeni"])
                    sure.append(abonelik["taahhut_suresi"] - abonelik["sure_ay"])
            pasifler[kisi["id"]] = list(zip(hizmetler, neden, sure))
            hizmetler = []
            neden = []
            sure = []

        secim = int(input("Pasif aboneliklerini ve nedenlerini gormek istediginiz kullanicinin id'sini giriniz: "))
        for kisi in icerikpy["kullanicilar"]:
            if kisi["id"] == secim:
                if pasifler[secim] != []:
                    print("\nId:", kisi["id"], "- Ad:", kisi["ad"])
                    for hizmet in pasifler[secim]:
                        print("---")
                        print("Hizmet:", hizmet[0])
                        print("Pasiflik nedeni:", hizmet[1])
                        print("Pasif kaldigi sure:", hizmet[2], "ay")
                    break
                else:
                    print("Kullanicinin pasif olan aboneligi yoktur.")
                    break
            if kisi["id"] == idler[-1]:
                print("Aradiginiz id kayitlarda bulunmamaktadir!")

        secenek = input("\nTum kullanicilarin pasif aboneliklerini gormek icin 'e' tusuna basiniz (gecmek icin 'h' tusuna basiniz): ")
        if secenek == 'e':
            for kisi in icerikpy["kullanicilar"]:
                print("\nId:", kisi["id"], "- Ad:", kisi["ad"])
                print("------")
                if pasifler[kisi["id"]] != []:
                    for hizmet in pasifler[kisi["id"]]:
                        print("Hizmet:", hizmet[0])
                        print("Pasiflik nedeni:", hizmet[1])
                        print("Pasif kaldigi sure:", hizmet[2], "ay")
                        print("------")
                else:
                    print("Kullanicinin pasif olan aboneligi yoktur.\n------")


    #8
    def pasiflik_nedeni():            #kullanıcıların en çok hangi nedenlerden dolayı aboneliklerini pasif yaptıklarını görebilmek ve uygun önlemler alabilmek için tasarlanmıştır.
        nedenler = []
        neden_adet = {}
        yuksek_fiyat={}
        for kisi in icerikpy["kullanicilar"]:
            for abonelik in kisi["abonelikler"]:
                if abonelik["durum"] == "pasif":
                    if abonelik["pasif_nedeni"] not in nedenler:        # eğer nedenler listesine eklenmiş bir pasif nedeni varsa tekrar eklememek için kontrol ediyoruz.
                        nedenler.append(abonelik["pasif_nedeni"])
                        neden_adet[abonelik["pasif_nedeni"]] = 1  # eğer pasiflik nedeni sözlüğe daha önceden eklenmemişse adetini 1 olarak ekliyoruz.
                    else:
                        neden_adet[abonelik["pasif_nedeni"]] += 1  # eğer pasiflik nedeni sözlüğe daha önceden eklenmişse olan adeti bir arttırıyoruz.
                    if abonelik["pasif_nedeni"]=="Yuksek fiyat":
                        yuksek_fiyat[kisi["id"]]=[kisi["ad"],abonelik["hizmet"],abonelik["aylik_ucret"]]

        print("\nAboneliklerin Pasif Olma Nedenleri ve Guncel Adetleri:")
        for neden,adet in neden_adet.items():
            print("* Neden:", neden, "- Adet:", adet,"kullanici")

        secim=input("\nYuksek fiyattan dolayi pasif olan abonelikleri ve kullanicilarini gormek icin 'e' tusuna basiniz (gecmek icin 'h' tusuna basiniz): ")
        if secim=="e":
            print("\nYUKSEK FIYAT SEBEBİYLE:")
            for id,hizmet in yuksek_fiyat.items():
                print("---")
                print("Id:",id,"- Ad:",hizmet[0])
                print("Abonelik:",hizmet[1],"\nUcret:",hizmet[2])

    #9
    def hizmet_kullanici():
        hizmetler={}
        for kisi in icerikpy["kullanicilar"]:
            for abonelik in kisi["abonelikler"]:
                if abonelik["hizmet"] not in hizmetler:
                    hizmetler[abonelik["hizmet"]] = list()
                hizmetler[abonelik["hizmet"]].append(kisi["ad"])
                hizmetler[abonelik["hizmet"]].append(abonelik["durum"])
        print("TUM HIZMETLER VE KULLANICILARI:")
        for hizmet,degerler in hizmetler.items():
            print("\n   --- Hizmet:",hizmet.upper(),"---")
            adet=0
            for i in range(0,len(degerler),2):
                print(adet+1,"-","Isim:",degerler[i],"- Durum:",degerler[i+1])
                adet+=1

    #10
    def yas_araligi():            #hangi yaş aralığındaki kullanıcıların hangi abonelikleri daha çok tercih ettiğini görebilmek ve bu sayede kullanıcıya en uygun tercihleri sunabilmek için tasarlanmıştır.
        yaslar=[]
        for kisi in icerikpy["kullanicilar"]:
            yaslar.append(kisi["yas"])
        def olustur(min,max):
            aktifler = []
            aktif_adet = {}
            pasifler = []
            pasif_adet = {}
            aralik = list(filter(lambda yas: min <= yas <= max, yaslar))
            for kisi in icerikpy["kullanicilar"]:
                if kisi["yas"] in aralik:
                    for abonelik in kisi["abonelikler"]:
                        if abonelik["durum"] == 'aktif':
                            if abonelik["hizmet"] not in aktifler:
                                aktifler.append(abonelik["hizmet"])
                                aktif_adet[abonelik["hizmet"]] = 1
                            else:
                                aktif_adet[abonelik["hizmet"]] += 1
                        if abonelik["durum"] == 'pasif':
                            if abonelik["hizmet"] not in pasifler:
                                pasifler.append(abonelik["hizmet"])
                                pasif_adet[abonelik["hizmet"]] = 1
                            else:
                                pasif_adet[abonelik["hizmet"]] += 1
            return aktif_adet,pasif_adet

        aktif_20_30, pasif_20_30=olustur(20,30)
        print("\n* 20 - 30 YAS ARALIGINDAKI KULLANICILARIN ABONELIK TERCIHLERI *\n")
        print("--AKTIF ABONELIKLER--")
        for hizmet,adet in aktif_20_30.items():
            print(hizmet,"-",adet,"kullanici")
        print("--PASIF ABONELIKLER--")
        for hizmet,adet in pasif_20_30.items():
            print(hizmet, "-", adet, "kullanici")

        aktif_30_40, pasif_30_40 = olustur(30, 40)
        print("\n* 30 - 40 YAS ARALIGINDAKI KULLANICILARIN ABONELIK TERCIHLERI *\n")
        print("--AKTIF ABONELIKLER--")
        for hizmet,adet in aktif_30_40.items():
            print(hizmet, "-", adet, "kullanici")
        print("--PASIF ABONELIKLER--")
        for hizmet,adet in pasif_30_40.items():
            print(hizmet, "-", adet, "kullanici")

        aktif_40_60, pasif_40_60 = olustur(40, 60)
        print("\n* 40 YAS VE UZERI KULLANICILARIN ABONELIK TERCIHLERI *\n")
        print("--AKTIF ABONELIKLER--")
        for hizmet,adet in aktif_40_60.items():
            print(hizmet, "-", adet, "kullanici")
        print("--PASIF ABONELIKLER--")
        for hizmet,adet in pasif_40_60.items():
            print(hizmet, "-", adet, "kullanici")


   #11
    def fiyat_sirala():
        ucretler={}
        hizmet=[]
        ucret=[]
        adet=1
        for kisi in icerikpy["kullanicilar"]:
            for abonelik in kisi["abonelikler"]:
                ucretler[abonelik["hizmet"]]=abonelik["aylik_ucret"]      #burda ilk olarak sözlüğe eklememizin amacı; sözlük aynı olan hizmetleri tekrar tekrar eklemez sadece değerini günceller. Eğer ilk olarak listeye ekleseydik aynı hizmetleri her seferinde listeye tekrar eklerdi.
        for key in ucretler:
            hizmet.append(key)
            ucret.append(ucretler[key])
        sirali=list(zip(ucret,hizmet))          # burada ise tekrar bir liste oluşturmamızın amacı  hizmetlerin ve kendilerine ait ücretlerin bir arada tutulması ve karışmamasıdır.
        sirali.sort()
        print("-ABONELIKLERIN EN DUSUK FIYATTAN EN YUKSEGE DOGRU SIRALANISI-")
        for fiyat,program in sirali:
            print(str(adet)+". Hizmet:",program,"--- Ucret:",fiyat)
            adet+=1

    #12
    def yeni_veri():
        yeni_kayit={}
        idler.append(idler[-1]+1)
        yeni_kayit["id"]=idler[-1]
        print("\nYeni Kullanici Bilgilerini Giriniz:")
        yeni_kayit["ad"]=input("Ad Soyad: ")
        yeni_kayit["yas"]=int(input("Yas: "))
        yeni_kayit["eposta"]=input("E-posta: ")
        yeni_kayit["tel"]="+90 "+input("Telefon no: +90 ")
        yeni_kayit["adres"]={}
        print("-Adres Bilgisi-")
        yeni_kayit["adres"]["sokak"]=input("Sokak: ")
        yeni_kayit["adres"]["sehir"]=input("Sehir: ")
        yeni_kayit["adres"]["posta_kodu"]=int(input("Posta kodu: "))
        yeni_kayit["abonelikler"]=[]
        abonelik={}
        print("-Abonelik Bilgisi-")
        while(True):
            print("---")
            abonelik["hizmet"]=input("Hizmet: ")
            abonelik["durum"]=input("Durum[aktif/pasif]: ")
            abonelik["aylik_ucret"] = float(input("Aylik ucret: "))
            abonelik["sure_ay"]=int(input("Devam edilen sure(ay): "))
            abonelik["taahhut_suresi"]=int(input("Taahhut suresi(ay): "))
            if abonelik["durum"]=="pasif":
                abonelik["pasif_nedeni"]=input("Pasif nedeni: ")
            print("---")
            yeni_kayit["abonelikler"].append(abonelik)
            abonelik = {}
            secim=input("Yeni bir abonelik eklemek istiyor musunuz? [e/h] : ")
            if secim!='e':
                break
        #kayit_json = json.dumps(yeni_kayit, indent=3)         bu iki satır, verileri girilen kaydı dosyaya yüklemeden önce json string verisi olarak görmenizi sağlar.Yani dosyaya yüklenecek haliyle gösterir.
        #print(kayit_json)
        icerikpy["kullanicilar"].append(yeni_kayit)  # yeni veriyi, tüm dosya verilerinin bulunduğu python objesi olan icerikpy adlı sözlüğün, kullanicilar listesine ekliyoruz.
        with open('abonelik.json', 'w') as file:     # json dosyasıni yazma modunda açıyoruz.
            json.dump(icerikpy, file, indent=3)  # yeni veriyi ekleyip tüm dosya içeriğini yeniden dosyaya yazıyoruz.
        print("Yeni kullanici kaydediliyor...")
        for i in range(3, 0, -1):
            print(i, "sn kaldi.")
            time.sleep(1)  # 3 saniyeliğine program durdurulur sonra devam eder.
        print("Basariyla kaydedildi!\n")
        devam=input("Yeni bir kayit daha eklemek istiyor musunuz? [e/h] : ")
        if devam=='e':
            yeni_veri()



    dongu=True
    print("                                       * ABONELIK ISLEMLERI *")
    while(dongu):
        print("""-----------------------------------------------------------------------------------------------------------
| 1-Tum dosyayi ekrana yazdirma                                                                           |
| 2-Tum kullanici adlari ve id'lerini listeleme (isimden id sorgulama)                                    |
| 3-Bir kullanicinin tum bilgilerini ekrana yazdirma                                                      |
| 4-Kullanicilarin iletişim bilgilerini ekrana yazdirma                                                   |
| 5-Kullanicilarin aktif olan aboneliklerini ve taahhutun bitmesine kalan sureyi ekrana yazdirma          |
| 6-Tum kullanicilarin taahhutunun bitmesine 1 ay kalan aktif aboneliklerini listeleme                    |
| 7-Kullanicilarin pasif olan aboneliklerini, kaç aydir pasif olduklarini ve nedenlerini listeleme        |
| 8-Tum pasiflik nedenlerini ekrana listeleme (Kullanicidan bagimsiz)                                     |
| 9-Tum hizmetleri ve hangi kullanicilarin kullandigini listeleme                                         |
| 10-Yas araligina gore abonelik tercihlerini listeleme                                                   |
| 11-Abonelik hizmetlerini en dusuk fiyattan en yuksege dogru siralama                                    |
| 12-Yeni kullanici kaydi ekleme                                                                          |
-----------------------------------------------------------------------------------------------------------
        """)
        secim = int(input("Yapmak istediginiz islemin numarasini giriniz: "))

        if secim == 1:
            tumdosya()
        elif secim == 2:
            isimden_id()
        elif secim == 3:
            kullanici_bilgileri()
        elif secim == 4:
            iletisim_bilgileri()
        elif secim == 5:
            aktif_abonelikler()
        elif secim == 6:
            taahhut_1ay()
        elif secim == 7:
            pasif_abonelikler()
        elif secim == 8:
            pasiflik_nedeni()
        elif secim == 9:
            hizmet_kullanici()
        elif secim == 10:
            yas_araligi()
        elif secim == 11:
            fiyat_sirala()
        elif secim == 12:
            yeni_veri()
        else:
            print("GECERSIZ SECIM YAPTINIZ!")


        while(True):
            value = input("\nProgramdan cikmak icin 'e' tusuna, ana menuye donmek icin 'b' tusuna basiniz: ")
            if value == 'b':
                dongu = True
                print("                                             * ANA MENU *")
                break
            elif value == 'e':
                dongu = False
                break
            else:
                print("GECERSIZ SECIM YAPTINIZ!")

