import ujson

from modules.keyboards import back_from_add, menu_kb, search_kb, search_year_kb, back_from_book_kb


def kbhandler(update, context):
    bot = context.bot
    data = update.callback_query.data
    split = data.split("_")
    if split[0] == "add":
        database = ujson.load(open("db.json", "r"))
        add_contact_info = False
        try:
            if not database["users"][str(update.effective_chat.id)]["contact_info"]:
                add_contact_info = True
            database["users"][str(update.effective_chat.id)]["status"] = "adding_books"
        except KeyError:
            database["users"][str(update.effective_chat.id)] = {
                "status": "adding_books",
                "books": [],
                "contact_info": ""
            }
            add_contact_info = True
        ujson.dump(database, open("db.json", "w"))
        if add_contact_info:
            database["users"][str(update.effective_chat.id)]["status"] = "adding_contact_info"
            ujson.dump(database, open("db.json", "w"))
            bot.editMessageText(chat_id=update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Ciao! Sembra essere la prima volta che aggiungi libri!\n"
                                     "Prima di procedere è importante che tu mi dia le tue informazioni di contatto, "
                                     "gli acquirenti devono sapere come contattarti in caso siano interessati al "
                                     "tuo libro. Sappi che puoi usare qualunque mezzo: numero di telefono, username "
                                     "telegram, instagram, email.\nAttenzione! Usando il bot il tuo ID telegram verrà "
                                     "salvato nel database del bot.\n"
                                     "<a href=\"https://telegra.ph/FAQ-01-12-9\">"
                                     "Clicca qui per maggiori informazioni!</a>\n"
                                     "Ho fatto le dovute premesse. Ora perfavore inviami un messaggio "
                                     "con le tue informazioni di contatto.",
                                parse_mode="HTML",
                                disable_web_page_preview=True,
                                reply_markup=back_from_add()
                                )
            return 1
        bot.editMessageText(chat_id=update.effective_chat.id,
                            message_id=update.callback_query.message.message_id,
                            text="Ciao! Aggiungendo dei libri al bot il tuo ID telegram "
                                 "verrà salvato nel database del bot. Se ti va bene, prosegui con la procedura.\n"
                                 "<a href=\"https://telegra.ph/FAQ-01-12-9\">Clicca qui per maggiori informazioni</a>\n"
                                 "\nPer aggiungere dei libri inviami un messaggio in questo formato:\n"
                                 "<code>Nomelibro - CODICE ISBN - Prezzo di vendita - [1/0] per indicare se il prezzo è "
                                 "trattabile o no - [1/2/3/4/5/Biennio/Triennio] - #Categorie, #separate, #da_virgola </code>\n\n"
                                 "Se non hai capito eccoti un esempio! Io voglio mettere in vendita il libro "
                                 "Matematica.blu 2.0 per il quinto anno, ci vorrei fare intorno ai 20 euro ma "
                                 "non ho problemi a trattare il prezzo. L'edizione del libro è la 2017, "
                                 "ne approfitterò anche per aggiungere questa informazione.\n"
                                 "Quello che dovrò scrivere per inserire questo libro è:\n"
                                 "Matematica.Blu 2.0 - 9788808865007 - 20 - 1 - 5 - #Matematica, #Edizione2017\n\n"
                                 "Fatto! Volendo, puoi inserire più libri in più righe del messaggio. "
                                 "NON usare il trattino alto [-] all'interno del nome del libro o "
                                 "delle categorie o il bot ti ritornerà un errore!\n"
                                 "Se hai cliccato per sbaglio, usa pure il pulsante qui sotto ⬇️",
                            parse_mode="HTML",
                            disable_web_page_preview=True,
                            reply_markup=back_from_add())
    elif split[0] == "my":
        if split[1] == "books":
            uid = update.effective_chat.id
            database = ujson.load(open("db.json", "r"))
            my_books = []
            for book in database["users"][str(uid)]["books"]:
                my_books.append([database["books"][book], book])
            text = "Di seguito l'elenco dei tuoi libri:\n<i>Puoi cliccare sul nome per vederne i dettagli</i>\n\n"
            for book in my_books:
                text += "<a href=\"https://t.me/mercatinorummo_bot?start=lookup_{book_id}\">{Name}</a>\n".format(
                    book_id=book[1], Name=book[0]["Nome"]
                )
            bot.sendMessage(text=text, chat_id=uid, parse_mode="HTML")
    elif split[0] == "search":
        if split[1] == "nome":
            database = ujson.load(open("db.json", "r"))
            database["users"][str(update.effective_chat.id)]["status"] = "search_by_name"
            ujson.dump(database, open("db.json", "w"))
            bot.editMessageText(chat_id=update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Scrivi il nome del libro che vuoi cercare! \n"
                                     "Sarebbe preferibile inserire solo una parola chiave",
                                reply_markup=search_kb())
            return 1
        elif split[1] == "isbn":
            database = ujson.load(open("db.json", "r"))
            database["users"][str(update.effective_chat.id)]["status"] = "search_by_isbn"
            ujson.dump(database, open("db.json", "w"))
            bot.editMessageText(chat_id=update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Scrivi l'ISBN che vuoi cercare! \n"
                                     "Attenzione! L'ISBN deve essere preciso e senza i trattini",
                                reply_markup=search_kb())
            return 1
        elif split[1] == "anno":
            bot.editMessageText(chat_id=update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Seleziona l'anno di cui vuoi cercare i libri con i bottoni di sotto",
                                reply_markup=search_year_kb())
            return 1
        elif split[1] == "categorie":
            database = ujson.load(open("db.json", "r"))
            database["users"][str(update.effective_chat.id)]["status"] = "search_by_category"
            ujson.dump(database, open("db.json", "w"))
            bot.editMessageText(chat_id=update.effective_chat.id,
                                message_id=update.callback_query.message.message_id,
                                text="Scrivi la categoria del libro che vuoi cercare! \n"
                                     "Puoi cercare una categoria per volta",
                                reply_markup=search_kb())
            return 1
        elif split[1] == "year":
            if split[2] == "1":
                kword = "1"
            elif split[2] == "2":
                kword = "2"
            elif split[2] == "3":
                kword = "3"
            elif split[2] == "4":
                kword = "4"
            elif split[2] == "5":
                kword = "5"
            elif split[2] == "biennio":
                kword = "biennio"
            elif split[2] == "triennio":
                kword = "triennio"
            database = ujson.load(open("db.json", "r"))
            text2 = "Eccoti un elenco dei libri che rispondono alla tua ricerca:\n\n"
            for book in database["books"]:
                if kword in database["books"][book]["Anno"].lower():
                    text2 += "<a href=\"https://t.me/testphasebot?start=slookup_{book_id}\">{Name}</a>\n".format(
                        book_id=book, Name=database["books"][book]["Nome"]
                    )
            bot.sendMessage(text=text2, chat_id=update.effective_chat.id, parse_mode="HTML")
            database["users"][str(update.effective_chat.id)]["status"] = False
            ujson.dump(database, open("db.json", "w"))
            return 1
        bot.editMessageText(chat_id=update.effective_chat.id,
                            message_id=update.callback_query.message.message_id,
                            text="Seleziona di sotto il metodo di ricerca preferito!\n"
                                 "<i>Sarebbe consigliabile la ricerca tramite ISBN per avere risultati migliori</i>\n\n",
                            parse_mode="HTML",
                            reply_markup=search_kb())
    elif split[0] == "back":
        if split[2] == "add":
            database = ujson.load(open("db.json", "r"))
            database["users"][str(update.effective_chat.id)]["status"] = False
            ujson.dump(database, open("db.json", "w"))
        if split[2] == "search":
            database = ujson.load(open("db.json", "r"))
            try:
                database["users"][str(update.effective_chat.id)]["status"] = False
                ujson.dump(database, open("db.json", "w"))
            except KeyError:
                pass
        bot.editMessageText(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id,
                            text="Usa i bottoni di sotto per navigare nel menù ⬇️",
                            reply_markup=menu_kb())
    elif split[0] == "remove":
        if split[1] == "book":
            database = ujson.load(open("db.json", "r"))
            book = database["books"].pop(split[2])
            database["users"][str(update.effective_chat.id)]["books"].remove(split[2])
            ujson.dump(database, open("db.json", "w"))
            bot.sendMessage(text="Il libro {nome} è stato rimosso con successo dal database!".format(
                nome=book["Nome"]),
                chat_id=update.effective_chat.id
            )
    elif split[0] == "explore":
        database = ujson.load(open("db.json", "r"))
        text2 = "Eccoti i libri nel database:\n\n"
        for book in database["books"]:
            text2 += "<a href=\"https://t.me/testphasebot?start=slookup_{book_id}\">{Name}</a>\n".format(
                book_id=book, Name=database["books"][book]["Nome"]
            )
        bot.sendMessage(text=text2, chat_id=update.effective_chat.id, parse_mode="HTML")
    elif split[0] == "edit":
        database = ujson.load(open("db.json", "r"))
        try:
            database["users"][str(update.effective_chat.id)]["status"] = "adding_contact_info"
        except KeyError:
            database["users"][str(update.effective_chat.id)] = {
                "status": "adding_contact_info",
                "books": [],
                "contact_info": ""
            }
        ujson.dump(database, open("db.json", "w"))
        bot.editMessageText(chat_id=update.effective_chat.id,
                            message_id=update.callback_query.message.message_id,
                            text="Ciao! Forniscimi ora le tue nuove informazioni di contattto\n"
                                 "<i>Attenzione! Usando il bot il tuo ID telegram verrà "
                                 "salvato nel database del bot: <a href=\"https://telegra.ph/FAQ-01-12-9\">"
                                 "Clicca qui per maggiori informazioni!</a></i>",
                            parse_mode="HTML",
                            disable_web_page_preview=True,
                            reply_markup=back_from_add()
                            )
        return 1
    elif split[0] == "info":
        bot.editMessageText(chat_id=update.effective_chat.id,
                            message_id=update.callback_query.message.message_id,
                            text="Ciao! Se vuoi saperne di più sul bot leggi il mio discorso agli utenti:\n"
                                 "<a href=\"https://telegra.ph/FAQ-01-12-9#Un-discorso-agli-utenti\">"
                                 "Clicca qui per aprire la pagina web!</a>",
                            parse_mode="HTML",
                            disable_web_page_preview=True,
                            reply_markup=back_from_book_kb()
                            )
