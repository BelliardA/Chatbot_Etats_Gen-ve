#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, sys
from transport import recherche_gps, recherche_texte,afficher_arret

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

token = sys.argv[1]
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


TRANSPORT ,MENUE ,SORTI_CHOIX ,RECOMMANDE_SORTI ,RESTAURANT_CHOIX ,RESTAU_RESULT ,RESTAU_DETAILS = range(7)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Commencer la discusion en demandant si la personne veut manger ou sortir."""
    reply_keyboard = [["Sortir 🚶‍♂️", "Manger 🍔"]]

    await update.message.reply_text(
        "Bonjour,je m'appelle guidoBot, je suis votre guide touristique ;)\n"
        "est-ce que vous voulez sortir ou manger quelques part\n\nPour avoir de l'aide entrez /help",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Sortir ou Manger?"
        ),
    )

    return MENUE

#------------------------------------------------------------------------Restaurant---------------------------------------------------------

async def restau_choix(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Italien 🇮🇹", "Asiatique 🌏"],
        ["Suisse 🇨🇭", "Français 🇫🇷", "Thaïlandais 🇹🇭"],
        ["Retour"]
    ]

    await update.message.reply_text(
        "Quelle type de nourriture voulez-vous manger ?\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Type de nourriture"
        ),
    )

    return RESTAURANT_CHOIX

#-------------------------------------------restaurants italien----------------------------------------
async def afficher_restau_Italien(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["La Tranche Gerardo Scalea"],
        ["Restaurant Intenso"],
        ["Braceria Gerardo Scalea"],
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des restaurants Italiens, faites votre choix !\n\nCliquer pour voir les détails",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Top 3 restaurants italien"
        ),
    )

    return RESTAU_RESULT

async def la_tranche_gerardo_scalea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        " Une cuisine à l'italienne concoctée par des italiens pure souche\n"
        "Le risotto dans la meule de parmesan et les pâtes fraiches maison sont les deux spécialités de l'Italia qui propose en outre des plats originaux de saison en plus de la carte fixe des mets.\n\n"
        "Tous les fruits et légumes de l'Italia proviennent de producteurs locaux genevois. Le restaurant reste fidèle à ses maraîchers de Plan-les-Ouates depuis le début.\n"
        "La Mozzarella di Bufala, les vins italiens et certains autres ingrédients typiques de la cuisine italiennesont sélectionnés directement par le patron.\n\n"
        "heure d'ouverture : \n du Lundi au Vendredi\t 11:30 - 14:30 / 18:00 - 23:00 \n Samedi et Dimanche\t 18:00 - 23:00",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Type de nourriture"
        ),
    )

    return RESTAU_DETAILS

async def intenso(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Une équipe soudée, disponible pour les clients. Une cuisine qui excelle dans la recherche et la matière première, dans la créativité, comme dans la technique de cuisson.\n"
        "Une ambiance intime et chaleureuse; un voyage unique dans les parfums et les saveurs authentiques de l’Italie.\n"
        "Le Chef Ciro Guarino et son team italienne, vous proposera une sélection de plats de la tradition du Bel Paese, notamment de la Côte Amalfitaine.\n"
        "heure d'ouverture : \n du Mardi au Samedi\t 10:00 - 22:00",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Restaurant Intenso"
        ),
    )

    return RESTAU_DETAILS


async def braceria_gerardo_scalea(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Le restaurant Italia accueille sa clientèle dans un décor étonnant mêlant l'ambiance italienne traditionnelle à l'esprit méditerranéen avec une verrière et des plantes suspendues.\n"
        "Le risotto dans la meule de parmesan et les pâtes fraiches maison sont les deux spécialités de l'Italia qui propose en outre des plats originaux de saison en plus de la carte fixe des mets.\n"
        "heure d'ouverture : \n du Lundi au Dimanche\t 11:45 - 14:00 / 18:45 - 23:00 ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Braceria Gerardo Scalea"
        ),
    )

    return RESTAU_DETAILS


#---------------------------------------------restaurant français-------------------------------------------

async def afficher_restau_Français(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Au Furet"],
        ["Domaine de Chateauvieux"],
        ["Les Curiades"],
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des restaurants Français, faites votre choix !\n\nCliquer pour voir les détails",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Top 3 restaurants italien"
        ),
    )

    return RESTAU_RESULT

async def au_furet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        " Michel Corajod et son équipe vous souhaite la bienvenue au Furet , le numéro 1 des gambas à gogo !\n"
        "Tout les midis retrouvez notre entrecôte parisienne à 17.-chf ainsi que le coquelet entier aux bolets à 15.-chf !!\n\n"
        "Dans le quartier populaire des Charmilles, le restaurant le furet vous propose une cuisine variée, un plat du jour soigné à  17 frs, et ses spécialités.\n"
        "heure d'ouverture : \n du Lundi au Vendredi\t 06:30 - 00h00\n Samedi et Dimanche\t09:00 - 00:00",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Au furet"
        ),
    )

    return RESTAU_DETAILS

async def domaine_chateauvieux(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        " Dans ce lieu historique où une atmosphère conviviale règne, vous serez choyés dès votre arrivée et aurez l’impression de vous sentir comme chez vous. Toutes nos chambres ont été décorées avec élégance et raffinement et ont toutes une vue magnifique donnant sur les vignes, le Rhône ou sur les montagnes du Jura. Nous sommes certains que vous serez sensibles au fait que l’Hôtel du Domaine de Châteauvieux abrite un restaurant gastronomique de réputation internationale, sous la direction de son chef étoilé Philippe Chevrier, également propriétaire du domaine.\n"
        "heure d'ouverture : \n du Mardi au Samedi\t 06:30 - 23:00",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Domaine de Chateauvieux"
        ),
    )

    return RESTAU_DETAILS

async def les_curiades(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        " nous proposons 3 menus à l'année inspirés par l'humeur et les trouvailles du Chef au marché : un menu Terroir, un menu végétarien Retour du potager et un Grand Menu Curiades accompagnés d'accords mets et vins. Selon les saisons nous pouvons aussi proposer des menus à durée limitée comme le menu Chasse à l'automne ou encore chaque samedi midi un menu Retour du marché en quantité limitée (la réservation est vivement recommandée!).\n"
        "heure d'ouverture : \n du Mardi au Samedi\t 12:15 - 15:00 / 19:00 - 00:00",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Les Curiades"
        ),
    )

    return RESTAU_DETAILS

#---------------------------------------------restaurant thaïlandais----------------------------------------
async def afficher_restau_Thailandais(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Lanna Thai"],
        ["Baï-Toey"],
        ["Thai Phuket"],
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des restaurants Thailandais, faites votre choix !\n\nCliquer pour voir les détails",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Top 3 restaurants italien"
        ),
    )

    return RESTAU_RESULT

async def lanna_thai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Véritable cuisine thailandaise à déguster dans une ambiance familiale et chaleureuse. Spécialités Salade de Papaye, Phad Thai, Curry. Jolie terrasse ensoleillée.\n"
        "Tout nos plats sont disponibles à l'emporter. Carte des vins et bière Thai ( Singha ).\n\n"
        "Organisation de fêtes et événements particuliers sur réservation ( 60 places à l'intérieur + 40 places en terrasse ).\n"
        "heure d'ouverture : \n du Lundi au Samedi\t 11:30 - 22:00",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Lanna Thai"
        ),
    )

    return RESTAU_DETAILS

async def bai_toey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        " Dans ce lieu historique où une atmosphère conviviale règne, vous serez choyés dès votre arrivée et aurez l’impression de vous sentir comme chez vous. Toutes nos chambres ont été décorées avec élégance et raffinement et ont toutes une vue magnifique donnant sur les vignes, le Rhône ou sur les montagnes du Jura. Nous sommes certains que vous serez sensibles au fait que l’Hôtel du Domaine de Châteauvieux abrite un restaurant gastronomique de réputation internationale, sous la direction de son chef étoilé Philippe Chevrier, également propriétaire du domaine.\n"
        "heure d'ouverture : \n du Lundi au Vendredi\t 11:00 - 23:00\n Dimanche\t 17:00 - 22:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Baï-Toey"
        ),
    )

    return RESTAU_DETAILS

async def thai_phukets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Dans un cadre authentique vous retrouverez une qualité de service et une excellente cuisine thaï. Ce restaurant gastronomique accueille des diplomates, des fonctionnaires internationaux et des hommes d'affaires pour le lunch ou pour le dîner\n"
        "heure d'ouverture : \n du Lundi au Samedi\t 12:00 - 14:30 / 19:00 - 22:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Thai Phuket"
        ),
    )

    return RESTAU_DETAILS

#--------------------------------------------Restaurant suisse----------------------------------------------
async def afficher_restau_Suisse(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Planet Caviar"],
        ["Café de Mategnin"],
        ["Trigal"],
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des restaurants Suisse, faites votre choix !\n\nCliquer pour voir les détails",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Top 3 restaurants italien"
        ),
    )

    return RESTAU_RESULT

async def planet_caviar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Depuis 1997, Planet Caviar s’est imposé comme une référence en matière de caviars d’excellence.\n"
        "Spécialiste de ce mets savoureux et précieux, Planet Caviar accorde un soin attentif et particulier à la qualité et la fraîcheur des caviars, sélectionnés avec soin, certifiés CITES et d’origine contrôlée\n\n"
        "Planet Caviar importe et commercialise les meilleurs caviars des quatre coins du monde et apporte son savoir-faire grâce à la collaboration de fournisseurs réputés (en France, Italie, Bulgarie, Uruguay, Israël, Chine…)\n"
        "heure d'ouverture : \n du Lundi au Samedi\t 9:00 - 22:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Planet Caviar"
        ),
    )

    return RESTAU_DETAILS

async def cafe_de_mategnin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Venez déguster l'une des meilleures fondues de fromage de Genève dans notre café typiquement genevois (depuis 1917).\n"
        "Vous pouvez également profiter d'une ambiance plus feutrée dans notre salle de restaurant où vous sera servie une cuisine traditionnelle genevoise accompagnée de ses vins du terroir.\n"
        "Plusieurs assiettes du jour dès 17.–. Notre restaurant dispose d'une salle de 100 places, du café de 60 places et d'une terrasse l'été de 80 places.\n\n"
        "heure d'ouverture : \n du Mardi au Samedi\t 10:30 - 14:30 / 18:30 - 23:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Café de Mategnin"
        ),
    )

    return RESTAU_DETAILS

async def trigal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Il a été fondé par Luis Coutinho, cuisinier de formation ayant toujours travaillé dans le domaine de la restauration. \n"
        "A la tête de l'établissement et d'une équipe de 8 employés, il propose des plats variés issus de la cuisine italienne, française et suisse qui raviront petits et grands !\n"
        "Grâce à ses 96 places intérieures et ses 120 places extérieures idéalement réparties sur deux terrasses, le restaurant accueille volontiers les particuliers souhaitant fêter leurs anniversaire, mariage, baptême ou encore communion.\n\n"
        "heure d'ouverture : \n du Lundi au Dimache\t 06:30 - 23:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Trigal"
        ),
    )

    return RESTAU_DETAILS
#--------------------------------------------Restaurant asiatique-------------------------------------------
async def afficher_restau_Asiatique(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Misuji"],
        ["Pakùpakù"],
        ["Wasabi"],
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des restaurants Asiatiques, faites votre choix !\n\nCliquer pour voir les détails",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Top 3 restaurants italien"
        ),
    )
    return RESTAU_RESULT

async def misuji(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Depuis 1997, Planet Caviar s’est imposé comme une référence en matière de caviars d’excellence.\n"
        "Spécialiste de ce mets savoureux et précieux, Planet Caviar accorde un soin attentif et particulier à la qualité et la fraîcheur des caviars, sélectionnés avec soin, certifiés CITES et d’origine contrôlée\n\n"
        "Planet Caviar importe et commercialise les meilleurs caviars des quatre coins du monde et apporte son savoir-faire grâce à la collaboration de fournisseurs réputés (en France, Italie, Bulgarie, Uruguay, Israël, Chine…)\n"
        "heure d'ouverture : \n du Lundi au Samedi\t 9:00 - 22:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Misuji"
        ),
    )

    return RESTAU_DETAILS

async def pakupaku(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Venez déguster l'une des meilleures fondues de fromage de Genève dans notre café typiquement genevois (depuis 1917).\n"
        "Vous pouvez également profiter d'une ambiance plus feutrée dans notre salle de restaurant où vous sera servie une cuisine traditionnelle genevoise accompagnée de ses vins du terroir.\n"
        "Plusieurs assiettes du jour dès 17.–. Notre restaurant dispose d'une salle de 100 places, du café de 60 places et d'une terrasse l'été de 80 places.\n\n"
        "heure d'ouverture : \n du Mardi au Samedi\t 10:30 - 14:30 / 18:30 - 23:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Pakùpakù"
        ),
    )

    return RESTAU_DETAILS

async def wasabi(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Il a été fondé par Luis Coutinho, cuisinier de formation ayant toujours travaillé dans le domaine de la restauration. \n"
        "A la tête de l'établissement et d'une équipe de 8 employés, il propose des plats variés issus de la cuisine italienne, française et suisse qui raviront petits et grands !\n"
        "Grâce à ses 96 places intérieures et ses 120 places extérieures idéalement réparties sur deux terrasses, le restaurant accueille volontiers les particuliers souhaitant fêter leurs anniversaire, mariage, baptême ou encore communion.\n\n"
        "heure d'ouverture : \n du Lundi au Dimache\t 06:30 - 23:30",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Wasabi"
        ),
    )

    return RESTAU_DETAILS


#-------------------------------------------------------------------------------sorti--------------------------------------------------------------------


async def sortir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["🎨 Musées 🎨"],
        ["🍻 Bars 🍻"],
        ["🕺 Clubs 🕺"],
        ["Retour"]
    ]

    await update.message.reply_text(
        "Sortir ça fait du bien ! quel type d'établissement voulez-vous pour votre sortie ?\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Etablissement divertissement"
        ),
    )

    return SORTI_CHOIX

async def musees(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des meilleurs musée de Genève\n\n\t- Museum of Natural History🦣\n\t- CERN⚡\n\t- Musée d'art et d'histoire🧑‍🎨",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Wasabi"
        ),
    )

    return RECOMMANDE_SORTI

async def bars(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des meilleurs bars de Genève \n\n\t- Britannia Pub🎉\n\t- Mr. Pickwick☕\n\t- O'Brasseur🍺",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Wasabi"
        ),
    )

    return RECOMMANDE_SORTI

async def clubs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """l'utilisateur veut manger donc on lui propose des styles de nourritures"""
    reply_keyboard = [
        ["Retour"]
    ]

    await update.message.reply_text(
        "Voici le top 3 des meilleurs clubs de Genève\n\n\t- Village du soir🌆\n\t- Baby Boa🐍\n\t- La Gravière🪨",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Wasabi"
        ),
    )

    return RECOMMANDE_SORTI

#---------------------------------------------------------transport-------------------------------------------------------------
async def transport(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Il y a deux manières de chercher un arret de tram\n 1.\t Envoie ta localisation et je t'envpoie les transport les plus proche\n2.\t Ecris le nom de l'arret", reply_markup=ReplyKeyboardRemove()
    )

    return TRANSPORT

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    await update.message.reply_text(
        "Il y a plusieurs commande que vous pouvez faire n'importe quand : \n\n/help\tAide pour les commandes\n/menu Quitter le menu help\n/cancel\tFerme le Bot \n/transport\tOuvre le menu de transport\n   |-> /retour (dans le menu transport)\t Pour revenir en arrière", reply_markup=ReplyKeyboardRemove()
    )

    return MENUE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "A plus tard, profite de Genève et si tu a besoin je suis la 👋", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    application = Application.builder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENUE: [
                MessageHandler(filters.Regex("^(Sortir)"), sortir),
                MessageHandler(filters.Regex("^(Manger)"), restau_choix)
            ],
            RESTAURANT_CHOIX: [
                MessageHandler(filters.Regex("^(Italien)"), afficher_restau_Italien),
                MessageHandler(filters.Regex("^(Français)"), afficher_restau_Français),
                MessageHandler(filters.Regex("^(Asiatique)"), afficher_restau_Asiatique),
                MessageHandler(filters.Regex("^(Suisse)"), afficher_restau_Suisse),
                MessageHandler(filters.Regex("^(Thaïlandais)"), afficher_restau_Thailandais),
                MessageHandler(filters.Regex("(Retour)"), start)
            ],
            RESTAU_RESULT: [
                #-------restau italiens-------
                MessageHandler(filters.Regex("^(La Tranche Gerardo Scalea)$"), la_tranche_gerardo_scalea),
                MessageHandler(filters.Regex("^(Restaurant Intenso)$"), intenso),
                MessageHandler(filters.Regex("^(Braceria Gerardo Scalea)$"), braceria_gerardo_scalea),
                #------restau français-------
                MessageHandler(filters.Regex("^(Au Furet)$"), au_furet),
                MessageHandler(filters.Regex("^(Domaine de Chateauvieux)$"), domaine_chateauvieux),
                MessageHandler(filters.Regex("^(Les Curiades)$"), les_curiades),
                #------restau thailandais----
                MessageHandler(filters.Regex("^(Lanna Thai)$"), lanna_thai),
                MessageHandler(filters.Regex("^(Baï-Toey)$"), bai_toey),
                MessageHandler(filters.Regex("^(Thai Phuket)$"), thai_phukets),
                #------restau suisse--------
                MessageHandler(filters.Regex("^(Planet Caviar)$"), planet_caviar),
                MessageHandler(filters.Regex("^(Café de Mategnin)$"), cafe_de_mategnin),
                MessageHandler(filters.Regex("^(Trigal)$"), trigal),
                #-----restau asiatique------
                MessageHandler(filters.Regex("^(Misuji)$"), misuji),
                MessageHandler(filters.Regex("^(Pakùpakù)$"), pakupaku),
                MessageHandler(filters.Regex("^(Wasabi)$"), wasabi),

                MessageHandler(filters.Regex("(Retour)"), restau_choix)
            ],
            RESTAU_DETAILS: [
                MessageHandler(filters.Regex("(Retour)"), restau_choix)
            ],
            SORTI_CHOIX: [
                MessageHandler(filters.Regex("(Musées)"), musees),
                MessageHandler(filters.Regex("(Bars)"), bars),
                MessageHandler(filters.Regex("(Clubs)"), clubs),
                MessageHandler(filters.Regex("(Retour)"), start)
            ],
            RECOMMANDE_SORTI: [
                MessageHandler(filters.Regex("(Retour)"), sortir)
            ],
            TRANSPORT:[
                CommandHandler("cancel", cancel),
                CommandHandler("retour", start),
                MessageHandler(filters.COMMAND, afficher_arret),
                MessageHandler(filters.LOCATION, recherche_gps),
                MessageHandler(filters.TEXT, recherche_texte)
            ]
        },
        fallbacks=[
            CommandHandler("menu", start),
            CommandHandler("cancel", cancel),
            CommandHandler("transport", transport),
            CommandHandler('help', help)
        ],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()