#!/bin/bash

mkdir orenda-ua-bot
cd orenda-ua-bot
git init
git config core.sparseCheckout true
git remote add origin https://github.com/rin-gil/orenda-ua-bot
echo "src" > .git/info/sparse-checkout
git fetch --depth 1 origin master
git checkout master
rm -r -f .git
mv src/* .
mv src/.env.example .env
rm src -r -f
rm requirements-dev.txt -r -f
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools
pip install -r requirements.txt
deactivate
cd ..
rm deploy.sh -f
