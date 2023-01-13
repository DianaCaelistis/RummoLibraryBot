from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
import logging
import ujson
import random

from modules.keyboards import menu_kb, remove_book_kb, back_from_book_kb
from modules.kbhandler import kbhandler
from modules.my_filters import UserEditing, UserSearching, UserAddingContactInfo


def main():
    updater = Updater(token="INSERT_TOKEN_HERE", use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    def start(update, context):
        bot = context.bot
        if context.args:
            args = context.args
            args = args[0].split("_")
        else:
            args = [0]
        if args[0] == "lookup":
            database = ujson.load(open("db.json", "r"))
            book = database["books"][args[1]]
            category_text = ""
            for category in book["Categorie"]:
                category_text += category + " "
            text = "Ciao! Eccoti le informazioni sul libro che hai selezionato:\n" \
                   "<i>Puoi rimuovere il libro dal database con il pulsante in basso.\n" \
                   "⚠️ Attenzione! Il bot non chiede conferme!</i>\n\n" \
                   "Nome: {nome}\n" \
                   "ISBN: {isbn}\n" \
                   "Prezzo: {prezzo}\n" \
                   "Trattabilità: {trattabilità}\n" \
                   "Anno: {anno}\n" \
                   "Categorie: {categorie}".format(
                    nome=book["Nome"], isbn=book["ISBN"], prezzo=book["Prezzo"], trattabilità=book["Trattabilità"],
                    anno=book["Anno"], categorie=category_text
                    )
            bot.sendMessage(text=text, chat_id=update.effective_chat.id, reply_markup=remove_book_kb(args[1]),
                            parse_mode="HTML")
            return 1
        if args[0] == "slookup":
            database = ujson.load(open("db.json", "r"))
            contact_info = "C'è stato un errore nel recuperare i dati di contatto del proprietario di questo libro " \
                           "perfavore contatta l'amministratrice del bot su @DianaCaelistis"
            for user in database["users"]:
                for book in database["users"][user]["books"]:
                    if book == args[1]:
                        contact_info = database["users"][user]["contact_info"]
                        break
            book = database["books"][args[1]]
            category_text = ""
            for category in book["Categorie"]:
                category_text += category + " "
            text = "Ciao! Eccoti le informazioni sul libro che hai selezionato:\n" \
                   "Nome: {nome}\n" \
                   "ISBN: {isbn}\n" \
                   "Prezzo: {prezzo}€\n" \
                   "Trattabilità: {trattabilità} (1 = Prezzo trattabile)\n" \
                   "Anno: {anno}\n" \
                   "Categorie: {categorie}\n\n" \
                   "Puoi contattare il venditore in questo modo:\n{contact_info}".format(
                    nome=book["Nome"], isbn=book["ISBN"], prezzo=book["Prezzo"], trattabilità=book["Trattabilità"],
                    anno=book["Anno"], categorie=category_text, contact_info=contact_info
                    )
            bot.sendMessage(text=text, chat_id=update.effective_chat.id, reply_markup=back_from_book_kb(),
                            parse_mode="HTML")
            return 1
        bot.sendMessage(text="👋 Ciao! Benvenuto nel bot del mercatino del Rummo!\n"
                             "Qui potrai navigare facilmente la lista di tutti i libri usati messi in "
                             "vendita da studenti o ex studenti (per i libri del triennio) del Rummo!\n\n"
                             "Usa /menu per cominciare",
                        chat_id=update.effective_chat.id)

    def menu(update, context):
        bot = context.bot
        bot.sendMessage(text="Usa i bottoni di sotto per navigare nel menù ⬇️",
                        chat_id=update.effective_chat.id,
                        reply_markup=menu_kb())

    def adding_books(update, context):
        bot = context.bot
        text = update.effective_message.text
        split_1 = text.split("\n")
        database = ujson.load(open("db.json", "r"))
        books = []
        for book_info in split_1:
            info = book_info.split("-")
            if len(info) != 6:
                bot.sendMessage(text="Ops! Hai sbagliato qualcosa nella formattazione del messaggio.\n"
                                     "Rileggi le istruzioni e riprova :D. Non serve ripremere su Aggiungi Libri.",
                                chat_id=update.effective_message.id)
                return 0
            categories_info = info[5].split(",")
            categories_list = []
            for category in categories_info:
                category = category.strip()
                categories_list.append(category)
            book = {
                "Nome": info[0],
                "ISBN": info[1],
                "Prezzo": info[2],
                "Trattabilità": info[3],
                "Anno": info[4],
                "Categorie": categories_list
            }
            books.append(book)
        for book in books:
            ID = random.randint(0, 9999)
            database["books"][str(ID)] = book
            database["users"][str(update.effective_chat.id)]["books"].append(str(ID))
        database["users"][str(update.effective_chat.id)]["status"] = False
        ujson.dump(database, open("db.json", "w"))
        text = "Congratulazioni! Hai aggiunto i seguenti libri:\n"
        x = 1
        for book in books:
            category_text = ""
            for category in book["Categorie"]:
                category_text += category + " "
            bookinfo = "\n<b>Libro {n}</b>\n" \
                       "Nome: {nome}\n" \
                       "ISBN: {isbn}\n" \
                       "Prezzo: {prezzo}€\n" \
                       "Trattabile?: {trattabilità}\n" \
                       "Anno: {anno}\n" \
                       "Categorie: {categorie}\n".format(
                        n=str(x), nome=book["Nome"], isbn=book["ISBN"], prezzo=book["Prezzo"],
                        trattabilità=book["Trattabilità"], anno=book["Anno"], categorie=category_text
                        )
            text += bookinfo
            x += 1

        bot.sendMessage(text=text, chat_id=update.effective_chat.id, parse_mode="HTML")

    def searching_books(update, context):
        bot = context.bot
        text = update.effective_message.text
        database = ujson.load(open("db.json", "r"))
        if database["users"][str(update.effective_chat.id)]["status"] == "search_by_name":
            text2 = "Eccoti un elenco dei libri che rispondono alla tua ricerca:\n\n"
            for book in database["books"]:
                if text.lower() in database["books"][book]["Nome"].lower():
                    text2 += "<a href=\"https://t.me/mercatinorummo_bot?start=slookup_{book_id}\">{Name}</a>\n".format(
                        book_id=book, Name=database["books"][book]["Nome"]
                        )
            bot.sendMessage(text=text2, chat_id=update.effective_chat.id, parse_mode="HTML")
            database["users"][str(update.effective_chat.id)]["status"] = False
            ujson.dump(database, open("db.json", "w"))
            return 1
        if database["users"][str(update.effective_chat.id)]["status"] == "search_by_isbn":
            text2 = "Eccoti un elenco dei libri che rispondono alla tua ricerca:\n\n"
            for book in database["books"]:
                if text in database["books"][book]["ISBN"]:
                    text2 += "<a href=\"https://t.me/mercatinorummo_bot?start=slookup_{book_id}\">{Name}</a>\n".format(
                        book_id=book, Name=database["books"][book]["Nome"]
                        )
            bot.sendMessage(text=text2, chat_id=update.effective_chat.id, parse_mode="HTML")
            database["users"][str(update.effective_chat.id)]["status"] = False
            ujson.dump(database, open("db.json", "w"))
            return 1
        if database["users"][str(update.effective_chat.id)]["status"] == "search_by_category":
            text2 = "Eccoti un elenco dei libri che rispondono alla tua ricerca:\n\n"
            for book in database["books"]:
                for category in database["books"][book]["Categorie"]:
                    if text.lower() in category.lower():
                        text2 += "<a href=\"https://t.me/mercatinorummo_bot?start=slookup_{book_id}\">{Name}</a>\n".format(
                            book_id=book, Name=database["books"][book]["Nome"]
                            )
            bot.sendMessage(text=text2, chat_id=update.effective_chat.id, parse_mode="HTML")
            database["users"][str(update.effective_chat.id)]["status"] = False
            ujson.dump(database, open("db.json", "w"))
            return 1

    def adding_contact_info(update, context):
        bot = context.bot
        text = update.effective_message.text
        database = ujson.load(open("db.json", "r"))
        database["users"][str(update.effective_chat.id)]["contact_info"] = text
        database["users"][str(update.effective_chat.id)]["status"] = False
        bot.sendMessage(text="Ciao! Le tue informazioni di contatto sono state aggiornate con successo, "
                             "puoi visionarle qui sotto:\n\n{}".format(text),
                        chat_id=update.effective_chat.id)
        ujson.dump(database, open("db.json", "w"))

    userediting = UserEditing()
    usersearching = UserSearching()
    useraddinginfo = UserAddingContactInfo()

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("menu", menu, filters=Filters.chat_type.private))
    dispatcher.add_handler(MessageHandler(callback=adding_books, filters=Filters.chat_type.private & userediting))
    dispatcher.add_handler(MessageHandler(callback=searching_books, filters=Filters.chat_type.private & usersearching))
    dispatcher.add_handler(MessageHandler(callback=adding_contact_info, filters=Filters.chat_type.private & useraddinginfo))
    dispatcher.add_handler(CallbackQueryHandler(kbhandler))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
