from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import json
from huggingface_hub import InferenceClient

def story_gui(request):
    return render(request, 'generator/index.html')

@csrf_exempt
def generate_story(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_prompt = data.get('prompt', '')
            
            if not user_prompt:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No prompt provided'
                }, status=400)

            client = InferenceClient(api_key=settings.HUGGINGFACE_API_KEY)
            
            complete_prompt = f"""Create a detailed and immersive story based on this prompt: {user_prompt}

            Requirements for the story:
            - Start with a strong hook and vivid scene-setting
            - Develop at least 2-3 main characters with distinct personalities and motivations
            - Include rich sensory details and atmospheric descriptions
            - Incorporate meaningful dialogue that reveals character and advances the plot
            - Build tension through a clear conflict or challenge
            - Create a satisfying resolution that ties up the main story threads
            - Maintain an engaging narrative pace
            
            The story should be at least 6-8 detailed paragraphs long with proper spacing and structure.
            Focus on showing rather than telling, and bring the scenes to life through specific details.

            Story:"""

            completion = client.text_generation(
                model="tiiuae/falcon-7b-instruct",
                prompt=complete_prompt,
                max_new_tokens=1000,
                temperature=0.8,
                top_p=0.9,
                repetition_penalty=1.2
            )

            story = completion.strip()
            story = story.replace(complete_prompt, '')
            story = story.replace("\n\n", "<br><br>")
            
            return JsonResponse({'status': 'success', 'story': story})
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
            
        except Exception as e:
            print(f"Error generating story: {str(e)}")  # For debugging
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while generating the story'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=400)