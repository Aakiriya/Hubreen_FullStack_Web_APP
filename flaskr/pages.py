from flask import Flask, request, render_template, session, redirect, url_for, Response
from .backend import Backend


def make_endpoints(app):

    # Flask uses the "app.route" decorator to call methods when users
    # go to a specific route on the project's website.
    @app.route("/")
    def home():
        return render_template("main.html")  # render main page with background image

    @app.route("/upload", methods=['GET', 'POST'])
    def upload_file():
        # sets allowed file types, messages to return based on situation
        message = [
            "File was not uploaded correctly. Please try again.",
            "Uploaded successfully."
            ]

        if request.method == 'POST':
            # if no file is found in request/request made incorrectly, return first error message
            if 'file' not in request.files or 'prev' not in request.files:
                return render_template("upload.html", message=message[0])

            else:
                file = request.files['file']

                b = Backend("pages-content")
                b.upload(request.form.get("filename"), file)
                
                file = request.files['prev']
                    
                b = Backend("pages-content")
                b.upload((request.form.get("filename") + "prev"), file)
                return render_template("upload.html", message=message[1])
            
        return render_template("upload.html")

    @app.route('/login', methods=['POST', 'GET'])
    def sign_in():
        if request.method == "POST":
            username = request.form['name']
            password = request.form['psw']
            b = Backend('users-pws')  #passes the unsername and password entered to the login function in Backend class

            info = b.sign_in(username, password)

            if info == 'Invalid User' or info == 'Invalid Password':  #if the passward or username is invalid it renders back to the login page and displays the error message
                return render_template('login.html', info=info)

            else:
                session['username'] = username  #adds the username to the session
                return redirect('/')

        return render_template('login.html')

    @app.route('/signup', methods=['POST', 'GET'])
    def sign_up():
        if request.method == "POST":
            username = request.form['name']
            password = request.form['psw']
            b = Backend('users-pws')
            b.sign_up(
                username, password
            )  #passes the unsername and password entered to the signup function in Backend class
            session['username'] = username  #adds the username to the session
            return redirect('/')
        return render_template('signup.html')

    @app.route('/pages')
    def pages():
        backend = Backend("pages-content")  #Call the backend with the buckets name
        pages = backend.get_all_page_names()  #call the get allpages and save the dictionary in pages
        page_images = {}
        if pages:
            for page in pages:
                image_urls = []
                for i in range(1, 20):  # retrieve up to 10 images per page
                    image_url = backend.get_image(f"{page}img{i}")
                    if image_url:
                        image_urls.append(image_url)
                page_images[page] = image_urls
                prev_image = backend.get_image(f"{page}prev")
                if prev_image:
                    page_images[f"{page}_prev"] = prev_image
            return render_template('pages.html', pages=pages, page_images=page_images)
        return render_template('pages.html')

    @app.route('/pages/<name>')
    def show_page(name):
        backend = Backend("pages-content")
        content, mime_type = backend.get_wiki_page(name)
        page_title = f'{name}'
        if content:
            return render_template('page.html', content=content.decode(), page_title=page_title)
        else:
            return f'Page {name} not found'

    @app.route("/logout")
    def logout():
        # when user logs out, set session username to None, then redirect to home page
        session['username'] = None
        return redirect('/')

    @app.route("/tinyedit", methods=['POST', 'GET'])
    def editor():
        # Opens the renders the API html to displat the editor
        return render_template('tinyedit.html')

    @app.route("/about")
    def about():
        # gets background image along with about images for the three authors, then returns it to about page on render
        b = Backend("contentwiki")
        return render_template("about.html")
