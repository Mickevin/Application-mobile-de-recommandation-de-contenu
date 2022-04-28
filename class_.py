import pandas as pd
import numpy as np

import scipy
import scipy.sparse
import scipy.sparse as sparce
import pickle

import implicit
import collections

import os

from azureml.core import Workspace, Datastore, Dataset
from azureml.data.datapath import DataPath


class My_Recommandation():
    def __init__(self):
        self.ws = Workspace(subscription_id="d5bb9744-4790-446f-b7e1-591e22995cc7",
               resource_group="OpenClassrooms",
               workspace_name="OC_IA")

        self.datastore = Datastore.get(self.ws, 'workspaceblobstore')
        try :
            [os.remove(f"UI/utiles/{file}") for file in os.listdir('UI/utiles/')]
        except:
            pass
        self.datastore.download(target_path='.', prefix='UI/utiles')
        
    def add_user(self, user_id, article_read, n_click, publish=False):
        df = pd.DataFrame(np.load('UI/utiles/df_user.npy', allow_pickle=True), 
                          columns=['LIST_click_article_id', 'n_click'])
        df = df.append(pd.DataFrame(data = {'LIST_click_article_id':[article_read],
                                                'n_click' : n_click
                                                }, 
                                            index=[user_id]))
        
        np.save('UI/utiles/df_user', df)
        print('User added, file saved !')
        
    def add_article(self, id_, catégorie_id, publish=False):
        df_article = pd.read_csv('UI/utiles/df_article.csv',index_col='Unnamed: 0')
        df_article = df_article.append(pd.DataFrame(data = {'article_id':id_,
                                       'category_id':catégorie_id},
                               index=[id_]))
        df_article.to_csv('UI/utiles/df_article.csv')
        print('Article added, file saved !')
        
    def to_publish(self):
        
        for file in os.listdir('UI/utiles/'):
            try :
                self.datastore.blob_service.delete_blob('azureml-blobstore-f8554f92-a33d-430c-a1ff-4d9a166c55fc',
                                      f'UI/utiles/{file}')
            except:
                pass
        Dataset.File.upload_directory(src_dir='UI/utiles/',
                   target=DataPath(self.datastore, 'UI/utiles/'),
                   show_progress=True)
        
        print('Published on Azure Blob Storage')
        
    
    def sparse(self, n_user=True,  train=False, publish=False):
        print('Preprocessing...')
        Counter = collections.Counter
        df = pd.DataFrame(np.load('UI/utiles/df_user.npy', allow_pickle=True), 
                          columns=['LIST_click_article_id', 'n_click'])
        df_article = pd.read_csv('UI/utiles/df_article.csv',index_col='Unnamed: 0')
        n_click = df.n_click.values
        articles = df_article.article_id
        categories = df_article.category_id
        n_user = n_user
        
        if n_user==True:n_user = len(df)

        # TFIDF des article lus en fonction des utilisateurs
        user_tfidf = [np.isin(articles, 
                          df.LIST_click_article_id.values[n])
                           for n in range(n_user)]

        user_tfidf = np.array(user_tfidf)

        # Catégorie des articles lus
        user_tfidf = np.array([categories * user_tfidf[n] 
                               for n in range(len(user_tfidf))])

        # Dictionnaire du nombre d'article lu par catégorie
        d = [Counter(user_tfidf[n]) for n in range(len(user_tfidf))]
        print('Parsing...')

        # Ajouts du nombre d'article lu dans la catégorie de l'article
        tfidf_ = [np.array([u for u in map(lambda x: d[n][x] if x != 0 else 0, 
                                           user_tfidf[n])])/n_click[n]
              for n in range(len(user_tfidf))]
        
        
        sparse_ = scipy.sparse.csc_matrix(np.array(tfidf_))
        scipy.sparse.save_npz('UI/utiles/sparse.npz', sparse_)
        print('Save !')
        if train:
            print('Strat training')
            self.train_model()
        
        if publish:
            self.to_publish()
        
    
    def train_model(self, publish=False):
        sparse_ = scipy.sparse.load_npz('UI/utiles/sparse.npz')
        self.model = implicit.als.AlternatingLeastSquares(factors=100,iterations=200,regularization=0.1)
        self.model.fit(sparse_)
        print('model trained successfuly')
        
        with open('UI/utiles/model.pkl', 'wb') as f1:
            pickle.dump(self.model, f1)
            print('model save !')
            
        if publish:
            self.to_publish()
            
    def predict(self, user_id):
        sparse_ = sparce.csr_matrix(scipy.sparse.load_npz('UI/utiles/sparse.npz'))
        return list(self.model.recommend(user_id, sparse_[user_id], 5)[0])