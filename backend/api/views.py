from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from main.models import *

@csrf_exempt
@require_POST
def register(request):
    data = request.POST
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return JsonResponse({'message': 'All fields are required'}, status=400)

    if CustomUser.objects.filter(email=email).exists() or CustomUser.objects.filter(username=username).exists():
        return JsonResponse({'message': 'User already exists'}, status=400)

    user = CustomUser.objects.create_user(email=email, username=username, password=password)
    return JsonResponse({'message': 'User registered successfully'})

@csrf_exempt
@require_POST
def user_login(request):
    data = request.POST
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'message': 'Username and password are required'}, status=400)

    user = authenticate(request, username=username, password=password, model=CustomUser)


    if user is not None:
        login(request, user)
        
        # Get or create a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return the token in the response
        return JsonResponse({'message': 'Login successful', 'token': token.key})

    return JsonResponse({'message': 'Invalid credentials'}, status=401)

@csrf_exempt
def travelogue_api(request):
    if request.method == 'GET':
        travelogues = Travelogue.objects.all()
        # Convert the QuerySet into a list of dictionaries
        serialized_travelogues = [{'title': t.title, 'latin': t.latin, 'content': t.content, 'uploader': t.uploader.username, 'upload_date': t.upload_date, 'edit_date': t.edit_date, 'city': t.city.name, 'slug': t.slug} for t in travelogues]
        return JsonResponse({'travelogues': serialized_travelogues}, safe=False)

    # if request.method == 'POST':
    #     data = request.POST
    #     title = data.get('')
    #     latin = 
    #     content = 
    #     uploader = 

    
@csrf_exempt
def article_api(request):
    # Query the Article model to get all articles
    articles = Article.objects.all()

    # Serialize the articles into a list of dictionaries
    serialized_articles = []
    for article in articles:
        serialized_articles.append({
            'title': article.title,
            'latin': article.latin,
            'article': article.article,
            'cover': article.cover.url,
            'author': article.author.username,
            'upload_date': article.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
            'edit_date': article.edit_date.strftime('%Y-%m-%d %H:%M:%S'),
            'tags': [tag.title for tag in article.tags.all()],
            'category': article.category.title,
            'slug': article.slug,
        })

    # Return the serialized articles as JSON response
    return JsonResponse({'articles': serialized_articles}, safe=False)





