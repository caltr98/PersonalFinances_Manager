import sqlite3
from Entry import entry
import pandas

datasheet = sqlite3.connect("spese.db")
cur = datasheet.cursor()

print("DIGITARE IL NUMERO DELL'OPERAZIONE DA ESEGUIRE")
end = 'S'

# MAIN LOOP
while end == 'S' or end == 's':
    print('1.Nuovo inserimento\n2.Elenco completo movimenti\n3.Ricerca movimenti\n4.Modifica record\n5.Totali per '
          'voce/mese\n6.Elimina record\n')
    func = input()

    # INSERT NEW ENTRY
    if func == '1':
        print('Iserimento nuova voce')
        desc = input('Inserire la descrizione: ')
        amt = input('Inserire importo: ')
        prd = input('Inserire periodo riferimento (facoltativo) se non presente (*): ')
        new = entry(desc, amt, prd)
        new.display()
        cur.execute("INSERT INTO spese(ID,DDMMYY,DESCRIZIONE,IMPORTO,PERIODO) VALUES(?,?,?,?,?);",
                    (new.id, new.date, new.descript, new.amount, new.period))
        datasheet.commit()
        print("\nEseguire una nuova operazione? S/N ")
        end = input()

    # LIST ALL DATA
    elif func == "2":
        print("ELENCO COMPLETO DEI MOVIMENTI\n")
        query = "SELECT * FROM spese"
        df = pandas.read_sql_query(query, datasheet)
        print(df)
        # EXPORT QUERY TO TXT
        print("\nEsportare risultati in file di testo? S/N ")
        exp = input()
        if exp == "S" or exp == "s":
            report = open("report", "w")
            report.write("ELENCO COMPLETO MOVIMENTI\n\n")
            report.write(df.to_string())
            report.close()
        print("IMPORTANTE: Rimuovere dalla directory del programma il file creato prima di fare nuove esportazioni.\n")
        print("\nEseguire una nuova operazione? S/N ")
        end = input()

    # LIST DATA WITH FILTERS
    elif func == "3":
        print("INTERROGAZIONE PARAMETRICA DEI MOVIMENTI\n")
        print("Effettuare ricerca per mese (1) o per tipologia (2)?\n")
        src_mode = input()

        # SEARCH BY MONTH
        if src_mode == "1":
            print("Indicare mese di ricerca (es. 02 - 04...)")
            query = ("SELECT * FROM spese WHERE strftime('%m',DDMMYY) LIKE '%{}%'".format(input()))
            df = pandas.read_sql_query(query, datasheet)
            print(df)
            # GENERATE TXT FROM QUERY
            print("\nEsportare risultati in file di testo? S/N ")
            exp = input()
            if exp == "S" or exp == "s":
                report = open("report", "w")
                report.write("INTERROGAZIONE MOVIMENTI PER MESE\n\n")
                report.write(df.to_string())
                report.close()
                print(
                    "IMPORTANTE: Rimuovere dalla directory del programma il file creato prima di fare nuove "
                    "esportazioni.\n")
                print("\nEseguire una nuova operazione? S/N ")
                end = input()

        # SEARCH BY DESCRITPION
        elif src_mode == "2":
            print("Indicare la descrizione esattamente come è stata inserita: ")
            query = ("SELECT * FROM spese WHERE DESCRIZIONE LIKE '%{}%'".format(input()))
            df = pandas.read_sql_query(query, datasheet)
            print(df)
            # GENERATE TXT FROM QUERY
            print("\nEsportare risultati in file di testo? S/N ")
            exp = input()
            if exp == "S" or exp == "s":
                report = open("report", "w")
                report.write("INTERROGAZIONE MOVIMENTI PER TIPOLOGIA\n\n")
                report.write(df.to_string())
                report.close()
                print(
                    "IMPORTANTE: Rimuovere dalla directory del programma il file creato prima di fare nuove "
                    "esportazioni.\n")
                print("\nEseguire una nuova operazione? S/N ")
                end = input()

    # UPDATE RECORDS
    elif func == "4":
        print("MODIFICA DI UN RECORD\n")
        print("Effettuare ricerca per mese (1) o per tipologia (2)?\n")
        src_mode = input()
        # SEARCH BY MONTH
        if src_mode == "1":
            print("Indicare mese di ricerca (es. 02 - 04...)")
            query = ("SELECT * FROM spese WHERE strftime('%m',DDMMYY) LIKE '%{}%'".format(input()))
            df = pandas.read_sql_query(query, datasheet)
            print(df)
        # SEARCH BY DESCRITPION
        elif src_mode == "2":
            print("Indicare la descrizione esattamente come è stata inserita: ")
            query = ("SELECT * FROM spese WHERE DESCRIZIONE LIKE '%{}%'".format(input()))
            df = pandas.read_sql_query(query, datasheet)
            print(df)

        # UPDATE PROCEDURE
        print("Inserire ID operazione da modificare: ")
        edit_id = input()
        print("Modifica Descrizione (1)\nModifica Importo (2)")
        edit_field = input()
        if edit_field == "1":
            descr = input("Inserire descrizione da sostituire: ")
            cur.execute("UPDATE spese SET DESCRIZIONE = ? WHERE ID = ?", (descr, edit_id,))
        elif edit_field == "2":
            new_amount = input("Inserire nuovo importo")
            cur.execute("UPDATE spese SET IMPORTO = ? WHERE ID = ?", (new_amount, edit_id,))
        else:
            print("Scelta non valida!")
        print("\nEseguire una nuova operazione? S/N ")
        end = input()

    # SUM BY MONTH/DESCRIPRION
    elif func == "5":
        print("INTERROGAZIONE TOTALI\n")
        print("\nSelezionare paramtro: Mese (1) - Tipologia (2): - Totale tipologia per mese (3)")
        src_mode = input()
        # SUM BY MONTH
        if src_mode == "1":
            print("Inserire il mese di cui si vuole calcolare il totale (Es. 02 - 04...): ")
            key = input()
            cur.execute("SELECT SUM(IMPORTO) AS total FROM spese WHERE strftime('%m',DDMMYY) = ?", (key,))
            tot = cur.fetchone()
            print("Totale spese per il mese", key, ": E. ", tot[0])
            print("\nEseguire una nuova operazione? S/N ")
            end = input()
        # SUM BY DESCRIPTION
        elif src_mode == "2":
            print("Inserire la tipologia di cui si vuole calcolare il totale: ")
            key = input()
            cur.execute("SELECT SUM(IMPORTO) AS total FROM spese WHERE DESCRIZIONE = ?", (key,))
            tot = cur.fetchone()
            print("Totale delle spese inerenti alla tipologia", key, ": E. ", tot[0])
            print("\nEseguire una nuova operazione? S/N ")
            end = input()
        # SUM BY DESCRIPTION AND MONTH
        elif src_mode == "3":
            key = input("Inserire la tipologia: ")
            key2 = input("Inserire mese per cui si vuole ottenere il totale: ")
            cur.execute("SELECT SUM(IMPORTO) AS total FROM spese WHERE DESCRIZIONE = ? AND strftime('%m',DDMMYY) = ?",
                        (key, key2,))
            tot = cur.fetchone()
            print("Totale delle spese inerenti alla tipologia", key, "nel mese", key2, ": E. ", tot[0])
            print("\nEseguire una nuova operazione? S/N ")
            end = input()
        else:
            print("Scelta non valida!")

    # DELETE RECORDS
    elif func == "6":
        # FILTER RECORDS BY MONTH
        print("Eliminazione record\n")
        print("Indicare mese di ricerca (es. 02 - 04...)")
        query = ("SELECT * FROM spese WHERE strftime('%m',DDMMYY) LIKE '%{}%'".format(input()))
        df = pandas.read_sql_query(query, datasheet)
        print(df)
        # REMOVE RECORD BY ID NUMBER
        id_del = input("Indicare l'ID del record da eliminare: ")
        cur.execute("DELETE FROM spese WHERE ID = ?", (id_del,))
        datasheet.commit()
        print("Operazione Eseguita!")
        print("\nEseguire una nuova operazione? S/N ")
        end = input()
    else:
        print("Scelta non valida!")
