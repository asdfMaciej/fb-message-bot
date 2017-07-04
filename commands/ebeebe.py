class Command:
	command_names = [
		'.ebe', '.ebeebe', '.ebebe', '.mefedron'
	]
	admin_only = True
	description = "Mefedron to szmata"
	@staticmethod
	def run(self, params_d):
		tede = "bonusrpk"
		tede = """[Zwrotka]
Mefedron to szmata, suki nie chce znać, jebać
Może z kurwą ruszę, jeśli zajdzie potrzeba, a na razie to to zlewam, jebać
Czegoś się spodziewał, że tutaj zginę?
Pu pu pu, nie ten rocznik skurwysynie
Farszem nabijam cukinie, jeśli bit byłby cukinią
Ding dong, nie pojedziesz tą windą
Zagrasz w ping pong, to kurwa odbij
Lubisz plotki, Ty mój chuj jest słodki
Twoje ruchy mrzonki, Twoje ziomki to pionki
Przeciwko nam kurwa rządowe czołgi
Czujesz się spokojny, to pewnie żyjesz w błędzie
Czujesz niespokojnie, to pewnie masz wyjęte
Parę nocy z rzędu przegrywasz z wielodobem
Zasypiasz, pierdolić ćpuńskie fobie (tfu!)
Jadę z tym, jakbym kurwa jechał z dziwką
Polska, Warszawa, Ciemna Strefa, Hip-Hop
Macie coś przeciwko? To mamy beef na noże
Dobry Boże, ja pierdole co za młodzież
Co się rap to się woże, no bo co kurwa nie może?
Chuj mnie boli co se napiszesz na forze
Jointy smoże, voilà madame
Ty kurwa taka, że by smyrnął po pośladach
Takie właśnie tutaj wypierdalam
A Ty w populizmach się upierdalaj
Dzyń dzyń, co tam morda u Ciebie?
Ebe ebe, ebe ebe ebe
I bardzo dobrze, to nie głuchy telefon
Idź pokrzycz do lasu, to usłyszysz echo
Echo, satelita wysoko
Namierza Twój telefon, logowania (Hello Moto)
Weź ogarnij coś by nie wiedział o tym nikt
Że ściany mają uszy wiadomo nie od dziś
Sąsiedzi złe intencje, zawodzi czynnik ludzki
Tak jak bydle leci do garnka wódki
Potęga gotówki, nie chce skończyć jak reszta
Zresztą znowu wypada reszka
Jebana dilerka, wróżby z białego prochu
Wybierz jedną liczbę od dziesięciu do roku
Atmosfera gęsta coraz bardziej w butli
Exclusive rich bitch, kupują futra z nutrii
Putry, kasyna, hotele, zabawa
Jebnie Ci pikawa kurwa fa, zawał
La viva lambada, ładnie żeś nakłamał
Sąd Cię uniewinnia, bo sam tego nie ogarnia
To nie kurwa narnia, choć tysiące bajek
Cuda-wianki, pióropusze, kaszel od ruskich fajek
Tiri titi, meliniarsko kurwa dewastacyjne graffiti
Pod kołami big city, a problemy największe
Zawsze ktoś do kogoś ma gdzieś o coś pretensje
Ktoś maczety, miecze, ktoś ma rottweilery
Ktoś pierwsza liga samar, ktoś dopierdolony steryd
Ktoś ma dobry rap, a ktoś go kurwa nie ma
Siema, siema, siema, pozdrowienia z podziemia"""
		params_d['functions_holder']._send_multiline(tede.split('\n'), params_d['thread_id'], params_d['thread_type'])
