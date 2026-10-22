@echo off
title Padaria Aroma & Trigo - Jogo Desktop
cd /d "%~dp0"
echo ========================================================
echo    PADARIA AROMA & TRIGO - JOGO DE COMPRAS DESKTOP
echo    Projeto Pronatec: Negocios Inovadores com IA
echo    Site: https://padariaaromaetrigo.netlify.app/
echo ========================================================
echo.
echo Iniciando o jogo...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ops! Ocorreu um erro ao iniciar. Verifique se o Python esta instalado.
    pause
)
