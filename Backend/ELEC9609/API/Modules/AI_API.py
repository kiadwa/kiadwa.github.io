import os
import openai
import dotenv
from django.forms import model_to_dict

from ELEC9609.API.Modules.Base import *

dotenv.load_dotenv()
API_KEY = os.getenv("AI_API_KEY")
openai.api_key = API_KEY

def pet_help(data):
    """
    :param data: {
            "token": "<token>",
            "pet_help": {
                "message": str,
                "diagnosis": str
            }
        }
    :return: {
            "error_code": 200,
            "data": str,
            "error_msg": "str?"
        }
    """
    auth = get_authorisation(data)
    if not auth['error_code'] == 200:
        return auth
    assert 'pet_help' in data and type(data['pet_help']) == dict
    pet_help = data['pet_help']
    try:
        pethelp_breed=pet_help['breed']
        pethelp_species=pet_help['species']
        pethelp_data = pet_help['message']
        pethelp_diagnosis = pet_help['diagnosis']
        if not pethelp_data:
            return get_result(FALSE, None, "No message provided!")
        if not pethelp_diagnosis:
            return get_result(FALSE, None, "No diagnosis provided!")
        
        print("Sending request to OpenAI API...")
        # Use the new ChatCompletion endpoint
        response = openai.chat.completions.create(
            model="gpt-4-turbo",  # The model name for GPT-4
            messages=[
                {"role": "system", "content": "You are a professional vet."},
                {"role": "user", "content": f"Here is some context of the pet's behavior/situation: {pethelp_diagnosis}, the user's pet is a {pethelp_species} of breed {pethelp_breed}. The trouble with the user's pet is: {pethelp_data}"}
            ],
            max_tokens=200,
            temperature=0.7
        )
        bot_response = response.choices[0].message.content.strip('\\')
        return get_result(SUCCESS, {'data': bot_response}, "Got response from AI API")
    except Exception as e:
        print(f"Error in OpenAI API call: {str(e)}")
        return get_result(FALSE, None, f"Error in the backend to send API call: {str(e)}")
