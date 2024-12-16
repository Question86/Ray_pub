from fastapi import APIRouter, HTTPException
import json
import os
import subprocess

router = APIRouter(prefix="/profiles", tags=["Profiles"])

file_path = "./app/data/profiles.json"

@router.post("/update")
def update_json(data: dict):
    """
    Aktualisiert die JSON-Datei mit neuen Informationen.
    """
    try:
        # Überprüfen, ob die Datei existiert, und ggf. erstellen
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({"knowledge_base": {"conversations": [], "topics": {}}}, file)

        # Bestehende JSON-Daten laden
        with open(file_path, "r", encoding="utf-8") as file:
            existing_data = json.load(file)

        # JSON-Daten aktualisieren
        if "conversation" in data:
            existing_data["knowledge_base"]["conversations"].append(data["conversation"])
        if "topic" in data:
            topic = data["topic"]
            if topic not in existing_data["knowledge_base"]["topics"]:
                existing_data["knowledge_base"]["topics"][topic] = []
            existing_data["knowledge_base"]["topics"][topic].append(data["content"])

        # JSON-Daten speichern
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        # Änderungen zu GitHub pushen
        push_to_github()

        return {"message": "JSON updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        
@router.get("/view")
def view_json():
    """
    Gibt den Inhalt der JSON-Datei zurück.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

def push_to_github():
    """
    Synchronisiert die aktualisierte JSON-Datei mit GitHub.
    """
    try:
        # Git-Konfiguration setzen
        subprocess.run(["git", "config", "user.email", "you@example.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Your Name"], check=True)

        # Remote-Repository mit Token hinzufügen oder aktualisieren
        subprocess.run(["git", "remote", "set-url", "origin",
                        "https://Question86:ghp_abcd1234efgh5678ijkl9012mnop3456qrst7890@github.com/Question86/Ray_pub.git"], check=True)

        # Git-Befehle ausführen
        subprocess.run(["git", "add", file_path], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update profiles.json"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("Profiles.json erfolgreich zu GitHub gepusht.")
    except subprocess.CalledProcessError as e:
        print(f"Git-Fehler: {e}")


