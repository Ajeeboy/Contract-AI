# Introduction
Contract AI's webapp front-end

# Pre-Requisites
1. Powershell 7.4.6
2. Python 3.13.1
3. VS Code 1.96.4 (System)
4. GIT Credential Manager 1.20
5. Create python project file pyproject.toml in C:\Windows folder

# Getting Started
1.	Installation process
    Run the following in your pwsh terminal from within your IDE, after cloning the repo:
        python -m venv .venv
        
        pip install -r requirements.txt

2.  Runtime process
    Simply hit the play button on the "app-start.py" script or run the the following in your pwsh terminal:
        python runner.py
    To manually start the app for testing purposes run the following in your pwsh terminal:
        streamlit run filename.py
    In order to manually start the app, it may be required to initialise your venv, which can be achieved by running the following in your pswh terminal:
        .venv\scripts\activate
    To kill the app, once it has successfuly started, hit CTRL+C in the terminal or close your terminal

3.  Git mirroring
    In order to maintain a mirror between the host DevOps repo and the endpoint GitHub repo, run the following in your bash terminal:
        git clone --mirror https://dev.azure.com/contractai/Contract%20AI/_git/Contract%20AI%20Webapp
        rm -rf ./"Contract AI Webapp.git"
        mv ./"Contract%20AI%20Webapp.git" ./"Contract AI Webapp.git"
        cd ./"Contract AI Webapp.git"
        git push --mirror https://github.com/DMC-PA/Contract-AI-Webapp
        cd ..
    This creates a static copy of the DevOps repo based on the last time this clone/push sequence was run for 

4.	Software dependencies
    Please refer to the requirements.txt file found at root
    The main app file MUST be named "contract-ai-frontend.py", not having a file with this name in root will cause app hosting to fail
