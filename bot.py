import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7614211780:AAFuJT-AYCDSqJ_hczN-mRmwV8kJuRVKTMU"
bot = telebot.TeleBot(TOKEN)

# Base de données simple
users = {}  # Stocke les utilisateurs et leurs étoiles
invites = {}  # Stocke le nombre d'invitations
withdraw_requests = []  # Liste des demandes de retrait
admin_id = 5116530698  # Remplace par ton ID Telegram

# Cadeaux disponibles
gifts = [
    {"nom": "💎 100 étoiles", "prix": 100},
    {"nom": "🎁 200 étoiles", "prix": 200},
    {"nom": "🎮 Carte PSN", "prix": 500},
]

# Fonction pour récupérer le nombre total d’utilisateurs
def total_users():
    return len(users)


# Commande /start avec menu interactif
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = 0
        invites[user_id] = 0

    markup = InlineKeyboardMarkup()
    btn_balance = InlineKeyboardButton("💰 Mon solde", callback_data="balance")
    btn_invite = InlineKeyboardButton("📢 Inviter des amis", callback_data="invite")
    btn_shop = InlineKeyboardButton("🎁 Boutique", callback_data="shop")
    btn_withdraw = InlineKeyboardButton("💸 Demander un retrait", callback_data="withdraw")
    markup.add(btn_balance, btn_invite)
    markup.add(btn_shop, btn_withdraw)

    bot.send_message(user_id, f"⭐ Bienvenue ! Il y a {total_users()} utilisateurs actifs.\n"
                              "Invitez des amis pour gagner des étoiles !", reply_markup=markup)


# Voir son solde
@bot.callback_query_handler(func=lambda call: call.data == "balance")
def balance(call):
    user_id = call.message.chat.id
    bot.send_message(user_id, f"⭐ Vous avez {users[user_id]} étoiles.")


# Inviter des amis
@bot.callback_query_handler(func=lambda call: call.data == "invite")
def invite(call):
    user_id = call.message.chat.id
    bot.send_message(user_id, "📢 Partage ce lien avec tes amis :\n"
                              f"https://t.me/TON_BOT_USERNAME?start={user_id}\n"
                              "Une fois qu'ils rejoignent, tes étoiles seront mises à jour automatiquement.")


# Afficher la boutique
@bot.callback_query_handler(func=lambda call: call.data == "shop")
def shop(call):
    user_id = call.message.chat.id
    markup = InlineKeyboardMarkup()

    for i, gift in enumerate(gifts):
        btn = InlineKeyboardButton(f"{gift['nom']} - {gift['prix']} ⭐", callback_data=f"buy_{i}")
        markup.add(btn)

    bot.send_message(user_id, "🎁 Sélectionnez un cadeau :", reply_markup=markup)


# Acheter un cadeau
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy(call):
    user_id = call.message.chat.id
    index = int(call.data.split("_")[1])
    gift = gifts[index]

    if users[user_id] >= gift["prix"]:
        users[user_id] -= gift["prix"]
        bot.send_message(user_id, f"✅ Vous avez acheté {gift['nom']} !")
    else:
        bot.send_message(user_id, "❌ Vous n'avez pas assez d'étoiles.")


# Demander un retrait
@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def withdraw(call):
    user_id = call.message.chat.id
    withdraw_requests.append({"user_id": user_id, "status": "en cours"})
    bot.send_message(user_id, "✅ Votre demande de retrait a été envoyée à l'admin.")
    bot.send_message(admin_id, f"⚠️ Nouvelle demande de retrait de l'utilisateur {user_id}")


# Commande admin pour gérer les retraits
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != admin_id:
        return

    markup = InlineKeyboardMarkup()
    btn_broadcast = InlineKeyboardButton("📢 Diffuser un message", callback_data="broadcast")
    btn_withdraws = InlineKeyboardButton("💸 Gérer les retraits", callback_data="manage_withdraws")
    markup.add(btn_broadcast, btn_withdraws)

    bot.send_message(admin_id, "⚙️ Panneau Admin", reply_markup=markup)


# Diffuser un message
@bot.callback_query_handler(func=lambda call: call.data == "broadcast")
def broadcast(call):
    if call.message.chat.id != admin_id:
        return

    msg = bot.send_message(admin_id, "📢 Envoie le message à diffuser :")
    bot.register_next_step_handler(msg, send_broadcast)


def send_broadcast(message):
    for user in users:
        bot.send_message(user, f"📢 Annonce : {message.text}")
    bot.send_message(admin_id, "✅ Message diffusé avec succès !")


# Gérer les retraits
@bot.callback_query_handler(func=lambda call: call.data == "manage_withdraws")
def manage_withdraws(call):
    if call.message.chat.id != admin_id:
        return

    if not withdraw_requests:
        bot.send_message(admin_id, "Aucune demande de retrait en attente.")
        return

    markup = InlineKeyboardMarkup()
    for i, req in enumerate(withdraw_requests):
        btn = InlineKeyboardButton(f"Utilisateur {req['user_id']} - {req['status']}",
                                   callback_data=f"withdraw_{i}")
        markup.add(btn)

    bot.send_message(admin_id, "💸 Retraits en attente :", reply_markup=markup)


# Confirmer un retrait
@bot.callback_query_handler(func=lambda call: call.data.startswith("withdraw_"))
def confirm_withdraw(call):
    if call.message.chat.id != admin_id:
        return

    index = int(call.data.split("_")[1])
    user_id = withdraw_requests[index]["user_id"]

    withdraw_requests[index]["status"] = "effectué"
    bot.send_message(user_id, "✅ Votre retrait a été confirmé par l'admin.")
    bot.send_message(admin_id, f"✅ Retrait confirmé pour {user_id}.")

bot.polling()