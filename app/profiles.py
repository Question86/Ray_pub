import json
from fastapi import APIRouter, HTTPException
from app.services.json_utils import load_profiles

router = APIRouter(prefix="/profiles", tags=["Profiles"])

@router.post("/update")
def update_json(data: dict):
    """
    Aktualisiert die JSON-Datei mit neuen Informationen.
    """
    try:
        file_path = "./app/data/profiles.json"
        existing_data = load_profiles(file_path)

        # JSON-Datenstruktur überprüfen und aktualisieren
        if isinstance(existing_data, list):
            existing_data.append(data)
        elif isinstance(existing_data, dict):
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
