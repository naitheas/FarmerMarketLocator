from FarmerMarketLocator import create_app,create_db

app = create_app()
create_db(app)



if __name__ == '__main__':
    app.run(debug=True)

