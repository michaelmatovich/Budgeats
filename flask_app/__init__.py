from flask import Flask

app = Flask(__name__)
app.secret_key = "its_super_secret"
