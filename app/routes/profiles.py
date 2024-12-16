from fastapi import APIRouter, HTTPException
import json
import os

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

        # JSON-Datenstruktur überprüfen und aktualisieren
        if "knowledge_base" not in existing_data:
            existing_data["knowledge_base"] = {"conversations": [], "topics": {}}
        if "conversation" in data:
            existing_data["knowledge_base"]["conversations"].append(data["conversation"])
        if "topic" in data:
            topic = data["topic"]
            if topic not in existing_data["knowledge_base"]["topics"]:
                existing_data["knowledge_base"]["topics"][topic] = []
            existing_data["knowledge_base"]["topics"][topic].append(data["content"])

        # Aktualisierte JSON-Daten speichern
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return {"message": "JSON updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
