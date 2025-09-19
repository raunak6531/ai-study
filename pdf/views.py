from django.shortcuts import render
from django.http import JsonResponse
from .models import Document
import os
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from gemini import process_document_with_gemini

# Create your views here.
def landing(request):
    return render(request,'landing.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            # Validate file type (only PDF)
            if uploaded_file.content_type != 'application/pdf':
                return JsonResponse({'error': 'Invalid file type. Please upload a PDF file.'}, status=400)

            # Validate file size (50MB limit)
            if uploaded_file.size > 50 * 1024 * 1024:
                return JsonResponse({'error': 'File size exceeds 50MB limit.'}, status=400)

            # Ensure media directory exists
            media_dir = settings.MEDIA_ROOT
            if not os.path.exists(media_dir):
                os.makedirs(media_dir)

            # Create document instance
            document = Document(
                file=uploaded_file,
                file_name=uploaded_file.name,
                file_size=uploaded_file.size,
                file_type='pdf'  # Since we only accept PDFs now
            )
            document.save()

            # Get the full file path
            file_path = document.file.path

            return JsonResponse({
                'success': True,
                'message': 'File uploaded successfully',
                'file_name': document.file_name,
                'file_url': document.file.url  # This will give us the correct media URL
            })

        return JsonResponse({'error': 'No file uploaded'}, status=400)

    return render(request, 'upload.html')

@csrf_exempt
def analyze(request):
    if request.method == 'POST':
        try:

            data = json.loads(request.body)
            file_url = data.get('file_url')
            prompt = "You are an expert in structuring data from course syllabi into JSON format.  Given the following information from a syllabus, create a JSON object representing a detailed study plan.  The study plan should include a weekly breakdown, topics, sub-details.  Focus on extracting information from the 'Syllabus' and 'Lecture Plan' sections to create the weekly structure.  If specific weeks are not defined, create logical groupings based on the lecture sequence.  Prioritize accuracy and completeness. strictly use the folowing json structure {'course name':'name of the course','study plan':[{'week':1,'topic':'topic to learn on that week','subtopic':['list of subtopics for the week']},'more weeks']}"

            if not file_url:
                return JsonResponse({'error': 'No file URL provided'}, status=400)

            # Process the document with Gemini
            result = process_document_with_gemini(file_url, prompt)

            return JsonResponse({
                'success': True,
                'result': result
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
