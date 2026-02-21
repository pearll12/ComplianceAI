from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_parser import extract_text_from_pdf_bytes
from app.services.llm_extractor import extract_rules_json_with_llm
from app.schemas.rules import PolicyRules
from app.storage.rules_store import save_rules_json

router = APIRouter(tags=["Policy"])

@router.post("/upload-policy")
async def upload_policy(file: UploadFile = File(...)):

    # SAFE filename handling (.lower fix)
    filename = (file.filename or "").strip()
    content_type = (file.content_type or "").lower()

    is_pdf_ext = filename.lower().endswith(".pdf")
    is_pdf_type = content_type == "application/pdf"

    if not (is_pdf_ext or is_pdf_type):
        raise HTTPException(
            status_code=400,
            detail=f"Please upload a PDF. Got filename='{filename}', content_type='{content_type}'"
        )

    # Read file bytes
    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="Empty file")

    # Extract text
    policy_text = extract_text_from_pdf_bytes(pdf_bytes)
    if not policy_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract text")

    # Call LLM
    llm_json = extract_rules_json_with_llm(policy_text)

    # Validate JSON schema
    try:
        parsed = PolicyRules.model_validate(llm_json)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid rule JSON: {str(e)}")

    # Save JSON
    save_rules_json(parsed.model_dump())

    return {
        "message": "Policy processed successfully",
        "rules": parsed.model_dump()
    }