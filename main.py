"""
API REST para Análise de Ameaças STRIDE
FastAPI endpoint para análise de diagramas de arquitetura
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from analyzer import analyze_architecture
from pdf_generator import generate_stride_pdf_report
from stride_knowledge import STRIDE, STRIDE_DETAILS
import tempfile
import os
from typing import Dict, Any

# Constantes de validação
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Inicializar aplicação FastAPI
app = FastAPI(
    title="STRIDE Threat Analyzer API",
    description="API para análise de ameaças em diagramas de arquitetura usando metodologia STRIDE",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Endpoint raiz - Informações da API
    """
    return {
        "message": "STRIDE Threat Analyzer API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Verificação de saúde da API",
            "/analyze": "POST - Análise de diagrama de arquitetura (JSON)",
            "/analyze-pdf": "POST - Análise de diagrama de arquitetura (PDF)",
            "/stride-info": "Informações sobre metodologia STRIDE",
            "/docs": "Documentação interativa da API"
        }
    }


@app.get("/health")
async def health():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "service": "STRIDE Threat Analyzer",
        "api_key_configured": bool(os.getenv("OPENAI_API_KEY"))
    }


def _validate_image(image: UploadFile) -> None:
    """Valida tipo de conteúdo do arquivo de imagem."""
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de arquivo não suportado. Use PNG, JPG ou JPEG. Recebido: {image.content_type}"
        )


async def _save_temp_image(image: UploadFile) -> tuple[str, bytes]:
    """Salva imagem em arquivo temporário após validar tamanho. Retorna (caminho, conteúdo)."""
    content = await image.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Arquivo muito grande. Tamanho máximo: 10MB"
        )
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(content)
        return tmp.name, content


def _cleanup_files(*paths: str) -> None:
    """Remove arquivos temporários de forma segura."""
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.unlink(path)
            except OSError:
                pass


@app.post("/analyze")
async def analyze(image: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Analisa um diagrama de arquitetura e identifica ameaças usando STRIDE
    
    Args:
        image: Arquivo de imagem (PNG, JPG, JPEG) do diagrama de arquitetura
        
    Returns:
        JSON com a análise completa de ameaças STRIDE
    """
    _validate_image(image)
    tmp_path = None
    
    try:
        tmp_path, _ = await _save_temp_image(image)
        result = analyze_architecture(tmp_path)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(
                status_code=500,
                detail=f"Erro na análise: {result['error']}"
            )
        
        return {
            "status": "success",
            "filename": image.filename,
            "analysis": result
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar imagem: {str(e)}"
        )
    finally:
        _cleanup_files(tmp_path)


@app.post("/analyze-pdf")
async def analyze_pdf(image: UploadFile = File(...)) -> FileResponse:
    """
    Analisa um diagrama de arquitetura e retorna relatório em PDF
    
    Args:
        image: Arquivo de imagem (PNG, JPG, JPEG) do diagrama de arquitetura
        
    Returns:
        Arquivo PDF com relatório completo de ameaças STRIDE
    """
    
    _validate_image(image)
    tmp_img_path = None
    tmp_pdf_path = None
    
    try:
        tmp_img_path, _ = await _save_temp_image(image)
        result = analyze_architecture(tmp_img_path)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(
                status_code=500,
                detail=f"Erro na análise: {result['error']}"
            )
        
        tmp_pdf_path = tempfile.mktemp(suffix=".pdf")
        generate_stride_pdf_report(result, tmp_pdf_path, tmp_img_path)
        _cleanup_files(tmp_img_path)
        tmp_img_path = None
        
        return FileResponse(
            path=tmp_pdf_path,
            media_type="application/pdf",
            filename=f"stride_report_{image.filename.split('.')[0]}.pdf",
            background=None
        )
    
    except HTTPException:
        raise
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar PDF: {str(e)}"
        )
    finally:
        _cleanup_files(tmp_img_path, tmp_pdf_path)


@app.get("/stride-info")
async def stride_info():
    """
    Retorna informações sobre a metodologia STRIDE
    """
    return {
        "methodology": "STRIDE",
        "description": "Metodologia de modelagem de ameaças desenvolvida pela Microsoft",
        "categories": STRIDE,
        "details": STRIDE_DETAILS
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando STRIDE Threat Analyzer API...")
    print("📖 Documentação: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
