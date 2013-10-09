pip install mako
pip install cherrypy

cd findAuthor
cd sdk_python
python alchemyapi.py 2a9b4bfd98bc338774da9db0846b700356240dca
cp api_key.txt ../
cp api_key.txt ../../web

cd ../../web
python __init__.py
