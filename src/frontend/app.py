import streamlit as st
import requests
import azure_speech2text
import fonctions_db as fdb

def main():
    st.title("Ma Météo Vocale")
    st.write("Obtenez la météo de votre ville en un clin d'oeil")
    st.write("🎤 Appuyez sur le bouton ci-dessous et dites votre ville")

    if st.button("Commencer l'enregistrement🎤"):
        # Enregistrer la voix et obtenir le texte
        ret = azure_speech2text.recognize_from_microphone()
        transcribed_text = ret.text  # Utiliser le texte transcrit
        if transcribed_text == "":
            fdb.write_msg_DB("ERROR", "app.py : transcribed_text vide")
            st.write("Erreur : le texte transcrit est vide.")
            azure_speech2text.text2speech("Nous avons mal compris votre demande. Veuillez réessayer s'il vous plaît.")
            return
        
        # Envoyer le texte transcrit au backend
        response = requests.post("http://127.0.0.1:8000/demande_meteo/", json={"text": transcribed_text})
        #print(response.json())
        #result = response.json()
        if response.status_code == 200:
            try:
                result = response.json()
                # A EFFACER ENSUITE - Afficher les résultats
                #st.write(result)
                # Synthèse vocale des résultats
                azure_speech2text.text2speech("A " + result['location'] + " le " + result['forecast']['date'] + " les températures évolueront entre " + str(int(result['forecast']['temperature_min'])) + " et " + str(int(result['forecast']['temperature_max'])) + " degrés Celsius. ")
                if result['forecast']['precipitation'] == 0:
                    azure_speech2text.text2speech("Il n'y aura pas de pluie.")
                else: 
                    azure_speech2text.text2speech("Il est prévu " + str(result['forecast']['precipitation']) + "millimètres de pluie.")
                
                if result['forecast']['windspeed_max'] == 0:
                    azure_speech2text.text2speech("et il n'y aura pas de vent.")
                else:
                    azure_speech2text.text2speech("Le vent soufflera avec des pointes à " + str(int(result['forecast']['windspeed_max'])) + "km/h.") 
                
            except ValueError as e:
                fdb.write_msg_DB("ERROR", f"app.py : Erreur lors de la conversion de la réponse en JSON : {e}")
                st.write("Erreur : impossible de convertir la réponse en JSON.")  
        else:
            azure_speech2text.text2speech("Nous avons mal compris votre demande. Veuillez réessayer s'il vous plaît.")
            fdb.write_msg_DB("ERROR", f"app.py : Erreur lors de la requête au backend, code de retour {response.status_code}")
            st.write(f"Erreur : la requête au backend a échoué avec le code de retour {response.status_code}.")

if __name__ == "__main__":
    main()
