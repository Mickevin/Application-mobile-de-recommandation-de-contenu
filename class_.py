import numpy as np
import collections
import os
import pandas as pd
import scipy.sparse as sparse
import implicit
Counter = collections.Counter

class Model():
    def __init__(self, df, articles, catégories, n_user=True):
        """
        df : Dataframe['User_id', 'List_click_article']

        articles : array of all articles

        catégories : array of category by article

        n_user : int. Number of user in sparsMatrice

        """
        self.df = df
        self.articles = articles
        self.catégories = catégories
        self.n_user = n_user
    
    def pars_matrice(self):
        df = self.df
        articles = self.articles
        catégories = self.catégories
        n_user = self.n_user
        
        if n_user==True:n_user = len(df)

        print(n_user)
        # TFIDF des article lus en fonction des utilisateurs
        user_tfidf = [np.isin(articles, 
                          df.LIST_click_article_id.values[n])
                           for n in range(n_user)]

        user_tfidf = np.array(user_tfidf)

        print(True,1)
        # Catégorie des articles lus
        user_tfidf = np.array([catégories * user_tfidf[n] for n in range(len(user_tfidf))])

        print(True,2)
        # Dictionnaire du nombre d'article lu par catégorie
        d = [Counter(user_tfidf[n]) for n in range(len(user_tfidf))]

        print(True,3)
        # Ajouts du nombre d'article lu dans la catégorie de l'article
        tfidf_ = [np.array([u for u in map(lambda x: d[n][x] if x != 0 else 0, user_tfidf[n])]) 
              for n in range(len(user_tfidf))]

        print(True, 4)
        
        self.tfidf = np.array(tfidf_)
        self.sparse = sparse.csr_matrix(np.array(tfidf_))    
        return self
    
    
    def train_model(self,trainset):
        self.model = implicit.als.AlternatingLeastSquares(factors=100,iterations=200,regularization=0.1)
        self.model.fit(user_items=trainset)
        return self
    
    def predict(self, user_id):
        return self.model.recommend(user_id, self.sparse[user_id])[0].tolist()
    
    def add_article(self, id_, catégorie_id):
        self.articles = np.append(self.articles, id_)
        self.catégories = np.append(self.catégories, catégorie_id)
        
    def add_user(self, user_id, article_read):
        self.df = sf.df.append(pd.DataFrame(data = {'LIST_click_article_id':[article_read]}, 
                                            index=[user_id]))
        