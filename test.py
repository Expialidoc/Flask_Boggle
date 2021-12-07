from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
import json

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""
        with self.client:
            response = self.client.get('/')#trigger home route
            self.assertIn('board', session)
        #    self.assertIs(session.get('highscore'),0) #None is not zero!
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)
            
    def test_non_english_word(self):
        """Test if word is on the board"""
        with self.client:
            self.client.get('/')
            response = self.client.get('/check-word?word=asffffretttsshha')
            self.assertEqual(response.json['result'], 'not-word')
            
    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"],
                                ["C", "A", "T", "T", "T"]]
        response = self.client.get('/check-word?word=cat')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""
        with self.client:
            self.client.get('/')
            response = self.client.get('/check-word?word=impossible')
            self.assertEqual(response.json['result'], 'not-on-board')
        
    

    def test_higher_score(self):
        """Test if highscore is gotten correctly"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['highscore'] = 10

    # once this is reached the session was stored and ready to be used by the client
    
        res = self.client.post("/post-score",data=json.dumps({'score': 11}),content_type='application/json')
    #    self.assertEqual(res.status_code, 200)
        json_response = json.loads(res.get_data(as_text=True))
        print(json_response)
        self.assertTrue(json_response['brokeRecord'])
    
    def test_lower_score(self):
        """Test if highscore is gotten correctly"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess['highscore'] = 12

        res = self.client.post("/post-score",data=json.dumps({'score': 11}),content_type='application/json')
        json_response = json.loads(res.get_data(as_text=True))
        print(res.get_data(as_text=True)) #(json_response)
        self.assertFalse(json_response['brokeRecord'])
        
    