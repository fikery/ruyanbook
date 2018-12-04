from flask import Flask

from app import createApp

app = createApp()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81)


'''
http://localhost:81/book/search?q=9787070511209
http://localhost:81/book/search?q=村上春树
'''