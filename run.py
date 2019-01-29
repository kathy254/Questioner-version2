from app import create_app

config = 'development'

app = create_app(config)
if __name__ == "__main__":
    app.run()

