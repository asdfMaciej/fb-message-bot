class Command:
	command_names = [
		'.dtkj', '.tede', '.kurwa'
	]
	admin_only = True
	description = "Dlaczego Tede kurą jest?"
	@staticmethod
	def run(self, params_d):
		tede = "dtkj"
		tede = """Siedziałeś cicho na dupie prawie 3 miechy cieciu
		I ponownie awanturą chcesz wepchnąć album do sklepów
		L4 mi nie trzeba sam sobie pracodawcą
		Bo mam te prace sprawdź to bezrobotnym mięknie jajco
		Ty pajacyku i menago twój Jacyków
		Tede Jakuza dwoch przestrzelonych typów
		Gardło jak to gardło rapem je zajeżdzam ostro
		Lecz to ciebie pojebańcu dziwka zaraziła ospą
		Czy miał wtedy zwolnienie? bo na swoj koncert nie dotarł ?
		Przez kolumbijski katar i weneryk kurwa total
		Tak sie zamotał że nie czekał na odpowiedź
		Torpedując mą zapowiedź boi sie ten mały chłopiec
		A więc zaczynam bo wiem to co nie zakończone
		Mimo iż zapowiadałem że udziału w tym nie biore
		Mowisz na mnie pener? to jest moje drugie imie
		Wydziabane mam na szyi to ty tępy skurwysynie
		I jeśli chcesz ubliżyc to sie wysil kreaturo
		Obrażasz swą posturą polski rap gruba ruro
		Zebraleś baty czas spisać ciebie na straty
		Miedzy nogi bierzesz co? dildo z okładki erraty?
		Spocząć na propsach nie moja jazda
		Jazde urzadzic? ci sprawa ważna
		W życiu rozgardiasz swoim wprowadzasz
		Znów z dupy daleś , mowiąc ze suka zdradza
		Stracileś twarz pokazując swe oblicze
		Fałszywa dziwko dziś dla ciebie ten stryczek
		To jak policzek, uprzedzam bedzie wiecej
		Tede jest kurwą a kraj zaciera ręce
		[Hook]
		Te date zapamieta niebawem cały wszechświat
		To wydarzenia z 12 września
		To jest o hejtach jak będą kończyć
		Tede ten szmaciarz, do nich dołączył
		Po to by zdobyć nieco rozgłosu
		Masz gdzieś chłopaka, p-r hip hopu
		Chodzi o ciebie, chce fejmu rura
		Tylko po to ten beef, pretekst-Zielona Góra
		[Verse 2]
		Myślał że jest niezły a spierdolił do Tunezji
		Zamiast nagrywać teksty trzymał za zębami język
		Poparcia wiece to 35-lecie
		Nie o hip hop chodziło a o Jacusia przeciez
		Ciebie pierdole bo jesteś cieńki Bolek
		I odwołam Ci jeszcze kilka koncertów koleś
		No i widze co robisz, szalejesz jak ranny jeleń
		Chcialem to olać lecz jeszcze nie oleje
		Boli cie że ludzie skandują "jebać Tedego"
		Sami to krzyczą ja nie zmuszam ich do tego
		Ty i twoj dystans to raczej sprzeczność
		Rozrywką dla mnie,urządzić ci piekło
		Mieszkasz w stolicy a zachowujesz sie jak pastuch
		Hurtowo nagrywa na przód wstyd przynosi miastu
		Jest pocisk masz odpowiedź i tak w kółko [tak robie]
		A ty naprzód kombinujesz niezliczoną ilość zwrotek
		Zrozum debilu zakladam hipotetycznie
		Nawet gdybyś zdołał wygrać nic nie zdolasz , wiem to przykre
		Zszarganej reputacji nie dasz rady naprawić
		Jak na trupa to powinien zamknąc ryj, zamilcz panicz
		Tede plus hip hop równa sie jemu nie wyszło
		To bieguny przeciwległe wiec precz z tym kurestwem
		W Warszawie świety? raczej z chuja wyciety
		Ja gralem te dissy w Warszawie jesteś przeklęty
		A u mnie to nigdy gwiazdą nie bedziesz
		Chyba ze znow nawinę. spadająca gwiazda Tede..."""
		params_d['functions_holder']._send_multiline(tede.split('\n'), params_d['thread_id'], params_d['thread_type'])
