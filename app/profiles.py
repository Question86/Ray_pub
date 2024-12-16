import json
import os
from fastapi import APIRouter, HTTPException
from app.services.json_utils import load_profiles
from pydantic import BaseModel

router = APIRouter(prefix="/profiles", tags=["Profiles"])

class UpdateData(BaseModel):
    conversation: dict
    topic: str
    content: str
    
# Pfad zur JSON-Datei
file_path = "./app/data/profiles.json"

@router.post("/update")
def update_json(data: UpdateData):
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
        existing_data = load_profiles(file_path)

      # Daten aktualisieren
        if "conversation" in data:
            existing_data["knowledge_base"]["conversations"].append(data["conversation"])
        if "topic" in data:
            topic = data["topic"]
            if topic not in existing_data["knowledge_base"]["topics"]:
                existing_data["knowledge_base"]["topics"][topic] = []
            existing_data["knowledge_base"]["topics"][topic].append(data["content"])

        # JSON-Datei speichern
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return {"message": "JSON updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
