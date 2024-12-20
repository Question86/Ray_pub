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

def push_to_github():
    """
    Synchronisiert die aktualisierte JSON-Datei mit GitHub.
    """
    try:
        # Setze Berechtigungen für den privaten Schlüssel
        os.chmod("render_deploy_key", 0o600)

        # Setze GIT_SSH_COMMAND, um den SSH-Schlüssel zu verwenden
        os.environ["GIT_SSH_COMMAND"] = "ssh -i render_deploy_key -o StrictHostKeyChecking=no"

        # Git initialisieren, falls erforderlich
        if not os.path.exists(".git"):
            print("Git repository not initialized. Initializing...")
            subprocess.run(["git", "init"], check=True)

        # Git-Konfiguration setzen
        subprocess.run(["git", "config", "user.email", "Question86@protonmail.com"], check=True)
        subprocess.run(["git", "config", "user.name", "Question86"], check=True)

        # Remote hinzufügen oder aktualisieren
        remote_url = "git@github.com:Question86/Ray_pub.git"
        print(f"Remote URL: {remote_url}")
        remote_check = subprocess.run(["git", "remote"], capture_output=True, text=True)
        if "origin" not in remote_check.stdout:
            subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
        else:
            subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)

        # Git push ausführen mit SSH-Schlüssel
        subprocess.run(["git", "add", "app/data/profiles.json"], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update profiles.json"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)

        print("Änderungen erfolgreich zu GitHub gepusht!")
    except subprocess.CalledProcessError as e:
        print(f"Git push failed with return code {e.returncode} and output: {e.output}")
    except Exception as e:
        print(f"Fehler beim Pushen: {e}")

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

