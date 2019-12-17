from connexion.resolver import RestyResolver
import connexion


from flask import Flask, escape, request

if __name__ == '__main__':
    app = connexion.App(__name__, 9090, specification_dir='swagger/')
    app.add_api('my_super_app.yaml', resolver=RestyResolver('api'))
    app.run()