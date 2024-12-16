import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/profiles", tags=["Profiles"])

# Pydantic Modell zur Validierung der Daten
class UpdateRequest(BaseModel):
    conversation: dict
    topic: str
    content: str

@router.post("/update")
def update_json(data: UpdateRequest):
    """
    Aktualisiert die JSON-Datei mit neuen Informationen.
    """
    try:
        file_path = "C:\\Users\\ambas\\Ray\\app\\data\\profiles.json"
        
        # JSON-Datei laden
        with open(file_path, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
        
        # Wissenbasis aktualisieren
        if "knowledge_base" not in existing_data:
            existing_data["knowledge_base"] = {"conversations": [], "topics": {}}

        # Neue Konversation hinzufügen
        if "conversations" in existing_data["knowledge_base"]:
            existing_data["knowledge_base"]["conversations"].append(data.conversation)
        
        # Neues Thema hinzufügen oder erweitern
        if "topics" in existing_data["knowledge_base"]:
            if data.topic not in existing_data["knowledge_base"]["topics"]:
                existing_data["knowledge_base"]["topics"][data.topic] = []
            existing_data["knowledge_base"]["topics"][data.topic].append(data.content)
        
        # Änderungen in die JSON-Datei schreiben
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

        return {"message": "JSON updated successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="JSON file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

