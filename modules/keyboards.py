from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import ujson


def menu_kb():
    kb0 = InlineKeyboardButton("➕ Aggiungi libri", callback_data="add_books")
    kb1 = InlineKeyboardButton("📚 I miei libri", callback_data="my_books")
    kb2 = InlineKeyboardButton("🔎 Cerca libri", callback_data="search_books")
    kb3 = InlineKeyboardButton("👥 Le mie informazioni", callback_data="edit_contact_info")
    kb4 = InlineKeyboardButton("ℹ️ Informazioni sul bot", callback_data="info")
    return InlineKeyboardMarkup([[kb0, kb1], [kb2], [kb3], [kb4]])


def back_from_add():
    kb0 = InlineKeyboardButton("🔙 Torna Indietro", callback_data="back_from_add")
    return InlineKeyboardMarkup([[kb0]])


def remove_book_kb(book_id):
    kb0 = InlineKeyboardButton("➖ Rimuovi Libro", callback_data="remove_book_{}".format(book_id))
    kb1 = InlineKeyboardButton("🔙 Torna Indietro", callback_data="back_from_book")
    return InlineKeyboardMarkup([[kb0], [kb1]])


def back_from_book_kb():
    kb0 = InlineKeyboardButton("🔙 Torna Indietro", callback_data="back_from_book")
    return InlineKeyboardMarkup([[kb0]])


def search_kb():
    kb0 = InlineKeyboardButton("🔎 Nome", callback_data="search_nome")
    kb1 = InlineKeyboardButton("🔎 ISBN", callback_data="search_isbn")
    kb2 = InlineKeyboardButton("🔎 Anno", callback_data="search_anno")
    kb3 = InlineKeyboardButton("🔎 Categorie", callback_data="search_categorie")
    kb4 = InlineKeyboardButton("🌐 Naviga Database", callback_data="explore_database")
    kb5 = InlineKeyboardButton("🔙 Torna Indietro", callback_data="back_from_search")
    return InlineKeyboardMarkup([[kb0, kb1], [kb2, kb3], [kb4], [kb5]])


def search_year_kb():
    kb0 = InlineKeyboardButton("1", callback_data="search_year_1")
    kb1 = InlineKeyboardButton("2", callback_data="search_year_2")
    kb2 = InlineKeyboardButton("3", callback_data="search_year_3")
    kb3 = InlineKeyboardButton("4", callback_data="search_year_4")
    kb4 = InlineKeyboardButton("5", callback_data="search_year_5")
    kb5 = InlineKeyboardButton("Biennio", callback_data="search_year_biennio")
    kb6 = InlineKeyboardButton("Triennio", callback_data="search_year_triennio")
    kb7 = InlineKeyboardButton("🔙 Torna Indietro", callback_data="back_from_search")
    return InlineKeyboardMarkup([[kb0, kb1, kb2, kb3, kb4], [kb5], [kb6], [kb7]])
