from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps
import os

import api

app = Flask(__name__)
# augmenter le niveau de logging pour voir les infos de démarrage
app.logger.setLevel('INFO')
# clé secrète pour session (doit être défini en production via env)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "replace-with-a-secure-key")

# base url configurée depuis l'environnement si nécessaire (utilisé côté JS si besoin)
app.config['API_URL'] = os.getenv('CLOUD_API_URL', api.BASE_URL)

# log de configuration au démarrage
app.logger.info(f"Using API_URL={app.config['API_URL']}")
app.logger.info(f"FLASK_SECRET_KEY set={'yes' if os.getenv('FLASK_SECRET_KEY') else 'no'}")

# helpers accessibles dans les templates
@app.template_global()
def icon_bg_color(status_or_type=None):
    # retourne une couleur neutre, le backend ne fournit pas le type
    return 'bg-slate-50 dark:bg-slate-700/20'

@app.template_global()
def icon_color(status_or_type=None):
    return 'slate-600 dark:text-slate-300'

# ----- helpers -------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash('Vous devez être connecté pour accéder à cette page.', 'error')
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def set_api_token():
    token = session.get('token')
    # nothing to set globally; token passed explicitly on each call
    return token

# ----- pages ---------------------------------------------------------------
@app.route("/")
def home():
    # récuperation des fichiers publics via l'API
    public_files = []
    try:
        resp = api.get_all_files(token=set_api_token())
        all_files = resp.get('files', []) if resp else []
        # accepter majuscules/minuscules
        public_files = [f for f in all_files if str(f.get('status','')).lower() == 'public']
    except api.APIError as e:
        app.logger.error(f"get_all_files failed: {e}")
        flash(f"Impossible de charger les fichiers publics : {e}", 'error')
    return render_template("home.html", public_files=public_files)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            data = api.login(email, password)
            session['user'] = data.get('user')
            # certains backends renvoient un token ou access_token
            token = data.get('token') or data.get('access_token')
            if token:
                session['token'] = token
            flash('Connexion réussie', 'success')
            return redirect(url_for('dashboard'))
        except api.APIError as e:
            flash(str(e), 'error')
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        name = request.form.get("name")
        try:
            data = api.signup(email, password, name)
            session['user'] = data.get('user')
            # extraire éventuel jeton
            token = data.get('token') or data.get('access_token')
            if token:
                session['token'] = token
            flash('Inscription réussie. Vous êtes connecté.', 'success')
            return redirect(url_for('dashboard'))
        except api.APIError as e:
            flash(str(e), 'error')
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("token", None)
    # remove any cookies stored in requests session (backend auth)
    try:
        api._session.cookies.clear()
    except Exception:
        pass
    flash('Vous avez été déconnecté.', 'success')
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    user = session.get('user') or {}
    user_id = user.get('id')
    app.logger.debug(f"dashboard requested for user_id={user_id} session_user={user}")
    private_files = []
    try:
        resp = api.get_user_files(user_id, token=set_api_token())
        private_files = resp.get('files', []) if resp else []
        app.logger.debug(f"user files response: {private_files}")
    except api.APIError as e:
        app.logger.error(f"get_user_files failed for {user_id}: {e}")
        flash(f"Impossible de charger vos fichiers privés : {e}", 'error')
    # public files are not shown on dashboard; they belong to home page only
    return render_template("dashboard.html", private_files=private_files)

@app.route("/file/<file_id>/status", methods=["POST"])
@login_required
def change_status(file_id):
    new_status = request.form.get('status')
    try:
        api.update_file_status(file_id, new_status, token=set_api_token())
        flash('Statut du fichier mis à jour.', 'success')
    except api.APIError as e:
        flash(str(e), 'error')
    return redirect(url_for('dashboard'))

@app.route("/file/<file_id>/delete", methods=["POST"])
@login_required
def delete_file_route(file_id):
    try:
        api.delete_file(file_id, token=set_api_token())
        flash('Fichier supprimé.', 'success')
    except api.APIError as e:
        flash(str(e), 'error')
    return redirect(url_for('dashboard'))

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    user = session.get('user', {})
    user_id = user.get('id')
    if request.method == 'POST':
        # log contents of request for debugging integration
        app.logger.info(f"upload POST form keys={list(request.form.keys())} files={list(request.files.keys())}")
        file_obj = request.files.get('file')
        name = request.form.get('name')
        description = request.form.get('description')  # optionnel
        status = request.form.get('status', 'private')
        form_user_id = request.form.get('user_id')
        import os
        cwd = os.getcwd()
        log_line = (f"UPLOAD Debug: cwd={cwd} form_keys={list(request.form.keys())} "
                    f"files={list(request.files.keys())} name={name!r} "
                    f"status={status!r} desc={description!r} form_user={form_user_id!r} "
                    f"file_filename={file_obj.filename if file_obj else None}\n")
        # show cwd in flash (temporary for debugging purposes)
        flash(f"[DEBUG cwd]={cwd}", 'error')
        # write to persistent log file as well
        with open('upload_debug.log', 'a', encoding='utf-8') as flog:
            flog.write(log_line)
        app.logger.info(log_line)

        # sanity check: form and session ids should match
        if form_user_id and user_id and form_user_id != user_id:
            app.logger.warning(f"form user_id {form_user_id} != session user_id {user_id}")

        # validation simple
        if not file_obj or file_obj.filename == "":
            flash('Veuillez sélectionner un fichier à téléverser.', 'error')
            return render_template("upload.html", user=user)
        if not user_id:
            flash('Identifiant utilisateur introuvable, reconnectez-vous.', 'error')
            return redirect(url_for('login'))

        if not name or not name.strip():
            base = file_obj.filename.rsplit('.', 1)[0]
            name = base

        app.logger.debug(f"Upload attempt user_id={user_id} filename={file_obj.filename} status={status} name={name} desc={description}")
        try:
            resp = api.upload_file(file_obj, user_id, name=name, status=status, description=description, token=set_api_token())
            app.logger.debug(f"upload response: {resp}")
            if resp and not resp.get('success', True):
                message = resp.get('message') or resp.get('detail') or 'Erreur lors de l\'upload'
                flash(message, 'error')
                return render_template("upload.html", user=user)
            flash('Fichier uploadé avec succès.', 'success')
            return redirect(url_for('dashboard'))
        except api.APIError as e:
            app.logger.error(f"upload_file failed: {e}")
            flash(f"Échec de l'upload : {e}", 'error')
        except Exception as e:
            app.logger.error(f"upload exception: {e}")
            flash(f"Erreur inattendue pendant l'upload : {e}", 'error')
    return render_template("upload.html", user=user)


if __name__ == "__main__":
    # debug mode with reloader off prevents multiple restarts/exits when modules reload
    app.run(debug=True, use_reloader=False)
