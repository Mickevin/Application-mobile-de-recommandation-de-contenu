import logging

import azure.functions as func
import scipy
import implicit
import pickle

model = pickle.load(open( 'model.pkl', "rb" ))
sparse = scipy.sparse.load_npz('sparse.npz')

def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Python HTTP trigger function processed a request.')

    userId = req.params.get('userId')
    if not userId:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            userId = req_body.get('userId')

    if userId:
        l = list(model.recommend(int(userId), sparse[int(userId)])[0][:5])
        return func.HttpResponse(f'{l}')
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )