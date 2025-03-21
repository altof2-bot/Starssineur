import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "7614211780:AAFuJT-AYCDSqJ_hczN-mRmwV8kJuRVKTMU"
bot = telebot.TeleBot(TOKEN)
reward_per_invite = 1  # Default reward per invite



# Base de données simple
users = {}
invites = {}
withdraw_requests = []
admin_id = 5116530698

# Liste des cadeaux avec leurs prix
gifts = [
    {"nom": "💎 100 étoiles", "prix": 100, "callback": "buy_100"},
    {"nom": "🎁 200 étoiles", "prix": 200, "callback": "buy_200"},
    {"nom": "🚀 500 etoile ", "prix": 500, "callback": "buy_psn"},
    {"nom": "🧸 15 etoile", "prix": 15, "callback": "buy_ours"},
    {"nom": "🎧 25 etoile", "prix": 25, "callback": "buy_casque"},
    {"nom": "🏝️ 50 etoile", "prix": 50, "callback": "buy_pc"},
    {"nom": "📱 75 etoile", "prix": 75, "callback": "buy_phone"},
    {"nom": "🎮 120 etoile", "prix": 120, "callback": "buy_switch"},
    {"nom": "🖥️ 200 etoile", "prix": 200, "callback": "buy_pc_gamer"},
    {"nom": "🛒 250 etoile", "prix": 250, "callback": "buy_amazon"},
    {"nom": "🎵 10 etoile", "prix": 10, "callback": "buy_spotify"},
    {"nom": "🍔 30 etoile ", "prix": 30, "callback": "buy_restaurant"},
    {"nom": "🎫 40 etoile", "prix": 40, "callback": "buy_concert"},
    {"nom": "🎁 Carte cadeau premuim", "prix": 460, "callback": "buy_itunes"},
    {"nom": "🌟 Récompense surprise", "prix": 150, "callback": "buy_surprise"},
]



# Fonction pour récupérer le nombre total d’utilisateurs
def total_users():
    return len(users)

# Commande /start avec vérification des abonnements
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    
    # Vérifier l'abonnement au canal
    try:
        channel_username = "@sineur_x_bot"
        member = bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        if member.status in ["left", "kicked", "restricted"]:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📢 Rejoindre le canal", url=f"https://t.me/{channel_username.replace('@', '')}"))
            bot.send_message(user_id, "⚠️ Vous devez être abonné à notre canal pour utiliser le bot !\n\nAbonnez-vous et réessayez /start", reply_markup=markup)
            return
    except telebot.apihelper.ApiTelegramException as e:
        if "Bad Request: chat not found" in str(e):
            # Le canal n'existe pas ou le bot n'y a pas accès
            bot.send_message(admin_id, f"⚠️ Erreur avec le canal {channel_username}: Canal non trouvé ou bot non admin")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Rejoindre le canal", url=f"https://t.me/{channel_username.replace('@', '')}"))
        bot.send_message(user_id, "⚠️ Vous devez être abonné à notre canal pour utiliser le bot !\n\nAbonnez-vous et réessayez /start", reply_markup=markup)
        return

    # Si l'utilisateur a été invité par un lien
    text = message.text.split()
    if len(text) > 1 and text[1].isdigit():
        inviter_id = int(text[1])
        # Vérifier que l'inviteur existe et qu'il ne s'auto-invite pas
        if inviter_id in users and inviter_id != user_id:
            if user_id not in invites.get(inviter_id, []):
                invites.setdefault(inviter_id, []).append(user_id)
                # Ajouter des étoiles à l'invitant
                users[inviter_id] = users.get(inviter_id, 0) + reward_per_invite
                bot.send_message(inviter_id, f"🎉 Vous avez gagné {reward_per_invite} étoiles en invitant {user_id} !")

    # Enregistrer le nouvel utilisateur s'il n'existe pas encore
    if user_id not in users:
        users[user_id] = 0
        invites[user_id] = []
        # Notifier l'admin du nouvel utilisateur
        user_info = message.from_user
        admin_msg = f"🆕 Nouvel utilisateur:\n"\
                   f"ID: {user_id}\n"\
                   f"Nom: {user_info.first_name}\n"\
                   f"Username: @{user_info.username}\n"\
                   f"Solde: 0 étoiles"
        bot.send_message(admin_id, admin_msg)
    
    # Générer un lien d’invitation unique
    invite_link = f"https://t.me/stars_give_freebot?start={user_id}"

    # Ajouter le nouvel utilisateur s'il n'existe pas
    if user_id not in users:
        users[user_id] = 0



    markup = InlineKeyboardMarkup()
    btn_balance = InlineKeyboardButton("💰 Mon solde", callback_data="balance")
    btn_invite = InlineKeyboardButton("📢 Inviter des amis", callback_data="invite")
    btn_shop = InlineKeyboardButton("🎁 Boutique", callback_data="shop")
    btn_withdraw = InlineKeyboardButton("💸 Demander un retrait", callback_data="withdraw")
    btn_my_invites = InlineKeyboardButton("👥 Mes invitations", callback_data="my_invites")
    markup.add(btn_balance, btn_invite)
    markup.add(btn_shop, btn_withdraw, btn_my_invites)

    bot.send_message(user_id, "🎉 Bienvenue sur notre bot ! 🌟\n\n"
                           "Notre bot est conçu pour vous offrir des étoiles ⭐ en échange d'invitations. Voici comment ça marche :\n\n"
                           "👥 Invitez 50 personnes = 🎁 10 étoiles\n"
                           "🛍️ Utilisez vos étoiles dans la boutique pour obtenir des récompenses !\n\n"
                           "💡 Vérifiez vos étoiles et explorez les cadeaux disponibles dans la boutique.\n\n"
                           "⚠️ Un problème avec vos étoiles ? Si vous n'avez pas reçu vos étoiles ou si une erreur s'est produite, déposez une plainte ici : 👉 @altof2 notre canal @sineur_x_bot \n\n"
                           "Profitez bien et commencez à inviter vos amis ! 🚀 Choisissez une option pour commencer.", reply_markup=markup)



# ➜ Générer un lien d'invitation
@bot.callback_query_handler(func=lambda call: call.data == "invite")
def invite(call):
    user_id = call.message.chat.id
    invite_link = f"https://t.me/{bot.get_me().username}?start={user_id}"

    bot.send_message(user_id, f"📢 Invite tes amis avec ce lien :\n{invite_link}\n\nChaque invitation te rapporte {reward_per_invite} étoiles !")


# Callback pour inviter des amis
@bot.callback_query_handler(func=lambda call: call.data == "invite")
def invite(call):
    user_id = call.message.chat.id
    invite_link = f"https://t.me/stars_give_freebot?start={user_id}"
    num_invites = len(invites.get(user_id, []))
    bot.send_message(user_id, f"🔗 Voici votre lien d'invitation:\n{invite_link}\n\nVous avez invité {num_invites} personnes. Continuez à inviter pour gagner plus d'étoiles !")

# ➜ Afficher la boutique avec des boutons
@bot.callback_query_handler(func=lambda call: call.data == "shop")
def shop(call):
    user_id = call.message.chat.id
    markup = InlineKeyboardMarkup()

    for gift in gifts:
        markup.add(InlineKeyboardButton(f"{gift['nom']} - {gift['prix']}⭐", callback_data=gift["callback"]))

    bot.send_message(user_id, "🎁 Voici les cadeaux disponibles :", reply_markup=markup)

# ➜ Confirmation d'achat avec boutons
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def confirm_purchase(call):
    user_id = call.message.chat.id
    gift = next(g for g in gifts if g["callback"] == call.data)

    markup = InlineKeyboardMarkup()
    markup.add(
        InlineKeyboardButton("✅ Confirmer", callback_data=f"confirm_{gift['callback']}"),
        InlineKeyboardButton("❌ Annuler", callback_data="shop")
    )

    bot.send_message(user_id, f"Voulez-vous acheter {gift['nom']} pour {gift['prix']} étoiles ?", reply_markup=markup)

# ➜ Achat final après confirmation
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def buy_gift(call):
    user_id = call.message.chat.id
    gift_callback = "_".join(call.data.split("_")[1:])  # Get everything after "confirm_"
    gift = next(g for g in gifts if g["callback"] == gift_callback)

    if users.get(user_id, 0) >= gift["prix"]:
        users[user_id] -= gift["prix"]
        bot.send_message(user_id, f"🎉 Félicitations ! Vous avez acheté {gift['nom']} pour {gift['prix']} étoiles.")
    else:
        bot.send_message(user_id, "❌ Pas assez d'étoiles !")



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
    markup.add(InlineKeyboardButton("⚙️ Modifier récompense", callback_data="change_reward"))
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
    try:
        parts = message.text.split()
        if len(parts) != 2:
            bot.send_message(admin_id, "❌ Format incorrect. Utilisez: [ID_UTILISATEUR] [NOMBRE_ETOILES]")
            return
            
        user_id, stars_to_add = map(int, parts)
        if user_id in users:
            users[user_id] += stars_to_add
            bot.send_message(admin_id, f"✅ {stars_to_add} étoiles ont été ajoutées à l'utilisateur {user_id}.")
            bot.send_message(user_id, f"🎉 Vous avez reçu {stars_to_add} étoiles supplémentaires !")
        else:
            bot.send_message(admin_id, "❌ Utilisateur non trouvé.")
    except ValueError:
        bot.send_message(admin_id, "❌ Format incorrect. Utilisez: [ID_UTILISATEUR] [NOMBRE_ETOILES]")

# ➜ Modifier la récompense par invitation (Admin uniquement)
@bot.callback_query_handler(func=lambda call: call.data == "change_reward")
def change_reward(call):
    if call.message.chat.id != admin_id:
        return
    msg = bot.send_message(admin_id, "🖊️ Entrez le nouveau nombre d'étoiles par invitation :")
    bot.register_next_step_handler(msg, update_reward)

def update_reward(message):
    global reward_per_invite
    try:
        new_reward = float(message.text)
        if new_reward > 0:
            reward_per_invite = new_reward
            bot.send_message(admin_id, f"✅ La récompense par invitation est maintenant de {reward_per_invite} étoiles !")
        else:
            bot.send_message(admin_id, "❌ La récompense doit être supérieure à 0.")
    except ValueError:
        bot.send_message(admin_id, "❌ Veuillez entrer un nombre valide (ex: 0.5, 1.5, 2).")
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