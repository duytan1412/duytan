@echo off
echo Pushing to GitHub...
git branch -M main
git push -u origin main
echo.
echo Done! Now go to https://share.streamlit.io to deploy
pause
