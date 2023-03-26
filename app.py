import requests

API_KEY = 'AIzaSyBFBO43lMRZDTMLCYRSoySCSblkoOwR5jk'

def get_toxicity_score(text):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key=' + API_KEY
    data = {
        'comment': {'text': text},
        'requestedAttributes': {
            'TOXICITY': {},
            'INSULT': {},
            'THREAT': {}
        }
    }
    response = requests.post(url, json=data)
    if response.status_code != 200:
        print("Error: API request failed with status code", response.status_code)
        return None
    response_dict = response.json()
    try:
        toxicity_score = response_dict['attributeScores']['TOXICITY']['summaryScore']['value']
        insult_score = response_dict['attributeScores']['INSULT']['summaryScore']['value']
        threat_score = response_dict['attributeScores']['THREAT']['summaryScore']['value']
    except KeyError:
        print("Error: Response does not contain expected key 'attributeScores'")
        return None
    return toxicity_score, insult_score, threat_score


# def word_tracker(prompt, threshold=0.5, insult_threshold=0.7, threat_threshold=0.8):
#     toxicity_score, insult_score, threat_score = get_toxicity_score(prompt)
    
#     if toxicity_score is not None and toxicity_score > threshold:
#         print("Given text is toxic")
#         return True
    
#     if insult_score is not None and insult_score > insult_threshold:
#         print("Given text is insulting")
#         return True
    
#     if threat_score is not None and threat_score > threat_threshold:
#         print("Given text contains threats")
#         return True
    
#     return False




def word_tracker(prompt, threshold=0.5, insult_threshold=0.7, threat_threshold=0.9):
    toxicity_score, insult_score, threat_score = get_toxicity_score(prompt)
    
    if insult_score is not None and insult_score > insult_threshold:
        print("Given text is insulting")
        return True
    
    if threat_score is not None and threat_score > threat_threshold:
        print("Given text contains threats")
        return True
    
    if toxicity_score is not None and toxicity_score > threshold:
        print("Given text is toxic")
        return True
    
    return False

text = input("Text here: ")
result = word_tracker(text)
if not result:
    print("No inappropriate words or texts found")
