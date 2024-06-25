# Creating a project
```bash
npx degit cloim/webapp my-new-project
```

# Initializing the project
```bash
cd my-new-project
npm install

cd backend
python -m venv venv

./venv/Scripts/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

# Configuring the project
Modify the `.env.*` files.
Create files `config_app.json` and `config_dev.json` in your backend path, referencing file `config_dev.json.example`.