from internal.webserver import create_app

app = create_app()

if __name__ == '__main__':
    app.logger.info("Starting Flask Server")
    app.run(debug=True)