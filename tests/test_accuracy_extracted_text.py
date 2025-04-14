from pathlib import Path
from backend.pdf_processor import process_pdf
import time
from datetime import timedelta
from models.gpt4_cleaning_text import cleaning
from backend.check_pdf import check

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Aßußfere Wendung.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Aßußfere Wendung.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtseinleitung.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtseinleitung .pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilf.txt") #problematik
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfe.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\test.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\test.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Kaiserschnitt.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Kaiserschnitt.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Narkose.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Narkose.pdf")

# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilfliche Maßnahmen.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfliche Maßnahmen.pdf")

text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\Geburtshilfliche_nahmen - edited.txt")
pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\Geburtshilfliche_nahmen.pdf")


# text_path = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\text\IntroductionToAnaesthesia.txt")
# pdf = Path(r"C:\Users\zohre\OneDrive\Desktop\sample_pdfs\IntroductionToAnaesthesia.pdf")


def compare_texts(extracted_text: str, real_text_path: Path):
    with open(real_text_path, 'r', encoding='utf-8') as f:
        real_text = f.read()

    real_words = real_text.split()
    extracted_words = extracted_text.split()

    missing_words_real_to_extract = [word for word in real_words if word not in extracted_words]

    total_words = len(real_words)
    correct_words = total_words - len(missing_words_real_to_extract)
    accuracy = (correct_words / total_words) * 100 if total_words else 0

    return round(accuracy, 2), missing_words_real_to_extract


def test_compare_extraction_accuracy():
    start = time.perf_counter()
    checking = check(pdf)
    data = process_pdf(pdf)
    duration = timedelta(seconds=time.perf_counter() - start)
    print(f"Extracting text from origin PDF took: {duration}")

    if checking:
        print("OCRRRRRRRRRRRRRRRRRR")
        data_org = ""
        if data["status"] == "success":
            extracted_data = data["extracted data"]
            for page_key in extracted_data:  # Iterate through all pages
                t = extracted_data[page_key].get("extracted text from image", "")
                print(page_key)
                print(t)
                data_org += " " + t + " "

        data_org = cleaning(data_org).lower().replace("perenne hoorsa stellt sich vor","sehr geehrte frau elli test,")
        data_org = data_org.replace("–", "").replace("- ", "").replace(".", "").replace(":", "").replace("/", " ")

        print(data_org)
        accuracy_org_real, loss_org_real = compare_texts(data_org, text_path)

        pdf_name = pdf.name
        print(f"\n---------- {pdf_name} ----------\n")
        print(f"Missing real to extract: {loss_org_real}")
        print(f"length of loss: {len(loss_org_real)}")
        print(f"Accuracy real to extract: {accuracy_org_real}%")
    else:
        print("Normallllllllllllllllllllllllllllll")
        data_scanned = ""
        if data["status"] == "success":
            pages = data["extracted data"][:5]
            for page in pages:
                for para in page.get("paragraphs", []):
                    data_scanned += para.get("paragraph", "") + " "
                for img in page.get("extracted images", []):
                    data_scanned += img.get("extracted text from image", "") + " "

        # data_scanned = cleaning(data_scanned)
        data_scanned.lower().replace("perenne hoorsa stellt sich vor","sehr geehrte frau elli test,")
        data_scanned = data_scanned.replace("–", "").replace("- ", "").replace(".", "").replace(":", "").replace("/", " ")

        # print(data_scanned)
        accuracy_scanned_real, loss_scanned_real = compare_texts(data_scanned, text_path)

        pdf_name = pdf.name
        print(f"\n---------- {pdf_name} ----------\n")
        print(f"Missing real to extract: {loss_scanned_real}")
        print(f"length of loss: {len(loss_scanned_real)}")
        print(f"Accuracy real to extract: {accuracy_scanned_real}%")



Missing: ['eli', 'unsere', 'unterlagen', 'gesundheitlichen', 'erkennen', 'echtzeit', 'bewussten', 'entscheidung', 'geburtshelfern', 'aufgeführten', 'sicherheit', 'ermöglichen', 'gefährdungen', 'erkennen', 'einzuleiten', '1', 'speziellen', 'hörrohr', 'stethoskop', 'ähnelt', 'regelmäßigen', 'abständen', 'abgehört', 'ultraschall', 'doppleruntersuchung', '2', 'eröffnet', 'genauere', 'eingelegt', '3', 'verdacht', 'könnte', 'erhält', 'wichtige', 'informationen', 'notwendige', 'linderung', 'geburtsschmerzen', 'entspannungsübungen', 'atemtechnik', 'arten', 'eröffnungswehen', 'beginn', 'vollständigen', 'eröffnung', 'muttermunds', '10', 'cm', 'akupunktur', 'akupressur', 'aromatherapie', 'hypnose', 'homöopathie', 'quaddeln', 'transkutane', 'elektrische', 'nervenstimulation', 'beruhigende', 'tabletten', 'zäpfchen', 'geburtsphase', 'sog', 'austreibungsphase', 'örtlich', 'pudendusanästhesie', 'örtliches', 'betäubungsmittel', 'nähe', 'schmerzleitenden', 'gespritzt', 'lachgassauerstoffgemisch', 'schmerzhafte', 'wehe', 'aufbaut', 'pda', 'unteren', 'wirbelsäule', 'speziell', 'ausgebildeten', 'pda', 'spezifischen', 'möglichen', 'aufklären', 'danach', 'entscheiden', 'gemeinsam', 'terminüberschreitung', 'verschiedenen', 'erkrankungen', 'störungen', 'sofern', 'vorgesehen', 'verschiedenen', 'möglichen', 'deren', 'nachteile', 'aktuelle', 'beweise', 'ermöglichen', 'ctgveränderungen', 'notkaiserschnitt', 'geplanten', 'berücksichtigen', 'gabe', 'anzeichen', 'vorzeitigen', 'nachweis', 'streptokokken', 'angeboten', 'reduzieren', 'schultern', 'somit', 'vermieden', 'aktive', 'ctgveränderungen', 'hindeuten', 'verlängerter', 'pressperiode', 'großem', 'saugglocken', 'zangengeburt', 'häufiger', 'zange', 'gefahrensituation', 'stillstand', 'abfall', 'pressperiode', 'stehendem', 'zange', 'verwendet', 'beschleunigen', 'instrument', 'eingeführt', 'seitlich', 'am', 'angelegt', 'ermöglicht', 'pressen', 'vorsichtigen', 'zug', 'sectio', 'caesarea', 'geburtsbeginn', 'risikofaktoren', 'großes', 'mehrlingsschwangerschaft', 'drohende', 'frühgeburt', 'abnormale', 'steißlage', 'bekannt', 'manchen', 'echte', 'alternative', 'spontanen', 'ärztliche', 'nachteile', 'kaiserschnitts', 'gegenüber', 'besprechen', 'gemeinsam', 'entscheidung', 'treffen', 'ergeben', 'übermäßige', 'nabelschnurvorfall', 'riss', 'veränderungen', 'zeichen', 'drohenden', 'gefährdung', 'regulierkrankungen', 'geburtsstillstand', 'notkaiserschnitt', 'starker', 'beeinträchtigung', 'miteinander', 'nachteile', 'belastungen', 'kaiserschnitts', 'sprechen', 'einwilligung', 'erteilen', 'bitten', 'schon', 'jetzt', 'einverständnis', 'verweigern', 'lebensgefährlichen', 'behindert', 'versterben', 'selbst', 'zuerst', 'schnitt', 'seitlich', 'schamhaargrenze', 'geöffnet', 'eröffnet', 'herausgenommen', 'danach', 'verschlossen', 'wünschen', 'nachgeburt', 'ausgestoßen', 'antidprophylaxe', 'rhesusnegativ', 'rhesuspositiv', 'impfung', 'blutgefäß', 'beinvenenthrombose', 'lungenembolie', 'schlaganfall', 'herzinfarkt', 'gerinnungsstörung', 'hit', 'allergieunverträglichkeit', 'latex', 'dauerhafte', 'organversagen', 'hirnschädigung', 'lähmungen', 'allergische', 'reaktionen', 'hämatome', 'beruhigungs', 'sauerstoffgabe', 'schwindel', 'euphorie', 'mittelohr', 'vorkommen', 'richtige', 'anwendung', 'verordnet', 'fälle', 'schwerer', 'behandlungsbedürftiger', 'worden', 'schamlippenrisse', 'schamlippen', 'am', 'darms', 'darmscheidenfistel', 'anatomischer', 'blasenscheidenfistel', 'darmvorfall', 'geschlechtsverkehr', 'darmausgangs', 'harn', 'beckenbodengymnastik', 'spätere', 'gebärmutteroperation', 'harnblase', 'harnleiter', 'atonie', 'nähten', 'versorgen', 'weiter', 'notig', 'klitoris', 'hepatitis', 'aids', 'be', 'vergleich', 'geplanten', 'kaiser', 'handelbar', 'aufsteigen', 'schnitt', 'eilei', 'grundsätzlich', 'zwillingsschwanger', 'ter', 'sterilität', 'bauchfellentzündung', 'schaft', 'spezialisierten', 'klinik', 'fak', 'sepsis', 'toren', 'dauer', 'kinder', 'anzahl', 'plazenten', 'berücksichtigt', 'fektion', 'saugglockenzangenentbindung', 'gebärmutterwand', 'steht', 'gebärmutterhals', 'verletzt', 'kommt', 'tritt', 'durchriss', 'ruptur', 'sofortige', 'openabelschnur', 'rative', 'gesauerstoffmangel', 'ihrem', 'fühbärmutter', 'saugglockenentbindung', 'dieses', 'verletzung', 'seltener', 'va', 'geburtsgewicht', 'uberverletzungen', 'blase', 'könnnen', 'gewicht', 'diabetes', 'stuhlhalteschwäche', 'inkontinenz', 'burt', 'fistelbildung', 'evtl', 'hängen', 'richtige', 'dreht', 'vergeht', 'saugglockenzangenentbindung', 'druckstellen', 'abschürfungen', 'ua', 'ge', 'schehen', 'mehrmaliger', 'schwellungen', 'am', 'besondere', 'beanschließender', 'handlung', 'selbst', 'abheilen', 'hüfte', 'hiermit', 'schul', 'erhöhte', 'blutungsneigung', 'gehirn', 'deshalb', 'ter', 'evtl', 'vitamin', 'k', 'blutgerinnung', 'lagerungs', 'fördern', 'wechsel', 'tiefes', 'schwere', 'schädelhand', 'bruch', 'himblutung', 'gesichtslähmung', 'lösen', 'haufig', 'sorg', 'al', 'falt', 'absoluter', 'sicherheit', 'ausschließen', 'ler', 'schlüsselbeins', 'schiedlich', 'dammnaht', 'vollnarkose', 'lichen', 'örtlicher', 'betäubung', 'ersten', 'kleine', 'wundhei', 'lungsstörungen', 'weder', 'gewendet', 'ausschließen', 'haufig', 'manualhilfe', 'äußerlich', 'intaktem', 'aufgrund', 'abgewartet', 'dehnung', 'bindegewebes', 'wundinfektionen', 'operati', 've', 'symptomatische', 'fasst', 'ge', 'tibiotikagabe', 'eröffnung', 'naht', 'lokale', 'kühlung', 'sitzbäder', 'kommt', 'sepsis', 'intensiv', 'metho', 'medizinisch', 'wund', 'kin', 'wunde', 'gedreht', 'bereich', 'nie', 'steril', 'kommt', 'sichtig', 'eingegangen', 'manchen', 'fallen', 'einigen', 'fa', 'veit', 'teilweisem', 'komplettem', 'klaffen', 'wunde', 'smelliehandgriff', 'nahtversorgung', 'wundreini', 'gung', 'man', 'situati', 'on', 'selbstständiges', 'zuheilen', 'wunde', 'abwarten', 'unterarm', 'arztin', 'wochen', 'dauern', 'narbenwucherungen', 'keloide', 'ver', 'anlagung', 'wundheilungsstörungen', 'sauerstoffmangelsituation', 'dauerhafte', 'hautverfarbungen', 'bewegungseinschränkungen', 'erniedrigte', 'sauerstoffwerte', 'nabelschnurblut', 'späterer', 'korrektureingriff', 'fallen', 'nabelschnurvorfall', 'schadigungen', 'armnerven', 'seiten', 'funktionseinschränkungen', 'insgespezielle', 'samt', 'vergleich', 'kopfladieser', 'aufkdärungsbogen', 'wichtigsten', 'ri', 'ge', 'normal', 'verlausiken', 'kaiserschnitts', 'informieren', 'kaiser', 'fenden', 'kein', 'weschnitt', 'geplant', 'gesonderten', 'bogen', 'benachbarte', 'organe', 'verletzt', 'harnblase', 'leiter', 'sofortige', 'jeweiligen', 'behandeln', 'schmerzhafte', 'missempfindungen', 'bauchfellentzündung', 'darmverschluss', 'fistelbildung', 'urinvergiftung', 'voroperationen', 'verwachsungen', 'schwierigen', 'anatomischen', 'verhältnissen', 'beherrschbare', 'übertragen', 'blutungsquelle', 'versorgt', 'eierstocke', 'genaht', 'warden', 'haut', 'gewebe', 'nervenschäden', 'lagerung', 'eingriffsbegleitende', 'einspritzungen', 'desinfektionen', 'laser', 'elektrischer', 'strom', 'dauerhafte', 'absterben', 'gewebe', 'narben', 'empfindungs', 'funktionsstörungen', 'lähmungen', 'gliedmaßen', 'bauchfellentzündung', 'lungenentzündung', 'bauchfellentzündung', 'eierstöcken', 'wundheilungsstörungen', 'überschießender', 'narbenbildung', 'narbenbruch', 'darmverschluss', 'infolge', 'darmlähmung', 'verwachsungen', 'bauchraum', 'jahren', 'bauchhöhle', 'erneut', 'eröffnet', 'einzelfällen', 'künstlicher', 'darmausgang', 'angelegt', 'warden', 'zerreißen', 'narbe', 'nächsten', 'einzelfällen', 'notkaiserschnitt', 'macht', 'plazentationsstörungen', 'häufiger', 'missempfindungen', 'bereich', 'schnitts', 'ersten', 'kein', 'grund', 'besorgnis', 'monate', 'bestehen', 'bleiben', 'langsam', 'bessern', 'schnittverletzung', 'gebärmuttereröffnung', 'meisten', 'selbst', 'abheilt', 'verletzung', 'kleinen', 'naht', 'versorgt', 'kommt', 'anpassungsstörungen', 'gestörte', 'atmung', 'sauerstoff', 'künstlich', 'beatmen', 'erkrankungen', 'asthma', 'diabetes', 'allergien', 'entzündliche', 'darmerkrankungen', 'scheinen', 'kindern', 'häufiger', 'vorzukommen', 'fragen', 'aufklärungsgespräch', 'wichtig', 'unklar']
