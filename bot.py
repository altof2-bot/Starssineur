import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7614211780:AAFuJT-AYCDSqJ_hczN-mRmwV8kJuRVKTMU"
bot = telebot.TeleBot(TOKEN)



# Base de données simple
users = {}
invites = {}
withdraw_requests = []
admin_id = 5116530698

# Liste des cadeaux disponibles
gifts = [
    {"nom": "💎 100 étoiles", "prix": 100},
    {"nom": "🎁 200 étoiles", "prix": 200},
    {"nom": "🎮 Carte PSN", "prix": 500},
    {"nom": "🧸 Ours en peluche", "prix": 15},
    {"nom": "🎧 Casque audio", "prix": 25},
    {"nom": "💻 Ordinateur portable", "prix": 50},
    {"nom": "📱 Smartphone", "prix": 75},
    {"nom": "🎮 Console Switch", "prix": 120},
    {"nom": "🖥️ PC gamer", "prix": 200},
    {"nom": "🛒 Chèque cadeau Amazon", "prix": 250},
    {"nom": "🎵 Abonnement Spotify", "prix": 10},
    {"nom": "🍔 Bon de restaurant", "prix": 30},
    {"nom": "🎫 Billet de concert", "prix": 40},
    {"nom": "🎁 Carte cadeau iTunes", "prix": 60},
    {"nom": "🌟 Récompense surprise", "prix": 150},
]

# Fonction pour récupérer le nombre total d’utilisateurs
def total_users():
    return len(users)

# Commande /start avec vérification des abonnements
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # Si l'utilisateur a été invité par un lien
    if len(text) > 1 and text[1].isdigit():
        inviter_id = int(text[1])

        # Vérifier que l'inviteur existe et qu'il ne s'auto-invite pas
        if inviter_id in users and inviter_id != user_id:
            if user_id not in invites.get(inviter_id, []):
                invites.setdefault(inviter_id, []).append(user_id)
                users[inviter_id] += 1  # Ajouter 1 étoile pour chaque nouvel invité

                bot.send_message(inviter_id, f"🎉 Une nouvelle personne a rejoint grâce à vous ! Vous avez maintenant {users[inviter_id]} étoiles.")

    # Enregistrer le nouvel utilisateur s'il n'existe pas encore
    if user_id not in users:
        users[user_id] = 0
        invites[user_id] = []

    # Générer un lien d’invitation unique
    invite_link = f"https://t.me/NOM_DU_BOT?start={user_id}"



  

    markup = InlineKeyboardMarkup()
    btn_balance = InlineKeyboardButton("💰 Mon solde", callback_data="balance")
    btn_invite = InlineKeyboardButton("📢 Inviter des amis", callback_data="invite")
    btn_shop = InlineKeyboardButton("🎁 Boutique", callback_data="shop")
    btn_withdraw = InlineKeyboardButton("💸 Demander un retrait", callback_data="withdraw")
    btn_my_invites = InlineKeyboardButton("👥 Mes invitations", callback_data="my_invites")
    markup.add(btn_balance, btn_invite)
    markup.add(btn_shop, btn_withdraw, btn_my_invites)

    bot.send_message(user_id, "⭐ Bienvenue ! Choisissez une option pour commencer.", reply_markup=markup)



# Callback pour afficher le solde de l'utilisateur
@bot.callback_query_handler(func=lambda call: call.data == "balance")
def show_balance(call):
    user_id = call.message.chat.id
    stars = users.get(user_id, 0)
    bot.send_message(user_id, f"Vous avez {stars} étoiles.")

# Callback pour inviter des amis
@bot.callback_query_handler(func=lambda call: call.data == "invite")
def invite(call):
    user_id = call.message.chat.id
    invites[user_id] += 1
    bot.send_message(user_id, f"Vous avez invité {invites[user_id]} personnes. Continuez à inviter pour gagner plus d'étoiles !")

# Callback pour afficher les cadeaux disponibles dans la boutique
@bot.callback_query_handler(func=lambda call: call.data == "shop")
def shop(call):
    user_id = call.message.chat.id
    stars = users.get(user_id, 0)
    message = "🎁 Voici les cadeaux disponibles :\n\n"
    for gift in gifts:
        message += f"{gift['nom']} - {gift['prix']} étoiles\n"

    message += "\nChoisissez un cadeau en envoyant son nom."
    bot.send_message(user_id, message)

# Callback pour acheter un cadeau
@bot.message_handler(func=lambda message: any(gift['nom'] == message.text for gift in gifts))
def buy_gift(message):
    user_id = message.chat.id
    gift_name = message.text
    gift = next(gift for gift in gifts if gift['nom'] == gift_name)
    price = gift['prix']

    # Vérifie si l'utilisateur a suffisamment d'étoiles
    if users.get(user_id, 0) >= price:
        users[user_id] -= price
        bot.send_message(user_id, f"Félicitations ! Vous avez acheté un {gift_name} pour {price} étoiles.")
    else:
        bot.send_message(user_id, "Désolé, vous n'avez pas assez d'étoiles pour acheter ce cadeau.")

# Callback pour demander un retrait
@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def withdraw(call):
    user_id = call.message.chat.id
    stars = users.get(user_id, 0)
    bot.send_message(user_id, f"Vous avez demandé un retrait de {stars} étoiles. Cette demande est en cours.")

# Callback pour afficher les invitations de l'utilisateur
@bot.callback_query_handler(func=lambda call: call.data == "my_invites")
def my_invites(call):
    user_id = call.message.chat.id
    user_invites = invites.get(user_id, 0)
    bot.send_message(user_id, f"Vous avez invité {user_invites} personnes.")

    # Option de notification au admin
    status_message = f"Utilisateur {user_id} a invité {user_invites} personnes."
    bot.send_message(admin_id, status_message)

# Commande admin pour gérer les retraits
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != admin_id:
        return

    markup = InlineKeyboardMarkup()
    btn_broadcast = InlineKeyboardButton("📢 Diffuser un message", callback_data="broadcast")
    btn_withdraws = InlineKeyboardButton("💸 Gérer les retraits", callback_data="manage_withdraws")
    btn_add_balance = InlineKeyboardButton("➕ Ajouter des étoiles à un utilisateur", callback_data="add_balance")
    btn_status = InlineKeyboardButton("📊 Statut des utilisateurs", callback_data="status")
    markup.add(btn_broadcast, btn_withdraws)
    markup.add(btn_add_balance, btn_status)

    bot.send_message(admin_id, "⚙️ Panneau Admin", reply_markup=markup)

# Callback pour diffuser un message
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

# Callback pour gérer les retraits
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

# Callback pour confirmer un retrait
@bot.callback_query_handler(func=lambda call: call.data.startswith("withdraw_"))
def confirm_withdraw(call):
    if call.message.chat.id != admin_id:
        return

    index = int(call.data.split("_")[1])
    user_id = withdraw_requests[index]["user_id"]

    withdraw_requests[index]["status"] = "effectué"
    bot.send_message(user_id, "✅ Votre retrait a été confirmé par l'admin.")
    bot.send_message(admin_id, f"✅ Retrait confirmé pour {user_id}.")

# Callback pour ajouter des étoiles à un utilisateur
@bot.callback_query_handler(func=lambda call: call.data == "add_balance")
def add_balance(call):
    if call.message.chat.id != admin_id:
        return

    msg = bot.send_message(admin_id, "🖋️ Entrez l'ID de l'utilisateur et le nombre d'étoiles à ajouter :")
    bot.register_next_step_handler(msg, process_add_balance)

def process_add_balance(message):
    user_id, stars_to_add = map(int, message.text.split())
    if user_id in users:
        users[user_id] += stars_to_add
        bot.send_message(admin_id, f"✅ {stars_to_add} étoiles ont été ajoutées à l'utilisateur {user_id}.")
        bot.send_message(user_id, f"🎉 Vous avez reçu {stars_to_add} étoiles supplémentaires !")
    else:
        bot.send_message(admin_id, "❌ Utilisateur non trouvé.")


# Statut des utilisateurs
@bot.callback_query_handler(func=lambda call: call.data == "status")
def status(call):
    if call.message.chat.id != admin_id:
        return

    status_message = "📊 Statut des utilisateurs :\n"
    for user_id, stars in users.items():
        status_message += f"Utilisateur {user_id} : {stars} étoiles\n"

    bot.send_message(admin_id, status_message)

bot.polling()