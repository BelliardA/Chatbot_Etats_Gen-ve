import sys
import time
import math
import requests

token = sys.argv[1]

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters


def appeler_opendata(path):
    url = f"http://transport.opendata.ch/v1{path}"
    reponse = requests.get(url)
    return reponse.json()

def rechercher_arrets(parametres):
    data = appeler_opendata(parametres)
    arrets = data['stations']
    message_texte = "Voici les résultats:\nCliquer sur les chiffres en bleu pour voir l'activité de l'arret.\n\n"

    for arret in arrets:
        if arret['id']:
            message_texte = f'{message_texte}\n /s{arret["id"]}'
            message_texte = f'{message_texte} {arret["name"]}'
            message_texte = f'{message_texte} ({arret["icon"]})'

    return message_texte

def rechercher_prochains_departs(id):

    data = appeler_opendata(f'/stationboard?id={id}')
    stationboard = data['stationboard']

    message_texte = "Voici les prochains départs:\n"
    maintenant = time.time()

    for depart in stationboard:
        message_texte += f"\n\n{depart['number']} → {depart['to']}\n"

        timestamp_depart = depart['stop']['departureTimestamp']
        diff = timestamp_depart - maintenant
        temps_en_minutes = math.floor(diff/60)

        if temps_en_minutes < 0:
            message_texte += ' Déjà parti...'
        elif temps_en_minutes < 2:
            message_texte += ' COURS! Il part dans 2 minutes'
        else:
            message_texte += f' dans {temps_en_minutes} minutes'

    return message_texte


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def recherche_texte(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texte_a_rechercher = update.message.text
    arrets = rechercher_arrets(f'/locations?query={texte_a_rechercher}')
    await update.message.reply_text(arrets)

async def recherche_gps(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_location = update.message.location
    arrets = rechercher_arrets(f'/locations?x={user_location.latitude}&y={user_location.longitude}')
    await update.message.reply_text(arrets)

async def afficher_arret(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    identifiant = update.message.text[2:]
    prochains_departs = rechercher_prochains_departs(identifiant)
    await update.message.reply_text(
        prochains_departs + "\n\n/retour pour revenir au menu"
    )


#app = ApplicationBuilder().token(token).build()

#app.add_handler(CommandHandler("start", start))
#app.add_handler(MessageHandler(filters.COMMAND, afficher_arret))
#app.add_handler(MessageHandler(filters.LOCATION, recherche_gps))
#app.add_handler(MessageHandler(filters.TEXT, recherche_texte))

#app.run_polling()