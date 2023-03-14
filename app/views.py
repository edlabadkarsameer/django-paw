#iamthebest@123
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate ,login
from django.urls import reverse
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import os
import cv2
import random
import csv
import nltk

liste = []
def webcam(request):
    return render(request, 'preppython.html')

# Define the threaded function to read frames from the video stream
def frame_generator():
    warning_counter = 0
    global warning
    # Video capture object
    count = 0
    cap = cv2.VideoCapture(0)
    # Define cascade classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        # Read a frame from the video capture object
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) == 0:
            count += 1
            cv2.putText(frame, 'Warning: No face', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)


        # if there is a more faces it will throw warning
        elif len(faces) > 1:
            cv2.putText(frame, 'Super Warning: Multiple faces detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255),
                        2, cv2.LINE_AA)
            warning_counter += 1

        # Draw a rectangle around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Convert frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        warning = count
        # Yield the JPEG data as an HTTP response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    return warning
# Decorate the view function with the gzip decorator to compress the response
@gzip.gzip_page
def stream_video(request):
    # Return a StreamingHttpResponse object with the generator function as content
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

# Load the questions from the CSV file
with open('questions.csv', newline='') as csvfile:
    questions_reader = csv.reader(csvfile)
    questions = list(questions_reader)

# Index of the current question
#random_question_index = random.randint(1, 5)
#current_question_index = random_question_index
current_question_index = 0
def summation(liste):
    total = 0
    for ele in range(0, len(liste)):
        total = total + liste[ele]
    total = total/len(liste)
    return total
def interview(request):
    global current_question_index

    if request.method == 'POST':
        # Get the user's answer from the form
        user_answer = request.POST.get('answer')

        # Get the correct answer from the CSV file
        correct_answer = questions[current_question_index][1]

        # Use NLTK to compare the user's answer to the correct answer
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        user_words = set(tokenizer.tokenize(user_answer.lower()))
        correct_words = set(tokenizer.tokenize(correct_answer.lower()))
        num_common_words = len(user_words.intersection(correct_words))
        num_total_words = len(correct_words)
        score = float((num_common_words / num_total_words) * 100)
        print(score)
        liste.append(score)
        # Move to the next question
        current_question_index += 1

        # If there are more questions, render the next question page
        if current_question_index < len(questions):
            context = {
                'question': questions[current_question_index][0],
                'next_url': '/interview/'
            }
            return render(request, 'interview.html', context)

        # Otherwise, render the final score page
        else:
            print(liste)
            score = summation(liste)
            print(score)
            context = {
                'score': score, 'warning':warning
            }
            return render(request, 'score.html', context)

    else:
        # Render the first question page
        current_question_index = 0
        context = {
            'question': questions[current_question_index][0],
            'next_url': '/interview/'
        }
        return render(request, 'interview.html', context)

def home(request):
    return render(request , "index.html")
def prepython(request):
    return render(request , "prepython.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request ,"Successfully created.....")

        return redirect ('login')
    return render(request , "authentication/register.html")

def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "prepython.html", {'fname' : fname} )

        else:
            messages.error(request, "bad credential")
            return redirect('home')

    return render(request , "authentication/login.html")

def logout(request):

    return redirect(reverse('home'))