import pytest
import pandas as pd
from src import *
import os 
 
        
def test_afficher_utilisateurs() :
    
    data_test = {
        'nom_utilisateur' : ['user1', 'user2', 'user3'],
        'mot_de_passe' : ['password1','password2' , 'password3'],
        'addresse_mail': ['user1@example.com', 'user2@example.com', 'user3@example.com']
        }
    test_df = pd.DataFrame(data_test)
    
    df = afficher_utilisateurs()
    
    assert 'user1' in df
    assert 'user2' in df
    assert 'user3' in df
    
    assert 'user1@exaple.com' in df
    assert 'user2@exaple.com' in df
    assert 'user3@exaple.com' in df
    
    assert '*******' in df 
    
test_afficher_utilisateurs()