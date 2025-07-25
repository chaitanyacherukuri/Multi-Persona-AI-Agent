from fastapi import FastAPI, HTTPException
from requests import JSONResponse
from pydantic import BaseModel, Field
from typing import List
from app.core.ai_agent import get_response_from_ai_agents
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from app.config.settings import settings

logger = get_logger(__name__)

app = FastAPI(title="AI Agent API")

class RequestBody(BaseModel):
    model_name: str = Field(..., description="The name of the model to be used")
    messages: List[str] = Field(..., description="The message to be sent to the AI agent")
    allow_search: bool = Field(..., description="Whether to allow search or not")
    system_prompt: str = Field(..., description="The system prompt to be used")

@app.post("/chat")
def chat_endpoint(request: RequestBody):
    logger.info(f"Received request for model: {request.model_name}")

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        logger.warning(f"Invalid model name: {request.model_name}")
        raise HTTPException(status_code=400, detail="Invalid model name")
    
    try:
        response = get_response_from_ai_agents(
            request.model_name,
            request.messages,
            request.allow_search,
            request.system_prompt
        )

        logger.info(f"Successfully received response from AI agent {request.model_name}")

        return {"response": response}
        #return JSONResponse(status_code=200, content=response)
    
    except Exception as e:
        logger.error(f"Error while generating response: {str(e)}")
        raise HTTPException(status_code=500, detail=str(CustomException("Error while generating response", error_detail=e)))
        

