#!/bin/bash

BASE_DIR=/home/bassturtle4/Documents/GitHub/Py-Img-Sorter/

update_base_dir() {
    read -p "The directory $BASE_DIR does not exist. Please provide a new directory (full file path, where you are holding python files): " NEW_DIR
    BASE_DIR=$NEW_DIR
    sed -i "s|^BASE_DIR=.*|BASE_DIR=$NEW_DIR|" $0
    echo "Updated the script with the new directory: $NEW_DIR"
}

if [ ! -d "$BASE_DIR" ]; then
    update_base_dir
fi

cd "$BASE_DIR" || exit

if [ ! -d "env" ]; then
    read -p "The virtual environment does not exist. Would you like to create it and install required packages? (Y/n): " RESPONSE
    if [[ "$RESPONSE" =~ ^[Yy]$ ]]; then
        echo "Creating virtual environment and installing packages..."
        python -m venv env
        . ./env/bin/activate
        pip install jupyterlab
        python -m pip install jupyter_collaboration
        
        # Check if the system is Linux
        if [[ "$(uname)" == "Linux" ]]; then
            echo "Detected Linux system. Proceeding with installation..."
            curl -fsSL https://ollama.com/install.sh | sh
        else
            echo "Non-Linux system detected. Opening download page..."
            if command -v open &>/dev/null; then
                open https://ollama.com/download
            elif command -v xdg-open &>/dev/null; then
                xdg-open https://ollama.com/download
            else
                echo "Please open https://ollama.com/download in your browser."
            fi
            
            echo "Press Enter after you've downloaded the installer to continue."
            read -r
        fi

        ollama pull llama3.2-vision

        pip install ollama

    else
        echo "Skipping virtual environment creation and package installation."
        exit
    fi
else
    echo "Virtual environment already exists. Skipping environment creation and package installation..."
    . ./env/bin/activate
fi

jupyter lab --ip=0.0.0.0 --collaborative

deactivate

cd
